from generate_l8_geohash import Generate_Geohash_Metrix
from sample_polygon import Sample_Polygon
from osm_time_mapping import OSM_Time_Mapping

class L8:
	@staticmethod
	def create_metrix():
		# generate marix 
		kormangala_l8_file_name = 'kormangala_l8.txt'
		generate_l8_geohash = Generate_Geohash_Metrix(
			precision=8, polygon=Sample_Polygon.get_kormangala_polygon(), file_name=kormangala_l8_file_name)

		generate_l8_geohash.generate_and_save()
		generate_l8_geohash.print_metrix()
		geohash_metrix = generate_l8_geohash.get_polygon_geohash_metrix()

		# create OSM mapping
		intercept, slope = 7.04, 3.26 # 13th Feb data
		osm_mapping = OSM_Time_Mapping(4, geohash_metrix, intercept, slope, file_name="osm_l8_time_mapping.txt")
		osm_mapping.create_mapping_and_save()

L8.create_metrix()
