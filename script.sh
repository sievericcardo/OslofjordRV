#!/bin/bash
echo "Fetching..."
python3 get_data.py $1 "$2"
echo "Parsing..."
./main
echo "Monitoring..."
java -jar tessla.jar interpreter spec.tessla trace.log > output.out
echo "Posting..."
python3 post_data.py $1 "$2"
echo "Done!"
