from flask import request, jsonify
from server.utils import closest_stations, get_station
from server import db
from os import getenv
from requests import get

def route():
    def directions(origin_coord, dest_coord) -> str:
        origin     : str = 'origin={},{}'.format( origin_coord['latitude'], origin_coord['longitude'] )
        destination: str = 'destination={},{}'.format( dest_coord['latitude'], dest_coord['longitude'] )
        parameters : str = '{}&{}&key={}'.format( origin, destination, getenv('G_API_KEY') )
        url        : str = 'https://maps.googleapis.com/maps/api/directions/json?{}&mode=transit&transit_mode=subway&alternatives=true'.format(parameters)
        return url
    
    origin = {
        'latitude' : request.args.get('origin_latitude'),
        'longitude': request.args.get('origin_longitude')
    }

    destination = {
        'latitude' : request.args.get('dest_latitude'),
        'longitude': request.args.get('dest_longitude')
    }

    data = get( directions(origin, destination) ).json()

    ratings = []

    for i, r in enumerate(data['routes']):
        count, rating = 0, 0
        for j, l in enumerate(r['legs']):
            for k, s in enumerate(l['steps']):
                if s['travel_mode'] == 'TRANSIT':
                    details = s['transit_details']
                    from_station_name = details['departure_stop']['name']
                    to_station_name = details['arrival_stop']['name']
                    line = details['line']['short_name']
                    count, rating = count + 1, rating + ( get_station(db, from_station_name, line)[0]['percentile'] + get_station(db, to_station_name, line)[0]['percentile'] ) / 2
        ratings.append( round(rating / count, 2) )

    # Output directions from origin -> destination
    return jsonify(
        {
            'data': data,
            'ratings': ratings
        }
    )
