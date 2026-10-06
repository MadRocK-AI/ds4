# DS4 for AMD Strix Halo

An opt-in **single-device ROCm prefill fork** of [antirez/ds4](https://github.com/antirez/ds4), targeting Ryzen AI Max+ 395 / Radeon 8060S (`gfx1151`) with 128 GB unified memory. The Halo work accelerates routed MoE, attention, projections and indexer scoring while preserving **bitwise logits and complete state in the documented test cases**.

**DS4 Strix Halo rc.2: 454.59 token/s prepared prefill, +44.12% over original DS4, with bitwise-identical complete payloads in the tested cases.** The rc.2 source passed the prepared performance gate and actual installer, complete-payload numerical and launcher/API checks on a second Strix Halo system with IOMMU off. [Installed release evidence](docs/halo/distribution-acceptance.json). [Validation scope](docs/HALO_RELEASE.md).

The source base is upstream [`8db1d1d`](https://github.com/antirez/ds4/commit/8db1d1d155cb0400a86a86b9c62d0defb3a6148b), which already contains gfx1151 tuning. This repository adds the compatible Halo prefill chain to the normal ROCm source build. The pinned setup/verification companion is [ds4-on-halo](https://github.com/MadRocK-AI/ds4-on-halo).

## What this fork adds

| Area | Additional Halo work |
|---|---|
| Routed MoE | S9 IQ2 gate/up producers, fused intermediate work and shape-specific Q2 down paths |
| Attention | Static query registers, direct QK, half-KV views, inverse RoPE and grouped packing |
| Projections | Cooperative Q8, shared-GU bridge, cached/uncached output-A, source-built output-B assembly and shared-down |
| Indexer | Resident-key scoring for admitted 2048-row causal geometry |
| Reproducibility | Source/component hashes, historical numerical and timing records, an exact-pin build/benchmark companion |

[Detailed dispatch domains, memory ownership and native fallbacks](docs/HALO.md). Added paths target DeepSeek V4 Flash 0731 and checked 2048/4096 prefill chunks. Native dispatch remains the default; enable Halo with `DS4_ROCM_HALO_PREFILL=1`. Other backends and upstream functionality retain their existing implementation. R9700, NPU, SSD streaming, GLM, vision and distributed execution are outside these added Halo paths.

## Performance

**Official DS4 published results:** 231.91 token/s at 2K, 292.86 for its warm 4K result and 295.27 in the later 2K→4K interval. [Official Strix Halo report](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md). Those are different workloads/SDK conditions. The **315.41** control below is our measurement of pinned original DS4 on the same machine and protocol as Halo; **+44.12%** refers to that matched comparison.

**Qualified prefill chain, 2026-10-06: 454.59 token/s mean, +44.12% against the original DS4 code measured on the same second Strix Halo system.** Complete position-zero 4K requests, capacity 4,352, IOMMU off, no generation; two independent processes per engine, each with three pure-prefill warmups and one measured request. Timing used no profiler, trace or payload dumps. [All samples and identities](docs/halo/halo2-qualification.json).

| Prepared complete 4K request, second Strix Halo system | Mean prefill |
|---|---:|
| Original DS4 inference, upstream `8db1d1d` | 315.41 token/s |
| DS4 Halo prefill chain | **454.59 token/s (+44.12%)** |

Candidate samples: **454.52 and 454.65 token/s**; the retained 440 minimum passed. Turning IOMMU off improved the same candidate's measured mean by **5.77%** from 429.79, with all compared complete on/off payloads unchanged bitwise. This is a before/after policy comparison. The cleaned rc.2 installer-built executable also matched all six complete reference payloads and passed its launcher/API smoke.

Historical 447.51/449.03 and long-context measurements remain separately documented in [HALO_PERFORMANCE.md](docs/HALO_PERFORMANCE.md).

![Original DS4 315.41 vs DS4 Halo 454.59 token/s: prepared 4K prefill](docs/halo/figures/prefill-4k-release.png)

[Context overview, starting at 2K](docs/halo/figures/prefill-context-overview.png).

The first panel starts at **2K context**. The middle panel shows the latest **315.41 → 454.59** prepared complete-4K comparison; the surrounding historical panels retain incremental 2K additions and first-use long prompts with fixed 2K chunks. Dates, systems and protocols remain distinct. Original DS4 is pinned to `8db1d1d`; these are our measurements, not timings published for today's upstream main. [Results and provenance](docs/HALO_PERFORMANCE.md).

## Quality

**The latest candidate matched fresh original-DS4 token IDs, full FP32 logits and complete serialized state bitwise in the tested 4K cases**, including after 16 generated tokens. Its 4K → 32-token continuation → fresh 4K cache lifetime check also passed. These results apply to the recorded source and configuration. Historical coverage includes fresh32K/64K/128K prompts, 223 incremental payload comparisons and 31 snapshot restorations; that wider matrix has not been rerun on this candidate. [Verification evidence](docs/HALO_EVIDENCE.md).

## Start Here

Clone the repository and build with a complete compatible Linux ROCm SDK:

```sh
git clone https://github.com/MadRocK-AI/ds4.git
cd ds4
make rocm HIPCC=/path/to/existing/hipcc ROCM_ARCH=gfx1151 -j2
DS4_ROCM_HALO_PREFILL=1 ./ds4 --rocm -m /path/to/compatible-0731.gguf
```

Required SDK components include HIP, hipBLAS, hipBLASLt, rocBLAS, hipCUB, rocPRIM and rocWMMA2.2.1. See [the verified build recipe and dependency identities](docs/HALO_RELEASE.md#build-dependencies), including the split core/math/header layout. Halo selects only admitted operator shapes; short prompts and unsupported configurations use native paths. The [companion](https://github.com/MadRocK-AI/ds4-on-halo) supplies exact source-pin bootstrap, build records, timing configuration and full payload comparisons.

## Release state and documentation

Normal gfx1151 build/link passed for all five targets in WSL and for both fresh candidate/reference builds on the second Halo system. The latest candidate passed the recorded 4K numerical, cache-lifetime and prepared performance gates; complete on/off payloads also matched. The actual rc.2 installer and API passed: 14- and 4,214-token prompts, eight generated tokens each, with 4K chunks. The older rc.1 smoke is retained separately. The companion pins the exact cleaned source verified by the real rc.2 installation. The installed binary has its own recorded hashes; no additional performance campaign is claimed for its diagnostic-only cleanup. [Release acceptance and build record](docs/HALO_RELEASE.md).

- [Halo differences, measurements and bitwise checks](docs/HALO_PERFORMANCE.md)
- [Operator admission, fallback and memory contracts](docs/HALO.md)
- [Historical evidence and numerical hashes](docs/HALO_EVIDENCE.md)
- [Reproduction protocol](docs/HALO_QUALIFICATION.md)
- [Source provenance and third-party credits](docs/HALO_THIRD_PARTY.md)
- [Retained upstream manual](README_UPSTREAM.md): models, CLI, server, APIs, other platforms and original project acknowledgements

DwarfStar/DS4 was created by Salvatore Sanfilippo and upstream contributors. This fork builds on that engine and the llama.cpp/GGML work it credits. Original licenses and copyrights remain in [LICENSE](LICENSE); ported components have their own recorded provenance.
