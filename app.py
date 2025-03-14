from flask import Flask, render_template, request, jsonify
from database import get_db_connection, return_db_connection
from flask_cors import CORS
from algorithms import astar, dijkstra
import json
from weather import get_weather
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CORS(app)

def load_mapping():
    mapping = {}
    with open('static/icao.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                iata = parts[0].strip().upper()
                icao = parts[1].strip().upper()
                mapping[iata] = icao
    return mapping

def load_location_mapping():
    mapping = {}
    with open('static/airports.csv', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 4:
                city = parts[0].strip()
                airport_name = parts[1].strip()
                iata = parts[2].strip().upper()
                country = parts[3].strip()
                mapping[iata] = {'airport_name': airport_name, 'city': city, 'country': country}
    return mapping

@app.route('/')
def hello_world():
    return render_template('input.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    departure = request.form['departure'].strip().upper()
    destination = request.form['destination'].strip().upper()
    aircraft = request.form['aircraft']
    algorithm = request.form['algorithm'].strip().lower()

    with open('static/graph.json', 'r') as f:
        graph = json.load(f)

    coordinates = {}
    if algorithm == "a*":
        with open("static/coordinates.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    iata = parts[0].strip().upper()
                    lat = float(parts[1])
                    lon = float(parts[2])
                    coordinates[iata] = (lat, lon)

    path, cost = [], None
    if algorithm == "dijkstra":
        path, cost = dijkstra(graph, departure, destination)
    elif algorithm == "a*":
        path, cost = astar(graph, coordinates, departure, destination)
    else:
        return "Error: invalid algorithm", 400

    cost_miles = cost * 0.621371 if cost else None

    iata_to_icao = load_mapping()
    icao_codes = []
    for iata in path:
        icao = iata_to_icao.get(iata)
        if icao:
            icao_codes.append(icao)

    iata_to_location = load_location_mapping()

    weather_data = get_weather(icao_codes)
    weather_along_route = []
    for iata in path:
        icao = iata_to_icao.get(iata, "Unknown ICAO")
        location = iata_to_location.get(iata, {'airport_name': "Unknown airport", 'city': "Unknown City", 'country': "Unknown Country"})
        metars = weather_data.get(icao, ["No data available"])
        weather_along_route.append({
            'airport': iata,
            'icao': icao,
            'airport_name': location['airport_name'],
            'city': location['city'],
            'country': location['country'],
            'weather': metars[0] if isinstance(metars, list) and metars else "No data available"
        })

    return render_template('output.html',
                           departure=departure, destination=destination, aircraft=aircraft, algorithm=algorithm,
                           path=path, cost=round(cost, 2) if cost else "No path found",
                           cost_miles=round(cost_miles, 2) if cost_miles else "No path found",
                           weather_along_route=weather_along_route)

@app.route('/airports', methods=['GET'])
def airports():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM airports")
    airports = cursor.fetchall()
    cursor.close()
    return_db_connection(connection)

    airport_list = [{
        'Airport Name': airport[0],
        'City': airport[1],
        'IATA Code': airport[2],
        'Country': airport[3]
    } for airport in airports]

    return jsonify(airport_list)
if __name__ == '__main__':
    app.run(debug=True)
