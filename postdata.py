import requests
import json

url = "http://localhost:8080/api/rest/runtime_monitoring"
headers = {
	"Content-Type": "application/json",
	"x-hasura-admin-secret": "mylongsecretkey"
}

f = open("output.out", "r")
lines = f.readlines()

i = 0
objects = {}
for line in lines:
	arr = line.split(" ")
	name = arr[1]
	value = arr[3].split("\n")[0]
	
	if value == "true":
		value = True
	elif value == "false":
		value = False
	
	if name == "record_number":
		objects[name] = int(value)
		i += 1
	elif name == "temperature":
		objects[name] = float(value)
		i += 1
	else:
		#Asumes that all other variables are boolean
		objects[name] = value
		i += 1
	
	if (i == 5):
		data = {}
		data["object"] = objects
		json_data = json.dumps(data)
		response = requests.post(url, data=json_data, headers=headers)
		print(response.json())
		objects = {}
		i = 0






















