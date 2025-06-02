import hashlib
import time
import os
import requests
from dotenv import load_dotenv
from typing import IO

load_dotenv()

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

def upload_to_cloudinary(file: IO):
    timestamp = int(time.time())
    signature_string = f"folder=rally&timestamp={timestamp}{CLOUDINARY_API_SECRET}"
    signature = hashlib.sha1(signature_string.encode()).hexdigest()

    files = {
        'file': file,
    }

    data = {
        'api_key': CLOUDINARY_API_KEY,
        'timestamp': timestamp,
        'signature': signature,
        'folder': 'rally'
    }

    response = requests.post(
        f'https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/image/upload',
        data=data,
        files=files,
    )

    response.raise_for_status()
    return response.json()
