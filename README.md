# OslofjordRV

Offline monitoring of data from the Oslofjord Database.

## Prerequisites

- Clone the repository.
- Install the following libraries:
    - libcurl
    - cJSON
    - GCC
    - TeSSLa logging library
- Install Java.
- Install Python.
- Get OslofjordDB up and running.
- Run the `post_sim_data.py` file.
- Set up a REST Endpoint for the "simulations" table with a GET method.
    - Only need to get "temperature" and "id_sim".
- Set up a "runtime_monitoring" table (see SQL below).
- Set up a REST Endpoint for the "runtime_monitoring" table with a POST method.
- Set ut a REST Endpoint with a GET method, and manually write in query to get fish info (see below).

## Execution

Use command `./script.sh` to run the entire process.

## Create table for runtime monitoring data

Remember to track table!

	CREATE TABLE IF NOT EXISTS runtime_monitoring (
		id_sim int NOT NULL UNIQUE,
		suitable_temperature boolean,
		suitable_spawning_temperature boolean,
		preferred_spawning_temperature boolean,
		PRIMARY KEY (id_sim)
	);

## Query to get fish information

	query fish_info($name: String!) {
		fishFields(name: $name) {
			maxSpawnTemp
			maxTemp
			minSpawnTemp
			minTemp
			name
			prefMaxSpawnTemp
			prefMinSpawnTemp
		}
	}	

## Instrument and compile C-code

Only do if changes have been made to the C-code

	java -jar tessla.jar instrumenter spec.tessla main.c /usr/lib/gcc/x86_64-linux-gnu/11/include/ && gcc main.c.instrumented.c -llogging -lcurl -lcjson -pthread -ldl -o main
