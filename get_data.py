import sys
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


#Set up GQL with url and headers
transport = AIOHTTPTransport(
        url="http://localhost:8080/v1/graphql",
    headers={"Content-Type":"application/json","x-hasura-admin-secret":"mylongsecretkey"}
)
client = Client(transport=transport, fetch_schema_from_transport=True)


#Query the simulation table for the data we want to monitor
sim_query = gql(f'''
	query myQuery {{
		simulations(where: {{grid_id: {{_eq: {sys.argv[1]} }} }}) {{
			id_sim
			temperature
		}}
	}}
''')
sim_response = client.execute(sim_query)


#Write response to file
f = open("sim_response.json", "w")
json.dump(sim_response, f);
f.close()


#Query the knowledgegraph for values about the species we want to check
species_query = gql(f'''
    query myQuery {{
        fishFields(name: "{sys.argv[2]}") {{
            prefMinSpawnTemp
            prefMaxSpawnTemp
            name
            minTemp
            minSpawnTemp
            maxTemp
            maxSpawnTemp
        }}
    }}
''')
species_response = client.execute(species_query)


#Isolate the values we are interested in, and format them according to TeSSLa syntax
items = species_response["fishFields"][0]
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


#If the species doesn't have any of the values we want to check in the knowledge graph
if counter == 0:
	f.close()
	f = open("spec.tessla", "w")


#Close out file
f.write(f"@InstFunctionCallArg(\"my_func\", 1)\n")
f.write(f"in id_sim: Events[Int]\n")
f.write(f"out id_sim\n")
f.close()
