#!/usr/bin/python3
"""
A simple Flask web application.
"""

from flask import Flask, render_template, Markup
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.state import State

app = Flask(__name__)
"""
The Flask application instance.
"""
app.url_map.strict_slashes = False


@app.route('/hbnb')
def hbnb():
    """
    Display the hbnb page.

    - Load states, amenities, and places from the database.
    - Sort them alphabetically.
    - Sort cities within states.
    - Format place descriptions with HTML markup.
    - Render the HTML template with the data.

    Returns:
        rendered HTML template with data
    """
    # Load data from the database and sort alphabetically
    all_states = sorted(storage.all(State).values(), key=lambda x: x.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda x: x.name)
    places = sorted(storage.all(Place).values(), key=lambda x: x.name)

    # Sort cities within states
    for state in all_states:
        state.cities.sort(key=lambda x: x.name)

    # Format place descriptions with HTML markup
    for place in places:
        place.description = Markup(place.description)

    # Prepare the context for the HTML template
    context = {
        'states': all_states,
        'amenities': amenities,
        'places': places
    }

    # Render the HTML template with the context data
    return render_template('100-hbnb.html', **context)


@app.teardown_appcontext
def flask_teardown(exception):
    """
    Handle the Flask app/request context end event.

    - Close the current SQLAlchemy Session.

    Args:
        exception: The exception, if any, that occurred during the request.
    """
    storage.close()


if __name__ == '__main__':
    # Start the Flask web application on 0.0.0.0:5000
    app.run(host='0.0.0.0', port=5000)
