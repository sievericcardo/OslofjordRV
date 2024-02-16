import csv

header = ["record_number", "temperature", "suitable_living_temp_cod", "suitable_spawning_temp_cod", "preferred_spawning_temp_cod"]
	
f = open("output.out", "r")
lines = f.readlines()

with open("monitor-data.csv", "w") as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(header)
	row = [None, None, None, None, None]
	i = 0
	for line in lines:
		arr = line.split(" ")
		name = arr[1]
		value = arr[3].split("\n")[0]
		
		if name == header[0]:
			row[0] = value
			i += 1
		elif name == header[1]:
			row[1] = value
			i += 1
		elif name == header[2]:
			row[2] = value
			i += 1
		elif name == header[3]:
			row[3] = value
			i += 1
		elif name == header[4]:
			row[4] = value
			i += 1
			
		if i == 5:
			writer.writerow(row)
			row = [None, None, None, None, None]
			i = 0
		
