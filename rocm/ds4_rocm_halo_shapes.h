#ifndef DS4_ROCM_HALO_SHAPES_H
#define DS4_ROCM_HALO_SHAPES_H
#include <stdint.h>

/* The model-qualified selector covers later 2048-token chunks only. Use
 * 64-bit arithmetic so an unsupported position cannot wrap into this domain. */
static inline int ds4_rocm_halo_indexer_shape(uint32_t n_comp,
        uint32_t n_tokens, uint32_t pos0, uint32_t n_head,
        uint32_t head_dim, uint32_t ratio, uint32_t causal) {
    return n_tokens == 2048u && n_head == 64u && head_dim == 128u &&
        ratio == 4u && causal == 1u && n_comp >= 1024u &&
        n_comp <= 32768u && n_comp % 512u == 0u &&
        (uint64_t)pos0 + n_tokens == (uint64_t)n_comp * ratio;
}

static inline int ds4_rocm_halo_q8_shape(uint64_t rows, uint64_t k, uint64_t n) {
    return (rows == 2048u || rows == 4096u) &&
        ((k == 1024u && n == 32768u) || (k == 4096u && n == 2048u));
}
static inline int ds4_rocm_halo_qa_shape(uint64_t rows, uint64_t k, uint64_t n) {
    return rows == 4096u && k == 4096u && n == 1024u;
}
#endif
