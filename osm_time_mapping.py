from helper import get_osm_distance_mapping
import Geohash
import json

class OSM_Time_Mapping:
	def __init__(self, level, metrix, intercept, slope, file_name):
		self.level = level
		self.metrix = metrix
		self.metrix_height = len(self.metrix)
		self.metrix_width = len(self.metrix[0])
		self.intercept = intercept
		self.slope = slope
		self.file_name = file_name

	def get_adjacent_till_level(self, h_iter, w_iter):
		i, j = h_iter, w_iter

		nearbys = []
		for level in range(1, self.level):
			# top
			if (i + level) < self.metrix_height and self.metrix[i + level][j] is not None:
				nearbys.append(self.metrix[i + level][j])

			# bottom
			if (i - level) > -1 and self.metrix[i - level][j] is not None:
				nearbys.append(self.metrix[i - level][j])

			# right
			if (j + level) < self.metrix_width and self.metrix[i][j + level] is not None:
				nearbys.append(self.metrix[i][j + level])

			# left
			if (j - level) > -1 and self.metrix[i][j - level] is not None:
				nearbys.append(self.metrix[i][j - level])

			# diagonal left bottom
			if  (i - level) > -1 and (j - level) > -1 and self.metrix[i - level][j - level] is not None:
				nearbys.append(self.metrix[i - level][j - level])

			# diagonal bottom right
			if  (i - level) > -1 and (j + level) < self.metrix_width -1 and self.metrix[i - level][j + level] is not None:
				nearbys.append(self.metrix[i - level][j + level])

			# diagonal top left
			if  (i + level) < self.metrix_height and (j - level) > -1 and self.metrix[i + level][j - level] is not None:
				nearbys.append(self.metrix[i + level][j - level])

			# diagonal top right
			if  (i + level) < self.metrix_height and (j + level) < self.metrix_width and self.metrix[i + level][j + level] is not None:
				nearbys.append(self.metrix[i + level][j + level])

		return nearbys

	def get_adjacent_osm_data(self, origin, h_iter, w_iter):
		destinations = self.get_adjacent_till_level(h_iter, w_iter)
		osm_result = []

		if len(destinations) > 0:
			print "Hitting OSM"
			origin_point = Geohash.decode(origin)
			destination_points = [Geohash.decode(d) for d in destinations]

			osm_result = get_osm_distance_mapping(origin_point, destination_points, self.intercept, self.slope)
			
		return osm_result

	def create_mapping(self):
		i, j = 0, 0
		osm_mapping = []
		for i in range(self.metrix_height):
			for j in range(self.metrix_width):
				origin = self.metrix[i][j]
				if origin is not None:
					osm_data = self.get_adjacent_osm_data(origin, i, j)
					osm_mapping += osm_data

		return osm_mapping

	def create_mapping_and_save(self):
		osm_mapping = self.create_mapping()
		self.save(osm_mapping)

	def save(self, mapping):
		with open(self.file_name.rstrip('.txt') + '_full_data.txt', 'w') as outfile:
			json.dump(mapping, outfile, indent=4)

		geohash_time_mapping = {}
		for m in mapping:
			origin_geohash = m['origin_geohash_l7']
			destination_geohah = m['destination_geohash_l7']
			if origin_geohash == destination_geohah:
				continue

			time = int(m['duration_in_sec_by_de_area_velocity'])

			if origin_geohash in geohash_time_mapping:
				geohash_time_mapping[origin_geohash][destination_geohah] = time
			else:
				geohash_time_mapping[origin_geohash] = {destination_geohah: time}
		
		with open(self.file_name, 'w') as outfile:
			json.dump(geohash_time_mapping, outfile, indent=4)

# print "kormangala string: \n", graph_string
# with open('kormangala_point_graph.txt', 'w') as outfile:
# 	outfile.write(graph_string)

# with open('osm_mapping.txt', 'w') as outfile:
#     json.dump(total_osm_map, outfile, indent=4)


# {"fdsadfs": 0: {"fds": }}