from keras.models import load_model
import json
import flask
import urllib.request
import cv2
import numpy as np
import tensorflow as tf
from flask import jsonify
import os
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


@app.route('/try', methods=['POST'])
def classification():
    image_size = int(app.meta["img_size"])
    classes = app.meta["classes"]

    images = []
    image = loadImage(flask.request.get_json()['url'])
    image = cv2.resize(image, (image_size, image_size), cv2.INTER_LINEAR)
    images.append(image)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0 / 255.0)

    # result = app.model.predict(images)
    with app.graph.as_default():
        result = app.model.predict(images)

    output = {}

    for i in range(0, len(classes)):
        output[classes[i]] = str("%.2f" % round(result[0][i], 2))

    return jsonify(output)


def loadImage(url):
    with urllib.request.urlopen(url) as response:
        image = np.asarray(bytearray(response.read()), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)


# modelFolder = '../tmp/saved_models/26_5_2018__15_24/'
modelPath = 'saved_models/{}'.format(os.environ['MODEL_NAME'])

app.model = load_model('{}/trained_model.h5'.format(modelPath))
app.model._make_predict_function()
app.graph = tf.get_default_graph()
app.meta = json.load(open('{}/meta.json'.format(modelPath)))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5001"), debug=True, use_reloader=False)
