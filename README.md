# DS4 for AMD Strix Halo

An opt-in **single-device ROCm prefill fork** of [antirez/ds4](https://github.com/antirez/ds4), targeting Ryzen AI Max+ 395 / Radeon 8060S (`gfx1151`) with 128 GB unified memory. The Halo work accelerates routed MoE, attention, projections and indexer scoring while preserving **bitwise logits and complete state on the documented historical test cases**.

The source base is upstream [`8db1d1d`](https://github.com/antirez/ds4/commit/8db1d1d155cb0400a86a86b9c62d0defb3a6148b), which already contains gfx1151 tuning. This repository adds the compatible Halo prefill chain to the normal ROCm source build. The pinned setup/verification companion is [ds4-on-halo](https://github.com/msala9/ds4-on-halo). Both repositories are currently private under msala9; their planned official home is madrock.

## What this fork adds

| Area | Additional Halo work |
|---|---|
| Routed MoE | S9 IQ2 gate/up producers, fused intermediate work and shape-specific Q2 down paths |
| Attention | Static query registers, direct QK, half-KV views, inverse RoPE and grouped packing |
| Projections | Cooperative Q8, shared-GU bridge, cached/uncached output-A, source-built output-B assembly and shared-down |
| Indexer | Resident-key scoring for admitted 2048-row causal geometry |
| Reproducibility | Source/component hashes, historical numerical and timing records, an exact-pin build/benchmark companion |

[Detailed dispatch domains, memory ownership and native fallbacks](docs/HALO.md). Added paths target DeepSeek V4 Flash 0731 and checked 2048/4096 prefill chunks. Native dispatch remains the default; enable Halo with `DS4_ROCM_HALO_PREFILL=1`. Other backends and upstream functionality retain their existing implementation. R9700, NPU, SSD streaming, GLM, vision and distributed execution are outside these added Halo paths.

## Historical performance

**Resident fresh4096: 447.506868 token/s.** This is the frozen controlled structural9 result. Its contemporary local upstream8db control measured 311.241615 token/s, giving **+43.781181% in that specific comparison**. That control uses resident prepared weights, warmup, core10/HIP7.15 and a host-only resident benchmark loop. It is not the original DS4 performance reference or an upstream-published result.

The upstream report separately lists **187.26 token/s for Clean DS4**, **292.86 for its tuned gfx1151 path**, and **294.38 in a later stock-launch follow-up**, with 2048-token increments. Those workloads and software conditions differ; we do not divide the fresh4096 result by them to claim an overall speedup. [Upstream results at the pinned base](https://github.com/antirez/ds4/blob/8db1d1d155cb0400a86a86b9c62d0defb3a6148b/speed-bench/gfx1151-prefill-results.md).

Historical long-context results against the local rebuilt upstream8db control, with each pair using the same **2048 chunk**, prompt and capacity:

| Fresh prompt | Local upstream8db | Optimized composition | Prefill throughput gain |
|---|---:|---:|---:|
| 32,768 tokens | 272.21 token/s | 373.87 token/s | +37.34% |
| 65,536 tokens | 251.71 token/s | 335.66 token/s | +33.35% |
| 131,072 tokens | 218.05 token/s | 278.58 token/s | +27.76% |

The matching 4096-chunk results, each arm's fastest configuration, later indexer gains and exact measurement boundaries are in [Halo performance and baseline attribution](docs/HALO_PERFORMANCE.md). These are separate historical campaigns; their gains are not added. No ordinary-decode acceleration is claimed.

## Bitwise preservation

Historical qualification checks full FP32 logits, prompt/generated token IDs and serialized prefill/decode state, including raw/compressed KV and indexer/compressor state. Coverage includes six fresh32K/64K/128K cases with 2048/4096 chunks and a separate incremental diagnostic with **223 payload comparisons and 31 snapshot restorations**. Structural9 also retains independent code/Italian prompt checks and 128 teacher-forced tokens.

Equality applies to the tested inputs, geometry, chunk, capacity and runtime identities. It does not assert equality across chunk sizes or to an unquantized model. [Test coverage and quality boundaries](docs/HALO_PERFORMANCE.md#what-bitwise-preservation-means-here), [case records and hashes](docs/HALO_EVIDENCE.md).

## Start Here

Clone the private repository using your existing GitHub access and build with a complete compatible Linux ROCm SDK:

```sh
git clone https://github.com/msala9/ds4.git
cd ds4
make rocm HIPCC=/path/to/existing/hipcc ROCM_ARCH=gfx1151 -j2
DS4_ROCM_HALO_PREFILL=1 ./ds4 --rocm -m /path/to/compatible-0731.gguf
```

Required SDK components include HIP, hipBLAS, hipBLASLt, rocBLAS, hipCUB, rocPRIM and rocWMMA2.2.1. See [the verified build recipe and dependency identities](docs/HALO_RELEASE.md#build-dependencies), including the split core/math/header layout. Halo selects only admitted operator shapes; short prompts and unsupported configurations use native paths. The [companion](https://github.com/msala9/ds4-on-halo) supplies exact source-pin bootstrap, build records, timing configuration and full payload comparisons.

## Release state and documentation

Normal gfx1151 ROCm build/link passed in local WSL for **ds4, ds4-server, ds4-bench, ds4-eval and ds4-agent**, with all five ELF relocation checks passing. Numerical/performance acceptance uses the documented historical evidence. The integrated executable has not received a new GPU model/timing run. [Release acceptance and build record](docs/HALO_RELEASE.md).

- [Halo differences, measurements and bitwise checks](docs/HALO_PERFORMANCE.md)
- [Operator admission, fallback and memory contracts](docs/HALO.md)
- [Historical evidence and numerical hashes](docs/HALO_EVIDENCE.md)
- [Reproduction protocol](docs/HALO_QUALIFICATION.md)
- [Source provenance and third-party credits](docs/HALO_THIRD_PARTY.md)
- [Retained upstream manual](README_UPSTREAM.md): models, CLI, server, APIs, other platforms and original project acknowledgements

DwarfStar/DS4 was created by Salvatore Sanfilippo and upstream contributors. This fork builds on that engine and the llama.cpp/GGML work it credits. Original licenses and copyrights remain in [LICENSE](LICENSE); ported components have their own recorded provenance.
