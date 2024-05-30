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
    
if __name__ == "__main__":
    # Example usage
    g = Generator("fishFields", "FishFields", [("maxSpawningTemperature", "Int"), ("minSpawningTemperature", "Int"), ("maxTemperature", "Int"), ("minTemperature", "Int"), ("preferredMaxSpawningTemperature", "Int"), ("preferredMinSpawningTemperature", "Int")], {("maxTemp", "minTemp"): ["suitable_temperature", "temperature", ">=", "100.0", "<="], ("maxSpawnTemp", "minSpawnTemp"): ["suitable_spawning_temperature", "temperature", ">=", "100.0", "<="], ("prefMaxSpawnTemp", "prefMinSpawnTemp"): ["preferred_spawning_temperature", "temperature", ">=", "100.0", "<="]})
    print(g.generateQuery())
