#!flask/bin/python
from flask import Flask
from flask_prometheus import monitor

app = Flask(__name__)

@app.route('/')
def index():
    return "Chirag"

if __name__ == '__main__':
    monitor(app, port=8002)
    app.run(host='0.0.0.0',port=5002)
