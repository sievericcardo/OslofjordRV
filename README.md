# OslofjordRV

Done in ubuntu environment

## Running monitor on your own computer

The API is already called and the trace is already generated, so all you have to do to run the monitor is to clone the repository to your own machine and run the following command:

	java -jar tessla.jar interpreter spec.tessla trace.log

## Complete runthrough of program

1. Download dependencies (will add soon).

2. Instrument the C code:

		java -jar tessla.jar instrumenter spec.tessla main.c /usr/lib/gcc/x86_64-linux-gnu/11/include/

3. Compile the instrumented C code:

		gcc main.c.instrumented.c -lcurl -llogging -pthread -ldl -o main

4. Start the Docker container for the database and API as described in the OslofjordDB repository.

5. Execute the compiled program to generate a trace that we can monitor:

		./main

6. Monitor the trace:

		java -jar tessla.jar interpreter spec.tessla trace.log
