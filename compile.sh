java -jar tessla.jar instrumenter spec.tessla main.c /usr/lib/gcc/x86_64-linux-gnu/11/include/ && gcc main.c.instrumented.c -llogging -lcurl -lcjson -pthread -ldl -o main
