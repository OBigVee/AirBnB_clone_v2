#!/usr/bin/python3
"""script starts a Flask web application"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def index():
    return "Hello HBNB!"


@app.route("/hbnb")
def Hbnb():
    return "HBNB"


@app.route("/c/<text>")
def displayC(text):
    return f"C {text.replace('_', ' ')}"

@app.route("/python")
@app.route("/python/<text>")
def python_is_cool(text="is cool"):
    return f"Python {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
