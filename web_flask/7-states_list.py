#!/usr/bin/python3
"""script starts flask web app and list all states"""

from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """close the current sqlalchemy sessoin"""
    storage.close()


@app.route("/states_list")
def list_all_states():
    """endpoint lists all states"""
    from models.state import State

    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
