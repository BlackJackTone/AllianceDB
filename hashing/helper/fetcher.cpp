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


fetch_t *PMJ_HS_NP_Fetcher::next_tuple() {
    milliseconds min_gap = (milliseconds) INT32_MAX;
    tuple_t *readR = nullptr;
    tuple_t *readS = nullptr;

    //try to read R first.
    if (state->start_index_R < state->end_index_R) {
        state->fetch.fat_tuple_size = min((int) progressive_step_tupleR,
                                          (state->end_index_R - state->start_index_R));//left-over..
        readR = &relR->tuples[state->start_index_R];
        //check the timestamp whether the tuple is ``ready" to be fetched.
        std::chrono::milliseconds timestamp
                = relR->payload->ts[readR[state->fetch.fat_tuple_size - 1].payloadID];
        auto timegap = RtimeGap(&timestamp);
        if (timegap.count() <= 0) {//if it's negative means our fetch is too slow.
            state->fetch.fat_tuple = readR;
            state->start_index_R += state->fetch.fat_tuple_size;
            state->fetch.ISTuple_R = true;
            return &(state->fetch);
        } else {
            min_gap = timegap;
        }
    }
    //try to read S then.
    if (state->start_index_S < state->end_index_S) {
        state->fetch.fat_tuple_size = min((int) progressive_step_tupleS,
                                          (state->end_index_S - state->start_index_S));//left-over..
        readS = &relS->tuples[state->start_index_S];
        //check the timestamp whether the tuple is ``ready" to be fetched.
        std::chrono::milliseconds timestamp
                = relR->payload->ts[readS[state->fetch.fat_tuple_size - 1].payloadID];
        auto timegap = RtimeGap(&timestamp);
        if (timegap.count() <= 0) {//if it's negative means our fetch is too slow.
            state->fetch.fat_tuple = readS;
            state->fetch.ISTuple_R = false;
            state->start_index_S += state->fetch.fat_tuple_size;
            return &(state->fetch);
        } else {
            if (min_gap > timegap) {//S is nearest.
                min_gap = timegap;
                DEBUGMSG("Thread %d is going to sleep for %d before get S", tid, min_gap)
                this_thread::sleep_for(min_gap);
                state->fetch.fat_tuple = readS;
                state->fetch.ISTuple_R = false;
                state->start_index_S += state->fetch.fat_tuple_size;
                return &(state->fetch);
            } else if (readR != nullptr) {//R is nearest.
                DEBUGMSG("Thread %d is going to sleep for %d before get R", tid, min_gap)
                this_thread::sleep_for(min_gap);
                state->fetch.fat_tuple = readR;
                state->fetch.ISTuple_R = true;
                state->start_index_R += state->fetch.fat_tuple_size;
                return &(state->fetch);
            }
        }
    }
    return nullptr;
}


fetch_t *baseFetcher::next_tuple() {
    milliseconds min_gap = (milliseconds) INT32_MAX;
    tuple_t *readR = nullptr;
    tuple_t *readS = nullptr;

    //try to read R first.
    if (state->start_index_R < state->end_index_R) {
        readR = &relR->tuples[state->start_index_R];
        //check the timestamp whether the tuple is ``ready" to be fetched.
        std::chrono::milliseconds timestamp = relR->payload->ts[readR->payloadID];
        auto timegap = RtimeGap(&timestamp);
        if (timegap.count() <= 0) {//if it's negative means our fetch is too slow.
            state->fetch.tuple = readR;
            state->fetch.ISTuple_R = true;
            state->start_index_R++;
            return &(state->fetch);
        } else {
            min_gap = timegap;
        }
    }
    //try to read S then.
    if (state->start_index_S < state->end_index_S) {
        readS = &relS->tuples[state->start_index_S];
        //check the timestamp whether the tuple is ``ready" to be fetched.
        std::chrono::milliseconds timestamp = relS->payload->ts[readS->payloadID];
        auto timegap = StimeGap(&timestamp);
        if (timegap.count() <= 0) {//if it's negative means our fetch is too slow.
            state->fetch.tuple = readS;
            state->fetch.ISTuple_R = false;
            state->start_index_S++;
            return &(state->fetch);
        } else {  //return the nearest tuple.
            if (min_gap > timegap) {//S is nearest.
                min_gap = timegap;
                DEBUGMSG("Thread %d is going to sleep for %d before get S", tid, min_gap)
                this_thread::sleep_for(min_gap);
                state->fetch.tuple = readS;
                state->fetch.ISTuple_R = false;
                state->start_index_S++;
                return &(state->fetch);
            } else if (readR != nullptr) {//R is nearest.
                DEBUGMSG("Thread %d is going to sleep for %d before get R", tid, min_gap)
                this_thread::sleep_for(min_gap);
                state->fetch.tuple = readR;
                state->fetch.ISTuple_R = true;
                state->start_index_R++;
                return &(state->fetch);
            }
        }
    }
    return nullptr;
}
