from flask import request, abort, jsonify
# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map
from server.utils import five_closest_stations, stations_within_half_mile, station_percentile_rank
from os import getenv

def route():
  def directions(origin_coord, origin_station_coord, dest_station_coord, dest_coord) -> str:
    origin     : str = 'origin={},{}'.format( origin_coord['latitude'], origin_coord['longitude'] )
    destination: str = 'destination={},{}'.format( dest_coord['latitude'], dest_coord['longitude'] )
    parameters : str = '{}&{}&key={}'.format( origin, destination, getenv('G_API_KEY') )
    url        : str = 'https://maps.googleapis.com/maps/api/directions/json?{}'.format(parameters)
    return url

  # Find the safest close station
  def safest_station(lat, lon):
    closest   = five_closest_stations(lat, lon)
    half_mile = stations_within_half_mile(lat, lon)
    stations  = half_mile if len(half_mile) > len(closest) else closest
    return min(stations, key=lambda x: round(station_percentile_rank((x['id'], ), tuple(range(1,13)), 365)[0]['percentile'], 2) )
  
  origin = {
    'latitude' : request.args.get('origin_latitude'),
    'longitude': request.args.get('origin_longitude')
  }

  destination = {
    'latitude' : request.args.get('dest_latitude'),
    'longitude': request.args.get('dest_longitude')
  }

  safe_origin_station = safest_station(origin['latitude'], origin['longitude'])
  safe_dest_station   = safest_station(destination['latitude'], destination['longitude'])

  # Output directions from origin -> destination
  return jsonify(
    directions(origin, safe_origin_station, safe_dest_station, destination)
  )
