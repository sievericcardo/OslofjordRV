import json
import requests


#What fish/species we want information about (TODO: Make dynamic somehow)
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

maxTemp = float(items["maxTemp"])
minTemp = float(items["minTemp"])
maxSpawnTemp = float(items["maxSpawnTemp"])
minSpawnTemp = float(items["minSpawnTemp"])
prefMaxSpawnTemp = float(items["prefMaxSpawnTemp"])
prefMinSpawnTemp = float(items["prefMinSpawnTemp"])


#Write the TeSSLa specification
f = open("spec.tessla", "w")
f.write("@InstFunctionCallArg(\"my_func\", 0)\n")
f.write("in temperature: Events[Float]\n\n")

f.write(f"def suitable_living_temp = temperature <=. {maxTemp} && temperature >=. {minTemp}\n")
f.write(f"out suitable_living_temp\n\n")

f.write(f"def suitable_spawning_temp_cod = temperature <=. {maxSpawnTemp} && temperature >=. {minSpawnTemp}\n")
f.write(f"out suitable_spawning_temp_cod\n\n")

f.write(f"def preferred_spawning_temp_cod = temperature <=. {prefMaxSpawnTemp} && temperature >=. {prefMinSpawnTemp}\n")
f.write(f"out preferred_spawning_temp_cod\n\n")

f.write(f"@InstFunctionCallArg(\"my_func\", 1)\n")
f.write(f"in record_number: Events[Int]\n")
f.write(f"out record_number\n")
f.close()
