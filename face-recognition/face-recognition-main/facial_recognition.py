from ast import And
from email import message
import tkinter as tk
from tkinter import TclError, ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
from tkinter import *
import cv2, sys, numpy, os
import pandas as pd
from csv import *
dir_path = os.path.dirname(os.path.realpath(__name__))
def recognize_face():

    frame = ttk.Frame()
    
    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=3)
    size = 4
    haar_file = os.path.join(dir_path,"haarcascade_frontalface_default.xml")
    datasets = os.path.join(dir_path, "dataset")

    # Part 1: Create fisherRecognizer
    print('Recognizing Face Please Be in sufficient Lights...')

    # Create a list of images and a list of corresponding names
    (images, labels, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(datasets):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(datasets, subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                label = id
                images.append(cv2.imread(path, 0))
                labels.append(int(label))
            id += 1
    (width, height) = (200, 200)

    # Create a Numpy array from the two lists above
    (images, labels) = [numpy.array(lis) for lis in [images, labels]]

    # OpenCV trains a model from the images
    # NOTEE FOR OpenCV2: remove '.face'
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, labels)

    # Part 2: Use fisherRecognizer on camera stream
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)
    while True:
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            # Try to recognize the face
            prediction = model.predict(face_resize)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            if (prediction[1]<500):
                cv2.putText(im, '% s - %.0f' %(names[prediction[0]], prediction[1]), (x-10, y-10),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            else:
                cv2.putText(im, 'not recognized',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        
        cv2.imshow('OpenCV', im)
        key = cv2.waitKey(1)
        if  0XFF == ('q'):
            break
        # ttk.Button(frame, text='Create Data',command=frame.quit).grid(column=0, row=2)

    # for widget in frame.winfo_children():
    #     widget.grid(padx=5, pady=5)
    
    # return frame
                    
    from distutils.fancy_getopt import fancy_getopt
    from turtle import home



# ------------------------------------------------------------------


def  create_data(names):
    haar_file = os.path.join(dir_path,"haarcascade_frontalface_default.xml")
    datasets = os.path.join(dir_path, "dataset")
    sub_data = names

    path = os.path.join(datasets, sub_data)
    if not os.path.isdir(path):
        os.mkdir(path)

    (width, height) = (200, 200)

    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)

    count = 1
    while count < 50:
        (_, im) = webcam.read()
        gray = im
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            cv2.imwrite('% s/% s.png' % (path, count), face_resize)
        count += 1
        
        
        cv2.imshow('OpenCV', im)
        cv2.waitKey(100)  
        if count==50 & 0XFF == ord('q' or 'Q') :
            break
                            

# ------------------------------------------------------------------------


def create_input_frame(container,main_lst):

    frame = ttk.Frame(container)
    
    
    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=3)

    # Find what
    ttk.Label(frame, text='Id').grid(column=0, row=0, sticky=tk.W)
    Id = ttk.Entry(frame, width=30)
    Id.focus()
    Id.grid(column=1, row=0, sticky=tk.W)

    # Replace with:
    ttk.Label(frame, text='Name').grid(column=0, row=1, sticky=tk.W)
    Name = ttk.Entry(frame, width=30)
    Name.grid(column=1, row=1, sticky=tk.W)

    def Add():
        lst=[Id.get(),Name.get()]
        main_lst.append(lst)
        messagebox.showinfo("Information","The data has been added successfully")

    def Save():
        with open(r"D:\Temp\face-recognition-main\face-recognition-main\data.csv","w") as file:
            Writer=writer(file)
            Writer.writerow(["Id","Name"])
            Writer.writerows(main_lst)
            messagebox.showinfo("Information","Saved succesfully")
    
    def Clear():
        Id.delete(0,END)
        Name.delete(0,END)
    
    # had to manage this bcz of 'entry', Layout management in tkinter
    save=tk.Button(frame,text="Save",command=Save)
    save.grid(row=2,column=1)
    add=tk.Button(frame,text="Add",command=Add)
    add.grid(row=0,column=2)
    clear=tk.Button(frame,text="Clear",command=Clear)
    clear.grid(row=1,column=2)
    Exit=tk.Button(frame,text="Exit",command=frame.quit)   
    Exit.grid(row=2,column=2)
    Recognize=tk.Button(frame,text="Recognize",command=recognize_face)   
    Recognize.grid(row=3,column=0)


    class karl22(Frame): 
        def __init__(self):
            tk.Frame.__init__(self)
            names=Name.get()
            create_data(names)
        def close_frame(self):
            self.destroy()

    ttk.Button(frame, text='Create Data',command=karl22).grid(column=0, row=2)

    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=5)
    
    return frame


# ------------------------------------------------------------------------


def create_main_frame():
    root = tk.Tk()
    root.title('Face recognizer')
    root.resizable(0, 0)
    main_lst=[]
    try:
        # frames only (remove the minimize/maximize button)
        root.attributes('-toolframe', True)
    except TclError:
        print('Not supported on your platform')

    # layout on the root frame
    root.columnconfigure(0, weight=4)
    root.columnconfigure(1, weight=1)

    input_frame = create_input_frame(root,main_lst)
    input_frame.grid(column=0, row=0)

    # if(is_number(Id) and name.isalpha()):


    root.mainloop()


# ----------------------------------------------------------------

if __name__ == "__main__":
    create_main_frame()
