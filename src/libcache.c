#include "libcache.h"
#include <stdio.h>
#include <string.h>

const static char a[1][4096] = {"Hello"};
const static char buf[10][4096] = {
	"Fancy rapid jumps over fence\n",
	"In blockchain we trust\n",
	"Cloud Security is the best lecture I ever had.\n",
	"The question should be, is it worth trying to do, not can it be done.\n",
	"Computers make it easier to do a lot of things, but most of the things they make it easier to do don't need to be done.\n",
	"To err is human, but to really foul things up requires a computer.\n",
	"In mathematics you don't understand things. You just get used to them.\n",
	"Have no fear of perfection - you'll never reach it.\n",
	"The secret to creativity is knowing how to hide your sources.\n",
	"The end.\n"
};
const char *foo() { return a[0]; }

const void* address_of_string(int choice) {
	return (void*)buf[choice];
	
}

void fetch_string(void *target, int choice, int size) {
	void *b = (void *)buf[choice];
	memcpy(target, b, size<1024?size:1024);
}

