from ast import increment_lineno
import matplotlib
from numpy.core.fromnumeric import resize
import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.python.keras import activations
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image

from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
import time
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def show_result(result):
    idx=np.argmax(result)
    return label[idx]

json_file=open('G:/image/modle2/model_json.json')
loaded_model_json=json_file.read()
json_file.close()
model=model_from_json(loaded_model_json)
model.load_weights('G:/image/modle2/model_weight.h5')
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),loss='mean_absolute_error',metrics=['acc'])
label={0:'其他',1:'厨余',2:'可回收',3:'有害'}

# 上传文件
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        f.save(os.path.join(file_dir, f.filename))
        image_path = 'D:/Python/flask1/upload/'+f.filename
        img_clssified = image.load_img(image_path, target_size=(256, 256))
        img_clssified = image.img_to_array(img_clssified)
        img_clssified = np.expand_dims(img_clssified, axis=0)
        result = model.predict(img_clssified)

        #print("该垃圾类型为：" + show_result(result))
        return show_result(result)
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')