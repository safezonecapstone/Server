from flask import request, abort, jsonify
from flask import jsonify
from server.models import db
from server.utils import crimes_near_point
from sqlalchemy.sql import text, select, join
from datetime import datetime, timedelta

def nearby_crimes_by_point():

    lat = request.args.get('latitude')
    lon = request.args.get('longitude')

    crime_filter = tuple([ int(a) for a in request.args.getlist('filter') ])
    crime_filter = crime_filter if len(crime_filter) > 0 else tuple(range(1,13))

    time_range = request.args.get('timeSpan', 'year')

    if time_range == 'week':
        time_range = datetime.today() - timedelta(days=7)
    elif time_range == 'month':
        time_range = datetime.today() - timedelta(days=30)
    elif time_range == 'year':
        time_range = datetime.today() - timedelta(days=365)

    results = crimes_near_point(lat, lon, crime_filter, time_range)

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
        crimes.append({
            "date": r[0],
            "category": r[1],
            "ofns_desc": r[2],
            "pd_desc": r[3],
            "latitude": r[4],
            "longitude": r[5],
        })
        category_counts[r[1]] += 1

    return jsonify(
        {
            'results': crimes,
            'frequencies': category_counts
        }
    )
