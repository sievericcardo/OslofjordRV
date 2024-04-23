import sys
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


#Set up GQL with url and headers.
transport = AIOHTTPTransport(
        url="http://localhost:8080/v1/graphql",
    headers={"Content-Type":"application/json","x-hasura-admin-secret":"mylongsecretkey"}
)
client = Client(transport=transport, fetch_schema_from_transport=True)


#Read monitor output to a string.
f = open("output.out", "r")
lines = f.readlines()
f.close()

start_mutation = f'mutation MyMutation {{insert_runtime_monitoring(objects: {{request_id: {sys.argv[1]}, '
mutation = start_mutation


#The length of the monitor output determines how many lines a "row" spans. The output length depends on the info available about the species.
suitable_temp = 'null'
suitable_spawn_temp = 'null'
preferred_spawn_temp = 'null'
id_sim = None


#Go through monitor output, build mutation, and post to database.
count = 0
i = 1
for line in lines:
    arr = line.split(" ")
    key = arr[1]
    value = arr[3].replace("\n", "")

    if key == "id_sim":
        if count != 0:
            mutation += f'id_sim: {id_sim}, suitable_temperature: {suitable_temp}, suitable_spawning_temperature: {suitable_spawn_temp}, preferred_spawning_temperature: {preferred_spawn_temp}'
            mutation += '}) {affected_rows}}'
            rv_response = client.execute(gql(mutation))
            mutation = start_mutation
        id_sim = value
        count += 1

    elif key == "suitable_temperature":
        suitable_temp = value

    elif key == "suitable_spawning_temperature":
        suitabble_spawn_temp = value

    elif key == "preferred_spawning_temperature":
        preferred_spawn_temp = value


#Post the last entry.
mutation += f'id_sim: {id_sim}, suitable_temperature: {suitable_temp}, suitable_spawning_temperature: {suitable_spawn_temp}, preferred_spawning_temperature: {preferred_spawn_temp}'
mutation += '}) {affected_rows}}'
rv_response = client.execute(gql(mutation))


#Update 'done' variable in request table when done.
mutation = f'mutation MyMutation {{update_requests_by_pk(pk_columns: {{request_id: {sys.argv[1]} }}, _set: {{done: true}}) {{done}} }}'
req_response = client.execute(gql(mutation))
