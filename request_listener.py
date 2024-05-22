from flask import Flask, request, jsonify
import os
from data_processor import DataProcessor
from generator import Generator

app = Flask(__name__)

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

    name = data['event']['data']['new']['name']
    field = data['event']['data']['new']['field']
    base_property = data['event']['data']['new']['base_property']
    parameters = data['event']['data']['new']['parameters']
    species_info = data['event']['data']['new']['species_info']
    offset = data['event']['data']['new']['offset']

    gen = Generator(name, field, base_property, parameters, species_info)
    graph_query = gen.generateQuery()

    # Save the query into the Oslofjord-DB-API container
    with open(f'/app/{name}.graphql', 'w') as f:
        f.write(graph_query)

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
    app.run(port=5001)
