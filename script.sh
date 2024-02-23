#!/bin/bash
python3 build_spec.py
java -jar tessla.jar instrumenter spec.tessla main.c /usr/lib/gcc/x86_64-linux-gnu/11/include/
gcc main.c.instrumented.c -llogging -lcurl -lcjson -pthread -ldl -o main
./main
java -jar tessla.jar interpreter spec.tessla trace.log > output.out
gcc post_data.c -lcurl -o post_data && ./post_data
