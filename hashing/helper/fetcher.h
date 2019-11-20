//
// Created by Shuhao Zhang on 1/11/19.
//

#ifndef ALLIANCEDB_FETCHER_H
#define ALLIANCEDB_FETCHER_H

#include "../utils/types.h"
#include <stdio.h>

struct fetch_t {
    fetch_t(fetch_t *fetch);

    fetch_t();

    tuple_t *tuple;

    bool flag;//whether this tuple from input R (true) or S (false).

    bool ack = false;//whether this is just a message. Used in HS model.
};

//thread local structure
struct t_state {
    int start_index_R = 0;//configure pointer of start reading point.
    int end_index_R = 0;//configure pointer of end reading point.
    int start_index_S = 0;//configure pointer of start reading point.
    int end_index_S = 0;//configure pointer of end reading point.
    //read R/S alternatively.
    bool flag;
    fetch_t fetch;
};

class baseFetcher {
public:
    virtual fetch_t *next_tuple(int tid) = 0;

    relation_t *relR;//input relation
    relation_t *relS;//input relation

    t_state *state;

    virtual bool finish(int32_t tid) = 0;

    baseFetcher(relation_t *relR, relation_t *relS) {
        this->relR = relR;
        this->relS = relS;
    }
};

inline bool last_thread(int i, int nthreads) {
    return i == (nthreads - 1);
}

class HS_NP_Fetcher : public baseFetcher {
public:
    fetch_t *next_tuple(int tid) override;

    bool finish(int tid) {
        return false;//should not be called.
    }

    /**
     * Initialization
     * @param nthreads
     * @param relR
     * @param relS
     */
    HS_NP_Fetcher(int nthreads, relation_t *relR, relation_t *relS)
            : baseFetcher(relR, relS) {
        state = new t_state[nthreads];

        int i;
        i = 0;

        //let first and last thread to read two streams.
        state[i].flag = true;
        /* replicate relR to thread 0 */
        state[i].start_index_R = 0;
        state[i].end_index_R = relR->num_tuples;
#ifdef DEBUG
        printf("TID:%d, R: start_index:%d, end_index:%d\n", i, state[i].start_index_R, state[i].end_index_R);
        printf("TID:%d, S: start_index:%d, end_index:%d\n", i, state[i].start_index_S, state[i].end_index_S);
#endif

        i = nthreads - 1;
        /* replicate relS to thread [nthread-1] */
        state[i].start_index_S = 0;
        state[i].end_index_S = relS->num_tuples;

#ifdef DEBUG
        printf("TID:%d, R: start_index:%d, end_index:%d\n", i, state[i].start_index_R, state[i].end_index_R);
        printf("TID:%d, S: start_index:%d, end_index:%d\n", i, state[i].start_index_S, state[i].end_index_S);
#endif

    }
};

class JM_NP_Fetcher : public baseFetcher {
public:
    fetch_t *next_tuple(int tid) override;

    bool finish(int tid) {
        return state[tid].start_index_R == state[tid].end_index_R
               && state[tid].start_index_S == state[tid].end_index_S;
    }

    /**
     * Initialization
     * @param nthreads
     * @param relR
     * @param relS
     */
    JM_NP_Fetcher(int nthreads, relation_t *relR, relation_t *relS)
            : baseFetcher(relR, relS) {
        state = new t_state[nthreads];

        int numSthr = relS->num_tuples / nthreads;//replicate R, partition S.
        for (int i = 0; i < nthreads; i++) {

            state[i].flag = true;
            /* replicate relR for next thread */
            state[i].start_index_R = 0;
            state[i].end_index_R = relR->num_tuples;

            /* assign part of the relS for next thread */
            state[i].start_index_S = numSthr * i;
            state[i].end_index_S = (last_thread(i, nthreads)) ? relS->num_tuples : numSthr * (i + 1);

#ifdef DEBUG
            printf("TID:%d, R: start_index:%d, end_index:%d\n", i, state[i].start_index_R, state[i].end_index_R);
            printf("TID:%d, S: start_index:%d, end_index:%d\n", i, state[i].start_index_S, state[i].end_index_S);
#endif
        }
    }
};

class JB_NP_Fetcher : public baseFetcher {
public:
    fetch_t *next_tuple(int tid) override;

    bool finish(int tid) {
        return state[tid].start_index_R == state[tid].end_index_R
               && state[tid].start_index_S == state[tid].end_index_S;
    }

    JB_NP_Fetcher(int nthreads, relation_t *relR, relation_t *relS)
            : baseFetcher(relR, relS) {
        state = new t_state[nthreads];
        int numRthr = relR->num_tuples / nthreads;// partition R,
        int numSthr = relS->num_tuples / nthreads;// partition S.
        for (int i = 0; i < nthreads; i++) {

            state[i].flag = true;
            /* assign part of the relR for next thread */
            state[i].start_index_R = numRthr * i;
            state[i].end_index_R = (last_thread(i, nthreads)) ? relR->num_tuples : numRthr * (i + 1);

            /* assign part of the relS for next thread */
            state[i].start_index_S = numSthr * i;
            state[i].end_index_S = (last_thread(i, nthreads)) ? relS->num_tuples : numSthr * (i + 1);

#ifdef DEBUG
            printf("TID:%d, R: start_index:%d, end_index:%d\n", i, state[i].start_index_R, state[i].end_index_R);
            printf("TID:%d, S: start_index:%d, end_index:%d\n", i, state[i].start_index_S, state[i].end_index_S);
#endif
        }
    }
};

#endif //ALLIANCEDB_FETCHER_H