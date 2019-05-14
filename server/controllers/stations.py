from flask import request, jsonify
from server.utils import closest_stations, crimes_near_station, Dates
from server import db

# Nearby Stations Endpoint
def nearby_stations_all():
    lat: float = request.args.get('latitude')
    lon: float = request.args.get('longitude')
    
    stations: list = closest_stations(db, lat, lon)

    return jsonify(
        [
            {
                "id": station['id'],
                "name": station['name'],
                "lines": station['line'].split(' '),
                "latitude": station['latitude'],
                "longitude": station['longitude'],
                "percentile": round(station['percentile'], 2),
            }
            for station in stations
        ]
    )

# Nearby Crimes of a Station Endpoint
def nearby_crimes_for_stations():
    station_id: int = request.args.get('id')
    time_range: int = Dates[request.args.get('timeSpan', 'year')]
    results: list = crimes_near_station(db, station_id, time_range)

    category_counts = {
        'Murder': 0,
        'Rape': 0,
        'Robbery': 0,
        'Felony Assault': 0,
        'Burglary': 0,
        'Grand Larceny': 0,
        'Petit Larceny': 0,
        'Misdemeanor Assault': 0,
        'Misdemeanor Sex Crimes': 0,
        'Kidnapping': 0,
        'Offenses against Public Order': 0,
        'Shootings': 0
    }

    crimes = []

    for r in results:
        crimes.append(
            {
                "date": r['crime_date'],
                "category": r['category'],
                "ofns_desc": r['ofns_desc'],
                "pd_desc": r['pd_desc'],
                "latitude": r['latitude'],
                "longitude": r['longitude'],
            }
        )
        category_counts[r['category']] += 1

    return jsonify(
        {
            'results': crimes,
            'frequencies': category_counts
        }
    )