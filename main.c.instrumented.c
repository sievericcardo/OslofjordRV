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




void ret_temperature_return(float value, char * arg0);
static float ret_temperature(char *str) {
	//Converts temperature value to float.
	//Function necessary so that the TeSSLa specification has a return value to monitor.
	return  ({float ret = atof(str); ret_temperature_return(ret, str); ret;});
}



static void read_and_clean_data(char *filename) {
	FILE *file = fopen("response.json", "r");
	char str[255];
	
	char *outer_token;
	char outer_delim[10] = ",][}{";
	char *outer_saveptr = NULL;
	char *inner_saveptr = NULL;

	//Reads response.json "word for word", i.e. splits it at every whitespace.
	while (fscanf(file, "%s", str) == 1) {
		char *substr = strstr(str, "\"temp");
		outer_token = strtok_r(substr, outer_delim, &outer_saveptr);
		char *inner_token;
		while (outer_token != NULL) {
			//Checks if substring has a temperature value.
			if (strstr(outer_token, "temperature") != NULL) {
				inner_token = strtok_r(outer_token, "temprau\":", &inner_saveptr);
				ret_temperature(inner_token);
			}
			/*
			//Checks if substring has a record_time value.
			else if (strstr(outer_token, "record_time") != NULL) {
			char inner_delim[10] = "\"";
				inner_token = strtok_r(outer_token, inner_delim, &inner_saveptr);
				int i = 0;
				while (inner_token != NULL) {
					if (i == 2) {
						//inner_token equals record_time value.
					}
					i++;
					inner_token = strtok_r(NULL, inner_delim, &inner_saveptr);
				}
			}
			*/
			outer_token = strtok_r(NULL, outer_delim, &outer_saveptr);
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
