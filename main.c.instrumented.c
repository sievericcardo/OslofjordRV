#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <cjson/cJSON.h>


struct string {
        char *ptr;
        size_t len;
};


void init_string(struct string *s) {
        s->len = 0;
        s->ptr = malloc(s->len+1);
        if (s->ptr == NULL) {
                fprintf(stderr, "malloc() failed\n");
                exit(EXIT_FAILURE);
        }
        s->ptr[0] = '\0';
}


size_t write_func(void *ptr, size_t size, size_t nmemb, struct string *s) {
	//Response from curl is passed to this function, which writes response to a string
        size_t new_len = s->len + size*nmemb;
        s->ptr = realloc(s->ptr, new_len+1);
        if (s->ptr == NULL) {
                fprintf(stderr, "realloc() failed\n");
                exit(EXIT_FAILURE);
        }
        memcpy(s->ptr+s->len, ptr, size*nmemb);
        s->ptr[new_len] = '\0';
        s->len = new_len;
        return size*nmemb;
}


int my_func(float temp, int id_sim) {
	//Values must be passed to or returned from function to be monitored by TeSSLa
	return 0;
}


void my_func_call(float arg0, int arg1);
int main() {
        CURL *curl;
        struct curl_slist *list = NULL;
        FILE *file;
        curl = curl_easy_init();
        if (curl) {
                //Endpoint URL
                curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8080/api/rest/simulations");

                //Add headers
                list = curl_slist_append(list, "Content-Type: application/json");
                list = curl_slist_append(list, "x-hasura-admin-secret: mylongsecretkey");
                curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);

                //Write response to string
                struct string s;
                init_string(&s);
                curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_func);
                curl_easy_setopt(curl, CURLOPT_WRITEDATA, &s);
                curl_easy_perform(curl);

                //Parse and access the JSON response
                cJSON *root = cJSON_Parse(s.ptr);
                free(s.ptr);
                cJSON *sim_array = cJSON_GetObjectItem(root, "simulations");
                cJSON *iterator = NULL;
                cJSON_ArrayForEach(iterator, sim_array) {
                        cJSON *temp_ptr = cJSON_GetObjectItem(iterator, "temperature");
                        cJSON *id_sim_ptr = cJSON_GetObjectItem(iterator, "id_sim");
                        float temp = temp_ptr->valuedouble;
                        int id_sim = id_sim_ptr->valueint;
                        if (temp - (int)temp == 0) {
                        	temp += 0.000001;
                        }
			({float __int_arg_call0; int __int_arg_call1; my_func_call(__int_arg_call0 = temp, __int_arg_call1 = id_sim); my_func(__int_arg_call0, __int_arg_call1);});
                }
                
                //Cleanup
                cJSON_Delete(root);
                curl_easy_cleanup(curl);
        }
        return 0;
}

#include "main.c.callbacks.h"
