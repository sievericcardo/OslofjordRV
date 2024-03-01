import json
import requests


#What fish/species we want information about
fish = "Porbeagle"


#Request API REST Endpoint for info about fish
url = "http://localhost:8080/api/rest/fish-info"
headers = {
	"Content-Type":"application/json",
	"x-hasura-admin-secret":"mylongsecretkey"
}
r = requests.get(url, headers=headers, params={"name":fish})


#Load json response string into a python dict
my_dict = json.loads(r.text)


#Isolate the values we are interested in, and format them
items = my_dict["fishFields"][0]
for x in items:
	if isinstance(items[x], int):
		items[x] = float(items[x])
		if items[x] < 0:
			s = str(items[x]).split("-")[1]
			items[x] = f"-.{float(s)}"


#Write the TeSSLa specification
f = open("spec.tessla", "w")
f.write("@InstFunctionCallArg(\"my_func\", 0)\n")
f.write("in temperature: Events[Float]\n\n")


counter = 0


#Check if suitable temperature
if items["maxTemp"] != None and items["minTemp"] != None:
	counter += 1
	maxTemp = items["maxTemp"]
	minTemp = items["minTemp"]
	f.write(f"def suitable_temperature = temperature <=. {maxTemp} && temperature >=. {minTemp}\n")
	f.write(f"out suitable_temperature\n\n")


#Check if suitable spawning temperature
if items["maxSpawnTemp"] != None and items["minSpawnTemp"] != None:
	counter += 1
	maxSpawnTemp = items["maxSpawnTemp"]
	minSpawnTemp = items["minSpawnTemp"]
	f.write(f"def suitable_spawning_temperature = temperature <=. {maxSpawnTemp} && temperature >=. {minSpawnTemp}\n")
	f.write(f"out suitable_spawning_temperature\n\n")


#Check if preferred spawning temperature
if items["prefMaxSpawnTemp"] != None and items["prefMinSpawnTemp"] != None:
	counter += 1
	prefMaxSpawnTemp = items["prefMaxSpawnTemp"]
	prefMinSpawnTemp = items["prefMinSpawnTemp"]
	f.write(f"def preferred_spawning_temperature = temperature <=. {float(prefMaxSpawnTemp)} && temperature >=. {float(prefMinSpawnTemp)}\n")
	f.write(f"out preferred_spawning_temperature\n\n")


#Close out file
f.write(f"@InstFunctionCallArg(\"my_func\", 1)\n")
f.write(f"in id_sim: Events[Int]\n")
f.write(f"out id_sim\n")
f.close()


#If the species doesn't have any of the values we want to check in the knowledge graph
if counter == 0:
	f = open("spec.tessla", "w")
	f.write("")
	f.close()
