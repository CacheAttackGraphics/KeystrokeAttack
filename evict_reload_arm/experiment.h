#ifndef FLUSHRELOADNATIVE_EXPERIMENT_H
#define FLUSHRELOADNATIVE_EXPERIMENT_H

#include "globals/all.h"
#include "flush_reload.h"
#include "tsc.h"
#include "evict_set.h"

void runFnr_BE(struct EvictSet * es, MEM_ADDR target_addr, struct EvictSet * es_2, MEM_ADDR target_addr_2) {
    uint64_t prev_ts = 100000;
    FILE * f = fopen(log_file, "w+");
    fprintf(stderr, "Writing to log %s: %#x\n", log_file, f);
    uint64_t ts, ts_prev, c0, c1, t0, t1, cbgn, cbgn_ts;
    int i;

#define LOG_SIZE 10000
#define THRESHOLD_BE 250000
    unsigned int log_idx = 0;
    uint64_t tbgn = 0, tbgn_ts = 0;
    uint64_t tend = 0, tend_ts = 0;
    enum STATUS { BEGIN, END } status = BEGIN;

    while (1) {
        cbgn = getTime();
        cbgn_ts = readtsc();
        if (status == BEGIN) {
            // RELOAD_EVICT(es, target_addr, ts);
            RELOAD_TIME(target_addr, ts);

            if (ts < FNR_THRESHOLD && ts > FNR_THRESHOLD_LOW) {
                tbgn = cbgn;
                tbgn_ts = cbgn_ts;
                status = END;
                ts_prev = ts;
                // accessEvictSet(es_2);
                EVICT(es);
                EVICT(es_2);
            } else {
                EVICT(es);
                EVICT(es_2);
            }
        } else if (status == END) {
            // RELOAD_EVICT(es_2, target_addr_2, ts);
            RELOAD_TIME(target_addr_2, ts);

            if (ts < FNR_THRESHOLD && ts > FNR_THRESHOLD_LOW) {
                tend = cbgn;
                tend_ts = cbgn_ts;
                fprintf(f, "> %llu %llu %llu\n", ts_prev, tbgn, tbgn_ts);
                fprintf(f, "< %llu %llu %llu\n", ts, tend, tend_ts);
                fflush(f);
                status = BEGIN;
                // accessEvictSet(es);
                EVICT(es);
                EVICT(es_2);
            } else {
                if (cbgn - tbgn > THRESHOLD_BE) {
                    status = BEGIN;
                    // accessEvictSet(es);
                    // fprintf(f, "> %llu %llu %llu\n", ts_prev, tbgn, tbgn_ts);
                    EVICT(es);
                    EVICT(es_2);
                } else {
                    EVICT(es);
                    EVICT(es_2);
                }
            }
        }
    }

    fclose(f);
}

#endif
