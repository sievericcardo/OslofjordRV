# docker build . -t oslofjord-monitoring:latest

# docker run --rm -it --entrypoint /bin/bash oslofjord-monitoring:latest

FROM ubuntu:24.04
WORKDIR /app
RUN apt-get update && \
apt-get install -y libcjson-dev unzip default-jre python3 pipx python3-venv wget snapd
RUN pipx install gql[all]
RUN pipx install flask
RUN wget https://www.tessla.io/logging.zip && unzip logging.zip && rm logging.zip && mv liblogging.a /usr/lib && mv logging.h /usr/include
COPY . /app
