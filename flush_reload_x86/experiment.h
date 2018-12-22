#ifndef _EXPERIMENT_H_
#define _EXPERIMENT_H_

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

static char log_file[20] = "log_fnr";

void runFnrBE(MEM_ADDR target_bgn, MEM_ADDR target_end) {
    uint64_t prev_ts = 100000;
    FILE * f = fopen(log_file, "w+");
    fprintf(stderr, "Writing to log %s: %#x\n", log_file, f);
    uint64_t ts, c0, c1, t0, t1, cbgn, cend;
    int i;

#define THRESHOLD_BE 50000
    unsigned int log_idx = 0;
    uint64_t tbgn = 0;
    uint64_t tend = 0;
    enum STATUS { BEGIN, END } status = BEGIN;

    while (1) {
        cbgn = getTime();
        if (status == BEGIN) {
            FLUSH_RELOAD(target_bgn, ts);

            if (ts < FNR_THRESHOLD) {
                tbgn = cbgn;
                // fprintf(f, "> %llu %llu\n", ts, tbgn);
                // fflush(f);
                status = END;
                CFLUSH(target_end);
            }
        } else if (status == END) {
            FLUSH_RELOAD(target_end, ts);

            if (ts < FNR_THRESHOLD) {
                tend = cbgn;
                fprintf(f, "%llu %llu\n", tbgn, tend);
                fflush(f);
                status = BEGIN;
                CFLUSH(target_bgn);
            } else {
                if (cbgn - tbgn > THRESHOLD_BE) {
                    status = BEGIN;
                    CFLUSH(target_bgn);
                }
            }
        }
    }

    fclose(f);
}

#endif
