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


#Delete existing data in runtime_monitoring table with the same grid_id and species_name
client.execute(gql(f'mutation MyMutation {{delete_runtime_monitoring(where: {{grid_id: {{_eq: {sys.argv[1]} }}, species_name: {{_eq: "{sys.argv[2]}"}} }}) {{affected_rows}} }}'))


#...
f = open("output.out", "r")
lines = f.readlines()
f.close()

first_key = lines[0].split(" ")[1]

count = 0

start_mutation = f'mutation MyMutation {{insert_runtime_monitoring(objects: {{grid_id: {sys.argv[1]}, species_name: "{sys.argv[2]}", '

mutation = start_mutation

for line in lines:
	arr = line.split(" ")
	key = arr[1]
	value = arr[3].replace("\n", "")
	
	if first_key == key and count != 0:
		mutation += '}) {affected_rows}}'
		rv_response = client.execute(gql(mutation))
		mutation = start_mutation

	if key == "id_sim":
		mutation += f'id_sim: {value}, '
		#Delete existing data in runtime_monitoring table with the same id_sim
		client.execute(gql(f'mutation MyMutation {{delete_runtime_monitoring_by_pk(id_sim: {value}) {{id_sim}} }}'))
		
	elif key == "suitable_temperature":
		mutation += f'suitable_temperature: {value}, '
		
	elif key == "suitable_spawning_temperature":
		mutation += f'suitable_spawning_temperature: {value}, '
		
	elif key == "preferred_spawning_temperature":
		mutation += f'preferred_spawning_temperature: {value}, '
	
	count += 1


















