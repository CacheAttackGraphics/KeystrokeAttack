#ifndef FLUSHRELOADNATIVE_TSC_H
#define FLUSHRELOADNATIVE_TSC_H

#include <assert.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/perf_event.h>

/*
 * clock_gettime()
 */
#define FNR_THRESHOLD_CLOCK_GETTIME 200
#define FNR_THRESHOLD_CLOCK_GETTIME_LOW 0

static struct timespec tsc_timespec;

static uint64_t getTime() {
    clock_gettime(CLOCK_MONOTONIC, &tsc_timespec);
    // syscall(__NR_clock_gettime, CLOCK_MONOTONIC, &tsc_timespec);
    return ((uint64_t) tsc_timespec.tv_sec) * 1000000000 + tsc_timespec.tv_nsec;
}

#define CLOCK_GETTIME(X) { \
    clock_gettime(CLOCK_MONOTONIC, &tsc_timespec); \
    X = ((uint64_t) tsc_timespec.tv_sec) * 1000000000 + tsc_timespec.tv_nsec; \
}

/*
#ifdef ENVIRONMENT_64_BIT
#define RDTSC(X) { \
    syscall(__NR_clock_gettime, CLOCK_MONOTONIC, &tsc_timespec); \
    X = ((uint64_t) tsc_timespec.tv_sec) * 1000000000 + tsc_timespec.tv_nsec; \
}
#else
#define RDTSC(X) { \
    asm volatile ("push {r7, lr}"); \
    asm volatile ("ldr r0, =%0" :: "r" (CLOCK_MONOTONIC)); \
    asm volatile ("ldr r1, =%0" :: "r" (&tsc_timespec)); \
    asm volatile ("ldr r7, =%0" :: "r" (SYSCALL_CLOCK_GETTIME)); \
    asm volatile ("swi #0"); \
    asm volatile ("pop {r7, lr}"); \
    X = ((uint64_t) tsc_timespec.tv_sec) * 1000000000 + tsc_timespec.tv_nsec; \
}
#endif
*/


/*
 * perf_event_open
 */
#define FNR_THRESHOLD_PERF_EVENT_OPEN 400
#define FNR_THRESHOLD_PERF_EVENT_OPEN_LOW 300

static FILE * perfEventFd;

static inline int __perf_init(int pid, int cpu) {
  static struct perf_event_attr attr;
  attr.type = PERF_TYPE_HARDWARE;
  attr.config = PERF_COUNT_HW_CPU_CYCLES;
  attr.size = sizeof(attr);
  attr.exclude_kernel = 1;
  attr.exclude_hv = 1;
  attr.exclude_callchain_kernel = 1;

  perfEventFd = syscall(__NR_perf_event_open, &attr, pid, cpu, -1, 0);
  assert(perfEventFd >= 0);

  return 1;
}

static inline int perf_init() {
  static struct perf_event_attr attr;
  attr.type = PERF_TYPE_HARDWARE;
  attr.config = PERF_COUNT_HW_CPU_CYCLES;
  attr.size = sizeof(attr);
  attr.exclude_kernel = 1;
  attr.exclude_hv = 1;
  attr.exclude_callchain_kernel = 1;

  perfEventFd = syscall(__NR_perf_event_open, &attr, 0, -1, -1, 0);
  assert(perfEventFd >= 0);

  return 1;
}

static inline int perf_terminate() {
  close(perfEventFd);
  return 1;
}

static uint64_t perf_get_timing() {
  long long result = 0;

  if (read(perfEventFd, &result, sizeof(result)) < (ssize_t) sizeof(result)) {
    return 0;
  }

  return result;
}

static uint64_t (*readtsc)();

#define TSC_TEST_ROUNDS 100
static void tscSetup() {
    int i = 0;
    uint64_t t0, t1;
    uint64_t t_clk[TSC_TEST_ROUNDS], t_perf[TSC_TEST_ROUNDS];
    float t_clk_avg = 0.0, t_perf_avg = 0.0;
    perf_init();
    for (i = 0; i < TSC_TEST_ROUNDS; i++) {
        CLOCK_GETTIME(t0); // t0 = getTime();
        CLOCK_GETTIME(t1); // t1 = getTime();
        t_clk[i] = t1 - t0;
        t_clk_avg += (float)(t1 - t0) / TSC_TEST_ROUNDS;
        t0 = perf_get_timing();
        t1 = perf_get_timing();
        t_perf[i] = t1 - t0;
        t_perf_avg += (float)(t1 - t0) / TSC_TEST_ROUNDS;
    }
    perf_terminate();

#ifdef VERBOSE
    fprintf(stderr, "clock_gettime:\t%f\n", t_clk_avg);
    fprintf(stderr, "perf_event_open:\t%f\n", t_perf_avg);
#endif

    if (t_perf_avg > 0 && t_perf_avg < t_clk_avg) {
        readtsc = perf_get_timing;
        FNR_THRESHOLD = FNR_THRESHOLD_PERF_EVENT_OPEN;
        FNR_THRESHOLD_LOW = FNR_THRESHOLD_PERF_EVENT_OPEN_LOW;
    } else {
        readtsc = getTime;
        FNR_THRESHOLD = FNR_THRESHOLD_CLOCK_GETTIME;
        FNR_THRESHOLD_LOW = FNR_THRESHOLD_CLOCK_GETTIME_LOW;
    }
}

#endif
