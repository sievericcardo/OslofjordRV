#include "logging.h"

inline __attribute__((always_inline)) void my_func_call(float arg0) {
uint8_t* events = trace_create_events(1);
trace_push_float(events, "temperature", (double) arg0);
trace_write(events);
}

