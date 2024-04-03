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



f = open("output.out", "r")
lines = f.readlines()
f.close()

first_key = lines[0].split(" ")[1]

count = 0

start_mutation = f'mutation MyMutation {{insert_runtime_monitoring(objects: {{grid_id: {sys.argv[1]}, species_name: "{sys.argv[2]}", request_id: {sys.argv[3]}, '

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
		
	elif key == "suitable_temperature":
		mutation += f'suitable_temperature: {value}, '
		
	elif key == "suitable_spawning_temperature":
		mutation += f'suitable_spawning_temperature: {value}, '
		
	elif key == "preferred_spawning_temperature":
		mutation += f'preferred_spawning_temperature: {value}, '
	
	count += 1



mutation = f'mutation MyMutation {{update_requests_by_pk(pk_columns: {{request_id: {sys.argv[3]} }}, _set: {{done: true}}) {{done}} }}'
req_response = client.execute(gql(mutation))
