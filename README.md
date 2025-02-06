# Crime and Crowd Management with CCTV

## Overview

Welcome to the **Crime and Crowd Management with CCTV** project! This system is designed to monitor public spaces for crowd control and crime prevention using CCTV footage. The project consists of three main modules: **Crowd Management**, **Crime Detection**, and **Facial Recognition for Criminals**. The system leverages machine learning, OpenCV, and facial recognition technologies for real-time surveillance and alerts.
It was a part of Smart India Hackathon Group Project

## Modules

### 1. Crowd Management
- **Description**:  
  The Crowd Management module uses OpenCV to detect individuals in each frame of the CCTV footage. It sets a maximum limit for the number of people in a specific area and triggers an alert when this limit is exceeded.
- **Features**:
  - Person detection and counting.
  - Alert when the maximum person limit is exceeded.
  - Beep sound alert.
  - Frames are stored in an output folder.
  - Data saved to MongoDB.
- **Implementation**:
  - The core logic is implemented in `crowd_management.py`.
  - To adjust the maximum person limit, modify the `MAX_PERSONS` variable.
  - **Integration with Twilio**: Twilio is used to send WhatsApp messages for immediate notifications.
  - **Twilio Setup**: Add your Twilio API key and phone number after verification.

### 2. Crime Detection
- **Description**:  
  The Crime Detection module employs machine learning to periodically analyze frames for potential criminal activities.
- **Features**:
  - Crime detection using machine learning models.
  - Storage of suspicious frames in the output folder.
  - Data saved to MongoDB.
- **Implementation**:
  - The core logic is implemented in `crime_detection.py`.
  - Adjust the time interval for frame capture by modifying the `TIME_INTERVAL` variable.

### 3. Facial Recognition for Criminals
- **Description**:  
  This module utilizes facial recognition to identify potential criminals upon entry into the monitored area.
- **Features**:
  - Uses `.xml` files to capture facial points for continuous surveillance.
  - Sends notifications upon detection of a potential criminal.
- **Implementation**:
  - The logic for facial recognition is found in `facial_recognition.py`.
  - You can customize the `.xml` file used for facial recognition.

## APIs Used

### Twilio
- **Purpose**: Twilio is integrated for sending WhatsApp messages when an alert is triggered.
- **Setup**: 
  - You need to add your Twilio API key and phone number after verifying your account with Twilio.

## Installation

### Prerequisites
- Install Python 3.x and necessary dependencies.
- Install MongoDB and set up a local database.
- Install Twilio and set up a Twilio account for WhatsApp notifications.

### Install Dependencies
Use the following command to install required libraries:
 ```
pip install -r requirements.txt
 ```

## Configuration

### MongoDB
Add MongoDB connection details in the `config.py` file.

### Twilio
After verifying your account, add your Twilio API key and phone number in the `config.py` file.

---

## Usage

### Running the Modules

#### Crowd Management
To start crowd monitoring, run the following command:
```
python crowd_management.py
 ```

### Crime Detection
To start crime detection, run the following command:
 ```
python crime_detection.py
 ```
### Notifications
When the crowd exceeds the set limit or a potential crime is detected, an alert will be sent to your WhatsApp via Twilio.

# Folder Structure
Crime-and-Crowd-Management/
│
├── crowd_management.py       # Crowd management module
├── crime_detection.py        # Crime detection module
├── facial_recognition.py     # Facial recognition module
├── config.py                 # Configuration file for MongoDB and Twilio
├── requirements.txt          # List of required libraries
└── output/                   # Folder where frames are stored



## Contributing

Feel free to fork this repository, make improvements, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV for real-time computer vision
- Twilio for messaging
- MongoDB for data storage
