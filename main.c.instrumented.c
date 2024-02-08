#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>


static size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream) {
	size_t written = fwrite(ptr, size, nmemb, (FILE *)stream);
	return written;
}


static void query_and_write_file(char *filename) {
	CURL *curl;
	struct curl_slist *list = NULL;
	FILE *file;
	curl = curl_easy_init();
	if (curl) {
		//Endpoint URL
		curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8080/api/rest/data");
		
		//Add headers
		list = curl_slist_append(list, "Content-Type: application/json");
		list = curl_slist_append(list, "x-hasura-admin-secret: mylongsecretkey");
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
		
		//Pass response to write function
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
		
		//Write response to file
		file = fopen(filename, "wb");
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, file);
		curl_easy_perform(curl);
		fclose(file);
		
		curl_easy_cleanup(curl);
		curl_global_cleanup();
	}
}




void do_something_return(float value, char * arg0);
static float do_something(char* str) {
	printf("Inner token: %s\n", str);
	return  ({float ret = atof(str); do_something_return(ret, str); ret;});
}


static void read_and_clean_data(char *filename) {
	FILE *file = fopen(filename, "r");
	char str[255];
	char *token;
	char delim[10] = ",][}{";
	
	char *outer_saveptr = NULL;
	char *inner_saveptr = NULL;

	while (fscanf(file, "%s", str) == 1) {
		token = strtok_r(str, delim, &outer_saveptr);
		char *inner_token;
		while (token != NULL) {
			if (strstr(token, "turbidity") != NULL) {
				printf("TURBIDITY:\n");
			}
			else if (strstr(token, "temperature") != NULL) {
				char *substr = strstr(token, "temperature");
				printf("%s\n", substr);
				inner_token = strtok_r(substr, ":", &inner_saveptr);
				int i = 1;
				while (inner_token != NULL) {
					if (i == 2) {
						do_something(inner_token);
					}
					i++;
					inner_token = strtok_r(NULL, ":", &inner_saveptr);
				}
			}
			token = strtok_r(NULL, delim, &outer_saveptr);
		}
	}
	fclose(file);
}




int main(void) {
	char *filename = "response.json";
	query_and_write_file(filename);
	read_and_clean_data(filename);
	return 0;
}

#include "main.c.callbacks.h"
