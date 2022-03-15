# -*- coding:utf-8 -*-

import tensorflow as tf
import sys
import cv2
from PIL import Image
import numpy as np
import shutil

from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])

model = tf.keras.models.load_model("G:/trash_classification_tf2.3-master/models/mobilenet_245_epoch1.h5")  # todo 修改为自己的模型路径
class_names = ['其他垃圾', '厨余垃圾', '可回收垃圾', '有害垃圾']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    # 预测图片
def predict_img():
    img = Image.open('static/photo/target.png')
    img = np.asarray(img)
    outputs = model.predict(img.reshape(1, 224, 224, 3))
    result_index = int(np.argmax(outputs))
    result = class_names[result_index]
    names = result.split("_")  # todo  文件夹命名是分开的
    return names[0]

@app.route('/upload')
def upload_test():
    #user = 'Cala'
    return render_template('up.html')

@app.route('/select_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        f.save(os.path.join(file_dir, f.filename))
        img_name = os.path.join(file_dir, f.filename)
        target_image_name = "static/photo/tmp_single" + img_name.split(".")[-1]
        shutil.copy(img_name, target_image_name)
        to_predict_name = target_image_name
        img_init = cv2.imread(to_predict_name)
        h, w, c = img_init.shape
        scale = 400 / h
        img_init = cv2.resize(img_init, (224, 224))
        cv2.imwrite('static/photo/target.png', img_init)

        return predict_img()
    else:
        return jsonify({"error": 1001, "msg": "失败"})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')