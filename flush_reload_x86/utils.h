#ifndef _UTILS_H_
#define _UTILS_H_

#include "global.h"

static int load_data = 0;
#define LOAD(ADDR) { load_data = load_data ^ *((int*)ADDR); }
#define LOAD_ROP(ADDR) { asm volatile ("call %[addr]" :: [addr] "r" (ADDR)); }
// #define RDTSC(X) asm volatile ( "xor %%eax, %%eax; cpuid; rdtsc;" : "=a" (X))
#ifdef __X86_32BIT__
#define RDTSC(X) asm volatile ( "rdtsc; movl %%eax, %[out]" : [out] "=r" (X))
#define RDTSCP(X) asm volatile ( "rdtscp; movl %%eax, %[out]" : [out] "=r" (X))
#else
#define RDTSC(X) asm volatile ( "rdtsc;" : "=a" (X))
#define RDTSCP(X) asm volatile ( "rdtscp;" : "=a" (X))
#endif
// #define MFENCE() asm volatile ( "xor %eax, %eax; cpuid;")
#define MFENCE() asm volatile ( "mfence")
// #define CFLUSH(X) asm volatile ("mfence; clflush (%0); mfence" :: "r" (X))
#define CFLUSH(X) asm volatile ("clflush (%0);" :: "r" (X))

void delay(uint64_t t) {
    REGISTER ts, ts_end;
    RDTSCP(ts);
    ts_end = ts + t;
    while (1) {
        RDTSCP(ts);
        if (ts > ts_end)
            return;
    }
}

void _sleep(unsigned long nsec) {
    struct timespec delay = { nsec / 1000000000, nsec % 1000000000 };
    nanosleep(&delay, 0);
}

#ifdef __X86_32BIT__
inline __attribute__((always_inline)) uint64_t rdtsc_bgn() {
  REGISTER a, d;
  asm volatile ("mfence\n\t"
    "RDTSCP\n\t"
    "mov %%edx, %[d]\n\t"
    "mov %%eax, %[a]\n\t"
    "xor %%eax, %%eax\n\t"
    "CPUID\n\t"
    : [d] "=r" (d), [a] "=r" (a));
  uint64_t r = d;
  r = (r<<32) | (uint64_t)a;
  return r;
}

inline __attribute__((always_inline)) uint64_t rdtsc_end() {
  REGISTER a, d;
  asm volatile(
    "xor %%eax, %%eax\n\t"
    "CPUID\n\t"
    "RDTSCP\n\t"
    "mov %%edx, %[d]\n\t"
    "mov %%eax, %[a]\n\t"
    "mfence\n\t"
    : [d] "=r" (d), [a] "=r" (a));
   uint64_t r = d;
   r = (r<<32) | (uint64_t)a;
   return r;
}

inline __attribute__((always_inline)) uint64_t rdtsc() {
  REGISTER a, d;
  asm volatile ("mfence");
  asm volatile ("rdtsc" : "=a" (a));
  asm volatile ("mfence");
  return a;
}
#else
inline __attribute__((always_inline)) uint64_t rdtsc_bgn() {
  REGISTER a, d;
  asm volatile ("mfence\n\t"
    "RDTSCP\n\t"
    "mov %%rdx, %0\n\t"
    "mov %%rax, %1\n\t"
    "xor %%rax, %%rax\n\t"
    "CPUID\n\t"
    : "=r" (d), "=r" (a)
    :
    : "%rax", "%rbx", "%rcx", "%rdx");
  uint64_t r = d;
  r = (r<<32) | (uint64_t)a;
  return r;
}

inline __attribute__((always_inline)) uint64_t rdtsc_end() {
  REGISTER a, d;
  asm volatile(
    "xor %%rax, %%rax\n\t"
    "CPUID\n\t"
    "RDTSCP\n\t"
    "mov %%rdx, %0\n\t"
    "mov %%rax, %1\n\t"
    "mfence\n\t"
    : "=r" (d), "=r" (a)
    :
    : "%rax", "%rbx", "%rcx", "%rdx");
   uint64_t r = d;
   r = (r<<32) | (uint64_t)a;
   return r;
}

/*
inline __attribute__((always_inline)) uint64_t rdtsc() {
  REGISTER a, d;
  asm volatile ("mfence");
  asm volatile ("rdtsc" : "=a" (a));
  asm volatile ("mfence");
  return a;
}
*/

uint64_t rdtsc() {
  uint64_t a, d;
  asm volatile ("mfence");
  asm volatile ("rdtsc" : "=a" (a), "=d" (d));
  a = (d<<32) | a;
  asm volatile ("mfence");
  return a;
}
#endif

void flush(void* p) {
    asm volatile ("clflush 0(%0)\n"
      :
      : "c" (p)
      : "rax");
}

static struct timespec tsc_timespec;

static uint64_t getTime() {
    clock_gettime(CLOCK_MONOTONIC, &tsc_timespec);
    // syscall(__NR_clock_gettime, CLOCK_MONOTONIC, &tsc_timespec);
    return ((uint64_t) tsc_timespec.tv_sec) * 1000000000 + tsc_timespec.tv_nsec;
}

/**
 * Pagemap access
 */
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
    fprintf(stderr, "Setting Affinity to %d: %d\n", affinity, syscallres);
    return syscallres;
}

#endif
