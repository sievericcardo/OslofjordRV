import sys
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class DataProcessor:
    def __init__(self, name, type, parameters, species_info):
        """"
        Constructor for the DataProcessor class
        
        Parameters:
        name (str): The name of the query
        field (str): The field of the query
        parameters (list): A list of tuples containing the parameter name 
            and the corresponding type type
        species_info (list): A dictionary containing the species information
            to be checked in the knowledge graph. The first element can be a
            tuple containing the two extremities of a range, or a single value.
            The second element is a list containing the TeSSLa specification
        """
        self.name = name
        self.type = type
        self.parameters = parameters
        self.species_info = species_info
        #Set up GQL with url and headers
        self.transport = AIOHTTPTransport(
            url="http://172.17.0.1:8080/v1/graphql",
            headers={"Content-Type":"application/json","x-hasura-admin-secret":"mylongsecretkey"}
        )
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    def get_data(self):
        #Query the simulation table for the data we want to monitor
        sim_query = gql(f'''
            query myQuery {{
                simulations(where: {{grid_id: {{_eq: {sys.argv[1]} }} }}) {{
                    id_sim
                    temperature
                }}
            }}
        ''')
        sim_response = self.client.execute(sim_query)

        #Parse response to a trace and write to file
        f = open("trace.log", "w")
        i = 1
        for x in sim_response["simulations"]:
            f.write(f'{i}: id_sim = {x["id_sim"]}\n')

            temp = x["temperature"]
            if temp == "NaN":
                f.write(f'{i}: temperature = 100.0\n')
            else:
                f.write(f'{i}: temperature = {temp}\n')
            i += 1
        f.close()

        query = "query myQuery {{\n" + \
                " " * 8 +self.name + "(name: \"{sys.argv[2]}\") {{\n"
        for parameter, _ in self.parameters:
            query += " " * 12 + parameter + "\n"
        query += " " * 8 + "}}\n"
        query += " " * 4 + "}}"

        #Query the knowledgegraph for values about the species we want to check
        species_query = gql(query)

        species_response = self.client.execute(species_query)

        #Isolate the values we are interested in, and format them according to TeSSLa syntax
        items = species_response[self.name][0]
        for x in items:
            if isinstance(items[x], int):
                items[x] = float(items[x])
                if items[x] < 0:
                    s = str(items[x]).split("-")[1]
                    items[x] = f"-.{float(s)}"

        #Write the TeSSLa specification
        f = open("spec.tessla", "w")
        f.write("in temperature: Events[Float]\n\n")
        counter = 0

        # Iterate over the species info
        for info in self.species_info:
            data = self.species_info[info]

            if isinstance(info, tuple):
                if items[str(info[0])] is not None and items[str(info[1])] is not None:
                    counter += 1
                    val1 = items[str(info[0])]
                    val2 = items[str(info[1])]
                    f.write(f"def {data[0]}=\n")
                    f.write(f"\tif {data[1]} {data[2]}. {data[3]}\n")
                    f.write(f"\tthen false\n")
                    f.write(f"\telse {data[1]} {data[4]}. {val1} && {data[1]} {data[2]}. {val2}\n")
                    f.write("out " + data[0] + "\n\n")
            else:
                if items[str(info)] is not None:
                    counter += 1
                    val = items[str(info)]
                    f.write(f"def {data[0]}=\n")
                    f.write(f"\tif {data[1]} {data[2]}. {data[3]}\n")
                    f.write(f"\tthen false\n")
                    f.write(f"\telse {data[1]} {data[4]}. {val}\n")
                    f.write("out " + data[0] + "\n\n")

        #If the species doesn't have any of the values we want to check in the knowledge graph
        if counter == 0:
            f.close()
            f = open("spec.tessla", "w")

        #Close out file
        f.write("in id_sim: Events[Int]\n")
        f.write("out id_sim\n")
        f.close()

    def post_data(self):
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
                    rv_response = self.client.execute(gql(mutation))
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
        rv_response = self.client.execute(gql(mutation))


        #Update 'done' variable in request table when done.
        mutation = f'mutation MyMutation {{update_requests_by_pk(pk_columns: {{request_id: {sys.argv[1]} }}, _set: {{done: true}}) {{done}} }}'
        req_response = self.client.execute(gql(mutation))
