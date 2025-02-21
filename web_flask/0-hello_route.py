#!/usr/bin/python3
"""script starts a Flask web application hello world app"""

from flask import Flask

app = Flask(__name__)


@app.route("/airbnb-onepage", strict_slashes=False)
def index():
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
