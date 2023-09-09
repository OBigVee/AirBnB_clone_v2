#!/usr/bin/python3
"""script starts a Flask web application and fetch
data from db loading all cities from state
"""

from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(exception=None):
    """close current db session"""
    storage.close()


@app.route("/states_list")
def list_all_states():
    """list/return all states rendered in
    HTML template"""
    from models.state import State

    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)


@app.route("/cities_by_states")
def get_cities_by_states():
    """list/get cities by state"""
    from models.state import State

    states = storage.all(State).values()
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
