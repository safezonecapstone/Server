from flask import Flask, request, Blueprint

StationRouter = Blueprint('stations', __name__, url_prefix='/stations')

@StationRouter.route('/nearby', methods=['GET'])
def nearby_stations():
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    station_filter = request.args.get('filter')
    # Expects 
    # {
    #   latitude:   FLOAT
    #   longitude:  FLOAT
    #   filter:     ARRAY [TRAIN LINE]  Possible Values Listed Above
    # }
    return '''
        <h1>TESTING nearby_stations</h1>
        <p>Received Latitude: {}, Longitude: {}, Filter: {}</p>
        '''.format(lat, lon, station_filter)

