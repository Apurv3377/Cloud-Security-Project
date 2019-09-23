#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include "libcache.h"

int main(int argc, char* argv[]) {
	if(argc<2) { fprintf(stderr, "Usage: %s <choice>\nchoice: 0..9\n", argv[0]); return 1; }
	int choice = atoi(argv[1]);
	char buf[4096];
	printf("Choice is %d\n",choice);
	while (1 == 1) {
		fetch_string(buf, choice, 100);
		usleep(1);
	}

}
