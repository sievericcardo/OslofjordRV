# OslofjordRV

## Setup

The monitoring process is dockerized through the Dockerfile and compose.yaml in OslofjordDB. But ngrok and request_listener.py (a Flask application) is not dockerized. After you have set up the project through the compose.yaml file, you have to set up ngrok and request_listener.py manually.

1. Go to the [ngrok](https://ngrok.com) website and create a free account.

2. Navigate to your ngrok dashboard, and create a free static domain.

3. Navigate to `OslofjordDB-API/db/scripts/create-event-listener.py` and insert your ngrok static domain for the webhook (keep the `/new-request` at the end).

4. Insert your ngrok authtoken and static domain into the `ngrok.yml` file in this repo.

5. Install dependencies:

        apt-get install snapd python3 python3-pip
        snap install ngrok
        python3 -m pip install flask

6. Start background processes (do in OslofjordRV directory):

        nohup ngrok start requests --config ngrok.yml &
        nohup python3 request_listener.py &

## Usage

After the setup, the OslofjordRV component is triggered by the front end and will run in the back end.

To check on the background processes, run `ps -ef | grep ngrok` or `ps -ef | grep request_listener.py`. To kill the background process, use the ID you got from the previous command and run `kill <ID>`.
