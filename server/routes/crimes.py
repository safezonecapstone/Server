from flask import request, abort, jsonify
from flask import jsonify
from server.models import db
from sqlalchemy.sql import text, select, join
from datetime import datetime, timedelta

# CRIME_NAME
# Possible values:
# ----

# timeSpan
# Possible Values:
# 'YEAR' - Year To Date
# 'MONT' - Last 28 Days
# 'WEEK' - Week To Date

# Expects
# {
#   latitude:  FLOAT
#   longitude: FLOAT
#   filter:    ARRAY [CRIME_NAME]  Possible Values Listed Above
#   timeSpan:  STRING              Possible Values Listed Above
# }

def nearby_crimes():
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    crime_filter = tuple([ int(a) for a in request.args.getlist('filter') ])
    crime_filter = tuple(range(1,13)) if len(crime_filter) == 0 else crime_filter
    time_range = request.args.get('timeSpan')

    today = datetime.today()
    week = today - timedelta(days=7)
    month = today - timedelta(days=30)
    year = today - timedelta(days=365)

    with db.connect() as conn:
        query = text(
            '''
            select t1.crime_date, t1.pd_desc, t1.latitude, t1.longitude, t2.category from crime_info as t1
            join crime_categories as t2 on t1.category_id = t2.id 
            where acos( sin( radians(:lat) ) * sin( radians(latitude) ) + cos( radians(:lat) ) * cos( radians(latitude) ) * cos( radians( :lon - longitude) ) ) * 6371 < 0.1524 and t1.category_id = ANY(:cat)
            '''
        )
        results = conn.execute(query, lat=lat, lon=lon, cat=crime_filter).fetchall()

    return jsonify([
        {
            "date": r[0],
            "crime_desc": r[1],
            "latitude": r[2],
            "longitude": r[3],
            "category": r[4],
        }
        for r in results
    ])
