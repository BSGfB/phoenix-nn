import configparser
import datetime
import json
import os
import time

import cv2
import flask
import numpy as np
from flask import jsonify, request, url_for
from keras.models import load_model
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'image' not in request.files:
        return 'no file'
    file = request.files['image']
    print(file.filename)
    if file.filename == '':
        return 'empty file name'
    if file and allowed_file(file.filename):
        now = int(time.mktime(datetime.datetime.now().timetuple()))
        fileArr = file.filename.split('.')
        filename = '{}_{}.{}'.format(secure_filename(fileArr[0]), now, fileArr[1])
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return '{}/{}'.format(app.host, filename)
    return 'bad'


@app.route('/try', methods=['POST'])
def classification():
    UPLOAD_FOLDER = './static'
    upload_file = request.files['image']
    filename = secure_filename(upload_file.filename)
    upload_file.save(os.path.join(UPLOAD_FOLDER, filename))
    image_size = int(app.meta["img_size"])
    classes = app.meta["classes"]

    images = []
    # Reading the image using OpenCV
    image = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
    # Resizing the image to our desired size and preprocessing will be done exactly as done during training
    image = cv2.resize(image, (image_size, image_size), cv2.INTER_LINEAR)
    images.append(image)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0 / 255.0)

    result = app.model.predict(images)

    output = {}

    for i in range(0, len(classes)):
        output[classes[i]] = str("%.2f" % round(result[0][i], 2))

    return jsonify(output)


config = configparser.RawConfigParser()
config.read('./resources/application.properties')

modelFolder = config.get('Web', 'modelFolder')

app.model = load_model('{}/trained_model.h5'.format(modelFolder))
app.meta = json.load(open('{}/meta.json'.format(modelFolder)))
app.uploadFolder = config.get('Web', 'uploadFolder')
app.config['UPLOAD_FOLDER'] = app.uploadFolder
app.host = config.get('Web', 'host')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True, use_reloader=False)
