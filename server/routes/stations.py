from flask import request, abort, jsonify
from server.models import db
from server.utils import five_closest_stations, stations_within_half_mile
from sqlalchemy.sql import text

def nearby_stations():
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    
    five_closest = five_closest_stations(lat, lon)
    half_mile = stations_within_half_mile(lat, lon)

    stations = half_mile if len(half_mile) > len(five_closest) else five_closest 

    return jsonify([
        {
            "id": station[0],
            "name": station[1],
            "lines": station[2].split('-'),
            "latitude": station[3],
            "longitude": station[4]
        }
        for station in stations
    ])
