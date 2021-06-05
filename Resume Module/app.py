from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello'


@app.route('/sujeewa')
def good_man():
    return 'my name is sujeewa'


app.run()
