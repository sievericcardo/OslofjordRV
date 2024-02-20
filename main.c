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


int my_func(float temp, int rec_num) {
	//Values must be passed to or returned from function to be monitored by TeSSLa
	return 0;
}


int main() {
        CURL *curl;
        struct curl_slist *list = NULL;
        FILE *file;
        curl = curl_easy_init();
        if (curl) {
                //Endpoint URL
                curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8080/api/rest/turbidity");

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
                
                //printf("RESPONSE:\n%s\n", s.ptr);

                //Parse and access the JSON response
                cJSON *root = cJSON_Parse(s.ptr);
                free(s.ptr);
                cJSON *turb_array = cJSON_GetObjectItem(root, "turbidity");
                cJSON *iterator = NULL;
                cJSON_ArrayForEach(iterator, turb_array) {
                        cJSON *temp = cJSON_GetObjectItem(iterator, "temperature");
                        cJSON *rec_num = cJSON_GetObjectItem(iterator, "record_number");
                        my_func(temp->valuedouble, rec_num->valueint);
                }
                
                //Cleanup
                cJSON_Delete(root);
                curl_easy_cleanup(curl);
        }
        return 0;
}
