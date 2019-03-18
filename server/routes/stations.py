from flask import request, abort, jsonify
from server.models import db
from sqlalchemy.sql import text

def nearby_stations():
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    limit = request.args.get('limit', 5)

    with db.connect() as conn:
        query = text(
            '''
            select * from (select name, line, latitude, longitude, acos( sin( radians(:lat) ) * sin( radians(latitude) ) + cos( radians(:lat) ) * cos( radians(latitude) ) * cos( radians(:lon - longitude) ) ) * 6371 as distance from stations) as t1
            where distance < 0.402336 limit :limit
            '''
        )
        stations = conn.execute(query, lat=lat, lon=lon, limit=limit)

    return jsonify([
        {
            "name": station[0],
            "lines": station[1],
            "latitude": station[2],
            "longitude": station[3]

        }
        for station in stations
    ])
