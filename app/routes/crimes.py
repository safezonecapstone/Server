from flask import Flask, request, Blueprint

CrimeRouter = Blueprint('crimes', __name__, url_prefix='/crimes')

@CrimeRouter.route('/nearby', methods=['GET'])
def nearby_crimes():
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    crime_filter = request.args.get('filter')
    time_range = request.args.get('timeSpan')
    # Expects
    # {
    #   latitude:  FLOAT
    #   longitude: FLOAT
    #   filter:    ARRAY [CRIME_NAME]  Possible Values Listed Above
    #   timeSpan:  STRING              Possible Values Listed Above
    # }
    return '''
        <h1>TESTING nearby_crimes</h1>
        <p>Received Latitude: {}, Longitude: {}, Filter: {}, Range: {}</p>
        '''.format(lat, lon, crime_filter, time_range)