#ifndef FLUSHRELOADNATIVE_EVICT_SET_H
#define FLUSHRELOADNATIVE_EVICT_SET_H

#include "globals/all.h"

#include "globals/all.h"
#include "utils.h"
#include "tsc.h"
#include "evict_set.h"
#include "flush_reload.h"

/*
typedef struct EvictSet {
    void * mappedMem[EVICT_SET_NUM_BLOCKS_MAX];
    int numMemBlocks;
    MEM_ADDR * addrList;
    int addrListLen;
} EvictSet;
*/

static int setLinkEvictSet(struct EvictSet * s, int n, int step, int inc) {
    // Not enough space to store eviction set
    if (step / inc > CACHE_LINE_SIZE / sizeof(MEM_ADDR)) {
        return -1;
    }
    int count = 0;
    int i, j;
    int * used = malloc(n * sizeof(int));
    MEM_ADDR prev = 0, head = 0;
    memset(used, 0, n * sizeof(int));
    for (i = 0; i < n - step + 1; i += inc) {
        for (j = 0; j < step; j ++) {
            if (prev != 0)
                MEM_ADDR_VALUE(prev) = (s->addrList[i+j] + used[i+j]);
            if (head == 0)
                head = s->addrList[i+j] + used[i+j];
            prev = s->addrList[i+j] + used[i+j];
            used[i+j] += sizeof(MEM_ADDR);
            count += 1;
        }
    }
    if (prev != 0)
        MEM_ADDR_VALUE(prev) = head;
    free(used);
    // fprintf(stderr, "%d %d %d %d\n", n, step, inc, count);
    return count;
}

static void accessEvictSetLinked(struct EvictSet * s, int n) {
    int i;
    MEM_ADDR ptr = s->addrList[0];
    // fprintf(stderr, "%d---------------\n", n);
    for (i = 0; i < n; i++) {
        ptr = MEM_ADDR_VALUE(ptr);
        // fprintf(stderr, "%lx\n", ptr);
    }
}

/*
static void accessEvictSet(struct EvictSet * s) {
    int i, j;
    for (i = 0; i < EVICT_SET_ACCESS_SIZE - EVICT_SET_ACCESS_STEPS + 1; i += EVICT_SET_ACCESS_INC) {
        for (j = 0; j < EVICT_SET_ACCESS_STEPS; j ++) {
            LOAD(s->addrList[i+j]);
        }
    }
}
*/
static void accessEvictSet(struct EvictSet * s) {
    int i, j;
    for (i = 0; i < s->addrListLen - EVICT_SET_ACCESS_STEPS + 1; i += EVICT_SET_ACCESS_INC) {
        for (j = 0; j < EVICT_SET_ACCESS_STEPS; j ++) {
            LOAD(s->addrList[i+j]);
        }
    }
}

static void accessEvictSetIns(struct EvictSet * s) {
    MEM_ADDR read = 0;
    int i, j;
    for (i = 0; i < EVICT_SET_ACCESS_SIZE - EVICT_SET_ACCESS_STEPS + 1; i += EVICT_SET_ACCESS_INC) {
        for (j = 0; j < EVICT_SET_ACCESS_STEPS; j ++) {
            PREFETCHI(s->addrList[i+j]);
        }
    }
}

static int __accessEvictSet(struct EvictSet * s, int n, int step, int inc) {
    MEM_ADDR read = 0;
    int count = 0;
    int i, j;
    for (i = 0; i < n - step + 1; i += inc) {
        for (j = 0; j < step; j ++) {
            read += MEM_ADDR_VALUE(s->addrList[i+j]);
            count ++;
        }
    }
    return count;
}

