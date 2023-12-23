from flask import Flask, render_template, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
import base64
import io
import cv2
import numpy as np
import subprocess

app = Flask(__name__)

client = MongoClient('') 
db = client['croud']  
collection = db['croud img']

@app.route('/')
def index():
    latest_frame = collection.find_one(sort=[('_id', -1)])
    if latest_frame:
        image_data = latest_frame['frame']
        img_np = np.frombuffer(image_data, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        _, img_encoded = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        return render_template('index.html', img_data=img_base64)

    return "No frames in the database."

@app.route('/image')
def get_image():
    latest_frame = collection.find_one(sort=[('_id', -1)])
    if latest_frame:
        image_data = latest_frame['frame']
        return send_file(io.BytesIO(image_data), mimetype='image/png')

    return "No frames in the database."

@app.route('/start_system', methods=['POST'])
def start_system():
    # Run your Python code when the start button is clicked
    subprocess.run(["python", "self.py"])
    return "System started"

if __name__ == '__main__':
    app.run(debug=True)
