#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "../rocm/ds4_rocm_halo_shapes.h"
int main(void) {
    for (uint32_t nc = 1024; nc <= 32768; nc += 512) {
        uint32_t pos = nc * 4 - 2048;
        assert(ds4_rocm_halo_indexer_shape(nc, 2048, pos, 64, 128, 4, 1));
        assert(!ds4_rocm_halo_indexer_shape(nc, 4096, pos, 64, 128, 4, 1));
        assert(!ds4_rocm_halo_indexer_shape(nc, 2048, pos+1, 64, 128, 4, 1));
        assert(!ds4_rocm_halo_indexer_shape(nc+1, 2048, pos, 64, 128, 4, 1));
    }
    assert(!ds4_rocm_halo_indexer_shape(512, 2048, 0, 64, 128, 4, 1));
    assert(!ds4_rocm_halo_indexer_shape(33280, 2048, 130048, 64, 128, 4, 1));
    assert(!ds4_rocm_halo_indexer_shape(1024, 1, 4095, 64, 128, 4, 1));
    assert(!ds4_rocm_halo_indexer_shape(1024, 2048, UINT32_MAX-2047, 64, 128, 4, 1));
    assert(!ds4_rocm_halo_indexer_shape(1024, 2048, 2048, 32, 128, 4, 1));
    assert(!ds4_rocm_halo_indexer_shape(1024, 2048, 2048, 64, 64, 4, 1));
    assert(!ds4_rocm_halo_indexer_shape(1024, 2048, 2048, 64, 128, 0, 1));
    assert(!ds4_rocm_halo_indexer_shape(1024, 2048, 2048, 64, 128, 4, 0));
    puts("Halo production admission: PASS (CPU only)");
    return 0;
}
