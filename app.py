from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_db_connection, return_db_connection
from flask_cors import CORS
from algorithms import astar, dijkstra
import json

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

    with open('static/graph.json', 'r') as f:
        graph = json.load(f)

    coordinates={}
    if algorithm=="astar":
        with open("static/coordinates.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                iata = parts[0].strip()
                lat = float(parts[1])
                lon = float(parts[2])
                coordinates[iata] = (lat, lon)
    path = []
    cost=None
    if algorithm == "Dijkstra":
        path, cost = dijkstra(graph, departure, destination)
    elif algorithm == "A*":
        path, cost = astar(graph,coordinates, departure, destination)
    else:
        return "Error: invalid algorithm", 400

    cost_miles = cost * 0.621371 if cost else None

    return render_template('output.html',
                           departure=departure, destination=destination, aircraft=aircraft, algorithm=algorithm,
                           path=path, cost=round(cost, 2) if cost else "No path found",
                           cost_miles=round(cost_miles, 2) if cost_miles else "No path found")

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
