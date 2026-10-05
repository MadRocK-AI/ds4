# Halo changes, performance and bitwise checks

This fork adds opt-in ROCm prefill paths for single-device AMD Strix Halo (`gfx1151`) to [antirez/ds4 at `8db1d1d`](https://github.com/antirez/ds4/commit/8db1d1d155cb0400a86a86b9c62d0defb3a6148b). That upstream commit already contains gfx1151 tuning. The additional Halo chain covers MoE, attention, projections and the resident-key indexer. [HALO.md](HALO.md) lists the exact dispatch domains and fallbacks; [sources.json](halo/sources.json) binds the ported components to their historical sources.

## Which DS4 reference?

There is no single DS4 throughput independent of workload, software and preparation. These references must remain distinct:

| Reference | Recorded result | Measurement scope |
|---|---:|---|
| Upstream report's **Clean DS4** | 187.26 token/s | ROCm 7.14; warm 4K frontier in a pure-prefill sweep with 2048-token increments |
| Upstream report's **Tuned gfx1151 path** | 292.86 token/s | Same report; tuning already selected by default |
| Upstream report's retained stock launch, later follow-up | 294.38 token/s at 4K; 268.51 at 16K | ROCm 10.0 follow-up; 2K-step pure-prefill sweep |
| Local **upstream8db resident fresh4096 control P** | 311.241615 token/s | Rebuilt upstream `8db1d1d`, core10/HIP7.15; complete fresh4096 requests after cache fill, preparation and warmup; host-only resident harness |

The first three rows come from [the original upstream report](https://github.com/antirez/ds4/blob/8db1d1d155cb0400a86a86b9c62d0defb3a6148b/speed-bench/gfx1151-prefill-results.md). The last row is a local historical control, **not the upstream report's original Clean DS4 baseline**. It also differs from the [upstream benchmark protocol](https://github.com/antirez/ds4/blob/8db1d1d155cb0400a86a86b9c62d0defb3a6148b/speed-bench/README.md), which starts at 2048 and advances by 2048 with 128 generated tokens per frontier. We do not compute a speedup by dividing our fresh4096 result by the published incremental results.

An offline attribution audit on 2026-10-05 checked all **3,092 archived P source hashes against the upstream Git tree**. The build links the upstream inference objects to a benchmark frontend with a host-only resident loop. The two P process environments contain no research preload; their recorded loaded-library maps contain only SDK/system shared libraries. The exact executable, commands, raw times and source/evidence hashes are retained in [baseline-attribution.json](halo/baseline-attribution.json). This audit reads existing evidence and does not rerun a benchmark.

## Historical resident fresh4096 comparison

Ryzen AI Max+ 395, 128 GB unified RAM, `gfx1151`; DeepSeek V4 Flash 0731 IQ2_XXS/Q2_K with the frozen Q8 projection/shared-expert recipe. The same 4096-token Promessi Sposi prefix is used in six independent resident processes, ordered **P/R/C then C/R/P**. Each process performs native cache fill, first preparation and warmup before two timed fresh requests. Prefix reuse and speculation are disabled. Loading, startup and diagnostic readbacks are separate; recurring preparation remains in the complete candidate timer.

| Historical arm | Complete prefill mean (s) | Token/s | Gain versus local P |
|---|---:|---:|---:|
| Local upstream8db control P | 13.160193910 | 311.241615 | Reference |
| Previous optimized C8 checkpoint R | 9.305038587 | 440.191619 | +41.43% |
| Structural9 checkpoint C | 9.152932156 | **447.506868** | **+43.781181%** |

Structural9's marginal gain over C8 is **+1.661833%**, with 152.106430 ms saved per request on average. The four measured C times are 9.145823750, 9.153302905, 9.155847166 and 9.156754805 seconds. A later ordinary profiling bracket reported **449.0337 token/s**; it did not retime P and does not replace this controlled comparison.

These measurements belong to the frozen structural9 checkpoint `9405793e0ad534c747a2036fc2e807554691031ebc68b8a240bf0805779fac71`. They describe the historical compatible chain accepted for release preparation, rather than a new GPU benchmark of the integrated executable. [Release build and acceptance](HALO_RELEASE.md).

## Historical long-context comparisons

The final long-context checkpoint compares the local rebuilt upstream8db control with the optimized composition at the **same prompt length, actual chunk and context capacity**. These are first requests after model initialization with resident weights; first-use preparation and recurring work are included. They have a different timing protocol from the resident fresh4096 table above.

| Fresh tokens | Actual chunk | Local upstream8db token/s | Optimized composition token/s | Throughput gain, same chunk |
|---|---:|---:|---:|---:|
| 32,768 | 2,048 | 272.21 | 373.87 | +37.34% |
| 32,768 | 4,096 | 262.88 | 400.58 | +52.38% |
| 65,536 | 2,048 | 251.71 | 335.66 | +33.35% |
| 65,536 | 4,096 | 223.18 | 354.53 | +58.85% |
| 131,072 | 2,048 | 218.05 | 278.58 | +27.76% |
| 131,072 | 4,096 | 171.70 | 288.48 | +68.01% |

The local upstream control is faster with 2048 chunks in this campaign. Comparing each arm's best measured choice gives **+47.15%, +40.85% and +32.30%** at 32K/64K/128K, respectively (upstream2048 versus composition4096). That is a throughput comparison across configurations; numerical equality was checked against the matching **same-chunk** reference, not across chunk sizes.

The later resident-key indexer improves the preceding optimized chain by **+4.5654%, +7.8356% and +14.4563%** at 32K/64K/128K with 2048 chunks. Its control already contains the earlier optimizations. Those incremental gains are separately recorded in [HALO_EVIDENCE.md](HALO_EVIDENCE.md); they must not be added to the long-context percentages above. [Long-context case records](halo/longcontext-cases.json), [indexer observations](halo/indexer-observations.csv).

## What bitwise preservation means here

The Halo paths retain model weights, quantization, expert routing and the qualified accumulation/rounding boundaries. Correctness evidence compares bytes of the numerical outputs and complete state, rather than relying only on similar text:

- Structural9: frozen independent code and Italian prompts, first and reused fresh4K requests and 128 teacher-forced tokens; matching full frontier/final FP32 logits, score vectors, prompt IDs and serialized prefill/decode states against the operational reference. The contemporary timed frontiers match the frozen reference.
- Long context: all six fresh32K/64K/128K cases with 2048/4096 chunks; identical full frontier and post-decode FP32 logits, serialized state and 16 greedy token IDs against the matching local upstream control. State coverage includes raw/compressed KV, indexer and compressor state.
- Incremental long-context diagnostic: 223 payload comparisons and 31 serialized snapshot restorations, with no prefix replay. A final fresh frontier with zero snapshot bytes does not establish restore coverage.
- Resident-key indexer: exact tested outputs/state against the preceding optimized chain; individual numerical hashes and extents are retained in [historical-numeric-hashes.json](halo/historical-numeric-hashes.json).

Equality is established for these frozen inputs, tensor geometries, capacities and compiler/runtime identities. It is not a claim of equality to an unquantized model, universal equivalence for every input, or new task-evaluation scores. The short decode measurements are regression controls; this release does not claim a useful ordinary-decode acceleration. The upstream report's earlier Clean DS4 comparison has its own tolerance-based quality scope and must not be relabelled as one of these bitwise comparisons.

## Changes included in this fork

| Area | Added Halo paths | Preserved behavior |
|---|---|---|
| Routed MoE | S9 IQ2 gate/up producers and fused intermediate work; shape-specific Q2 down staging/store paths | Original quantizer, top6 routing and qualified arithmetic order; native unsupported-shape/decode fallback |
| Attention | Static query-register paths, direct QK, half-KV views, inverse RoPE and grouped packing | Original RoPE parameters and checked producer/lifetime boundaries |
| Dense projections | Cooperative Q8, shared-GU bridge, cached/uncached output-A, assembled output-B and shared-down | Checked shape/cache admission and original numerical boundaries |
| Indexer | Resident-key scoring for admitted 2048-row causal geometry | No additional tensor scratch; native first-chunk/4K/decode fallback |
| Integration | Normal ROCm source build, source-built assembly module, explicit `DS4_ROCM_HALO_PREFILL=1` switch | Native dispatch remains default; other backends retained |
| Verification companion | Exact source pin, executable/config/model identity, full payload comparisons and snapshot checks | Uses the engine benchmark; keeps timing and diagnostic collection separate |

This fork targets **single-device Halo prefill**. Its added paths do not cover R9700, NPU offload, SSD streaming, GLM, vision or distributed execution. Upstream functionality and licenses are retained, but these areas do not inherit the Halo performance or bitwise claims. [Detailed admission and memory contracts](HALO.md), [source and third-party credits](HALO_THIRD_PARTY.md).
