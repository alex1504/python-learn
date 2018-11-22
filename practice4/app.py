from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello/<param>')
def hello(param = None):
    return render_template('hello.html', param=param)
