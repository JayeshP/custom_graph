# generate custom 4 level adjacent point to point geohash distance metrix 

import json 
from helper import custom_geohash_base16_encode, custom_geohash_base16_decode

osm_metrix = json.load(open("osm_mapping_50_by_50_metrix.txt", "r"))

# for p in osm_metrix:
# 	print p['origin'], p['destination']

a =  custom_geohash_base16_encode(12.9215330053, 77.6208730225)
b = custom_geohash_base16_encode(12.9233296359, 77.6227164202)
print 12.9215330053, 77.6208730225, a

print 12.9233296359, 77.6227164202, b
print a, custom_geohash_base16_decode(a)
print b, custom_geohash_base16_decode(b)
