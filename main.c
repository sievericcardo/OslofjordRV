#include <stdio.h>
#include <stdlib.h>
#include <cjson/cJSON.h>


int my_func(float temp, int id_sim) {
	//Values must be passed to or returned from a function to be monitored by TeSSLa
	return 0;
}


int main() {
	//Read json file and save contents to a string
	char *str = 0;
	long len;
        FILE *fp = fopen("sim_response.json", "r");
        fseek(fp, 0, SEEK_END);
        len = ftell(fp);
        fseek(fp, 0, SEEK_SET);
        str = malloc(len);
        fread(str, 1, len, fp);
        fclose(fp);

        //Make json string into a cJSON object
        cJSON *root = cJSON_Parse(str);
        free(str);
        
        //Parse through the JSON and isolate the variables
        cJSON *sim_array = cJSON_GetObjectItem(root, "simulations");
        cJSON *iterator = NULL;
        cJSON_ArrayForEach(iterator, sim_array) {
                cJSON *temp_ptr = cJSON_GetObjectItem(iterator, "temperature");
                cJSON *id_sim_ptr = cJSON_GetObjectItem(iterator, "id_sim");
                float temp = temp_ptr->valuedouble;
                if (temp - (int)temp == 0) {
                	temp += 0.000001;
                }
                int id_sim = id_sim_ptr->valueint;
		my_func(temp, id_sim);
        }
        

	cJSON_Delete(root);
        return 0;
}
