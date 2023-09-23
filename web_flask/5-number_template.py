#!/usr/bin/python3
'''The script starts flask web appliation at 0.0.0.0:5000'''
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
'''Flask applicarion instance'''
app.url_map.strict_slashes = False


@app.route('/')
def index():
    '''Returns "Hello HBNB!" when the / route is requested.'''
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    '''called when "/hbnb" route is requested'''
    return 'HBNB'


@app.route('/c/<text>')
def display_variable(text):
    '''display “C ” followed by the value of the text variable
        (it replace underscore _ symbols with a space )'''
    text_with_spaces = text.replace('_', ' ')
    return f'C {text_with_spaces}'


# Define a Flask route with a variable <text> and a default value "cool"
@app.route('/python//<text>')
@app.route('/python//')
def display_python_value(text='is cool'):
    '''display “Python ”, followed by the value of the text variable
    (replace underscore _ symbols with a space )
    The default value of text is “is cool”'''
    text_with_spaces = text.replace('_', ' ')
    return f'Python {text_with_spaces}'


@app.route('/number/<int:n>/')
def check_integer(n):
    '''display “n is a number” only if n is an integer'''
    if isinstance(n, int):
        return f'{n} is a number'
    else:
        return 404


@app.route('/number_template/<int:n>/')
def number_template(n):
    '''display a HTML page only if n is an integer:
            H1 tag: “Number: n” inside the tag BODY'''
    if isinstance(n, int):
        return render_template('5-number.html', integer=n)
    else:
        return 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
