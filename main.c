#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>




//-----GET DATA-----
size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream) {
	size_t written = fwrite(ptr, size, nmemb, (FILE *)stream);
	return written;
}

void get_data(char *filename) {
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
void my_func(float temp) {
	//Function using values so TeSSLa monitor has something to monitor
	printf("Temperature: %f\n", temp);
}

void verify_data(char *filename) {
	FILE *file = fopen(filename, "r");
	char str[255];
	while (fscanf(file, "%s", str) == 1) {
		//Getting temperature value
		char *temp_token = strtok(strtok(strstr(str, "temp"), ","), "temperature\":");
		my_func(atof(temp_token));
	}
	fclose(file);
}




//-----POST DATA-----
/*
TODO:

Somehow merge output.out with response.json into a csv file.
This way; the data can be posted back to the database.
*/
	




int main(void) {
	char *filename = "response.json";
	//get_data(filename);
	verify_data(filename);
	//post_data("output.out");
	return 0;
}
