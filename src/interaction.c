#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include "libcache.h"
#include <termios.h>

static struct termios old, new;

/* Initialize new terminal i/o settings */
void initTermios(int echo) 
{
  tcgetattr(0, &old); /* grab old terminal i/o settings */
  new = old; /* make new settings same as old settings */
  new.c_lflag &= ~ICANON; /* disable buffered i/o */
  if (echo) {
      new.c_lflag |= ECHO; /* set echo mode */
  } else {
      new.c_lflag &= ~ECHO; /* set no echo mode */
  }
  tcsetattr(0, TCSANOW, &new); /* use these new terminal i/o settings now */
}



int main(int argc, char* argv[]) {
	initTermios(0);
	while(1) {
		printf("\nEnter a number from 0 to 9: ");
		char c;
		scanf("%c",&c);
		if(c<'0'||c>'9') {
			printf("... invalid char %c\n",c);
			continue;
		}

		char buf[4096];
		fetch_string(buf, c-'0', 200);
		printf("\nYour choice: %s",buf);
	}

}
