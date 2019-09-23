
OBJS=

PROG=loop interaction probe
CFLAGS=-g -std=gnu99 -O2
LDFLAGS= -L. -Wl,-rpath,. -lm

all: libcache.so ${PROG}

interaction: interaction.c libcache.so
	 $(CC) $(CFLAGS) $(OBJECTS) -o $@ $(LDFLAGS) interaction.c -lcache

loop: loop.c libcache.so
	 $(CC) $(CFLAGS) $(OBJECTS) -o $@ $(LDFLAGS) loop.c -lcache

libcache.so: libcache.c
	 $(CC) $(CFLAGS) $(OBJECTS) -o $@ $(LDFLAGS) -fpic -shared libcache.c 

probe: probe.c libcache.so
	 $(CC) $(CFLAGS) $(OBJECTS) -o $@ $(LDFLAGS) probe.c -lcache

autoprobe: autoprobe.c libcache.so
	 $(CC) $(CFLAGS) $(OBJECTS) -o $@ $(LDFLAGS) autoprobe.c -lcache


clean: 
	rm -f libcache.so ${PROG} ${OBJS}
