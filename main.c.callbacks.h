#include "logging.h"

inline __attribute__((always_inline)) void my_function_call(float arg0, char * arg1) {
uint8_t* events = trace_create_events(2);
String
trace_push_float(events, "temperature", (double) arg0);
trace_write(events);
}

