#!/bin/bash
echo "Fetching data from knowledgegraph and building TeSSLa specification..."
python3 build_spec.py
echo "Fetching simulation data and generating a trace..."
./main
echo "Running the TeSSLa monitor on the trace..."
java -jar tessla.jar interpreter spec.tessla trace.log > output.out
echo "Posting the monitor output to the database..."
./post_data
echo "Done!"
