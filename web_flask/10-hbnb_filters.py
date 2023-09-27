#!/usr/bin/python3
"""
A simple Flask web application for the AirBnB clone project.
"""

from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.state import State

app = Flask(__name__)
"""
The Flask application instance.
"""
app.url_map.strict_slashes = False


def get_sorted_states_and_amenities():
    """
    Helper function to retrieve and sort states and amenities.

    Returns:
        sorted_states (list): A list of states sorted by name.
        sorted_amenities (list): A list of amenities sorted by name.
    """
    all_states = storage.all(State).values()
    amenities = storage.all(Amenity).values()

    sorted_states = sorted(all_states, key=lambda x: x.name)
    sorted_amenities = sorted(amenities, key=lambda x: x.name)

    for state in sorted_states:
        state.cities.sort(key=lambda x: x.name)

    return sorted_states, sorted_amenities


@app.route('/hbnb_filters')
def hbnb_filters():
    """
    Display a page with filters for the AirBnB clone.

    Returns:
        rendered HTML template with data
    """
    states, amenities = get_sorted_states_and_amenities()

    context = {
        'states': states,
        'amenities': amenities
    }

    return render_template('10-hbnb_filters.html', **context)


@app.teardown_appcontext
def flask_teardown(exception):
    """
    Handle the Flask app/request context end event.

    Args:
        exception: The exception, if any, that occurred during the request.
    """
    storage.close()


if __name__ == '__main__':
    # Start the Flask web application on 0.0.0.0:5000
    app.run(host='0.0.0.0', port=5000)
