import json
import requests

fp = open("sim_data.json");
data = json.load(fp);
fp.close();

url = "http://localhost:8080/api/rest/simulations"
headers = {
	"Content-Type":"application/json",
        "x-hasura-admin-secret":"mylongsecretkey"
}

for item in data:
	obj = {"object":item}
	response = requests.post(url, headers=headers, json=obj)
