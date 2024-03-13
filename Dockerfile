# docker build . -t oslofjord-monitoring:latest

# docker run --rm -it --entrypoint /bin/bash oslofjord-monitoring:latest

FROM ubuntu:24.04
WORKDIR /app
RUN apt-get update && \
apt-get install -y libcjson-dev build-essential unzip default-jre python3 pipx python3-venv wget
RUN pipx install gql[all] && \
wget https://www.tessla.io/logging.zip && unzip logging.zip && rm logging.zip && mv liblogging.a /usr/lib && mv logging.h /usr/include
COPY . /app