from math import cos
import Geohash
from shapely.geometry import Point
from shapely.geometry import Polygon
import requests
import json

def displacement_vertically_down(lat, offset=50.0):
	# offset is in meter
	r_earth = 6378137.0
	pi = 3.14159265

	return lat - (offset/r_earth) * 180 / pi


def displacement_horizontal_right(lat, lon, offset=50.0):
	# offset is in meter
	r_earth = 6378137.0
	pi = 3.14159265
	dLon = offset/(r_earth * cos(pi * lat/180))

	return lon + dLon * 180 / pi

def generate_vertically_down_displaced_points(lat, lon, bottom_boundary):
	latd = lat

	final = []
	while 1:
		latd = displacement_vertically_down(latd)
		if latd < bottom_boundary:
			break

		next_point = Point(latd, lon)

		# print "next point: ", next_point
		final.append(next_point)

	return final


def generate_horizontal_right_points(lat, lon, right_boundary):
	longd = lon

	final = []
	while 1:
		longd = displacement_horizontal_right(lat, longd)
		if longd > right_boundary:
			break

		next_point = Point(lat, longd)

		# print "next point: ", next_point

		final.append(next_point)

	return final


def get_osm_distance_mapping(origin, destinations):
	# osm url
	osm_url = "http://ec2-54-251-156-88.ap-southeast-1.compute.amazonaws.com:8001/v1/maps/distancematrix"

	# format request payload
	destination_list = ["%s,%s" %(d[0], d[1]) for d in destinations]
	destination_string_list = "|".join(destination_list)

	post_data = {
		"origins": "%s,%s" %(origin[0], origin[1]),
		"destinations": destination_string_list,
		"vehicleType": "bike"
	}

	# send request to osm
	# print "post data: %s" %(post_data)
	r = requests.post(osm_url, json = post_data)

	# form custom response
	# print "here result comes from osm url"
	osm_api_result = r.json()["rows"][0]["elements"]

	dist_iter = 0
	custom_response = []
	for dist_map in osm_api_result:
		p = {
			"origin": "%s,%s" %(origin[0], origin[1]),
			"destination": "%s,%s" %(destinations[dist_iter][0], destinations[dist_iter][1]),
			"duration_in_minutes": dist_map["duration_in_minutes"],
			"distance_in_meters": dist_map["distance_in_meters"]
		}

		dist_iter = dist_iter + 1

		custom_response.append(p)

	return custom_response
