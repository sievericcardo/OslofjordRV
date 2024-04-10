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
count = 0
limit = 0
if len(lines) == 24:
    limit = 1
elif len(lines) == 24*2:
    limit = 2
elif len(lines) == 24*3:
    limit = 3
elif len(lines) == 24*4:
    limit = 4


#Go through monitor output, build mutation, and post to database.
for line in lines:
    count += 1

    arr = line.split(" ")
    key = arr[1]
    value = arr[3].replace("\n", "")

    if key == "id_sim":
        mutation += f'id_sim: {value}, '

    elif key == "suitable_temperature":
        mutation += f'suitable_temperature: {value}, '

    elif key == "suitable_spawning_temperature":
        mutation += f'suitable_spawning_temperature: {value}, '

    elif key == "preferred_spawning_temperature":
        mutation += f'preferred_spawning_temperature: {value}, '

    if count == limit:
        mutation += '}) {affected_rows}}'
        rv_response = client.execute(gql(mutation))
        mutation = start_mutation
        count = 0


#Update 'done' variable in request table when done.
mutation = f'mutation MyMutation {{update_requests_by_pk(pk_columns: {{request_id: {sys.argv[1]} }}, _set: {{done: true}}) {{done}} }}'
req_response = client.execute(gql(mutation))
