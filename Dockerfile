FROM ubuntu:latest
WORKDIR /monitor
COPY . /monitor
RUN apt-get update && \
apt-get install -y libcjson-dev unzip default-jre python3 pipx python3-venv wget
RUN pipx install gql[all]
RUN wget https://www.tessla.io/logging.zip && unzip logging.zip && rm logging.zip && mv liblogging.a /usr/lib && mv logging.h /usr/include
