# Halo prefill implementation

This fork adds the Halo prefill chain to the normal ROCm backend and preserves upstream history from `8db1d1d155cb0400a86a86b9c62d0defb3a6148b`. Historical checkpoints and the qualified prefill chain have separate evidence. The candidate passed recorded 4K bitwise and cache-lifetime gates and reached **454.59 token/s** prepared prefill on a second Halo system with IOMMU off, passing the unchanged 440 minimum. Complete compared on/off payloads remained bitwise identical. The rc.2 cleaned source also passed actual installer-built numerical and launcher/API acceptance. See [qualification status](HALO_RELEASE.md).

Use the normal build with an existing complete ROCm installation:

```sh
make rocm HIPCC=/path/to/existing/hipcc ROCM_ARCH=gfx1151 -j2
DS4_ROCM_HALO_PREFILL=1 ./ds4-bench --rocm ...
```

`DS4_ROCM_HALO_PREFILL=1` explicitly admits the candidate. The default and `0` use native selectors. Other backends retain their build and arithmetic. The normal build needs HIP, hipBLAS, hipBLASLt, rocBLAS, hipCUB, rocPRIM and rocWMMA2.2.1; no script installs them. Cached dense donor paths require the recognized rocBLAS 5.6 solution family. Unknown libraries and architectures keep native dispatch. Rebuilding against a different compiler/header/library combination needs qualification even when compilation succeeds.

For the fork delta, baseline definitions, measured improvements and bitwise coverage, start with [HALO_PERFORMANCE.md](HALO_PERFORMANCE.md).

## Admission and fallbacks

The host admits single-device DeepSeek V4 Flash geometry: 43 layers, embedding4096 and HC4, with operator-specific original tensor types and dimensions. Native layer entry supplies the real position, chunk, context capacity and layer ordinal. Actual chunks are 2048 or4096, aligned to their chunk grid, ending at most131072 with capacity at most262144 and spare context space. Quality mode, GLM, SSD streaming, vision, tensor parallelism and graph dumps are excluded. Individual pointer extents, alignment, aliases and native routing/quantization flags are also checked where required.

| Contribution | Selected physical domain | Preserved fallback |
|---|---|---|
| Resident-key indexer | 2048 rows; H64/D128; ratio4; causal compressed rows1024..32768 in512 steps | 4K, first chunk, decode, other score geometry |
| Cooperative Q8 | Q-b K1024/N32768 and shared-GU K4096/N2048; 2K/4K | Native Q8 for other shapes |
| Shared-GU bridge | 2K K4096/N2048; exact prepared W/X and qualified unpatched vendor WMMA | Cooperative Q8/native when the dead-heads lease is unavailable; 4K keeps cooperative |
| Q-A K16 | 4K K4096/N1024 | Native Q-A outside this domain |
| HC RMS-to-half | 2K/4K K16384/N24; explicit native FP32 rounding boundary | Original normalization and projection |
| Static query registers | Qualified first-chunk raw/ratio128 shapes and 2K ratio4 | Original attention selectors |
| Direct QK | Native FP32 ring and indexed producers, H64/D512/window128 | Native producer before failed admission |
| KV-half + inverse RoPE + grouped pack | Indexed top512/ratio4; original runtime RoPE parameters; cached float-output chain | Direct/native producer when any lease or cache preflight fails |
| Cached output-A | 2K/4K, eight groups K4096/rank1024, heads-first FP16 epilogue | Native cached grouped projection |
| Uncached output-A | 2K/4K at capacities32897/65665/131201, original Q8 W/XQ/scales and unchanged quantizer | Native warp8 elsewhere |
| Output-B S4+D2 | 2K/4K K8192/N4096; one typed cache allocation | Native Wt for unsupported rows; candidate rebuilds DonorW again for a later admitted prefill |
| Shared-down K32 | 2K/4K K2048/N4096, original FP16 inputs and native FMA order | Original GEMM |
| S9 IQ2 producers | 2K/4K, IQ2_XXS K4096/mid2048, 256 experts/top6; original MMQ quantizer | Original gate/up, activation and middle producer |
| Q2 down | Original cold1..7; compact direct-X4K/Wstage64-2K for8..511; prepared-store>=512 | Original scalar/hot/prepared paths when preflight fails |

Arithmetic bodies retain original operand roles, K ordering, rounding and native routing/top6. Host bindings and lifetime code are new. The latest candidate's recorded 4K numerical and cache-lifetime checks passed; wider branch, model and context coverage remains separate. A selected path reports enqueue failure to its caller; a dead-heads attention lease cannot replay a native FP32 consumer after mutation.

## Memory and source build

The indexer adds no tensor scratch. Cooperative Q8 uses the existing temporary allocator. Shared-GU borrows dead attention heads; the attention half view and copied sorted indices also borrow dead heads, while the grouped packet uses the native output temporary. S9 retains a lazy2K arena (9,454,600 payload bytes plus guards) and borrows the qualified4K up-buffer reservation18,894,848B. Q2 retains the original96MiB arena and recurring W reconstruction/X gathering. Cache limits, native allocations and cleanup own these lifetimes. Candidate cache demotion/re-promotion passed the recorded 4K/32-row/4K sequence; peak memory, alias/fault injection and wider reuse cases remain unqualified.

Output-B is redistributable assembly source. The normal Makefile assembles, links and embeds a newly built code object. It does not ship an experimental object/HSACO or load private paths. With the cached core10 compiler this assembly reconstructs the archived S4+D2 module SHA256 `4c3997d9bcf4763c81a444aad0e1894bf7331b1ff14963d0390dfe35fa51e162`. That module identity does not qualify the new host composition or complete executable.

See [evidence](HALO_EVIDENCE.md), [qualification](HALO_QUALIFICATION.md) and [third-party credits](HALO_THIRD_PARTY.md).
