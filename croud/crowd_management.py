
import numpy as np
import sys
import cv2 as cv
import Person
import time
import sounddevice as sd
from twilio.rest import Client
import os
from flask import Flask, send_file
from pymongo import MongoClient
from bson import ObjectId
from PIL import Image
from io import BytesIO 
import requests
import os
import datetime
from tkinter import filedialog
import tkinter as tk
from bson.binary import Binary


client = MongoClient('')  
db = client['croud'] 
collection = db['croud img']


max_person_limit = 12
frame_capture_folder = "D:/Temp/croud/output_folder"

# Twilio credentials
account_sid = ''
auth_token = ''
client_twilio = Client(account_sid, auth_token)

# Variables
font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

def send_twilio_message():
    custom_link = doc_id 
    message_body = f'place is over crouded: {custom_link}'

    message = client_twilio.messages.create(
        from_='whatsapp:+14155238886',
        body=message_body,
        to='whatsapp:+91'
    )

    print(message.sid)

try:
    log = open('num_people.txt', "w")
except:
    print('Error writing to file')

root = tk.Tk()
root.withdraw() 

video_file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi")])
if not video_file_path:
    print("No file selected. Exiting.")
    sys.exit()

cap = cv.VideoCapture(video_file_path)

cnt_up = 0
cnt_down = 0
max_frames_to_capture = 1 

for i in range(19):
    print(i, cap.get(i))
h = 500
w = 1500
frameArea = h * w
areaTH = frameArea / 250
print('Area Threshold', areaTH)
line_up = int(2 * (h / 5))
line_down = int(3 * (h / 5))

up_limit = int(1 * (h / 5))
down_limit = int(4 * (h / 5))

print("Red line y:", str(line_down))
print("Blue line y:", str(line_up))
line_down_color = (255, 0, 0)
line_up_color = (0, 0, 255)
pt1 = [0, line_down]
pt2 = [w, line_down]
pts_L1 = np.array([pt1, pt2], np.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))
pt3 = [0, line_up]
pt4 = [w, line_up]
pts_L2 = np.array([pt3, pt4], np.int32)
pts_L2 = pts_L2.reshape((-1, 1, 2))

pt5 = [0, up_limit]
pt6 = [w, up_limit]
pts_L3 = np.array([pt5, pt6], np.int32)
pts_L3 = pts_L3.reshape((-1, 1, 2))
pt7 = [0, down_limit]
pt8 = [w, down_limit]
pts_L4 = np.array([pt7, pt8], np.int32)
pts_L4 = pts_L4.reshape((-1, 1, 2))

fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)

kernelOp = np.ones((3, 3), np.uint8)
kernelOp2 = np.ones((5, 5), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)

while (cap.isOpened()):
    ret, frame = cap.read()

    for i in persons:
        i.num_ppl() 

    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    try:
        ret, imBin = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)
        ret, imBin2 = cv.threshold(fgmask2, 200, 255, cv.THRESH_BINARY)
        mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernelCl)
        mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
    except:
        print('end of program')
        print('DOWN:', cnt_down)
        break

    contours0, hierarchy = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv.contourArea(cnt)
        if area > areaTH:
            M = cv.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv.boundingRect(cnt)

            new = True
            if cy in range(up_limit, down_limit):
                for i in persons:
                    if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                        new = False
                        i.updateCoords(cx, cy)
                        if i.going_UP(line_down, line_up):
                            cnt_up += 1
                            print("person", cnt_up)
                        elif i.going_DOWN(line_down, line_up):
                            cnt_down += 1
                            print("person", cnt_down)
                            log.write("ID: " + str(cnt_down) + '\n')

                           
                            if cnt_down >= max_person_limit:
                                print("Person limit reached!")

                                ret, frame_to_capture = cap.read()
                                if ret:
                                    frame_filename = os.path.join(frame_capture_folder, "frame_max_limit_reached.png")
                                    cv.imwrite(frame_filename, frame_to_capture)
                                    print("Frame captured at max limit:", frame_filename)

                                    with open(frame_filename, "rb") as image_file:
                                        encoded_frame = image_file.read()
                                        doc_id = collection.insert_one({"frame": encoded_frame}).inserted_id
                                        print("Frame saved to MongoDB with _id:", doc_id)

                  
                                for _ in range(2):
                                    beep_duration = 1  
                                    sample_rate = 44100
                                    t = np.linspace(0, beep_duration, int(beep_duration * sample_rate), endpoint=False)
                                    beep_signal = 0.5 * np.sin(2 * np.pi * 1000 * t)
                                    sd.play(beep_signal, samplerate=sample_rate)
                                    sd.wait()
                                send_twilio_message()
                                os.system("python app.py")
                                sys.exit()


                            break

                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > down_limit:
                                i.setDone()
                            elif i.getDir() == 'up' and i.getY() < up_limit:
                                i.setDone()
                        if i.timedOut():
                            index = persons.index(i)
                            persons.pop(index)
                            del i
                if new == True:
                    p = Person.MyPerson(pid, cx, cy, max_p_age)
                    persons.append(p)
                    pid += 1

            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    for i in persons:
        cv.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv.LINE_AA)

    str_down = ('Total Count: ' + str(cnt_down))
    frame = cv.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
    frame = cv.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)
    frame = cv.polylines(frame, [pts_L4], False, (255, 255, 255), thickness=1)
    cv.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv.LINE_AA)

    cv.imshow('Crowd Counter', frame)

    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

log.flush()
log.close()
cap.release()
cv.destroyAllWindows()
