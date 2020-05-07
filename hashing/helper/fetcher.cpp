//
// Created by Shuhao Zhang on 1/11/19.
//

#include <cstdio>
#include <assert.h>
#include "fetcher.h"
#include "pmj_helper.h"

fetch_t::fetch_t(fetch_t *fetch) {
    this->fat_tuple = fetch->fat_tuple;
    this->fat_tuple_size = fetch->fat_tuple_size;
    this->tuple = fetch->tuple;
    this->ISTuple_R = fetch->ISTuple_R;
    this->ack = fetch->ack;
}

fetch_t::fetch_t() {}


fetch_t *HS_NP_Fetcher::next_tuple() {
    if (tid == 0) {//thread 0 fetches R.
        if (state->start_index_R < state->end_index_R) {
            state->fetch.tuple = &relR->tuples[state->start_index_R++];
            state->fetch.ISTuple_R = true;
            return &(state->fetch);
        } else {
            return nullptr;
        }
    } else {//thread n-1 fetches S.
        if (state->start_index_S < state->end_index_S) {
            state->fetch.tuple = &relS->tuples[state->start_index_S++];
            state->fetch.ISTuple_R = false;
            return &(state->fetch);
        } else {
            return nullptr;
        }
    }
    return nullptr;
}

/**
 * outdated.
 * @return
 */
fetch_t *PMJ_HS_NP_Fetcher::next_tuple() {
//    uint64_t min_gap = (uint64_t) INT32_MAX;
//    tuple_t *readR = nullptr;
//    tuple_t *readS = nullptr;
//
//    //try to read R first.
//    if (state->start_index_R < state->end_index_R) {
//        state->fetch.fat_tuple_size = min((int) progressive_step_tupleR,
//                                          (state->end_index_R - state->start_index_R));//left-over..
//        readR = &relR->tuples[state->start_index_R];
//        //check the timestamp whether the tuple is ``ready" to be fetched.
//        uint64_t timestamp
//                = relR->payload->ts[readR[state->fetch.fat_tuple_size - 1].payloadID];
////                = (milliseconds) 0;
//        auto timegap = timeGap(&timestamp);
//        if (timegap  <= 0) {//if it's negative means our fetch is too slow.
//            state->fetch.fat_tuple = readR;
//            state->start_index_R += state->fetch.fat_tuple_size;
//            state->fetch.ISTuple_R = true;
//            return &(state->fetch);
//        } else {
//            min_gap = timegap;
//        }
//    }
//    //try to read S then.
//    if (state->start_index_S < state->end_index_S) {
//        state->fetch.fat_tuple_size = min((int) progressive_step_tupleS,
//                                          (state->end_index_S - state->start_index_S));//left-over..
//        readS = &relS->tuples[state->start_index_S];
//        //check the timestamp whether the tuple is ``ready" to be fetched.
//        uint64_t timestamp
//                = relS->payload->ts[readS[state->fetch.fat_tuple_size - 1].payloadID];
//
//        auto timegap = timeGap(&timestamp);
//        if (timegap  <= 0) {//if it's negative means our fetch is too slow.
//            state->fetch.fat_tuple = readS;
//            state->fetch.ISTuple_R = false;
//            state->start_index_S += state->fetch.fat_tuple_size;
//            return &(state->fetch);
//        } else {
//            if (min_gap > timegap) {//S is nearest.
//                min_gap = timegap;
//                DEBUGMSG("Thread %d is going to sleep for %d before get S", tid, min_gap)
//#ifndef NO_TIMING
//                BEGIN_MEASURE_WAIT_ACC(timer)
//#endif
//                this_thread::sleep_for(min_gap);
//#ifndef NO_TIMING
//                END_MEASURE_WAIT_ACC(timer)
//#endif
//                state->fetch.fat_tuple = readS;
//                state->fetch.ISTuple_R = false;
//                state->start_index_S += state->fetch.fat_tuple_size;
//                return &(state->fetch);
//            } else if (readR != nullptr) {//R is nearest.
//                DEBUGMSG("Thread %d is going to sleep for %d before get R", tid, min_gap)
//#ifndef NO_TIMING
//                BEGIN_MEASURE_WAIT_ACC(timer)
//#endif
//                this_thread::sleep_for(min_gap);
//#ifndef NO_TIMING
//                END_MEASURE_WAIT_ACC(timer)
//#endif
//                state->fetch.fat_tuple = readR;
//                state->fetch.ISTuple_R = true;
//                state->start_index_R += state->fetch.fat_tuple_size;
//                return &(state->fetch);
//            }
//        }
//    }
    return nullptr;
}

