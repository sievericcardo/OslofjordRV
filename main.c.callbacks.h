#include "logging.h"

inline __attribute__((always_inline)) void my_func_call(float arg0, int arg1) {
uint8_t* events = trace_create_events(2);
trace_push_float(events, "temperature", (double) arg0);
trace_push_int(events, "record_number", (int64_t) arg1);
trace_write(events);
}

