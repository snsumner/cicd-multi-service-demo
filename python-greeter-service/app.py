#!flask/bin/python
from flask import Flask
from flask_prometheus import monitor

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

if __name__ == '__main__':
    monitor(app, port=8001)
    app.run(host='0.0.0.0',port=5001)
