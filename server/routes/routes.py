from flask import request, abort, jsonify
# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map
# from server.models import db
# from sqlalchemy.sql import text
# from server.routes import nearby_stations_all
# from server.utils import five_closest_stations, station_percentile_rank, stations_within_half_mile


# def directions(start_lat, start_long, start_stn_lat, start_stn_long, stop_stn_lat, stop_stn_long, dest_lat, dest_long):
# 	origin = "origin=" + start_lat + "," + start_long
# 	destination = "destination=" + dest_lat + "," + dest_long 
# 	waypoints = "waypoints=" + start_stn_lat + "," + start_stn_long + "|" + stop_stn_lat + "," + stop_stn_long 
# 	parameters = origin + "&" + destination + "&" + waypoints + "&key=" + api_key
# 	directions_url = "https://maps.googleapis.com/maps/api/directions/json?" + parameters
# 	return directions_url


# def route():
#     # Find the safest close station to origin
#     lat_orig: float = request.args.get('latitude')
#     lon_orig: float = request.args.get('longitude')
    
#     closest: list = five_closest_stations(lat_orig,lon_orig)
#     half_mile: list = stations_within_half_mile(lat_orig,lon_orig)

#     if len(half_mile) > len(five_closest)
#     	stations = half_mile 
#     else
#     	stations = closest

#     value = 0
#     for station in stations
#         x = round(station_percentile_rank((station['id'],), tuple(range(1,13)), 365)[0], 2)
#         if x > value
#             value = x
#             orig_station = station

#     # Find the safest close station to destination
#     lat_dest: float = request.args.get('latitude_dest')
#     lon_dest: float = request.args.get('longitude_dest')

#     closest_dest: list = five_closest_stations(lat_dest,lon_dest)
#     half_mile_dest: list = stations_within_half_mile(lat_dest,lon_dest)

#     if len(half_mile) > len(five_closest)
#     	stations_dest = half_mile_dest 
#     else
#     	stations_dest = closest_dest

#     value = 0
#     for station in stations_dest
#         x = round(station_percentile_rank((station['id'],), tuple(range(1,13)), 365)[0], 2)
#         if x > value
#             value = x
#             dest_station = station

#     # Output directions from origin -> destination 
#     directions(lat_orig, lon_orig, orig_station.latitude, orig_station.longitude, 
#     	dest_station.latitude, dest_station.longitude, lat_dest, lon_dest)


