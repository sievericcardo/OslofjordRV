#include "logging.h"

inline __attribute__((always_inline)) void do_something_call(char * arg0) {
uint8_t* events = trace_create_events(1);
trace_push_unit(events, "call");
trace_write(events);
}

inline __attribute__((always_inline)) void do_something_return(float value, char * arg0) {
uint8_t* events = trace_create_events(1);
trace_push_float(events, "temperature", (double) value);
trace_write(events);
}

