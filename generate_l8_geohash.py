import Geohash
from shapely.geometry import Point
from shapely.geometry import Polygon
from helper import generate_vertically_down_displaced_points, generate_horizontal_right_points, get_osm_distance_mapping, custom_geohash_base16_encode
import json
import geohash as geohash_func

class Generate_Geohash_Metrix:
	def __init__(self, precision, polygon, file_name):
		self.polygon = polygon
		self.file_name = file_name
		self.min_lat, self.min_lng, self.max_lat, self.max_log = polygon.bounds
		self.precision = precision

		left_top_geohash = Geohash.encode(self.max_lat, self.min_lng, precision=self.precision)
		bottom_left_boundary_geohash = Geohash.encode(self.min_lat, self.min_lng, precision=self.precision)
		self.left_bound_vertical_geohashes = self.generate_vertically_down_geohashes(left_top_geohash, bottom_left_boundary_geohash)

		top_right_boundary_geohash = Geohash.encode(self.max_lat, self.max_log, precision=self.precision)
		self.top_bound_horizontal_geohashes = self.generate_horizontal_right_geohashes(left_top_geohash, top_right_boundary_geohash)

		self.Metrix = self.initialise_metrix()

	def generate_vertically_down_geohashes(self, geohash, boundary):
		result = []
		result.append(geohash)
		while geohash != boundary:
			geohash = geohash_func.neighbors(geohash)[6]
			result.append(geohash)

		return result

	def generate_horizontal_right_geohashes(self, geohash, boundary, is_inside_polygon=True):
		result = []
		def get_geohash():
			if is_inside_polygon:
				if self.is_inside_polygon(geohash):
					return geohash
				else:
					return None

			return geohash

		# print boundary
		result.append(get_geohash())
		while geohash != boundary:
			geohash = geohash_func.neighbors(geohash)[1]
			result.append(get_geohash())
			# print geohash

		return result

	def is_inside_polygon(self, geohash):
		point = Geohash.decode(geohash)
		# print point, point[0], point[1]
		if self.polygon.contains(
				Point(float(point[0]), float(point[1]))):
			return True

		return False

	def generate_and_save(self):
		top_right_boundary_geohash = Geohash.encode(self.max_lat, self.max_log, precision=self.precision)

		self.Metrix[0] = self.top_bound_horizontal_geohashes
		i = 1
		for g in self.left_bound_vertical_geohashes[1:]:
			# print "parsing vertical line ", i
			top_right_boundary_geohash = geohash_func.neighbors(top_right_boundary_geohash)[6]
			horizontal_geohashes = self.generate_horizontal_right_geohashes(g, top_right_boundary_geohash)
			self.Metrix[i] = horizontal_geohashes
			i += 1

		self.save()

	def initialise_metrix(self):
		self.metrix_width, self.metrix_height = len(self.top_bound_horizontal_geohashes), len(self.left_bound_vertical_geohashes)

		return [[0 for x in range(self.metrix_width)] for y in range(self.metrix_height)]

	def print_metrix(self):
		metrix_str = 'Kormangala : \n'
		# print 'max height and width: ', self.metrix_height, self.metrix_width
		# print 'metrix size: ', len(self.Metrix), len(self.Metrix[0])
		for h in range(0, self.metrix_height):
			for w in range(0, self.metrix_width):
				# print 'height, width ', h, w
				if self.Metrix[h][w] == None:
					metrix_str += ' '
				else:
					metrix_str += '-'
			metrix_str += '\n'

		print metrix_str

	def save(self):
		with open(self.file_name, 'w') as outfile:
			for h in range(0, self.metrix_height):
				for w in range(0, self.metrix_width):
					if self.Metrix[h][w] is not None:
						print "adding to file"
						outfile.write("%s\n" % self.Metrix[h][w])

	def get_polygon_geohash_metrix(self):
		return self.Metrix

###############################################################################

