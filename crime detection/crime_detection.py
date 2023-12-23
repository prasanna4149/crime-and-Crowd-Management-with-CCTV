import os
import torch
import cv2
from transformers import ViTImageProcessor, AutoModelForImageClassification
from PIL import Image
import time
from tkinter import filedialog
import tkinter as tk
from pymongo import MongoClient
from bson.binary import Binary
from twilio.rest import Client
#twilio api 
account_sid = ''
auth_token = ''
client_twilio = Client(account_sid, auth_token)
def send_twilio_message():
    message_body = f'we detected a crime'

    message = client_twilio.messages.create(
        from_='whatsapp:+14155238886',
        body=message_body,
        to='whatsapp:+91'
    )

    print(message.sid)

# Disable oneDNN custom operations warning
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Load model and image processor
model_name = "csr2000/UCF_Crime"
processor = ViTImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# Create a tkinter window (it won't be shown)
root = tk.Tk()
root.withdraw()

# Ask the user to select a video file
video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])

# Check if the user selected a file
if not video_path:
    print("No file selected. Exiting.")
    exit()

# MongoDB setup
client = MongoClient('')
db = client['crime']
collection = db['crime_img']

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video is opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Read and process frames every 5 seconds
frame_interval = 3  # seconds
start_time = time.time()

# Create the output_frames folder if it doesn't exist
output_folder = "output_frames"
os.makedirs(output_folder, exist_ok=True)

unique_frames = set()

while True:
    ret, frame = cap.read()

    # Break the loop if the video is finished
    if not ret:
        break

    elapsed_time = time.time() - start_time

    # Check if it's time to process the next frame
    if elapsed_time >= frame_interval:
        # Convert the OpenCV BGR frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to PIL Image
        image = Image.fromarray(frame_rgb)

        # Tokenize and forward pass
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # Access logits or other relevant outputs
        logits = outputs.logits

        # Get the index of the maximum value in logits
        predicted_class_index = torch.argmax(logits).item()

        # Get the corresponding label
        predicted_label = model.config.id2label[predicted_class_index]

        # Print the best prediction
        print("found in video:", predicted_label)

        # Save the frame if it's unique
        frame_hash = hash(frame.tobytes())
        if frame_hash not in unique_frames:
            unique_frames.add(frame_hash)

            # Save the image to the file system
            output_path = os.path.join(output_folder, f"frame_{len(unique_frames)}.png")
            cv2.imwrite(output_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            print(f"Saved frame {len(unique_frames)} to {output_path}")

            # Store the image in MongoDB
            with open(output_path, "rb") as image_file:
                binary_data = Binary(image_file.read())
                collection.insert_one({"label": predicted_label, "image": binary_data})

            # Display the frame (you can remove this line if you don't want to display frames)
            cv2.imshow("Frame", frame)

        # Reset the start time for the next frame
        start_time = time.time()

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV window
send_twilio_message()
cap.release()
cv2.destroyAllWindows()
from app import app
if __name__ == '__main__':
    # You can do additional setup or import other modules here if needed
    app.run()