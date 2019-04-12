from flask import request, abort, jsonify
# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map
from server.utils import five_closest_stations, stations_within_half_mile
from os import getenv

def route():
  def directions(origin_coord, origin_station_coord, dest_station_coord, dest_coord):
    origin = 'origin={},{}'.format(
      origin_coord['latitude'], origin_coord['longitude']
    )
    destination = 'destination={},{}'.format(
      dest_coord['latitude'], dest_coord['longitude']
    )
    waypoints = 'waypoints={},{}|{},{}'.format(
      origin_station_coord['latitude'], origin_station_coord['longitude'], dest_station_coord['latitude'], dest_station_coord['longitude']
    )
    parameters = '{}&{}&{}&key={}'.format(
      origin, destination, waypoints, getenv('G_API_KEY')
    )
    url = 'https://maps.googleapis.com/maps/api/directions/json?{}'.format(parameters)
    return url

  # Find the safest close station
  def safest_station(lat, lon):
    closest = five_closest_stations(lat, lon)
    half_mile = stations_within_half_mile(lat, lon)
    stations = half_mile if len(half_mile) > len(closest) else closest
    return min(stations, key=lambda x: x['percentile'])
  
  origin = {
    'latitude': request.args.get('origin_latitude'),
    'longitude': request.args.get('origin_longitude')
  }

  # Find the safest close station to destination
  destination = {
    'latitude': request.args.get('dest_latitude'),
    'longitude': request.args.get('dest_longitude')
  }

  safe_origin_station = safest_station(origin['latitude'], origin['longitude'])
  safe_dest_station = safest_station(destination['latitude'], destination['longitude'])

  # Output directions from origin -> destination
  directions(origin, safe_origin_station, safe_dest_station, destination)
