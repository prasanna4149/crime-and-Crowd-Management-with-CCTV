# Creating database
# It captures images and stores them in datasets
# folder under the folder name of sub_data
import cv2, sys, numpy, os
haar_file = 'haarcascade_frontalface_default.xml'

# All the faces data will be
# present this folder
datasets = 'dataset'


# These are sub data sets of folder,
# for my faces I've used my name you can
# change the label here
sub_data = 'shreeya'	

path = os.path.join(datasets, sub_data)
if not os.path.isdir(path):
	os.mkdir(path)

# defining the size of images
(width, height) = (200, 200)

#'0' is used for my webcam
# if you've any other camera
# attached use '1' like this
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)

# The program loops until it has 40 images of the face.
count = 1
while count < 40:
	(_, im) = webcam.read()
	gray = im
	faces = face_cascade.detectMultiScale(gray, 1.3, 4)
	for (x, y, w, h) in faces:
		cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
		face = gray[y:y + h, x:x + w]
		face_resize = cv2.resize(face, (width, height))
		cv2.imwrite('% s/% s.png' % (path, count), face_resize)
	count += 1
	
	key = cv2.waitKey(10)
	if key == 27:
		break
	cv2.imshow('OpenCV', im)

































# import cv2  
# vid_cam= cv2.VideoCapture(0)
# face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# face_id=1
# count=0
# while (vid_cam.isOpened()):
#     ret,image_frame=vid_cam.read()
#     gray=cv2.cvtColor(image_frame,cv2.COLOR_BGR2GRAY)
#     faces=face_detector.detectMultiScale(gray,1.3,5)
#     for(x,y,w,h) in faces:
#         cv2.rectangle(image_frame,(x,y),(x+w,y+h),(255,0,0),2)
#         count+=1
#         cv2.imwrite("dataset/User." + str(face_id) + '.'+ str(count)+".jpg"+gray[y:y+h,x:x+w])  
#         cv2.imshow('frame',image_frame)  
#     if cv2.waitkey(100) & 0xFF==ord('q'):
#         break
#     elif count>100:
#         break
# vid_cam.release()
# cv2.destroyAllWindows()
    

# #https://pysource.com/2021/08/16/face-recognition-in-real-time-with-opencv-and-python/
# #https://linuxhint.com/opencv-face-recognition/