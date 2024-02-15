#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>




//-----GET DATA-----

static size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream) {
	size_t written = fwrite(ptr, size, nmemb, (FILE *)stream);
	return written;
}

static void get_data(char *filename) {
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




//-----VERIFY DATA-----
static void my_function(float temp, char *time) {
	//Converts temperature value to float.
	//Function necessary so that the TeSSLa specification has a return value to monitor.
	printf("Temperature: %f\n", temp);
	printf("Record time: %s\n\n", time);
}

static void verify_data(char *filename) {
	FILE *file = fopen(filename, "r");
	char str[255];
	
	while (fscanf(file, "%s", str) == 1) {
		char *time_token = strtok(strstr(str, "202"), "\"");
		char *temp_token = strtok(strtok(strstr(str, "temp"), ","), "temperature\":");
		my_function(atof(temp_token), time_token);
	}
	fclose(file);
}



/*
//TODO:-----POST DATA-----
static void post_data(char *filename) {
	CURL *curl;
	struct curl_slist *list = NULL;
	FILE *file;
	curl = curl_easy_init();
	if (curl) {
		//Endpoint URL
		curl_easy_setopt(curl, CURLOPT_URL, //Add post url here! Need to make one in hasura first);
		
		//Add headers
		list = curl_slist_append(list, "Content-Type: application/json");
		list = curl_slist_append(list, "x-hasura-admin-secret: mylongsecretkey");
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
		
		//Specify the POST data
		//TODO: open file
		while (//there is still data to parse) {
			curl_easy_setopt(curl, CURLOPT_POSTFIELDS, //data to post);
		}
		
		//Perform post
		curl_easy_perform(curl);
		
		curl_easy_cleanup(curl);
		curl_global_cleanup();
	}
}
*/



int main(void) {
	char *filename = "response.json";
	//get_data(filename);
	verify_data(filename);
	//post_data("output.out");
	return 0;
}
