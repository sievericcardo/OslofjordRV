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
- Set up two REST Endpoint for the "runtime_monitoring" table; a POST method and a DELETE method.
- Set ut a REST Endpoint with a GET method, and manually write in query to get fish info (see below).

## Execution

Use command `sh script.sh "<species name>"` to run the entire process. Name is case sensitive. For example: `sh script.sh "Atlantic Cod"`

## Create table for runtime monitoring data

Remember to track table!

	CREATE TABLE IF NOT EXISTS runtime_monitoring (
		id_sim int NOT NULL UNIQUE,
		suitable_temperature boolean,
		suitable_spawning_temperature boolean,
		preferred_spawning_temperature boolean,
		species_name TEXT,
		grid_id int,
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

`sh compile.sh`. Only do if changes have been made to the main.c file.
