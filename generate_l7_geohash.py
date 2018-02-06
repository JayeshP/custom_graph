# following tasks are done in this script 
# 1. Given a area polygon, it will generate points inside polygon having vertical and horizontal displacement as set
# 2. It will create mapping of each point inside polygon with level 4 (varible) neighbour points and store distance between them
# by calculating from OSM endpoint

import Geohash
from shapely.geometry import Point
from shapely.geometry import Polygon
from helper import generate_vertically_down_displaced_points, generate_horizontal_right_points, get_osm_distance_mapping
import json

# Constant variables

# horizontal_displacement: 50
# vertical_displacement: 50
# level: 4 -> nearby neighbours level for a point to point distance
# polygon: kormangala
# file name: kormangala_l7.txt, osm_mapping_50_by_50_metrix
# slope and intercept from database

###

# initialise
kormangala_polygon = Polygon([(12.949705,77.62063699999999), (12.9499340325728,77.62065525924686), (12.95036222728716,77.62092188093561), (12.950832244964888,77.6212099602966), (12.951083941889555,77.62131438092047), (12.952446804482006,77.6214620925598), (12.955668986121669,77.62155740605169), (12.955168909774535,77.62277924732985), (12.954802556198178,77.62349939052206), (12.953934324489722,77.62396204164884), (12.950692202652117,77.62392174865727), (12.950576382702108,77.62445544839477), (12.950411500502751,77.6257422232054), (12.949723820220761,77.62679296362296), (12.949101286852766,77.62760698413081), (12.948652446750618,77.6278065998763), (12.947408945971782,77.6283495383758), (12.947494130816644,77.6283196164245), (12.948594982729626,77.6277751984253), (12.94750381028593,77.62830765213016), (12.944969685795082,77.62995590478522), (12.943049095798743,77.63050190213016), (12.942628128361227,77.63083020635986), (12.941936655172654,77.63117674868772), (12.941256315663145,77.63160751191708), (12.939880965412431,77.63212330094143), (12.938735649171765,77.63281075134273), (12.938178207076634,77.63335858434675), (12.937348895157173,77.63457160518647), (12.93945459588482,77.63695473152154), (12.937388175084738,77.63850100864397), (12.935089714786644,77.63720348184575), (12.933668604106538,77.63818550152769), (12.932247485331782,77.6371075846863), (12.931246755277645,77.63765929367071), (12.930977995239177,77.63814662963864), (12.930820743690992,77.63860994313052), (12.930830800302576,77.63877284921273), (12.93083,77.63892699999997), (12.930570286840155,77.64016525131228), (12.930900528012069,77.64076291929632), (12.930731032119175,77.64149090673061), (12.930228012962829,77.64149012002179), (12.92953731708228,77.6414038959789), (12.928423526869617,77.64160764552548), (12.927477042193857,77.64232637920281), (12.927743556350974,77.64351718166677), (12.928512,77.64419299999997), (12.92889453215653,77.64499316665649), (12.929211280012861,77.64528596162415), (12.92840762413776,77.64656961573041), (12.927457569061936,77.64791764285269), (12.927047989302437,77.64849838689418), (12.927558617746767,77.64907913093566), (12.92725971584108,77.65018489449699), (12.927964676340856,77.65146231943515), (12.928899685514564,77.65188143748856), (12.92915805222028,77.65309950710491), (12.928956318069211,77.65350218518074), (12.928240947299559,77.65371580688475), (12.92698396731534,77.65289993783563), (12.92537251969857,77.65298552976992), (12.925382438614248,77.65184815377052), (12.924409398486455,77.65159054232788), (12.924610963160893,77.65062239682766), (12.924791613642135,77.64920364021305), (12.924567321495482,77.64709568783564), (12.924510341642659,77.64533105821226), (12.923324,77.64124900000002), (12.92416517339723,77.63914778836056), (12.925257311994752,77.63708949206546), (12.925264437821962,77.63544104167181), (12.924895111524586,77.63310594577024), (12.924156457290884,77.62873616137699), (12.923452503282572,77.62604701388545), (12.922874032472967,77.62327203570544), (12.921354417731287,77.62075454959097), (12.921006,77.62029699999994), (12.929442252120959,77.61519966931155), (12.933785750957066,77.61262954629524), (12.938171,77.610274), (12.938678533420722,77.61078863095099), (12.939478845185468,77.6119040767212), (12.940117476512382,77.61310500000002), (12.942970699996216,77.6114472539673), (12.943493626328904,77.61168952114872), (12.94279311491004,77.61378476057439), (12.94171617477807,77.6158156269837), (12.943590954611345,77.61579360052497), (12.943775492538522,77.61615809655768), (12.944265097346783,77.6166407519836), (12.944922,77.61682300000007), (12.945387965726104,77.61649608465586), (12.946314,77.61625500000002), (12.945373350790318,77.6180988306885), (12.945908033780174,77.61814482803345), (12.945861691067922,77.61857552247625)])

