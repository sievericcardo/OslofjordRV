# OslofjordRV

Offline monitoring of data from the Oslofjord Database.

## Prerequisites

- Clone the repository.
- Install the following libraries:
    - cJSON
    - GCC
    - TeSSLa logging library
    - GQL
- Install Java.
- Install Python.
- Connect to the OslofjordDB (either via docker or nrec).

## Execution

Use command `sh script.sh <grid_id> "<species name>"` to run the entire process. Name is case sensitive. For example: `sh script.sh 234 "Atlantic Cod"`

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

## Instrument and compile C-code

`sh compile.sh`. Only do if changes have been made to the main.c file.
