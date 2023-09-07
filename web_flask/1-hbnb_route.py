#!/usr/bin/python3
"""script starts a Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello HBNB!"


@app.route("/hbnb")
def Hbnb():
    return "HBNB"
