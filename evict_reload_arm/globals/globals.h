#ifndef FLUSHRELOADNATIVE_GLOBALS_H
#define FLUSHRELOADNATIVE_GLOBALS_H

static int FNR_THRESHOLD = 400;
static int FNR_THRESHOLD_LOW = 300;

#define EVICT_SET_NUM_BLOCKS_MAX    128
#define EVICT_SET_BLOCK_SIZE        0x100000
#define EVICT_SET_SIZE_MIN          60

#define EVICT_SET_ACCESS_SIZE 32
#define EVICT_SET_ACCESS_STEPS 8
#define EVICT_SET_ACCESS_INC 3
#define ROP_EVICT_SET_FACTOR 4

#define EVICT_SET_ACCESS_NUM (((EVICT_SET_ACCESS_SIZE - EVICT_SET_ACCESS_STEPS + 1) / EVICT_SET_ACCESS_INC) * EVICT_SET_ACCESS_STEPS)

#define EVICT_SET_MISS_TIMING_THRESHOLD FNR_THRESHOLD
#define EVICT_SET_MISS_TIMING_THRESHOLD_REL 1.5
#define EVICT_SET_MISS_RATIO 0.8

static char log_file[100] = "/mnt/sdcard/log_fnr";

#endif
