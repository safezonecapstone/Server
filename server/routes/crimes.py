from flask import request, abort, jsonify
from flask import jsonify
from server import db

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
        crime_filter = request.args.get('filter')
        time_range = request.args.get('timeSpan')

        # if lat == None or lon == None:
        #         abort(500)

        with db.connect() as conn:
                crimes = conn.execute(
                        '''select crime_info.crime_date, crime_info.pd_desc, crime_info.latitude, crime_info.longitude, crime_categories.category from crime_info
                        join crime_categories on crime_info.category_id=crime_categories.id 
                        limit 1'''
                        ).fetchall()

        return jsonify([
                {
                        "date": crime[0],
                        "pd_desc": crime[1],
                        "latitude": crime[2],
                        "longitude": crime[3],
                        "category": crime[4]
                }
                for crime in crimes
        ])
