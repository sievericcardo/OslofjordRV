# docker build . -t oslofjord-monitoring:latest

# docker run --rm -it --entrypoint /bin/bash oslofjord-monitoring:latest

FROM ubuntu:latest
WORKDIR /app
COPY . /app
RUN apt-get update && \
apt-get install -y libcjson-dev unzip default-jre python3 pipx python3-venv wget
RUN pipx install gql[all]
RUN pipx install flask
RUN wget https://www.tessla.io/logging.zip && unzip logging.zip && rm logging.zip && mv liblogging.a /usr/lib && mv logging.h /usr/include

#Create separate dockerfile/compose for ngrok?
#   Install ngrok:
#       apt-get install -y snapd
#       snap install ngrok
#   Add ngrok authtoken:
#       ngrok authtoken <token>
#   Configure ngrok.yml (add port and static domain, see ngrok.yml on nrec):
#       ...
#   Start ngrok and request listener:
#       nohup ngrok start requests &
#       nohup python3 /path/to/dir/request_listener.py &