/*
float testEvictSetCompleteness(struct EvictSet * set, MEM_ADDR addr) {
    int j;
    int n_rounds = 50;
    uint64_t ts0, ts1, ts2, ts3;
    int count = 0;
    LOAD(addr);
    for (j = 0; j < n_rounds; j++) {
        LOAD(addr);
        ts0 = readtsc();
        // PREFETCH(addr);
        LOAD(addr);
        ts1 = readtsc();
        accessEvictSet(set);
        ts2 = readtsc();
        // PREFETCH(addr);
        LOAD(addr);
        ts3 = readtsc();
        // if ((float)(ts3 - ts2) / (float)(ts1 - ts0) > EVICT_SET_MISS_TIMING_THRESHOLD)
        // fprintf(stderr, "%llu\n", ts3 - ts2);
        if (ts3 - ts2 > EVICT_SET_MISS_TIMING_THRESHOLD)
            count += 1;
    }
    return (float)count / n_rounds;
}
*/
static float testEvictSetCompleteness(struct EvictSet * es, MEM_ADDR target_addr, int rounds) {
    int i;
    uint64_t ts, t0, t1, c0, c1;
    float mr, tsv, tv, cv;
    float mr0, mr1;

    mr = tsv = tv = cv = 0.0;
    for (i = 0; i < rounds; i++) {
        c0 = getTime();
        // RELOAD_EVICT_ALL_LEVELS(es, es_rop, target_addr, ts);
        // RELOAD_EVICT(es, target_addr, ts);
        RELOAD_TIME(target_addr, ts);
        EVICT(es);
        c1 = getTime();
        if (ts > FNR_THRESHOLD)
            mr += 1.0 / rounds;
        tsv += ts * 1.0 / rounds;
        cv += (c1 - c0) * 1.0 / rounds;
    }
    // fprintf(stderr, "%.02f\t%.02f\t%.02f\n", mr, tsv, cv);
    mr0 = mr;

    mr = tsv = tv = cv = 0.0;
    for (i = 0; i < rounds; i++) {
        c0 = getTime();
        // RELOAD_EVICT_ALL_LEVELS(es, es_rop, target_addr, ts);
        // RELOAD_EVICT(es, target_addr, ts);
        RELOAD_TIME(target_addr, ts);
        EVICT(es);
        c1 = getTime();
        if (ts > FNR_THRESHOLD)
            mr += 1.0 / rounds;
        tsv += ts * 1.0 / rounds;
        cv += (c1 - c0) * 1.0 / rounds;
        // LOAD(target_addr);
        // PREFETCHI(target_addr);
        // LOAD_ROP(target_addr);
        EVICT(es);
        LOAD(target_addr);
    }
    // fprintf(stderr, "%.02f\t%.02f\t%.02f\n", mr, tsv, cv);
    mr1 = mr;
    fprintf(stderr, "%.02f\t%.02f\n", mr0, mr1);

    return mr0 - mr1;
}

static struct EvictSet * createEvictSetFromIteration(MEM_ADDR addr) {
    fprintf(stderr, "Creating eviction set by iteration.\n");

    int i, j, k;
    int num_of_iterations = 3;
    float cmp;
    int numPagesPerBlock = EVICT_SET_BLOCK_SIZE / PAGE_SIZE;
    struct EvictSet * ret = malloc(sizeof(struct EvictSet));
    MEM_ADDR * vaddrs = malloc(EVICT_SET_BLOCK_SIZE / PAGE_SIZE * sizeof(MEM_ADDR));
    MEM_ADDR * paddrs = malloc(EVICT_SET_BLOCK_SIZE / PAGE_SIZE * sizeof(MEM_ADDR));
    ret->numMemBlocks = 0;
    ret->addrList = malloc(numPagesPerBlock * EVICT_SET_NUM_BLOCKS_MAX * sizeof(MEM_ADDR));
    ret->addrListLen = 0;

    MEM_ADDR offset = PAGE_OFFSET(addr);
    MEM_ADDR offset_aligned = (offset >> OFFSET_BITS) << OFFSET_BITS;

    /* Allocate memory to produce conflict */
    for (i = 0; i < EVICT_SET_NUM_BLOCKS_MAX; i++) {
        ret->mappedMem[i] = mmap(NULL, EVICT_SET_BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
        ret->numMemBlocks ++;
        ret->addrListLen += numPagesPerBlock;
        for (j = 0; j < numPagesPerBlock; j++) {
            ret->addrList[i * numPagesPerBlock + j] = (MEM_ADDR)ret->mappedMem[i] + j * PAGE_SIZE + offset;
        }
        cmp = testEvictSetCompleteness(ret, addr, 1000);
        if (cmp > EVICT_SET_MISS_RATIO)
           break;
    }
    fprintf(stderr, "%d %f\n", ret->addrListLen, cmp);

    /* Reduce size of eviction set */
    MEM_ADDR * tmpAddrs = malloc(ret->addrListLen * sizeof(MEM_ADDR));
    int tmpAddrsLen;
    int numRemoval;

    for (k = 0; k < num_of_iterations; k++) {
        i = 0;
        numRemoval = 0;
        while (i < ret->addrListLen) {
            memcpy(tmpAddrs, ret->addrList, ret->addrListLen * sizeof(MEM_ADDR));
            tmpAddrsLen = ret->addrListLen;
            // Remove one item
            for (j = i; j < ret->addrListLen - 1; j++) {
                ret->addrList[j] = ret->addrList[j + 1];
            }
            ret->addrListLen -= 1;
            // Test result
            cmp = testEvictSetCompleteness(ret, addr, 1000);
            if (cmp > EVICT_SET_MISS_RATIO) {
                // fprintf(stderr, "0");
                numRemoval ++;
                continue;
            } else {
                // fprintf(stderr, "1");
                memcpy(ret->addrList, tmpAddrs, tmpAddrsLen * sizeof(MEM_ADDR));
                ret->addrListLen = tmpAddrsLen;
                i ++;
            }
        }
        cmp = testEvictSetCompleteness(ret, addr, 1000);
        fprintf(stderr, "%d %f\n", ret->addrListLen, cmp);
        // if (numRemoval == 0)
        //     break;
    }

    return ret;
}

static struct EvictSet * createEvictSetFromPagemap(MEM_ADDR addr) {
    FILE * pagemapFp;
    int i, j, k;
    int conflictCount;
    MEM_ADDR vaddr_base, paddr_base;
    int cidx_base, cidx_offset;
    int numPagesPerBlock = EVICT_SET_BLOCK_SIZE / PAGE_SIZE;

#ifdef VERBOSE
    fprintf(stderr, "Creating eviction set from pagemap.\n");
#endif
    pagemapFp = fopen("/proc/self/pagemap", "rb");
    if (!pagemapFp) {
        fprintf(stderr, "Cannot open pagemap.\n");
        return createEvictSetFromIteration(addr);
    }

