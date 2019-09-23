#ifndef __RDTSC_H_DEFINED__
#define __RDTSC_H_DEFINED__


#if defined(__i386__)

 __inline__ unsigned long long rdtsc(void)
{
  unsigned long long int x;
     __asm__ volatile (".byte 0x0f, 0x31" : "=A" (x));
     return x;
}

#elif defined(__x86_64__)

 inline int probe_64(char *adrs) {
 	volatile unsigned long time_start;
 	volatile unsigned long time_end;

 	asm __volatile__ (
 			"  mfence             \n"
 			"  lfence             \n"
 			"  rdtsc              \n"
 			"  lfence             \n"
 			"  shl $32, %%rdx     \n"
 			"  movq %%rdx, %%rcx  \n"
 			"  movl %%eax, %%ebx  \n"
 			"  movl (%2), %%eax   \n"
 			"  lfence             \n"
 			"  rdtsc              \n"
 			"  shl $32, %%rdx     \n"
 			: "=b" (time_start), "=a" (time_end)
 			: "S" (adrs)
 			: "%rcx", "%rdx");
 	return time_end - time_start;
 }

 inline void maccess(char* p)
 {
   asm volatile ("movq (%0), %%rax\n"
     :
     : "c" (p)
     : "rax");
 }


 inline void cflush(volatile char *address)
{
    asm __volatile__ (
        "mfence         \n"
        "clflush 0(%0)  \n"
        :
        : "r" (address)
        :            );
}


 __inline__ unsigned long long rdtsc(void)
{
	unsigned cycles_high0, cycles_low0;
asm volatile (
			"cpuid\n\t"
		  "rdtsc\n\t"
		  "mov %%edx, %0\n\t"
		  "mov %%eax, %1\n\t"
		  : "=r" (cycles_high0), "=r" (cycles_low0)
		  :: "%rax", "%rbx", "%rcx", "%rdx");

return ( (unsigned long long)cycles_low0)|( ((unsigned long long)cycles_high0)<<32 );
}

#else

#error "No tick counter is available!"

#endif


#endif
