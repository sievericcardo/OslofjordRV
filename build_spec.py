import json
import requests


#What fish/species we want information about
fish = "Atlantic Cod"


#Request API REST Endpoint for info about fish
url = "http://localhost:8080/api/rest/fish-info"
headers = {
	"Content-Type":"application/json",
	"x-hasura-admin-secret":"mylongsecretkey"
}
r = requests.get(url, headers=headers, params={"name":fish})


#Load json response string into a python dict
my_dict = json.loads(r.text)


#Isolate the values we are interested in
items = my_dict["fishFields"][0]


#Write the TeSSLa specification
f = open("spec.tessla", "w")
f.write("@InstFunctionCallArg(\"my_func\", 0)\n")
f.write("in temperature: Events[Float]\n\n")

counter = 0


#Check if suitable temperature
maxTemp = items["maxTemp"]
minTemp = items["minTemp"]
if maxTemp != None and minTemp != None:
	counter += 1
	f.write(f"def suitable_temperature = temperature <=. {float(maxTemp)} && temperature >=. {float(minTemp)}\n")
	f.write(f"out suitable_temperature\n\n")


#Check if suitable spawning temperature
maxSpawnTemp = items["maxSpawnTemp"]
minSpawnTemp = items["minSpawnTemp"]
if maxSpawnTemp != None and minSpawnTemp != None:
	counter += 1
	f.write(f"def suitable_spawning_temperature = temperature <=. {float(maxSpawnTemp)} && temperature >=. {float(minSpawnTemp)}\n")
	f.write(f"out suitable_spawning_temperature\n\n")


#Check if preferred spawning temperature
prefMaxSpawnTemp = items["prefMaxSpawnTemp"]
prefMinSpawnTemp = items["prefMinSpawnTemp"]
if prefMaxSpawnTemp != None and prefMinSpawnTemp != None:
	counter += 1
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
	f.write("ERROR - Not enough data to monitor\n")
	f.close()
