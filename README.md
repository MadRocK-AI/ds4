# DS4 for AMD Strix Halo

An opt-in **single-device ROCm prefill fork** of [antirez/ds4](https://github.com/antirez/ds4), targeting Ryzen AI Max+ 395 / Radeon 8060S (`gfx1151`) with 128 GB unified memory. The Halo work accelerates routed MoE, attention, projections and indexer scoring while preserving **bitwise logits and complete state on the documented historical test cases**.

**Release candidate 0.1.0-rc.1.** The integrated ROCm engine builds and links in WSL. Performance and bitwise results below describe the verified historical checkpoints; the integrated executable has not had a new GPU model run. [Validation scope](docs/HALO_RELEASE.md).

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

**Best recorded prefill: 449.03 token/s.** DeepSeek V4 Flash 0731 on AMD Strix Halo (`gfx1151`), 128 GB unified memory. Bitwise logits and state are preserved in the verified cases.

| Prepared complete 4K request, same-machine test | Prefill |
|---|---:|
| Original DS4 code, upstream `8db1d1d` | 311.24 token/s |
| DS4 Halo, controlled comparison | **447.51 token/s (+43.78%)** |

**Best separate recorded mean: 449.03 token/s.** It has no contemporary upstream timing and is not used to calculate the gain. These are our historical measurements of the original engine and optimized checkpoints; 311.24 is not a number published by upstream. [Measurement evidence](docs/halo/peak-performance.json).

![Original DS4 and DS4 Halo: separate incremental, prepared 4K and full-prompt benchmarks](docs/halo/figures/prefill-context-overview.png)

The first panel starts at **2K context**. Each panel keeps its own benchmark protocol: incremental 2K additions, prepared complete 4K requests, or complete first-use long prompts with fixed 2K chunks. The original engine is explicitly pinned to `8db1d1d`; these are our measurements, not published timings for today's upstream main. [Results, official published figures and provenance](docs/HALO_PERFORMANCE.md).

## Quality

**Full FP32 logits, complete serialized state and token IDs are bitwise identical to the reference in the verified cases.** Model weights and quantization are preserved. Coverage includes fresh32K/64K/128K prompts, 223 incremental payload comparisons and 31 snapshot restorations. [Verification evidence](docs/HALO_EVIDENCE.md).

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

Normal gfx1151 ROCm build/link passed in local WSL for **ds4, ds4-server, ds4-bench, ds4-eval and ds4-agent**, with all five ELF relocation checks passing. Numerical/performance acceptance uses the documented historical evidence. The integrated executable has not received a new GPU model/timing run. [Release acceptance and build record](docs/HALO_RELEASE.md).

- [Halo differences, measurements and bitwise checks](docs/HALO_PERFORMANCE.md)
- [Operator admission, fallback and memory contracts](docs/HALO.md)
- [Historical evidence and numerical hashes](docs/HALO_EVIDENCE.md)
- [Reproduction protocol](docs/HALO_QUALIFICATION.md)
- [Source provenance and third-party credits](docs/HALO_THIRD_PARTY.md)
- [Retained upstream manual](README_UPSTREAM.md): models, CLI, server, APIs, other platforms and original project acknowledgements

DwarfStar/DS4 was created by Salvatore Sanfilippo and upstream contributors. This fork builds on that engine and the llama.cpp/GGML work it credits. Original licenses and copyrights remain in [LICENSE](LICENSE); ported components have their own recorded provenance.
