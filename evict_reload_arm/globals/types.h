#ifndef FLUSHRELOADNATIVE_TYPES_H
#define FLUSHRELOADNATIVE_TYPES_H

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
// #include <cstdint>

#include "globals.h"

typedef uint8_t LOG_ENTRY;

#define PAGE_SIZE 4096

#if INTPTR_MAX == INT32_MAX
    #define ENVIRONMENT_32_BIT
    #define SYSTEM_BITS 32
#elif INTPTR_MAX == INT64_MAX
    #define ENVIRONMENT_64_BIT
    #define SYSTEM_BITS 64
#endif

#ifdef ENVIRONMENT_32_BIT
typedef uint32_t MEM_ADDR;
#define MEM_ADDR_SIZE 4
#else
typedef uint64_t MEM_ADDR;
#define MEM_ADDR_SIZE 8
#endif

#define MEM_ADDR_VALUE(X) *((MEM_ADDR*)X)

typedef struct EvictSet {
    void * mappedMem[EVICT_SET_NUM_BLOCKS_MAX];
    int numMemBlocks;
    MEM_ADDR * addrList;
    int addrListLen;
} EvictSet;

static int setLinkEvictSet(struct EvictSet * s, int n, int step, int inc);

static void accessEvictSetLinked(struct EvictSet * s, int n);

static void accessEvictSet(struct EvictSet * s);

static void accessEvictSetIns(struct EvictSet * s);

static int __accessEvictSet(struct EvictSet * s, int n, int step, int inc);

static float testEvictSetCompleteness(struct EvictSet * es, MEM_ADDR target_addr, int rounds);

static struct EvictSet * createEvictSetFromIteration(MEM_ADDR addr);

static struct EvictSet * createEvictSetFromPagemap(MEM_ADDR addr);

static struct EvictSet * createEvictSet(MEM_ADDR addr);

static void destroyEvictSet(struct EvictSet * es);

static MEM_ADDR locate_flush_reload_target(char * lib_name, unsigned int cidx_offset);

#endif
