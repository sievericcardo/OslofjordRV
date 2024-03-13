#!/bin/bash
echo "Running TeSSLa..."
python3 get_data.py $1 "$2"
./main
java -jar tessla.jar interpreter spec.tessla trace.log > output.out
python3 post_data.py $1 "$2"
echo "Done!"
