from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, return_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cheie..'

@app.route('/')
def hello_world():
    return render_template('input.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    departure = request.form['departure']
    destination = request.form['destination']
    aircraft = request.form['aircraft']
    algorithm = request.form['algorithm']
    return render_template('output.html', departure=departure, destination=destination, aircraft=aircraft, algorithm=algorithm)


if __name__ == '__main__':
    app.run(debug=True)
