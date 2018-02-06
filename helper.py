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


def get_osm_distance_mapping(origin, destinations, intercept, slope):
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

	### form custom response
	custom_response = []
	osm_api_result = r.json()["rows"][0]["elements"]

	dist_iter = 0
	for dist_map in osm_api_result:
		p = {
			"origin": "%s,%s" %(origin[0], origin[1]),
			"origin_geohash_l7": Geohash.encode(origin[0], origin[1], precision=7),
			"origin_geohash_l8": Geohash.encode(origin[0], origin[1], precision=8),
			"destination": "%s,%s" %(destinations[dist_iter][0], destinations[dist_iter][1]),
			"destination_geohash_l7": Geohash.encode(destinations[dist_iter][0], destinations[dist_iter][1], precision=7),
			"destination_geohash_l8": Geohash.encode(destinations[dist_iter][0], destinations[dist_iter][1], precision=8),
			"osm_duration_in_minutes": dist_map["duration_in_minutes"],
			"distance_in_meters": dist_map["distance_in_meters"],
			"duration_in_sec_by_de_area_velocity": (((dist_map["distance_in_meters"]/1000) * slope) + intercept) * 60
		}

		dist_iter = dist_iter + 1

		custom_response.append(p)

	return custom_response

# 50m * 50m area, india boundary
# left = 0, right = 1, top = 0, bottom = 1
def custom_geohash_base16_encode(lat, lng):
	# india's boundary
	min_lat, max_lat = 06.0, 36.0
	min_lng, max_lng = 68.0, 98.0

	binary = ''
	result = 0
	for i in xrange(0, 32):
		if i % 2 == 0:
			mid = (min_lng + max_lng) / 2
			# print "i:%s, min_lng:%s, max_lng:%s, mid:%s" %(i, min_lng, max_lng, mid)
			if lng < mid:
				result = result * 2
				max_lng = mid
				binary += '0'
				# print '0'
			else:
				result = result * 2 + 1
				min_lng = mid
				binary += '1'
				# print '1'
		else:
			mid = (min_lat + max_lat) / 2
			# print "i:%s, min_lat:%s, max_lat:%s, mid:%s" %(i, min_lat, max_lat, mid)
			if lat < mid:
				result = result * 2 + 1
				max_lat = mid
				binary += '1'
				# print '1'
			else:
				result = result * 2
				min_lat = mid
				binary += '0'
				# print '0'

	# test
	print 'binary ', binary
	print "encode number: ", result 
	return hex(result)[2:]

# 50m * 50m area, india boundary
# left = 0, right = 1, top = 0, bottom = 1
def custom_geohash_base16_decode(geohash):
	# india's boundary
	min_lat, max_lat = 06.0, 36.0
	min_lng, max_lng = 68.0, 98.0


	location_point = int(geohash, 16)
	print "integer of geohash", location_point
	blocation_point = format(location_point, '0>32b')

	print 'binary of geohash', blocation_point

	for i in xrange(0, 32):
		if i % 2 == 0:
			# lng
			mid = ( min_lng + max_lng ) / 2
			# print "binary: %s, i:%s, min_lng:%s, max_lng:%s, mid:%s" %(blocation_point[i], i, min_lng, max_lng, mid)
			if blocation_point[i] == '0':
				max_lng = mid						
			else:
				min_lng = mid
		else:
			# lat
			mid = (min_lat + max_lat ) / 2
			# print "binary:%s, i:%s, min_lat:%s, max_lat:%s, mid:%s" %(blocation_point[i], i, min_lat, max_lat, mid)
			if blocation_point[i] == '1':
				max_lat = mid
			else:
				min_lat = mid

	
	return (( min_lat + max_lat ) / 2, ( min_lng + max_lng ) / 2)