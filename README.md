Project Title: Crime and Crowd Management with CCTV

Welcome to the Crime and Crowd Management with CCTV project! This project is designed to address the challenges of monitoring public spaces for crowd control and crime prevention using CCTV footage. The system consists of three main modules: Crowd Management, Crime Detection, and Facial Recognition for Criminals.

Modules
1. Crowd Management
•	Description:
•	The Crowd Management module utilizes OpenCV to detect individuals in a given frame.
•	A maximum limit for the number of persons is set, triggering an alert when exceeded.
•	Actions include a beep, storing frames in the output folder, and saving data to MongoDB.
•	Implementation:
•	The core logic is in crowd_management.py.
•	To adjust the maximum person limit, modify the MAX_PERSONS variable.
•	Integration with Twilio:
•	Twilio is used to send WhatsApp messages for immediate notifications.
•	To use Twilio, add your API key and phone number after verification.
2. Crime Detection
•	Description:
•	The Crime Detection module employs machine learning for periodic frame analysis.
•	Upon detecting a potential crime, frames are stored in the output folder and MongoDB.
•	Implementation:
•	Refer to crime_detection.py.
•	Adjust the time interval for frame capture in the TIME_INTERVAL variable.
3. Facial Recognition for Criminals
•	Description:
•	Facial recognition is used for identifying potential criminals upon entry.
•	.xml files assist in capturing facial points, enabling continuous surveillance and notifications.
•	Implementation:
•	Find the facial recognition logic in facial_recognition.py.
•	Customize the .xml file for facial recognition.


APIs Used
•	Twilio:
•	Twilio is integrated for sending messages on WhatsApp.
•	Add your Twilio API key and phone number after verification.

Usage
•	Configuration:
•	Add MongoDB details, Twilio API key, and number after verifying with Twilio.

