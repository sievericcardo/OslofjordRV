# OslofjordRV

Offline monitoring of data from the Oslofjord Database.

## Running the monitor

All necessary files are already generated in this repository. To run the monitor on the current trace in this repository; clone this repository, make sure you have Java installed, and run the following command:

		java -jar tessla.jar interpreter spec.tessla trace.log > output.out

Dependencies: Java

### If you have made changes to the C-code, you need to do the following before running the monitor:

1. Instrument the C-code:

		java -jar tessla.jar instrumenter spec.tessla main.c /usr/lib/gcc/x86_64-linux-gnu/11/include/

Dependencies: GCC, Java

2. Compile the instrumented C-code:

		gcc main.c.instrumented.c -llogging -pthread -ldl -o main

Dependencies: TeSSLa logging library

3. Execute the compiled program (executable):

		./main

### If new data is added to the database, but no changes have been made to the C-code, you need to do the following before running the monitor:

- Execute the compiled program (executable):

		./main
