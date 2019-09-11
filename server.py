from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from pcap.proc.pcap import Pcap
import os
import pandas as pd
from PcapFeature import PcapFeature

app = Flask(__name__)
bootStarp = Bootstrap(app)


@app.errorhandler(404)
def miss(e):
    return render_template('pages-error-404.html'), 404


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/hello')
def hello():
    return render_template('hello.html')


@app.route('/result')
def model_select():
    labels = ['pktNum', 'type']
    content = [
        [0, 35],
        [1, 40]
    ]
    return render_template('result.html', labels=labels, content=content)


@app.route('/fileupload', methods=['POST', 'GET'])
def upload():
    result = ['failed']
    labels = ['pktNum', 'type']
    content = []
    if request.method == 'POST':
        f = request.files['file']
        module_name = request.form['module']
        if module_name == 'feature':
            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
            f.save(upload_path)
            result = feature_module(upload_path).tolist()

        elif module_name == 'binary':
            basepath = os.path.dirname(__file__)
            upload_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
            f.save(upload_path)
            result = binary_module(upload_path).tolist()

        for i in range(0, 100):
            content.append([i, result[i]])

        return render_template('result.html', labels=labels, content=content)
    return jsonify(result[0])


def binary_module(file, module='./module/pkt=1000.pkl'):
    km = joblib.load(module)
    _pcap = Pcap()
    _gen = _pcap.parse(file)
    i = 0
    testData = []
    for pkt in _gen:
        data = bytearray(pkt.data)
        length = len(data)
        # 长度不足100用0补齐，超过100取前100
        if length < 100:
            data = data + bytes([0] * (100 - length))
            testData.append(data)
        else:
            testData.append(data[:100])
        # 读取所有 dataFile 文件里面的前100个packet
        i += 1
        if i >= 100:
            break
    return km.predict(pd.DataFrame(testData))


def feature_module(file, module='./module/feature-k=32.pkl'):
    km = joblib.load(module)
    _pcap = PcapFeature()
    _pcap.read_packet(file)
    testData = _pcap.get_DataFrame()
    return km.predict(testData)


if __name__ == '__main__':
    try:
        app.run()
    except():
        pass
    # print(feature_module('./testData/email2a.pcap'))

