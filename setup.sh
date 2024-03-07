sudo apt install libcjson-dev build-essential unzip default-jre python3 python3-pip
python3 -m pip install gql[all]
wget https://www.tessla.io/logging.zip && unzip logging.zip && rm logging.zip && sudo mv liblogging.a /usr/lib && sudo mv logging.h /usr/include
