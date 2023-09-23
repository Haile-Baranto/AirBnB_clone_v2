#!/usr/bin/python3
from flask import Flask
"""The script starts flask web appliation"""

app = Flask(__name__)  # create an instance of flask app.
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """Returns 'Hello HBNB!' when the / route is acceesed."""
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
