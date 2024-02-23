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
- Get OslofjordDB up and running.
- Set up a REST Endpoint for the "turbidity" table with a GET method.
	- Only need to get "temperature" and "record_number".
- Set up an "example" table in Hasura (see SQL below).
- Set up a REST Endpoint for the "example" table with a POST method.
- Set ut a REST Endpoint with a GET method, and manually write in query (see below).

## Execution

All necessary processes can be executed with `./script.sh`

## Create table for runtime monitoring data

	CREATE TABLE IF NOT EXISTS example (
		record_number int NOT NULL UNIQUE,
		suitable_temperature boolean,
		suitable_spawning_temperature boolean,
		preferred_spawning_temperature boolean,
		PRIMARY KEY (record_number)
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
