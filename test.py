import requests

url = "http://localhost:8000"

data = {
    "grid_id": 234,
    "species_name": "Atlantic Cod"
}

r = requests.post(url=url, data=data)