import os

# The url must be taken from the API_HOST of docker if present, localhost if not.
base_url = 'http://' + os.getenv('API_HOST', 'localhost')

class Generator:
    def __init__(self, name, field, parameters, species_info):
        """
        Constructor for the Generator class

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
        self.field = field
        self.parameters = parameters
        self.species_info = species_info

    def generateQuery(self):
        graphQlData = "\"\"\"\n\n" + \
            "--- endpoint ---\n" + \
            base_url + ":3030/ds/query\n\n" + \
            "--- sparql ---\n" + \
            "PREFIX ast: <http://www.smolang.org/oslofjordDT#>\n" + \
            "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n" + \
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" + \
            "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\n" + \
            "SELECT DISTINCT\n" + \
            "  ?name\n"
        
        for parameter, _ in self.parameters:
            graphQlData += "  ?" + parameter + "\n"

        graphQlData += "WHERE {\n" + \
            "  ?species rdfs:subClassOf ?b1 .\n" + \
            "  ?b1 owl:hasValue ?name ;\n" + \
            "      owl:onProperty ast:Name .\n" + \
            "{{#if name}}\n" + \
            "FILTER (?name = \"{{name}}\"^^xsd:string)\n" + \
            "{{/if}} \n\n"
        
        i=2
        for parameter, _ in self.parameters:
            graphQlData += "OPTIONAL {\n" + \
                "  ?species rdfs:subClassOf b" + str(i) + " .\n" + \
                "  b" + str(i) + " owl:hasValue ?" + parameter + " ;\n" + \
                "       owl:onProperty ast:" + parameter + " .\n" \
                "\n\n"
            i+=1
        graphQlData += "}\n\n" + \
            "\"\"\"\n" + \
            "type " + str(self.field) + " {\n" + \
            "  name: String!\n"
        for parameter, type in self.parameters:
            graphQlData += "  " + parameter + ": " + str(type) + "\n"
        graphQlData += "}\n\n"

        return graphQlData
    
    def generateGetData(self):
        code_string = """
import sys
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

