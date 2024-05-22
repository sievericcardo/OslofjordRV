import sys
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os

hasura_host = os.getenv("HASURA_HOST", "localhost")
hasura_url = f"http://{hasura_host}:8080/v1/graphql"

#Set up GQL with url and headers.
transport = AIOHTTPTransport(
    url=hasura_url,
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
suitable_temp = "false"
suitable_spawn_temp = "false"
preferred_spawn_temp = "false"
id_sim = None


#Go through monitor output, build mutation, and post to database.
count = 0
for line in lines:
    arr = line.split(" ")
    key = arr[1]
    value = arr[3].replace("\n", "")

    if key == "id_sim":
        if count != 0:
            mutation += '}) {affected_rows}}'
            rv_response = client.execute(gql(mutation))
            mutation = start_mutation
        mutation += f'id_sim: {value}, '

    elif key == "suitable_temperature":
        mutation += f'suitable_temperature: {value}, '

    elif key == "suitable_spawning_temperature":
        mutation += f'suitable_spawning_temperature: {value}, '

    elif key == "preferred_spawning_temperature":
        mutation += f'preferred_spawning_temperature: {value}, '

    count += 1


mutation += '}) {affected_rows}}'
rv_response = client.execute(gql(mutation))


#Update 'done' variable in request table when done.
mutation = f'mutation MyMutation {{update_requests_by_pk(pk_columns: {{request_id: {sys.argv[1]} }}, _set: {{done: true}}) {{done}} }}'
req_response = client.execute(gql(mutation))
