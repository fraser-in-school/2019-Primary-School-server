from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootStarp = Bootstrap(app)

@app.route('/index')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

