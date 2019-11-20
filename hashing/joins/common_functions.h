//
// Created by Shuhao Zhang on 26/10/19.
//

#ifndef ALLIANCEDB_COMMON_FUNCTIONS_H
#define ALLIANCEDB_COMMON_FUNCTIONS_H

#include <iostream>
#include <list>
#include <mutex>
#include "npj_types.h"

#ifndef PTHREAD_BARRIER_SERIAL_THREAD
#define PTHREAD_BARRIER_SERIAL_THREAD 1
#endif

#ifndef BARRIER_ARRIVE
/** barrier wait macro */
#define BARRIER_ARRIVE(B, RV)                            \
    RV = pthread_barrier_wait(B);                       \
    if(RV !=0 && RV != PTHREAD_BARRIER_SERIAL_THREAD){  \
        printf("Couldn't wait on barrier\n");           \
        exit(EXIT_FAILURE);                             \
    }
#endif

#ifdef JOIN_RESULT_MATERIALIZE
#include "tuple_buffer.h"       /* for materialization */
#endif

#ifndef HASH
#define HASH(X, MASK, SKIP) (((X) & MASK) >> SKIP)
#endif

#define DEBUG

/** Debug msg logging method */
#ifdef DEBUG
#define DEBUGMSG(MSG, ...)                                                        \
    {                                                               \
        fprintf(stdout, "[DEBUG] @ %s:%d " MSG, __FILE__, __LINE__, ## __VA_ARGS__);    \
          fprintf(stdout, "\n");                                                        \
    }
#else
#define DEBUGMSG(MSG, ...)
#endif

#define MSG(MSG, ...)                                                                   \
    { fprintf(stdout, "[INFO] @ %s:%d " MSG , __FILE__, __LINE__, ## __VA_ARGS__);      \
        fprintf(stdout, "\n");                                                          \
    }

#define EAGER
#define MEASURE
#define expected_results 1280000.0

struct t_window {
    std::list<intkey_t> R_Window;
    std::list<intkey_t> S_Window;
    std::mutex mutex;
};
extern t_window window0;
extern t_window window1;

std::string
print_window(const std::list<intkey_t> &list);

/**
 * Allocates a hashtable of NUM_BUCKETS and inits everything to 0.
 *
 * @param ht pointer to a hashtable_t pointer
 */
void allocate_hashtable(hashtable_t **ppht, uint32_t nbuckets);

/**
 * Single-thread hashtable build method, ht is pre-allocated.
 *
 * @param ht hastable to be built
 * @param rel the build relation
 */
void
build_hashtable_st(hashtable_t *ht, relation_t *rel);

/**
 * Probes the hashtable for the given outer relation, returns num results.
 * This probing method is used for both single and multi-threaded version.
 *
 * @param ht hashtable to be probed
 * @param rel the probing outer relation
 * @param output chained tuple buffer to write join results, i.e. rid pairs.
 *
 * @return number of matching tuples
 */
int64_t
probe_hashtable(hashtable_t *ht, relation_t *rel, void *output, uint64_t progressivetimer[]);


/**
 * Remove the effect of tuple from hashtable. (reverse of build hashtable)
 * @param ht
 * @param tuple
 * @param hashmask
 * @param skipbits
 */
void debuild_hashtable_single(const hashtable_t *ht, const tuple_t *tuple,
                              const uint32_t hashmask,
                              const uint32_t skipbits);


void
build_hashtable_single(const hashtable_t *ht, const tuple_t *, const uint32_t hashmask,
                       const uint32_t skipbits);

void
build_hashtable_single(const hashtable_t *ht, const relation_t *rel, uint32_t i, const uint32_t hashmask,
                       const uint32_t skipbits);

int64_t proble_hashtable_single_measure(const hashtable_t *ht, const tuple_t *,
                                        const uint32_t hashmask, const uint32_t skipbits, int64_t *matches,
                                        uint64_t progressivetimer[]);

int64_t proble_hashtable_single_measure(const hashtable_t *ht, const relation_t *rel, uint32_t index_rel,
                                        const uint32_t hashmask, const uint32_t skipbits, int64_t *matches,
                                        uint64_t progressivetimer[]);

int64_t proble_hashtable_single(const hashtable_t *ht, const tuple_t *,
                                const uint32_t hashmask, const uint32_t skipbits, int64_t *matches);

int64_t proble_hashtable_single(const hashtable_t *ht, const relation_t *rel, uint32_t index_rel,
                                const uint32_t hashmask, const uint32_t skipbits, int64_t *matches);


/**
 * Multi-thread hashtable build method, ht is pre-allocated.
 * Writes to buckets are synchronized via latches.
 *
 * @param ht hastable to be built
 * @param rel the build relationO
 * @param overflowbuf pre-allocated chunk of buckets for overflow use.
 */
void
build_hashtable_mt(hashtable_t *ht, relation_t *rel,
                   bucket_buffer_t **overflowbuf);

/**
 * Releases memory allocated for the hashtable.
 *
 * @param ht pointer to hashtable
 */
void destroy_hashtable(hashtable_t *ht);

/** De-allocates all the bucket_buffer_t */
void
free_bucket_buffer(bucket_buffer_t *buf);


std::string print_relation(tuple_t *tuple, int length);

#endif //ALLIANCEDB_COMMON_FUNCTIONS_H