#Set up GQL with url and headers
transport = AIOHTTPTransport(
    url="http://172.17.0.1:8080/v1/graphql",
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

#Parse response to a trace and write to file
f = open("trace.log", "w")
i = 1
for x in sim_response["simulations"]:
    f.write(f'{i}: id_sim = {x["id_sim"]}\\n')

    temp = x["temperature"]
    if temp == "NaN":
        f.write(f'{i}: temperature = 100.0\\n')
    else:
        f.write(f'{i}: temperature = {temp\\n')
    i += 1
f.close()

#Query the knowledgegraph for values about the species we want to check
species_query = gql(f'''
    query myQuery {{
"""
        code_string += " " * 8 +self.name + "(name: \"{sys.argv[2]}\") {{\n"
        for parameter, _ in self.parameters:
            code_string += " " * 12 + parameter + "\n"
        code_string += " " * 8 + "}}\n"
        code_string += " " * 4 + "}}\n"

        code_string += """
''')
species_response = client.execute(species_query)


#Isolate the values we are interested in, and format them according to TeSSLa syntax
"""

        code_string += "Iems = species_response[\"" + self.name + "\"][0]\n"
        code_string += """
for x in items:
	if isinstance(items[x], int):
		items[x] = float(items[x])
		if items[x] < 0:
			s = str(items[x]).split("-")[1]
			items[x] = f"-.{float(s)}"

#Write the TeSSLa specification
f = open("spec.tessla", "w")
f.write("in temperature: Events[Float]\\n\\n")
counter = 0
"""

        for info in self.species_info:
            data = self.species_info[info]
            # Check if info is a tuple or a single value
            if isinstance(info, tuple):
                code_string += "if items[\"" + str(info[0]) + "\"] != None and items[\"" + str(info[1]) + "\"] != None:\n"
                code_string != " " * 4 + "counter += 1\n"
                code_string += " " * 4 + str(info[0]) + " = items[\"" + info[0] + "\"]\n"
                code_string += " " * 4 + str(info[1]) + " = items[\"" + info[1] + "\"]\n"
                code_string += " " * 4 + "f.write(f\"def" + str(data[0]) + "=\\n\")\n"
                code_string += " " * 4 + "f.write(f\"\\tif" + str(data[1]) + " " + str(data[2]) + ". " + str(data[3]) + "\\n\")\n"
                code_string += " " * 4 + "f.write(f\"\\tthen false\\n\")\n"
                code_string += " " * 4 + "f.write(f\"\\telse " + str(data[1]) + " " + str(data[4]) + ".  {" + str(info[0]) + "} && " + str(data[1]) + " " + str(data[2]) + ".  {" + str(info[1]) + "}\\n\")\n"
                code_string += " " * 4 + "f.write(\"out " + str(data[0])  + "\\n\\n\")\n\n"
            else:
                code_string += "if items[\"" + str(info) + "\"] != None:\n"
                code_string += " " * 4 + "counter += 1\n"
                code_string += " " * 4 + str(info) + " = items[\"" + info + "\"]\n"
                code_string += " " * 4 + "f.write(f\"def" + str(data[0]) + "=\\n\")\n"
                code_string += " " * 4 + "f.write(f\"\\tif" + str(data[1]) + " " + str(data[2]) + ". " + str(data[3]) + "\\n\")\n"
                code_string += " " * 4 + "f.write(f\"\\tthen false\\n\")\n"
                code_string += " " * 4 + "f.write(f\"\\telse " + str(data[1]) + " " + str(data[4]) + ".  {" + str(info) + "}\\n\")\n"
                code_string += " " * 4 + "f.write(\"out " + str(data[0])  + "\\n\\n\")\n\n"

        code_string += """
#If the species doesn't have any of the values we want to check in the knowledge graph
if counter == 0:
	f.close()
	f = open("spec.tessla", "w")


#Close out file
f.write("in id_sim: Events[Int]\\n")
f.write("out id_sim\\n")
f.close()
"""
        return code_string
    
    def generatePostData(self):
        code_string = """
import sys
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


#Set up GQL with url and headers.
transport = AIOHTTPTransport(
    url="http://172.17.0.1:8080/v1/graphql",
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
    value = arr[3].replace("\\n", "")

    if key == "id_sim":
        if count != 0:
            mutation += '}) {affected_rows}}'
            rv_response = client.execute(gql(mutation))
            mutation = start_mutation
        mutation += f'id_sim: {value}, '
"""
        for _, data in self.species_info:
            code_string += " " * 4 + "elif key == \"" + data[0] + "\":\n"
            code_string += " " * 8 + "mutation += f'" + data[0] + ": {value}, '\n"

        code_string += """
    count += 1


mutation += '}) {affected_rows}}'
rv_response = client.execute(gql(mutation))


#Update 'done' variable in request table when done.
mutation = f'mutation MyMutation {{update_requests_by_pk(pk_columns: {{request_id: {sys.argv[1]} }}, _set: {{done: true}}) {{done}} }}'
req_response = client.execute(gql(mutation))
"""

        return code_string

if __name__ == "__main__":
    # Example usage
    g = Generator("fishFields", "FishFields", [("maxSpawningTemperature", "Int"), ("minSpawningTemperature", "Int"), ("maxTemperature", "Int"), ("minTemperature", "Int"), ("preferredMaxSpawningTemperature", "Int"), ("preferredMinSpawningTemperature", "Int")], {("maxTemp", "minTemp"): ["suitable_temperature", "temperature", ">=", "100.0", "<="], ("maxSpawnTemp", "minSpawnTemp"): ["suitable_spawning_temperature", "temperature", ">=", "100.0", "<="], ("prefMaxSpawnTemp", "prefMinSpawnTemp"): ["preferred_spawning_temperature", "temperature", ">=", "100.0", "<="]})
    print(g.generateQuery())
    print(g.generateGetData())
    print(g.generatePostData())
