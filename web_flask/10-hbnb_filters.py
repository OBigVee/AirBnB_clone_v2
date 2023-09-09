#!usr/bin/python3
"""script starts a flask web app and load all
cities from db"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """close the current session of SQLalchemy"""
    storage.close()


@app.route("/")
def index():
    return "Hi this is index page"


@app.route("/hbnb_filters")
def Hbnb_index():
    """render html template"""
    from models.state import State
    from models.amenity import Amenity

    amenities = storage.all(Amenity).values()
    states = storage.all(State).values()

    return render_template("10-hbnb_filters.html", states=states,
                           amenities=amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
