from flask import request, jsonify
from server.utils import crimes_near_point, Dates
from server import db


# Nearby Crimes Endpoint Function
def nearby_crimes_by_point():

    lat: float = request.args.get('latitude')
    lon: float  = request.args.get('longitude')
    time_range: int = Dates[request.args.get('timeSpan', 'year')]

    results = crimes_near_point(db, lat, lon, time_range)

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
