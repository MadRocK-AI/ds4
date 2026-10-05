# Halo performance and quality

## Performance

**Up to 449.03 token/s prefill, with bitwise-preserved logits and state in verified cases.** DeepSeek V4 Flash 0731 on AMD Strix Halo (`gfx1151`), 128 GB unified memory.

| Result | Prefill |
|---|---:|
| DS4 Halo best recorded mean, resident 4K | **449.03 token/s** |
| DS4 Halo controlled resident 4K test | **447.51 token/s** |
| DS4 official published 4K interval | 295.27 token/s |

The official value comes from [DS4 main](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md). It measures a 2K increment at the 4K frontier; the Halo peak measures a prepared complete 4K request. These published figures use different protocols. [The archived matched A/B record](halo/peak-performance.json) separately documents the **+43.78%** internal gain against original DS4 code on the same machine.

## Prefill across context lengths

![DS4 Halo versus official DS4, starting at 2K](halo/figures/prefill-context-overview.png)

**DS4 Halo** is this repository; **DS4 official** uses only the gfx1151 results published in [antirez/ds4 main](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md), including integrated upstream tuning. It uses no unmerged PR or local rebuilt timing. The official report supplies 2K, 4K and 16K values; its curve stops at 16K.

| Context | DS4 official, published | DS4 Halo, recorded | Halo setting |
|---|---:|---:|---|
| 2K | 231.91 | **354.23** | Initial 2K request |
| 4K | 295.27 | **449.03** | Prepared 4K; controlled result **447.51** |
| 16K | 268.51 | — | No matching full-prompt point in this dataset |
| 32K | — | **400.58** | 4K chunks |
| 64K | — | **361.87** | 2K + indexer |
| 128K | — | **319.29** | 2K + indexer |

Rates are token/s. Official values measure **2K increments**; Halo points use an initial 2K request, prepared resident 4K and complete first-use long prompts. Both series summarize archived campaigns, with the protocols shown. Connecting lines do not establish a controlled speedup. Missing values remain unfilled.

**Fixed 2K + indexer:** 391.33 / 361.87 / 319.29 at 32K / 64K / 128K. The best 32K result, 400.58, belongs to 4K chunks.

[Official data and source binding](halo/figures/official-ds4-published-context.json) · [Overview source records](halo/figures/prefill-context-overview.json) · [Sources and plotting method](halo/figures/README.md) · [SVG](halo/figures/prefill-context-overview.svg) · [PDF](halo/figures/prefill-context-overview.pdf).

[Supplementary internal controls and indexer measurements](halo/figures/README.md) retain the matched local-original-code comparisons and the earlier incremental series separately from the official published reference.

## Quality

**Full FP32 logits, complete serialized state and token IDs are bitwise identical to the reference in the verified cases.** Model weights and quantization are preserved. Coverage includes fresh32K/64K/128K prompts, 223 incremental payload comparisons and 31 snapshot restorations. [Verification evidence](HALO_EVIDENCE.md).

## What changes

Halo adds optimized ROCm prefill paths for routed MoE, attention, projections and the resident-key indexer. Enable them with `DS4_ROCM_HALO_PREFILL=1`; unsupported shapes retain native dispatch. [Implementation and supported configurations](HALO.md).

Figures are the accepted historical measurements; the integrated release's ROCm build/link passed in WSL. [Release record](HALO_RELEASE.md). Exact measurements and benchmark conditions remain in the linked evidence files.