__always_inline
fetch_t *
next_tuple_S_first(t_state *state, const uint64_t *fetchStartTime, relation_t *relS) {
    tuple_t *readS = nullptr;
    uint64_t arrivalTsS;

    //try to read S first.
    if (state->start_index_S < state->end_index_S) {
        readS = &relS->tuples[state->start_index_S];
#ifdef WAIT
        //check the timestamp whether the tuple is ``ready" to be fetched.
        arrivalTsS = relS->payload->ts[readS->payloadID];
        auto tick = curtick();
        int64_t timegap = arrivalTsS - (tick - *fetchStartTime);

        if (timegap <= 0) {//if it's negative means our fetch is too slow.
            printf("arrival ts: %lu, offset: %ld, cur tick: %lu, fetch time: %lu, tid: %d\n", arrivalTsS, timegap, tick, *fetchStartTime, std::this_thread::get_id());
            state->fetch.tuple = readS;
            state->fetch.ISTuple_R = false;
            state->start_index_S++;
            return &(state->fetch);
        }
#else//return without checking for timestamp.
        state->fetch.tuple = readS;
        state->fetch.ISTuple_R = false;
        state->start_index_S++;
        return &(state->fetch);
#endif
//        if (retry)
//            printf("sid[%d], arrivalTsS:%ld, readTS:%ld\n", state->start_index_S, arrivalTsS, readTS);
    }
    return nullptr;
}

__always_inline
fetch_t *
next_tuple_R_first(t_state *state, const uint64_t *fetchStartTime, relation_t *relR) {
    tuple_t *readR = nullptr;
    uint64_t arrivalTsR;
    //try to read R first.
    if (state->start_index_R < state->end_index_R) {
        readR = &relR->tuples[state->start_index_R];
#ifdef WAIT
        //check the timestamp whether the tuple is ``ready" to be fetched.
        arrivalTsR = relR->payload->ts[readR->payloadID];
        int64_t timegap = arrivalTsR - (curtick() - *fetchStartTime);
        if (timegap <= 0) {//if it's negative means our fetch is too slow.
            state->fetch.tuple = readR;
            state->fetch.ISTuple_R = true;
            state->start_index_R++;
            return &(state->fetch);
        }
#else//return without checking for timestamp.
        state->fetch.tuple = readR;
        state->fetch.ISTuple_R = true;
        state->start_index_R++;
        return &(state->fetch);
#endif
//        if (retry)
//            printf("rid[%d] (%%d), arrivalTsR:%ld, readTS:%ld\n", state->start_index_R, arrivalTsR, readTS);
    }
    return nullptr;
}


fetch_t *baseFetcher::_next_tuple() {
    if (tryR) {
        tryR = false;
        return next_tuple_R_first(state, fetchStartTime, relR);
    } else {
        tryR = true;
        return next_tuple_S_first(state, fetchStartTime, relS);
    }
}


fetch_t *baseFetcher::next_tuple() {
    if (tryR) {
//        if (state->start_index_S < state->end_index_S)
        tryR = false;
        auto rt = next_tuple_R_first(state, fetchStartTime, relR);
        if (rt != nullptr)
            return rt;
        while (rt == nullptr &&
               !finish()) {
            rt = _next_tuple();
        }
        return rt;
    } else {
//        if (state->start_index_R < state->end_index_R)
        tryR = true;
        auto rt = next_tuple_S_first(state, fetchStartTime, relS);
        if (rt != nullptr)
            return rt;
        while (rt == nullptr &&
               !finish()) {
            rt = _next_tuple();
        }
        return rt;
    }
}
