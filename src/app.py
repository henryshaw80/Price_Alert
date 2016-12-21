__author__ = 'Timur'
# app.py stores the app but it runs from run.py

from flask import Flask

app = Flask(__name__)
# import config to be loaded to app
app.config.from_object('config')

@app.route('/')
def hello_world():
    return "Hello, world!"

