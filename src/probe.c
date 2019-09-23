#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>
#include "libcache.h"
#include "probe.h"

// RUN LOOP 3
void run_loop() {
	int ret;
	char command1[256];
	sprintf(command1, "./loop 3&");
	ret = system((char*) command1);
}

// Setting Different CPU
void set_different_affinity() {
	char command[256];
	char command1[256];
	char command2[256];
	int pid;
	int ret;
	pid = getpid();

	sprintf(command1, "taskset -c 1 ./loop 3&");
	ret = system((char*) command1);

	sprintf(command, "taskset -p  0x00000001 %d", pid);

	ret = system((char*) command);

	sprintf(command2, "taskset -p `pidof loop`");
	ret = system((char*) command2);

}

// Setting Same CPU
void set_same_affinity() {

	char command[256];
	char command1[256];
	char command2[256];
	char command3[256];
	int pid;
	int ret;
	pid = getpid();

	sprintf(command1, "taskset -c 0 ./loop 3&");
	ret = system((char*) command1);

	sprintf(command, "taskset -p  0x00000001 %d", pid);
	ret = system((char*) command);
	sprintf(command3, "taskset -p %d", pid);
	ret = system((char*) command3);

	sprintf(command2, "taskset -p `pidof loop`");
	ret = system((char*) command2);

}

//KILL LOOP
void killloop() {
	char command[256];
	int ret;
	sprintf(command, "kill -9 `pidof loop`");
	ret = system((char*) command);

}

int main() {

	char* addr;
	unsigned long long result = 0;
	int max_itr = 500, mem_itr = 11;

//OUTPUT FILE Pointers

	FILE *f_with_flush = fopen("result_with_flush.csv", "w");
	FILE *f_without_flush = fopen("result_without_flush.csv", "w");
	FILE *f_pv_diff = fopen("result_with_pv_on_diff.csv", "w");
	FILE *f_pv_same = fopen("result_with_pv_on_same.csv", "w");

//FLUSH&RELOAD loop with FLUSH(measures	memory access)

	for (int j = 0; j < mem_itr; j++) {

		for (int i = 0; i < max_itr; i++) {
			if (j == 10) {
				char* func_ptr = (char *) fetch_string;
				flush(func_ptr);
				result = reload(func_ptr);

				fprintf(f_with_flush, "%d,%d,%lld\n", j + 1, i + 1, result);

				continue;
			}

			addr = (char*) address_of_string(j);
			flush(addr);
			result = reload(addr);

			fprintf(f_with_flush, "%d,%d,%lld\n", j + 1, i + 1, result);

		}

	}

	fclose(f_with_flush);

//FLUSH&RELOAD loop without	FLUSH (measures cache access)
	for (int j = 0; j < mem_itr; j++) {

		for (int i = 0; i < max_itr; i++) {
			if (j == 10) {
				char* func_ptr = (char *) fetch_string;

				result = reload(func_ptr);

				fprintf(f_without_flush, "%d,%d,%lld\n", j + 1, i + 1, result);

				continue;

			}

			addr = (char*) address_of_string(j);

			result = reload(addr);
			fprintf(f_without_flush, "%d,%d,%lld\n", j + 1, i + 1, result);

		}
	}

	fclose(f_without_flush);

	//FLUSH&RELOAD loop with concurrently running “loop 3” Probe and Victim on different CPU - affinity 1 and 2

	set_different_affinity();

	for (int i = 0; i < max_itr; i++) {

		addr = (char*) address_of_string(3);
		result = reload(addr);
		flush(addr);
		usleep(100);
		fprintf(f_pv_diff, "3,%d,%lld\n", i + 1, result);

	}

	killloop();
	fclose(f_pv_diff);

	//FLUSH&RELOAD loop, same as before, but probe and victim running on same CPU cores

	set_same_affinity();

	for (int i = 0; i < max_itr; i++) {

		addr = (char*) address_of_string(3);
		result = reload(addr);

		flush(addr);
		usleep(100);
		fprintf(f_pv_same, "3,%d,%lld\n", i + 1, result);

	}

	killloop();
	fclose(f_pv_same);

}
