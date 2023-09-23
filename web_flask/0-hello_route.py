#!/usr/bin/python3
'''The script starts flask web appliation'''
from flask import Flask

app = Flask(__name__)
'''Flask applicarion instance'''
app.url_map.strict_slashes = False


@app.route('/')
def index():
    '''Returns "Hello HBNB!" when the / route is requested.'''
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
