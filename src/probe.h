#include "rdtsc.h"

inline __attribute__((always_inline)) int reload(char *addr);
inline __attribute__((always_inline)) void flush(char *addr);

inline __attribute__((always_inline)) int reload(char *addr){
		int a;
		a=probe_64(addr);
	    return a;
}
inline __attribute__((always_inline)) void flush(char *addr){
	cflush(addr);
}
