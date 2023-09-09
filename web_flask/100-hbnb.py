#!/usr/bin/python3
"""script starts flask web app
loads all data from db"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """close db"""
    storage.close()


@app.route("/")
def index():
    """index"""
    return """welcome to index page"""


@app.route('/hbnb')
def hbnb_index():
    """AirBnB index page for hbnb_web_static"""
    from models.state import State
    from models.amenity import Amenity
    from models.place import Place
       

    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()

    return render_template('100-hbnb.html', states=states,
                           amenities=amenities,
                           places=places,
                           )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)