from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

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
        self.wfile.write(bytes(response, 'utf-8'))
        parsed_post_data = urllib.parse.parse_qs(post_data)
        data_dict = {key: value[0] for key, value in parsed_post_data.items()}
        print(data_dict)
	# TODO: USE THE DATA TO START THE RUNTIME VERIFICATION PROCESS (script.sh)

# Create an HTTP server with the custom request handler
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port', port)
    httpd.serve_forever()

# Run the server
run()
