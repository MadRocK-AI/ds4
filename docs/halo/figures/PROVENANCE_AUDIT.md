# Benchmark provenance audit — 2026-10-05

The numerical records are real. The former combined overview was misleading because it connected different workloads and preparation regimes. It has been replaced by three independent protocol panels; its old appearance is not a valid comparative scaling curve.

## Original September 26 chart

The orange curves in `prefill-context-indexer-update.png` were labelled “public reference”. They mean **our measurements of the public DS4 engine**, upstream `8db1d1d155cb0400a86a86b9c62d0defb3a6148b`, not values copied from an official published benchmark. Original inputs are preserved in [the fresh campaign records](inputs/01-final-fresh-series.json).

| Context | Original engine, 2K chunks | Original engine, 4K chunks |
|---|---:|---:|
| 32K | 272.21 | 262.88 |
| 64K | 251.71 | 223.18 |
| 128K | 218.05 | 171.70 |

For example, `final32-2048-P` processed 32,768 tokens in 120.38 seconds, giving 272.21 token/s. The local campaign's `REPRODUCE.md` identifies `long-P` as the clean upstream reference and requires equal actual chunks and allocations for P/C comparisons. The benchmark adds host timing/readback instrumentation; the original reference inference code is unchanged.

The updated 2K + indexer curve is **391.33 / 361.87 / 319.29**. The previous 4K curve is **400.58 / 354.53 / 288.48**. Each is a real full-prompt series. Indexer measurements belong to the following day's campaign and retain the earlier original-engine reference. This is a historical throughput comparison; it is not a new contemporary alternating A/B against the original engine. Bitwise verification compares matching chunk sizes; it does not assert identity across 2K and 4K chunks.

Selecting 400.58 at 32K and 361.87/319.29 at 64K/128K is an explicitly changing-configuration best-result selection, not a fixed-configuration curve. The original four-curve graphic shows the configurations separately. Its 2K/4K labels describe **chunk size**, while its context axis starts at **32K**, not 2K.

## Official repository audit

All 3,447 tracked files of `antirez/ds4` main at `0aaea5a238fb41a35106a551e73c8409dfb751ac` were inspected, including all decodable text, benchmark CSVs and hardware documentation. Unmerged PRs were excluded.

- [Official gfx1151 report](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md): initial 2K **231.91**, a later 4K-frontier interval **295.27**, and 16K-frontier interval **268.51**. These are archived observations under documented software profiles, not one contemporaneous context sweep. No matching Strix Halo complete 32K/64K/128K rates were found in main.
- [Official performance documentation](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/docs/PERFORMANCE.md): 32K and 64K measurements exist for Mac and DGX Spark, with different hardware. These cannot populate a Halo comparison. Its benchmark explicitly counts newly added intervals.
- The original chart's six upstream-reference rates match our preserved run records. Their full-precision strings are absent from the official main snapshot.

Absence is scoped to this audited commit and the matching hardware/workload. It is not a claim that the official repository has no long-context measurements of any kind.

## Peak and quality scope

The historical prepared complete-4K comparison is **311.24 → 447.51 token/s (+43.78%)**. **449.03** is a separate best recorded mean with no contemporary upstream retiming. Neither is comparable to the official published 295.27 incremental rate. [Prepared benchmark attribution](../baseline-attribution.json).

The October 6 overview update uses the independently qualified current prepared-4K comparison **315.41 → 454.59 (+44.12%)**, IOMMU off, on the second Halo system. Schema 4 binds [the current source/sample record](../halo2-qualification.json) separately and retains the historical prepared block. The surrounding context curves remain historical; their data and numerical claims are not replaced by the new 4K point.

All claims describe recorded checkpoints and tested numerical cases. They are not new speed or numerical measurements of the integrated release binary. [Quality evidence](../../HALO_EVIDENCE.md). No benchmark was rerun and no remote machine was contacted for this audit.
