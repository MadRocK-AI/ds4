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
static inline int ds4_rocm_halo_static_query_shape(uint32_t rows,
        uint32_t n_comp, uint32_t window, uint32_t ratio,
        uint32_t n_head, uint32_t head_dim) {
    return window == 128u && n_head == 64u && head_dim == 512u &&
        ((rows == 2048u && ((n_comp == 0u && ratio == 1u) ||
          (n_comp == 16u && ratio == 128u) || (n_comp == 512u && ratio == 4u))) ||
         (rows == 4096u && ((n_comp == 0u && ratio == 1u) ||
          (n_comp == 32u && ratio == 128u))));
}
static inline int ds4_rocm_halo_hc_shape(uint64_t rows, uint64_t k, uint64_t n) {
    return (rows == 2048u || rows == 4096u) && k == 16384u && n == 24u;
}
static inline int ds4_rocm_halo_direct_qk_shape(uint32_t rows, uint32_t pos0,
        uint32_t n_raw, uint32_t raw_cap, uint32_t raw_start, uint32_t n_comp,
        uint32_t top_k, uint32_t window, uint32_t ratio, uint32_t heads,
        uint32_t dim, int indexed) {
    const uint64_t end = (uint64_t)pos0 + rows;
    const uint64_t nr = rows + (pos0 < 128u ? pos0 : 128u);
    if ((rows != 2048u && rows != 4096u) || end > 131072u || window != 128u ||
        heads != 64u || dim != 512u || n_raw != nr || raw_cap < nr ||
        raw_cap > 262144u || raw_start >= raw_cap ||
        raw_start != (end - nr) % raw_cap) return 0;
    return indexed ? top_k == 512u && ratio == 4u && n_comp == end / 4u && n_comp > 512u :
        pos0 > 0u && top_k == 0u && ((n_comp == 0u && ratio <= 1u) ||
          (ratio == 128u && n_comp == end / 128u));
}
#endif
