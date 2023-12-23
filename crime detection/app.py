from flask import Flask, render_template
from pymongo import MongoClient
from bson.binary import Binary
from io import BytesIO
import base64

app = Flask(__name__)

# MongoDB setup
client = MongoClient('')
db = client['crime']
collection = db['crime_img']

@app.route('/')
def index():
    # Retrieve the latest image from MongoDB
    latest_img = collection.find_one(sort=[('_id', -1)])

    if latest_img:
        # Convert binary data to base64 encoded image
        image_data = base64.b64encode(latest_img['image']).decode('utf-8')
        latest_image = {'label': latest_img['label'], 'image': image_data}
        return render_template('index.html', image=latest_image)
    else:
        return render_template('index.html', image=None)

if __name__ == '__main__':
    app.run(debug=True)
