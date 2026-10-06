# Halo performance and quality

## Performance

**Latest unpublished candidate: 454.59 token/s mean, +44.12%**, measured on a second Strix Halo system with IOMMU off on 2026-10-06. Fresh complete 4K bitwise checks passed before timing, including full payload equality against the retained IOMMU-on results; the source's recorded cache-lifetime check also passed.

| Prepared complete 4K request, same second system | Mean prefill |
|---|---:|
| Original DS4 inference, upstream `8db1d1d` | 315.41 token/s |
| Latest integration candidate | **454.59 token/s (+44.12%)** |

Candidate samples: **454.52 / 454.65**. Each engine used two independent processes, each with three pure-prefill warmups and one measured position-zero request, capacity 4,352, generation disabled. Timing had no trace, profiler or payload dumps. The retained **440 token/s** minimum passed. The same-binary IOMMU-on mean was 429.79; the before/after improvement is **5.77%**, with complete compared payloads bitwise unchanged. The pinned RC has not been replaced. [Qualification and limits](HALO_RELEASE.md#latest-candidate-qualification-2026-10-06) · [All samples and identities](halo/halo2-qualification.json).

## Historical checkpoint results

**Historical checkpoint prefill: 449.03 token/s.** DeepSeek V4 Flash 0731 on AMD Strix Halo (`gfx1151`), 128 GB unified memory. This older record is separate from the latest 454.59 result above.

| Prepared complete 4K request, same-machine test | Prefill |
|---|---:|
| Original DS4 code, upstream `8db1d1d` | 311.24 token/s |
| DS4 Halo, controlled comparison | **447.51 token/s (+43.78%)** |

**Best separate recorded mean: 449.03 token/s.** It has no contemporary upstream timing and is not used to calculate the gain. These are our historical measurements of the original engine and optimized checkpoints; 311.24 is not a number published by upstream. [Measurement evidence](halo/peak-performance.json).

## Prefill across context lengths

![Original DS4 and DS4 Halo, with each benchmark protocol in a separate panel](halo/figures/prefill-context-overview.png)

The first panel starts at **2K context** and shows the historical added-2K intervals. The middle panel shows the latest **315.41 → 454.59** prepared 4K comparison, on the second Halo system with IOMMU off. The final panel shows historical complete empty-context prompts with **fixed 2K chunks**. Dates and protocols are labeled; no line connects them. Original-engine references use pinned upstream `8db1d1d`, measured by us.

| Complete first-use prompt, 2K chunks | Original DS4 code, measured by us | DS4 Halo + indexer |
|---|---:|---:|
| 32K | 272.21 | **391.33** |
| 64K | 251.71 | **361.87** |
| 128K | 218.05 | **319.29** |

Rates are token/s. The original-engine measurements are from September 25; the indexer results are from September 26. They use the same model, prompt length, chunk size and allocation rule, but are not a contemporary alternating A/B campaign. The incremental panel predates the indexer upgrade.

The separate **4K-chunk** campaign reached **400.58 / 354.53 / 288.48** at 32K / 64K / 128K; its original-engine references were **262.88 / 223.18 / 171.70**. The 400.58 result is not a 2K + indexer measurement. [Separate 2K/4K campaign charts](halo/figures/prefill-context-four-variants.png).

[Full-precision data](halo/figures/prefill-context-data.json) · [Plotting method](halo/figures/README.md) · [SVG](halo/figures/prefill-context-overview.svg) · [PDF](halo/figures/prefill-context-overview.pdf).

## What official DS4 publishes

The [official gfx1151 report](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md) records **231.91** at the initial 2K request, **295.27** for the added 2K interval ending at 4K, and **268.51** for a 2K interval ending at 16K. These include integrated upstream tuning; no unmerged PR figures are used. The report contains no 32K/64K/128K full-prompt timings on Strix Halo. The official repository does contain 32K/64K interval measurements for other hardware in [its performance documentation](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/docs/PERFORMANCE.md).

These published figures are kept separate from our measurements. They do not support a percentage comparison with our prepared 447.51/449.03 results or our complete long-prompt rates. The percentage above comes only from the matched historical 4K comparison. [Provenance audit](halo/figures/PROVENANCE_AUDIT.md).

## Quality

**The latest candidate matches fresh reference token IDs, full FP32 logits and complete states bitwise in the tested 4K cases**, including generation and the short-continuation/cache-reuse sequence. Model weights and quantization are preserved. The fresh32K/64K/128K, 223 incremental payload and 31 snapshot comparisons belong to historical checkpoints; that wider matrix has not been rerun on this candidate. [Verification evidence](HALO_EVIDENCE.md).

## What changes

Halo adds optimized ROCm prefill paths for routed MoE, attention, projections and the resident-key indexer. Enable them with `DS4_ROCM_HALO_PREFILL=1`; unsupported shapes retain native dispatch. [Implementation and supported configurations](HALO.md).

The context charts and 447.51/449.03 figures remain accepted historical measurements. The new 454.59 candidate result has separate preparation, source and machine identities and does not replace those records. Final acceptance of the actual installer package remains separate. [Release record](HALO_RELEASE.md).
