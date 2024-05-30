from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import os
from data_processor import DataProcessor
from generator import Generator

app = Flask(__name__)
socketio = SocketIO(app)

# Base data
data_parameters = {
    "name": "fishFields",
    "field": "FishFields",
    "base_property": "temperature",
    "parameters": [
        ("maxSpawnTemp", "Int"),
        ("minSpawnTemp", "Int"),
        ("maxTemp", "Int"),
        ("minTemp", "Int"),
        ("prefMaxSpawnTemp", "Int"),
        ("prefMinSpawnTemp", "Int")
    ],
    "species_info": {
        ("maxTemp", "minTemp"): ["suitable_temperature", "temperature", ">=", "100.0", "<="],
        ("maxSpawnTemp", "minSpawnTemp"): ["suitable_spawning_temperature", "temperature", ">=", "100.0", "<="],
        ("prefMaxSpawnTemp", "prefMinSpawnTemp"): ["preferred_spawning_temperature", "temperature", ">=", "100.0", "<="]
    },
    "offset": "10.0"
}

@app.route('/new-request', methods=['POST'])
def new_request():
    # Confirm the authentication header is correct
    auth_header = request.headers.get('secret-authorization-string')
    if auth_header != 'super_secret_string_123':
        return jsonify({'message': 'Unauthorized'}), 401

    # Isolate grid_id and species_name
    data = request.get_json()
    print(data)
    grid_id = data['event']['data']['new']['grid_id']
    species_name = data['event']['data']['new']['species_name']
    request_id = data['event']['data']['new']['request_id']

    name = data_parameters['name']
    field = data_parameters['field']
    base_property = data_parameters['base_property']
    parameters = data_parameters['parameters']
    species_info = data_parameters['species_info']
    offset = data_parameters['offset']

    gen = Generator(name, field, parameters, species_info)
    graph_query = gen.generateQuery()

    # Save the query into the Oslofjord-DB-API container
    with open(f'/app/{name}.graphql', 'w') as f:
        # f.write(graph_query)
        print("Query generated...")

    dp = DataProcessor(name, field, base_property, parameters, species_info, offset)

    print('Getting data...')
    dp.get_data(grid_id, species_name)
    print('Running TeSSLa interpreter...')
    os.system('java -jar tessla.jar interpreter spec.tessla trace.log > output.out')
    print('Posting data...')
    dp.post_data(request_id)

    # os.system(f'sh script.sh {grid_id} "{species_name}" {request_id}')

    return jsonify({'message': 'Request received!'})

if __name__ == '__main__':
    port = int(os.environ.get('MONITORING_PORT', 5001))
    socketio.run(app, host='0.0.0.0', port=port)
