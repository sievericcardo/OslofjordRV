#include "logging.h"

inline __attribute__((always_inline)) void ret_temperature_return(float value, char * arg0) {
uint8_t* events = trace_create_events(1);
trace_push_float(events, "temperature", (double) value);
trace_write(events);
}

