#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>


size_t write_func(void *buffer, size_t size, size_t nmemb, void *userp) {
	return size * nmemb;
}


int main() {
	//Specify headers
	struct curl_slist *list = NULL;
	list = curl_slist_append(list, "Content-Type: application/json");
	list = curl_slist_append(list, "x-hasura-admin-secret: mylongsecretkey");
	
	CURL *curl;

	//Delete all items already in table
	curl = curl_easy_init();
	if (curl) {
		//Add headers
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
		
		//Specify custom request and url
		curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");
		curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8080/api/rest/runtime_monitoring/delete");
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_func);
		curl_easy_perform(curl);
		
		//Cleanup
		curl_easy_cleanup(curl);
	}

	//Post new monitor output to table
	curl = curl_easy_init();
	if (curl) {
		//Add headers
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
		
		//Specify url
		curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8080/api/rest/runtime_monitoring");
		
		//Use monitor output to build postfields to give to database
		FILE *fp = fopen("output.out", "r");
		char first_name[100];
		char post[1024] = "{\"object\":{";
		int len = 255;
		char str[len];
		int i = 0;
		while (fgets(str, len, fp)) {
			//Remove newline char
			str[strcspn(str, "\n")] = 0;
	
			//Isolate variable name and value
			char *name = strtok(str, ": ");
			name = strtok(NULL, " =");
			char *value = strtok(NULL, "= ");
			
			if (i == 0) {
				i++;
				strcpy(first_name, name);
				
				//Add to postfields
				strcat(post, "\"");
				strcat(post, name);
				strcat(post, "\":");
				strcat(post, value);
			} else {
				//If we're done with one row; post and start over
				if (strcmp(name, first_name) == 0) {
					strcat(post, "}}");
					
					//Perform post
					curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post);
					curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_func);
					curl_easy_perform(curl);
					
					strcpy(post, "{\"object\":{");
				} else {
					strcat(post, ",");
				}
				
				//Add to postfields
				strcat(post, "\"");
				strcat(post, name);
				strcat(post, "\":");
				strcat(post, value);
			}
		}
		//Need to do one last post to include last item
		strcat(post, "}}");
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_func);
		curl_easy_perform(curl);
	
		// Cleanup
		fclose(fp);
		curl_easy_cleanup(curl);
	}
	return 0;
}
