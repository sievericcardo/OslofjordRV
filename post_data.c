#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>


size_t write_func(void *buffer, size_t size, size_t nmemb, void *userp) {
	return size * nmemb;
}


int main() {
	struct curl_slist *list = NULL;
	CURL *curl;
	curl = curl_easy_init();
	if (curl) {
		//Endpoint URL
		curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8080/api/rest/example");

		//Add headers
		list = curl_slist_append(list, "Content-Type: application/json");
		list = curl_slist_append(list, "x-hasura-admin-secret: mylongsecretkey");
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);

		FILE *fp = fopen("output.out", "r");
		int len = 255;
		char str[len];
		char post[1024] = "{\"object\":{";
		int i = 0;
		while (fgets(str, len, fp)) {
			i++;
			str[strcspn(str, "\n")] = 0; //Removes newline char
			
			char *token = strtok(str, " ");
			int j = 0;
			while (token != NULL) {
				j++;
				if (j == 2) {
					strcat(post, "\"");
					strcat(post, token);
					strcat(post, "\":");
				} else if (j == 4) {
					strcat(post, token);
				}
				token = strtok(NULL, " ");
			}
			if (i == 5) {
				strcat(post, "}}");
				
				curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post);
				curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_func);
				curl_easy_perform(curl);
				
				strcpy(post, "{\"object\":{");
				i = 0;	
			} else {
				strcat(post, ",");
			}
		}
	
		// Cleanup
		fclose(fp);
		curl_easy_cleanup(curl);
	}
	return 0;
}
