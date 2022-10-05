import os
from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from flask import jsonify
from flask_cors import CORS
import cv2

import numpy as np

import base64
from io import BytesIO
from PIL import Image

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if os.path.isdir('uploads'):
    pass
else:
    os.mkdir('uploads')


@app.route('/image', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            return jsonify({"message": "fail"})

        file = request.files['file']

        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        # img = plt.imread(path)
        img = cv2.imread(path)  # Read image
        os.remove(path)

        # Setting parameter values
        t_lower = 50  # Lower Threshold
        t_upper = 150  # Upper threshold

        # Applying the Canny Edge filter
        edge = cv2.Canny(img, t_lower, t_upper)

        cv2.imwrite(path, edge)

        img = Image.open(path)
        im_file = BytesIO()
        img.save(im_file, format="JPEG")
        im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        im_b64 = base64.b64encode(im_bytes)

        d = {"output": str(im_b64)}

        os.remove(path)
        return jsonify(d)


if __name__ == '__main__':
    app.run()
