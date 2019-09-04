from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
bootStarp = Bootstrap(app)

@app.route('/index')
def hello_world():
    return render_template('index.html')

@app.route('/fileupload/pcapfile', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

