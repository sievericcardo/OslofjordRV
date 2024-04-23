#!/bin/bash
echo "Running 'get_data.py'..."
python3 get_data.py $1 "$2"
echo "Running TeSSLa interpreter..."
java -jar tessla.jar interpreter spec.tessla trace.log > output.out
echo "Running 'post_data.py'..."
python3 post_data.py $3
echo "Done!"
