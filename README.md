# OslofjordRV

Offline monitoring of data from the Oslofjord Database.

## Prerequisites to using this project

- Clone the repository.
- Install the following libraries:
    - libcurl
    - cJSON
    - GCC
    - TeSSLa logging library
- Install Java.
- Get OslofjordDB up and running.
- Set up a REST Endpoint for the "turbidity" table with a GET method.
- Set up an "example" table in Hasura (see SQL below).
- Set up a REST Endpoint for the "example" table with a POST method.

## All commands

1. Instrument the C-code (tell it to produce a trace for the TeSSLa specification):

		java -jar tessla.jar instrumenter spec.tessla main.c /usr/lib/gcc/x86_64-linux-gnu/11/include/

2. Compile the instrumented C-code:

		gcc main.c.instrumented.c -llogging -lcurl -lcjson -pthread -ldl -o main

3. Run the compiled code:

		./main

4. Run the TeSSLa interpreter:

		java -jar tessla.jar interpreter spec.tessla trace.log > output.out
        
5. Post the monitor output data to the database:

		gcc post_data.c -lcurl -o post_data && ./post_data'

## Create table for runtime monitoring data

	CREATE TABLE IF NOT EXISTS example (
		record_number int NOT NULL UNIQUE,
		suitable_temperature boolean,
		suitable_spawning_temperature boolean,
		preferred_spawning_temperature boolean
	);
