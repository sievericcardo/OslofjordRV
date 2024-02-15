#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <cjson/cJSON.h>




//-----GET DATA-----
size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream) {
	size_t written = fwrite(ptr, size, nmemb, (FILE *)stream);
	return written;
}

void get_data() {
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
		file = fopen("response.json", "wb");
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, file);
		curl_easy_perform(curl);
		fclose(file);
		
		curl_easy_cleanup(curl);
		curl_global_cleanup();
	}
}




//-----PARSE DATA-----
int my_func(float temp, int rec_num) {
	//TeSSLa needs a function to return or recieve values in order to monitor them
	return 0;
}

void my_func_call(float arg0, int arg1);
void parse_data() {
	//Read the file contents into a string 
	FILE *file = fopen("response.json", "r"); 
	char str[1024]; 
	int len = fread(str, 1, sizeof(str), file); 
	fclose(file); 

	//Parse and access the JSON data 
	cJSON *root = cJSON_Parse(str);
	cJSON *turb_array = cJSON_GetObjectItem(root, "turbidity");
	cJSON *iterator = NULL;
	cJSON_ArrayForEach(iterator, turb_array) {
		cJSON *temp = cJSON_GetObjectItem(iterator, "temperature");
		cJSON *rec_num = cJSON_GetObjectItem(iterator, "record_number");
		({float __int_arg_call0; int __int_arg_call1; my_func_call(__int_arg_call0 = temp->valuedouble, __int_arg_call1 = rec_num->valueint); my_func(__int_arg_call0, __int_arg_call1);});
	}

	cJSON_Delete(root);
}




//-----POST DATA-----
/*
TODO:
Format "output.out" to a csv file, so that it can more easily be posted to the api.
*/




//-----CONVERT DATA TO CSV
/*
TODO:
Turn "output.out" data into a csv format so that others in can easily add it to the database on their machines. Will no longer be necessary once database is up and running on server.
*/
	



//-----MAIN-----
int main(void) {
	get_data();
	parse_data();
	return 0;
}

#include "main.c.callbacks.h"