    struct EvictSet * ret = malloc(sizeof(struct EvictSet));
    MEM_ADDR * vaddrs = malloc(EVICT_SET_BLOCK_SIZE / PAGE_SIZE * sizeof(MEM_ADDR));
    MEM_ADDR * paddrs = malloc(EVICT_SET_BLOCK_SIZE / PAGE_SIZE * sizeof(MEM_ADDR));
    ret->numMemBlocks = 0;
    ret->addrList = malloc(2 * EVICT_SET_SIZE_MIN * sizeof(MEM_ADDR));
    ret->addrListLen = 0;

    vaddr_base = PAGE_ADDR(addr);
    cidx_offset = CACHE_IDX_L2(PAGE_OFFSET(addr));
    getPhyAddrs(pagemapFp, &vaddr_base, &paddr_base, 1);
    cidx_base = CACHE_IDX_L2(paddr_base);
#ifdef VERBOSE
    fprintf(stderr, "%x %x %x %x %x\n", addr, vaddr_base, paddr_base, cidx_base, cidx_offset);
#endif

    conflictCount = 0;
    for (i = 0; i < EVICT_SET_NUM_BLOCKS_MAX; i++) {
        ret->mappedMem[i] = mmap(NULL, EVICT_SET_BLOCK_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, 0, 0);
        for (j = 0; j < numPagesPerBlock; j ++) {
            vaddrs[j] = (MEM_ADDR)ret->mappedMem[i] + j * PAGE_SIZE;
            *(char*)(vaddrs[j]) = 0;
        }
        getPhyAddrs(pagemapFp, vaddrs, paddrs, numPagesPerBlock);
        for (j = 0; j < numPagesPerBlock; j ++) {
            if (CACHE_IDX_L2(paddrs[j]) == cidx_base) {
                ret->addrList[ret->addrListLen] = vaddrs[j] + cidx_offset * CACHE_LINE_SIZE;
                ret->addrListLen ++;
#ifdef VERBOSE
                // fprintf(stderr, "%lx -> %lx\n", vaddrs[j] + cidx_offset * CACHE_LINE_SIZE, paddrs[j]);
#endif
                conflictCount ++;
                if (conflictCount >= EVICT_SET_SIZE_MIN) {
                    break;
                }
            }
        }

        if (conflictCount >= EVICT_SET_SIZE_MIN) {
            break;
        }
    }

    fclose(pagemapFp);

    // Failed
    if (conflictCount < EVICT_SET_SIZE_MIN) {
        fprintf(stderr, "Eviction set creation failed.\n");
        fprintf(stderr, "%d / %d\n", conflictCount, EVICT_SET_SIZE_MIN);
        for (i = 0; i < EVICT_SET_NUM_BLOCKS_MAX; i++)
            munmap(ret->mappedMem[i], EVICT_SET_BLOCK_SIZE);
        free(ret->addrList);
        free(ret);
        return 0;
    }

    fprintf(stderr, "Conflict set size: %d\n", conflictCount);
    ret->addrListLen = EVICT_SET_ACCESS_SIZE; // Enforce access size
    /*
    for (i = 0; i < conflictCount; i++) {
        fprintf(stderr, "%lx\n",  ret->addrList[i]);
    }
    */

    return ret;
}

static struct EvictSet * createEvictSet(MEM_ADDR addr) {
    struct EvictSet * es = createEvictSetFromPagemap(addr);
    // struct EvictSet * es = createEvictSetFromIteration(addr);
    setLinkEvictSet(es, EVICT_SET_ACCESS_SIZE, EVICT_SET_ACCESS_STEPS, EVICT_SET_ACCESS_INC);
    return es;
}

static void destroyEvictSet(struct EvictSet * es) {
    int i;
    for (i = 0; i < es->numMemBlocks; i++) {
        munmap(es->mappedMem[i], EVICT_SET_BLOCK_SIZE);
    }
    fprintf(stderr, "Freeing address list\n");
    free(es->addrList);
    // fprintf(stderr, "Freeing eviction set struct\n");
    // free(es);
}

#endif
