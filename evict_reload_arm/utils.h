#ifndef FLUSHRELOADNATIVE_UTILS_H
#define FLUSHRELOADNATIVE_UTILS_H

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sched.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>



#include "globals/types.h"
#include "globals/cache_params.h"

#include "tsc.h"

static MEM_ADDR fnr_read;

#ifdef ENVIRONMENT_64_BIT
#define PREFETCH(X) {\
        asm volatile ("PRFM PLDL3KEEP, [%x0]" :: "p" (X)); \
        asm volatile ("PRFM PLDL2KEEP, [%x0]" :: "p" (X)); \
        asm volatile ("PRFM PLDL1KEEP, [%x0]" :: "p" (X)); \
}
#define PREFETCHI(X) {\
        asm volatile ("PRFM PLIL3KEEP, [%x0]" :: "p" (X)); \
        asm volatile ("PRFM PLIL2KEEP, [%x0]" :: "p" (X)); \
        asm volatile ("PRFM PLIL1KEEP, [%x0]" :: "p" (X)); \
}

#define MEMFENCE() asm volatile ("DSB SY; ISB")

#define LOAD_ROP(X) {}

#define CFLUSH(X) asm volatile ("DC CIVAC, %0" :: "r" (X))

#else // ENVIRONMENT_64_BIT

#define PREFETCH(X) {\
        asm volatile ("pld [%0]" :: "r" (X)); \
}
#define PREFETCHI(X) {\
        asm volatile ("pli [%0]" :: "r" (X)); \
}

#define MEMFENCE() asm volatile ("DSB; ISB")

#ifndef __TEST__
#define LOAD_ROP(X) asm volatile ("push	{r8}; push	{r3-r11, pc}; bx %0; pop {r8}" :: "r"(X))
#else
#define LOAD_ROP(X) asm volatile ("push	{r11, pc}; blx %0" :: "r"(X))
#endif

// #define CFLUSH(X)  	asm volatile ("DCIMVAC" :: "r" (X))
#define CFLUSH(X)  	asm volatile ("MCR p15, 0, %0, c7, c6, 1" :: "r" (X))
// #define CFLUSH(X)  	asm volatile ("push {r0}; LDREXB r0, [%0]; pop {r0}" :: "r" (X))

#endif // ENVIRONMENT_64_BIT

#define LOAD(ADDR) {\
    asm volatile ("ldr %0, [%1]\n\t" : "=r" (fnr_read) : "r" (ADDR)); \
}

#define PAGEMAP_ENTRY 8
#define GET_BIT(X,Y) (X & ((uint64_t)1<<Y)) >> Y
#define SET_BIT(X,Y) X = X | ((uint64_t)1<<Y)
#define CLEAR_BIT(X,Y) X = X & (~((uint64_t)1<<Y))
#define GET_PFN(X) X & 0x7FFFFFFFFFFFFF

static const int __endian_bit = 1;
#define is_bigendian() ( (*(char*)&__endian_bit) == 0 )

static int getPhyAddrs(FILE * f, MEM_ADDR * virt_addrs, MEM_ADDR * phy_addrs, int n) {
    int i, c, pid, status;
    char * end;
    uint64_t file_offset, read_val;
    int pagesize = sysconf(_SC_PAGESIZE);
    uint64_t virt_addr;

    int x = 0;
    while (x < n) {
        virt_addr = virt_addrs[x];
        file_offset = virt_addr / pagesize * PAGEMAP_ENTRY;
        status = fseek(f, file_offset, SEEK_SET);
        if (status) {
            fprintf(stderr, "Failed to do fseek!\n");
            return -1;
        }
        read_val = 0;
        unsigned char c_buf[PAGEMAP_ENTRY];
        for (i = 0; i < PAGEMAP_ENTRY; i++) {
            c = getc(f);
            if (c == EOF) {
                fprintf(stderr, "\nReached end of the file\n");
                return -1;
            }
            if (is_bigendian())
                c_buf[i] = c;
            else
                c_buf[PAGEMAP_ENTRY - i - 1] = c;
        }
        for (i = 0; i < PAGEMAP_ENTRY; i++) {
            read_val = (read_val << 8) + c_buf[i];
        }
        if (GET_BIT(read_val, 63)) {
            unsigned long pfn = GET_PFN(read_val);
            unsigned long paddr = (pfn * pagesize) + (virt_addr & (pagesize - 1));
            phy_addrs[x] = paddr;
        } else {
            phy_addrs[x] = 0;
        }
        x = x + 1;
    }
    return 0;
}

static int setAffinity(int affinity) {
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(affinity, &mask);
    // sched_setaffinity(0, sizeof(mask), &mask);
    int err, syscallres;
    // pid_t pid = gettid();
    pid_t pid = 0;
    syscallres = syscall(__NR_sched_setaffinity, pid, sizeof(mask), &mask);
    return syscallres;
}

static inline void busyWait(uint64_t time) {
	uint64_t c0, c1;
	c0 = getTime();
	while (1) {
		c1 = getTime();
		if (c1 >= c0 + time)
			break;
	}
}

static inline void busyWaitUntil(uint64_t time) {
	uint64_t c1;
	while (1) {
		c1 = getTime();
		if (c1 >= time)
			break;
	}
}

#endif
