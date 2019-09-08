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

app = Flask(__name__)
bootStarp = Bootstrap(app)


@app.errorhandler(404)
def miss(e):
    return render_template('pages-error-404.html'), 404

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/model_select')
def model_select():
    return render_template('model.html')


@app.route('/fileupload/pcapfile', methods=['POST', 'GET'])
def upload():
    result = ['failed']
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
        f.save(upload_path)
        result = load_module(upload_path).tolist()
        res = {}
        res['data'] = result
        res['status'] = 200
        print(result)
        print(type(result))
        return jsonify(result)
    return jsonify(result)


def load_module(file, module=None):
    km = joblib.load('./module/500-0.pkl')
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


if __name__ == '__main__':
    app.run()

