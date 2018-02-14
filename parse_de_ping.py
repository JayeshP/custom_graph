import Geohash
import json

file_handle = open("sorted_order_batch_time_location.csv", "r")

mapping = {}

def generate_geohash_mapping(pings):
	# for p in pings:

	total_pings = len(pings)
	print "total pings", total_pings
	start_geohash = pings[0][4]
	start_epoch = pings[0][3]
	start_point = pings[0][0] + ' ' + pings[0][1]

	for i, ping in enumerate(pings):
		print "i, start_geohash, loop_geohash", i, start_geohash, ping[4]

		if ping[4] == start_geohash:
			continue

		j = i
		next_point = ping[0] + ' ' + ping[1]
		next_geohash = ping[4]
		next_epoch = ping[3]
		while j < total_pings - 1:
			j += 1
			print "j: ", j
			if next_geohash == pings[j][4]:
				continue
			next_point = pings[j][0] + ' ' + pings[j][1]
			next_epoch = pings[j][3]


		print "mapping start_point, next_point, start_epoch, next_epoch diff ", start_point, next_point, start_geohash + ' ' + next_geohash, start_epoch, next_epoch, (int(next_epoch) - int(start_epoch)) / 1000

		if start_geohash in mapping:
			if next_geohash in mapping[start_geohash]:
				mapping[start_geohash][next_geohash].append((int(next_epoch) - int(start_epoch)) / 1000)
			else:
				mapping[start_geohash][next_geohash] = [(int(next_epoch) - int(start_epoch)) / 1000]
		else:
			mapping[start_geohash] = {next_geohash: [(int(next_epoch) - int(start_epoch)) / 1000]}
		start_point = ping[0] + ' ' + ping[1]
		start_geohash = ping[4]
		start_epoch = ping[3]


def parse_file():
	final_sorted_ping_data = []
	line_number = 0
	for line in file_handle.readlines():
		split1 = line.split(" ")
		split11 = split1[0].split(":")

		order_id = split11[0]
		batch_id = split11[1]
		order_date = split11[2]

		split12 = split1[1].split(":")
		order_time = order_date + ' ' + split12[0] + ':' + split12[1] + ':' + split12[2]

		# print order_id, batch_id, order_time

		# print split12
		pings = split12[3].strip("\n").split("#")

		# pings_sorted = sorted()
		pings_data_list = []
		for ping in pings:
			data = ping.split(',')
			lat = data[0]
			lng = data[1]
			accuracy = data[2]
			epoc = data[3]

			pings_data_list.append((lat, lng, accuracy, epoc, Geohash.encode(float(lat), float(lng), precision=8)))
			# print lat, lng, accuracy, epoc

		print "sorted...."
		pings_sorted_list = sorted(pings_data_list, key=lambda x:x[3])
		final_sorted_ping_data += pings_sorted_list
		# print pings_sorted_list

		generate_geohash_mapping(pings_sorted_list)

		line_number += 1

		# test
		print "line number: ", line_number
		if line_number > 5000:
			break


parse_file()

with open('ping_data_mapping_l8.txt', 'w') as outfile:
    json.dump(mapping, outfile, indent=4)
