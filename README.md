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
- Set up an "example" table in Hasura (see SQL at bottom of README).
- Set up a REST Endpoint for the "example" table with a POST method.

## Execution

All necessary processes can be executed with `./script.sh`.

## Create table for runtime monitoring data

	CREATE TABLE IF NOT EXISTS example (
		record_number int NOT NULL UNIQUE,
		suitable_temperature boolean,
		suitable_spawning_temperature boolean,
		preferred_spawning_temperature boolean,
		PRIMARY KEY (record_number)
	);