# kormangala_polygon = Polygon([(12.949705,77.62063699999999), (12.9499340325728,77.62065525924686), (12.95036222728716,77.62092188093561), (12.950832244964888,77.6212099602966), (12.951083941889555,77.62131438092047), (12.952446804482006,77.6214620925598), (12.955668986121669,77.62155740605169), (12.955168909774535,77.62277924732985), (12.954802556198178,77.62349939052206), (12.953934324489722,77.62396204164884), (12.950692202652117,77.62392174865727), (12.950576382702108,77.62445544839477), (12.950411500502751,77.6257422232054), (12.949723820220761,77.62679296362296), (12.949101286852766,77.62760698413081), (12.948652446750618,77.6278065998763), (12.947408945971782,77.6283495383758), (12.947494130816644,77.6283196164245), (12.948594982729626,77.6277751984253), (12.94750381028593,77.62830765213016), (12.944969685795082,77.62995590478522), (12.943049095798743,77.63050190213016), (12.942628128361227,77.63083020635986), (12.941936655172654,77.63117674868772), (12.941256315663145,77.63160751191708), (12.939880965412431,77.63212330094143), (12.938735649171765,77.63281075134273), (12.938178207076634,77.63335858434675), (12.937348895157173,77.63457160518647), (12.93945459588482,77.63695473152154), (12.937388175084738,77.63850100864397), (12.935089714786644,77.63720348184575), (12.933668604106538,77.63818550152769), (12.932247485331782,77.6371075846863), (12.931246755277645,77.63765929367071), (12.930977995239177,77.63814662963864), (12.930820743690992,77.63860994313052), (12.930830800302576,77.63877284921273), (12.93083,77.63892699999997), (12.930570286840155,77.64016525131228), (12.930900528012069,77.64076291929632), (12.930731032119175,77.64149090673061), (12.930228012962829,77.64149012002179), (12.92953731708228,77.6414038959789), (12.928423526869617,77.64160764552548), (12.927477042193857,77.64232637920281), (12.927743556350974,77.64351718166677), (12.928512,77.64419299999997), (12.92889453215653,77.64499316665649), (12.929211280012861,77.64528596162415), (12.92840762413776,77.64656961573041), (12.927457569061936,77.64791764285269), (12.927047989302437,77.64849838689418), (12.927558617746767,77.64907913093566), (12.92725971584108,77.65018489449699), (12.927964676340856,77.65146231943515), (12.928899685514564,77.65188143748856), (12.92915805222028,77.65309950710491), (12.928956318069211,77.65350218518074), (12.928240947299559,77.65371580688475), (12.92698396731534,77.65289993783563), (12.92537251969857,77.65298552976992), (12.925382438614248,77.65184815377052), (12.924409398486455,77.65159054232788), (12.924610963160893,77.65062239682766), (12.924791613642135,77.64920364021305), (12.924567321495482,77.64709568783564), (12.924510341642659,77.64533105821226), (12.923324,77.64124900000002), (12.92416517339723,77.63914778836056), (12.925257311994752,77.63708949206546), (12.925264437821962,77.63544104167181), (12.924895111524586,77.63310594577024), (12.924156457290884,77.62873616137699), (12.923452503282572,77.62604701388545), (12.922874032472967,77.62327203570544), (12.921354417731287,77.62075454959097), (12.921006,77.62029699999994), (12.929442252120959,77.61519966931155), (12.933785750957066,77.61262954629524), (12.938171,77.610274), (12.938678533420722,77.61078863095099), (12.939478845185468,77.6119040767212), (12.940117476512382,77.61310500000002), (12.942970699996216,77.6114472539673), (12.943493626328904,77.61168952114872), (12.94279311491004,77.61378476057439), (12.94171617477807,77.6158156269837), (12.943590954611345,77.61579360052497), (12.943775492538522,77.61615809655768), (12.944265097346783,77.6166407519836), (12.944922,77.61682300000007), (12.945387965726104,77.61649608465586), (12.946314,77.61625500000002), (12.945373350790318,77.6180988306885), (12.945908033780174,77.61814482803345), (12.945861691067922,77.61857552247625)])
# kormangala_l8_file_handle = open('kormangala_l8.txt', 'w')
# generate_l8_geohash = Generate_Geohash_Metrix(
# 	precision=8, polygon=kormangala_polygon, file_handle=kormangala_l8_file_handle)

# generate_l8_geohash.generate_and_save()

# generate_l8_geohash.print_metrix()
