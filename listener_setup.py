from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

class MyRequestHandler(BaseHTTPRequestHandler):

    """
    The post data passed to the endpoint should look like this:
    data = {
        "grid_id": 234,
        "species_name": "Atlantic Cod"
    }
    """

    # Handle POST requests
    def do_POST(self):
        self.send_response(200)  # HTTP status code 200 OK
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = 'POST Request Received'
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_post_data = urllib.parse.parse_qs(post_data)
        self.wfile.write(bytes(response, 'utf-8'))

        grid_id = parsed_post_data["grid_id"][0]
        species_name = parsed_post_data["species_name"][0]
        #print(f"{grid_id} og {species_name}")

        os.system(f'sh script.sh {grid_id} "{species_name}"')

# Create an HTTP server with the custom request handler
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port', port)
    httpd.serve_forever()

# Run the server
run()