sum_ = 0
kormangala_l7_file_handle = open('kormangala_l7.txt', 'w')

w_iter = 0
h_iter = 0

kormangala_points = []

total_osm_map = []
graph_string = ""

kormangala_last_mile_intercept = 8.30
kormangala_last_mile_slope = 2.67
####

# test
print 'Geohash for 42.6, -5.6:', Geohash.encode(12.9354922,77.6146828, precision=7)

point = Point(12.9354922,77.6146828)

print kormangala_polygon.contains(point)

print "bounds: ", kormangala_polygon.bounds
####

# find left bottom point for kormangala
min_lat, min_log, max_lat, max_log = kormangala_polygon.bounds

print "starting point", min_lat, min_log

# vertical left most boundary for kormangala
left_boundary_points = generate_vertically_down_displaced_points(max_lat, min_log, min_lat)

print "max points vertical boundary", len(left_boundary_points)

# initialise matrix
horizontal_points = generate_horizontal_right_points(left_boundary_points[0].x, left_boundary_points[0].y, max_log)

print "max points in horizontal boundary", len(horizontal_points)

w, h = len(horizontal_points) + 1, len(left_boundary_points) + 1

Matrix = [[0 for x in range(w)] for y in range(h)]
###


# Get all points in kormangala, traverse horizontal direction from above result
for p in left_boundary_points:
	Matrix[h_iter][0] = (p.x, p.y)
	result = generate_horizontal_right_points(p.x, p.y, max_log)

	w_iter = 1
	for r in result:
		sum_ = sum_ + 1
		# get all kormanagala points
		if kormangala_polygon.contains(r):
			# store geo hash into file
			kormangala_points.append(r)
			geohash_r = Geohash.encode(r.x, r.y, precision=8)
			kormangala_l7_file_handle.write("%s\n" % geohash_r)

		print "h_iter: %s w_iter: %s" %(h_iter, w_iter)
		Matrix[h_iter][w_iter] = (r.x, r.y)
		w_iter = w_iter + 1

	h_iter = h_iter + 1

print sum_

# find 4 level OSM distance for kormangala points
i, j = 0, 0
for i in range(h_iter):
	for j in range(w_iter):
		destinations = []
		origin = Matrix[i][j]
		# if Matrix[i][j] in kormangala_points: Checking in kormangala points list is slower than checking whether point lies in polygon
		# process only on kormangala points
		if kormangala_polygon.contains(Point(Matrix[i][j])):
			# print
			print "i: %s j:%s v:%s" %(i, j, Matrix[i][j])
			graph_string += "- "
			# find mapping till 4 level
			for level in range(1, 5):
				if (i + level) < h_iter and kormangala_polygon.contains(Point(Matrix[i + level][j])):
					destinations.append(Matrix[i + level][j])

				if (i - level) > -1 and kormangala_polygon.contains(Point(Matrix[i - level][j])):
					destinations.append(Matrix[i - level][j])

				if (j + level) < w_iter and kormangala_polygon.contains(Point(Matrix[i][j + level])):
					destinations.append(Matrix[i][j + level])

				if (j - level) > -1 and kormangala_polygon.contains(Point(Matrix[i][j - level])):
					destinations.append(Matrix[i][j - level])

				# diagonal left bottom
				if  (i - level) > -1 and (j - level) > -1 and kormangala_polygon.contains(Point(Matrix[i - level][j - level])):
					destinations.append(Matrix[i - level][j - level])

				# diagonal left top
				if  (i - level) > -1 and (j + level) < w_iter -1 and kormangala_polygon.contains(Point(Matrix[i - level][j + level])):
					destinations.append(Matrix[i - level][j + level])

				# diagonal right bottom
				if  (i + level) < h_iter and (j - level) > -1 and kormangala_polygon.contains(Point(Matrix[i + level][j - level])):
					destinations.append(Matrix[i + level][j - level])

				# diagonal right top
				if  (i + level) < h_iter and (j + level) < w_iter and kormangala_polygon.contains(Point(Matrix[i + level][j + level])):
					destinations.append(Matrix[i + level][j + level])
		else:
			graph_string += "  "
		if len(destinations) > 0:
			print "Hitting OSM"
			osm_result = get_osm_distance_mapping(origin, destinations, kormangala_last_mile_intercept, kormangala_last_mile_slope)
			total_osm_map = total_osm_map + osm_result


	graph_string += "\n"

print "kormangala string: \n", graph_string
with open('kormangala_point_graph.txt', 'w') as outfile:
	outfile.write(graph_string)

with open('osm_mapping_50_by_50_metrix.txt', 'w') as outfile:
    json.dump(total_osm_map, outfile, indent=4)


