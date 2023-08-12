# routes/upload_route.py
from flask import request, jsonify
from functions.upload_image import upload_image

def upload():
    return upload_image()

