#ifndef FLUSHRELOADNATIVE_CACHE_PARAMS_H
#define FLUSHRELOADNATIVE_CACHE_PARAMS_H

#include "types.h"

#define WAY_BITS_L2             4
#define WAY_BITS_L1_DATA        1
#define WAY_BITS_L1_INS         2
#define OFFSET_BITS             6
#define INDEX_BITS_L2           10
#define INDEX_BITS_L1_DATA      8
#define INDEX_BITS_L1_INS       8
#define NUM_WAYS_L2             16
#define NUM_WAYS_L1_DATA        2
#define NUM_WAYS_L1_INS         3

#define CACHE_LINE_SIZE 			(1 << OFFSET_BITS)
#define NUM_LINES_PER_PAGE 			PAGE_SIZE / CACHE_LINE_SIZE
#define NUM_CACHE_SETS_L2 			(1 << INDEX_BITS_L2)
#define NUM_CACHE_SETS_L1_DATA		(1 << INDEX_BITS_L1_DATA)
#define NUM_CACHE_SETS_L1_INS		(1 << INDEX_BITS_L1_INS)

#define CACHE_SIZE_L2 				(NUM_WAYS_L2 * NUM_CACHE_SETS_L2 * CACHE_LINE_SIZE)
#define CACHE_SIZE_L1_DATA 			(NUM_WAYS_L1_DATA * NUM_CACHE_SETS_L1_DATA * CACHE_LINE_SIZE)
#define CACHE_SIZE_L1_INS 			(NUM_WAYS_L1_INS * NUM_CACHE_SETS_L1_INS * CACHE_LINE_SIZE)

#define PAGE_ADDR(X) (X & ~(PAGE_SIZE - 1))
#define PAGE_OFFSET(X) (X & (PAGE_SIZE - 1))
#define CACHE_IDX_L2(X) ((X >> OFFSET_BITS) & ((1 << INDEX_BITS_L2) - 1))
#define CACHE_IDX_L1_DATA(X) ((X >> OFFSET_BITS) & ((1 << INDEX_BITS_L1_DATA) - 1))
#define CACHE_IDX_L1_INS(X) ((X >> OFFSET_BITS) & ((1 << INDEX_BITS_L1_INS) - 1))

static void printCacheSpecs() {
	fprintf(stderr, "WAY_BITS_L2 			%d\n", WAY_BITS_L2);
	fprintf(stderr, "WAY_BITS_L1_DATA 		%d\n", WAY_BITS_L1_DATA);
	fprintf(stderr, "WAY_BITS_L1_INS 		%d\n", WAY_BITS_L1_INS);
	fprintf(stderr, "OFFSET_BITS 			%d\n", OFFSET_BITS);
	fprintf(stderr, "INDEX_BITS_L2 			%d\n", INDEX_BITS_L2);
	fprintf(stderr, "INDEX_BITS_L1_DATA		%d\n", INDEX_BITS_L1_DATA);
	fprintf(stderr, "INDEX_BITS_L1_INS		%d\n", INDEX_BITS_L1_INS);
	fprintf(stderr, "NUM_WAYS_L2 			%d\n", NUM_WAYS_L2);
	fprintf(stderr, "NUM_WAYS_L1_DATA		%d\n", NUM_WAYS_L1_DATA);
	fprintf(stderr, "NUM_WAYS_L1_INS		%d\n", NUM_WAYS_L1_INS);
}

#endif
