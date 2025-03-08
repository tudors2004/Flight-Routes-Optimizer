from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_db_connection, return_db_connection
from flask_cors import CORS
from algorithms import astar, dijkstra

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cheie..'
CORS(app)

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

@app.route('/airports', methods=['GET'])
def airports():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM airports")
    airports = cursor.fetchall()
    cursor.close()
    return_db_connection(connection)
    airportlist = []
    for airport in airports:
        airportlist.append({
            'Airport Name': airport[0],
            'City': airport[1],
            'IATA Code': airport[2],
            'Country': airport[3]
        })
    return jsonify(airportlist)
if __name__ == '__main__':
    app.run(debug=True)
