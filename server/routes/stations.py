from flask import request, abort, jsonify
from server.models import db
from server.utils import five_closest_stations, stations_within_half_mile, station_percentile_rank, crime_categories_occurrences_per_station, crimes_near_station, Dates
from sqlalchemy.sql import text
from typing import List

def nearby_stations_all():
    lat: float = request.args.get('latitude')
    lon: float = request.args.get('longitude')
    
    five_closest: list = five_closest_stations(lat, lon)
    half_mile: list = stations_within_half_mile(lat, lon)

    stations = half_mile if len(half_mile) > len(five_closest) else five_closest

    return jsonify([
        {
            "id": station['id'],
            "name": station['name'],
            "lines": station['line'].split(' '),
            "latitude": station['latitude'],
            "longitude": station['longitude'],
            "percentile": round(station_percentile_rank((station['id'],), tuple(range(1,13)), 365)[0]['percentile'], 2),
        }
        for station in stations
    ])

def station_risk_percent():
    station_ids = tuple( int(a) for a in request.args.getlist('station_ids') )

    crime_filters = tuple( int(a) for a in request.args.getlist('filter') )
    crime_filters = crime_filters if len(crime_filters) > 0 else tuple(range(1,13))
    
    date = Dates[request.args.get('timeSpan', 'year')]

    stations: list = station_percentile_rank(station_ids, crime_filters, date)

    return jsonify([
        {
            "id": station['id'],
            "name": station['name'],
            "lines": station['line'].split(' '),
            "percentile": round(station[3], 2)
        }
        for station in stations
    ])
