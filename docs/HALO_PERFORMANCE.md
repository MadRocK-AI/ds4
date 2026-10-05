# Halo performance and quality

DeepSeek V4 Flash 0731 on AMD Strix Halo (`gfx1151`), 128 GB unified memory. Prefill at the **4K context frontier, in 2048-token increments**:

| Engine | Prefill | Increase |
|---|---:|---:|
| Official DS4 | 295.27 token/s | Reference |
| DS4 on Halo | **413.18 token/s** | **+39.93%** |

[Official DS4 result](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md) - [Halo measurement records](halo/published-performance.json).

The DS4 value is the latest pure-prefill 4K result in its official main-branch report, with the default gfx1151 path. The percentage compares published throughput from the respective setups, rather than a controlled A/B.

Our separate resident fresh4096 record is **447.51 token/s**; it is a different workload and is not used in the percentage above.

## Quality

**Bitwise logits, complete serialized state and token IDs match the reference in the verified cases.** The model weights and quantization are preserved. Checks include fresh32K/64K/128K prompts, 223 incremental payload comparisons and 31 snapshot restorations. [Verification evidence](HALO_EVIDENCE.md).

## What changes

Halo adds optimized ROCm prefill paths for routed MoE, attention, projections and the resident-key indexer. Enable them with `DS4_ROCM_HALO_PREFILL=1`; unsupported shapes retain native dispatch. [Implementation and supported configurations](HALO.md).

The measurements are the accepted historical results. The integrated release's ROCm build/link passed in WSL. [Release record](HALO_RELEASE.md). Exact values and provenance remain in the linked evidence files.
