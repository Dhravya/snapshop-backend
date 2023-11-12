import requests
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import os

def upload_image(image_as_base64):
    timestamp = str(datetime.now())
    image = Image.open(BytesIO(base64.b64decode(image_as_base64)))
    image.save(timestamp + '.jpeg')
    image_in_bytes = open(timestamp + '.jpeg', 'rb').read()
    response = requests.put('https://worker-silent-night-fcb9.dhravya.workers.dev/' + timestamp + '.jpg', data=image_in_bytes, headers={'Content-Type': 'image/jpeg', 'X-Custom-Auth-Key': 'yourmom'})

    os.remove(timestamp + '.jpeg')
    return response.text
