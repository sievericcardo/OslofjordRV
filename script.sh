#!/bin/bash
echo "Creating TeSSLa specification..."
python3 build_spec.py
echo "Instrumenting and compiling C-code..."
java -jar tessla.jar instrumenter spec.tessla main.c /usr/lib/gcc/x86_64-linux-gnu/11/include/
gcc main.c.instrumented.c -llogging -lcurl -lcjson -pthread -ldl -o main
echo "Fetching data and generating a trace..."
./main
echo "Running the TeSSLa monitor on the trace..."
java -jar tessla.jar interpreter spec.tessla trace.log > output.out
echo "Posting the monitor output to the database..."
gcc post_data.c -lcurl -o post_data && ./post_data
echo "Done!"
