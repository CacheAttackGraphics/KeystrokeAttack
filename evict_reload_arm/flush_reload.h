#ifndef FLUSHRELOADNATIVE_FLUSH_RELOAD_H
#define FLUSHRELOADNATIVE_FLUSH_RELOAD_H

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include "globals/all.h"
#include "tsc.h"
#include "utils.h"

static uint64_t fnr_ts0, fnr_ts1;
static uint64_t fnr_clk0, fnr_clk1;

static uint64_t reload_evict(struct EvictSet * s, MEM_ADDR target) {
    fnr_ts0 = readtsc(); \
    LOAD(target);
    MEMFENCE(); \
    fnr_ts1 = readtsc(); \
    return fnr_ts1 - fnr_ts0;
}

#define RELOAD_TIME(TARGET, RET) { \
    fnr_ts0 = readtsc(); \
    LOAD(TARGET); \
    fnr_ts1 = readtsc(); \
    RET = fnr_ts1 - fnr_ts0; \
}

#define EVICT(ES) { \
    accessEvictSet(ES); \
    MEMFENCE(); \
}

#define RELOAD_EVICT(ES, TARGET, RET) { \
    fnr_ts0 = readtsc(); \
    LOAD(TARGET); \
    fnr_ts1 = readtsc(); \
    accessEvictSet(ES); \
    MEMFENCE(); \
    RET = fnr_ts1 - fnr_ts0; \
}

#define RELOAD_EVICT_LINKED(ES, TARGET, RET) { \
    fnr_ts0 = readtsc(); \
    LOAD(TARGET); \
    fnr_ts1 = readtsc(); \
    accessEvictSetLinked(ES, EVICT_SET_ACCESS_NUM); \
    MEMFENCE(); \
    RET = fnr_ts1 - fnr_ts0; \
}

#include "flush_reload.h"
#include "globals/all.h"
#include "evict_set.h"

static MEM_ADDR locate_flush_reload_target(char * lib_name, unsigned int cidx_offset) {
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
        return ret_addr;
    else
        return 0;
}

#endif //FLUSHRELOADNATIVE_FLUSH_RELOAD_H
