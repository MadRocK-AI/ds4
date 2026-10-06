# Halo build and qualification record

Build validation recorded on 2026-10-02 for DS4 Halo. The [setup and verification companion](https://github.com/MadRocK-AI/ds4-on-halo) provides pinned-source bootstrap and benchmark tooling.

## Validation scope

Historical checkpoint observations and the new 2026-10-06 candidate checks have distinct executable, source and measurement identities. A bounded live installer/launcher/API smoke of the pinned RC passed on Halo on 2026-10-05. It adds no new throughput, answer-quality or bitwise qualification. The source remains opt-in with `DS4_ROCM_HALO_PREFILL=1`; native dispatch is the default.

Final distribution qualification remains open. The latest unpublished integration candidate passed fresh paired 4K bitwise, prepared-geometry and source cache-lifetime checks on a second Strix Halo system. With IOMMU off its mean reached **454.59 token/s**, passing the unchanged **440 token/s** minimum. Its patches are not included in the unchanged companion pin. Earlier numerical failures on the first Halo system and the second system's IOMMU-on 429.79 result remain recorded; the latest configuration-specific PASS does not erase them.

## Latest candidate qualification, 2026-10-06

The candidate is base `fd77fb67d97f1b40279793dc856af92af71267c9` plus four recorded patches: bidirectional output-B cache rebuilding, pure-prefill warmup controls, optional diagnostics and one-time BLAS initialization. Its fresh reference is upstream `8db1d1d` inference with only the disclosed common observation driver. Both use the same verified SDK, model, input and single visible gfx1151 device. [Portable identities and every timing sample](halo/halo2-qualification.json).

| Gate | Result | Tested scope |
|---|---|---|
| Paired build and relocation checks | PASS | All five normal ROCm targets per engine |
| Fresh numerical comparison | PASS | 4K prompt/chunk, capacity 65,665, 16 generated tokens; six complete paired payloads |
| Prepared geometry | PASS | 4K prompt/chunk, capacity 4,352, three pure warmups, 16 generated tokens; six complete paired payloads |
| Cache lifetime | PASS | 4K â†’ 32-token continuation â†’ invalidate â†’ fresh 4K; nine paired payloads and first/final equality within each arm; layout witnesses confirm DonorW â†’ native Wt â†’ DonorW |
| IOMMU-off prepared numerical comparison | PASS | Same 4K/capacity 4,352/warmup3/gen16 geometry; all six complete payloads and manifests match fresh original DS4 and each arm's retained IOMMU-on result |
| Bounded prepared timing, IOMMU off | PASS | Candidate 454.52 / 454.65, mean **454.59 token/s**; upstream 316.05 / 314.78, mean **315.41 token/s**; gain **44.12%**; unchanged minimum 440 passed |
| Actual package acceptance of patched candidate | PENDING | No new candidate commit or companion pin; published RC unchanged |

Timing used original qualified binaries without lifetime controls, trace, payload dumps or profiling. Order was upstreamâ€“candidateâ€“candidateâ€“upstream, with four independent processes total, each containing three pure warmups and one measured complete position-zero prefill; generation was disabled. Startup, first-use prefill, warmups and samples are retained separately. All numerical manifests and extents were verified. These checks do not establish general model quality or new long-context/snapshot coverage.

The second system runs Ubuntu 26.04.1, kernel `7.0.0-38-generic`, with a verified 106 GiB shared GPU ceiling and 16.20 GiB nominal Linux headroom. GPU policy remained `auto`; clocks and power limits were not changed. Its initial IOMMU-on timing gave candidate 429.79 and upstream 299.14 token/s, with the iGPU default DMA domain already `identity`. An owner-authorized single-parameter `amd_iommu=off` reboot exposed zero groups and preserved all original binary, SDK, kernel, memory, model and input identities. Both arms' complete prefill/decode payloads and manifests stayed bitwise identical. The subsequent unchanged timing recipe improved candidate mean by **5.77%** and upstream mean by **5.44%**. Every sample is retained; this is a same-binary before/after comparison, not an interleaved on/off/on experiment or an attribution of a specific driver mechanism. No threshold was lowered or extra samples taken.

The older 449.03 result used a different executable/preload composition, native-first cache preparation, four ordinary samples and kernel 31 with IOMMU off. SDK families are similar, but byte-exact historical closure and effective clock/power series are missing. It remains a separate historical result. The cache-lifetime trace was acquired under the earlier on-mode policy; the off contrast rechecked prepared prefill/generation equality, rather than rerunning that entire lifetime sequence. New package acceptance remains pending.

## Retained build and package records

The normal `make rocm` path built **ds4, ds4-server, ds4-bench, ds4-eval and ds4-agent** in local WSL for gfx1151. All five ELF relocation checks passed, with 29 real shared-library files resolved and no missing symbols. The actual runtime object contains a gfx1151 AMD HSA code image. The successful build and source checks took 312.10 seconds. [The portable build record](halo/release-build.json) contains executable, compiler and library hashes and exact SDK package identities.

The compiled engine commit is `34ec09459cc64c1f565dbb2e49744ce7d852d9de`. Subsequent documentation revisions preserve the compiled engine source; the companion pins the corresponding engine revision. The archived compiler logs and original receipts remain local; this repository contains the path-independent evidence summary.

Historical fresh resident 4096-token prefill reached **447.51 tokens/s** in the frozen controlled comparison (9.15 seconds). A later ordinary profiling bracket reported **449.03 tokens/s**; the observations are kept separate. The frozen structural9 checkpoint SHA256 is `9405793e0ad534c747a2036fc2e807554691031ebc68b8a240bf0805779fac71`. Long-context and indexer evidence, numerical hashes, tested geometry and measurement boundaries are retained in [HALO_EVIDENCE.md](HALO_EVIDENCE.md). These are historical performance observations, not a new binary benchmark.

The [performance overview](HALO_PERFORMANCE.md) explains the added paths, same-protocol gains, the measured original-engine reference and bitwise test coverage.

## Live package check

The public **0.1.0-rc.1** package was installed in an isolated directory using the existing SDK and model. Full model SHA256, normal ROCm build, executable/source checks and launcher preview passed. The launcher started `ds4-server` on the single visible gfx1151 device, and `/v1/models` and two `/v1/completions` requests returned HTTP 200.

| Request | Prompt tokens | Generated tokens | Chunk size |
|---|---:|---:|---:|
| Short startup check | 14 | 8 | 2048 |
| Complete chunks check | 4214 | 8 | 2048 |

The second request crossed two complete 2K chunks. Both stopped at the eight-token budget during thinking; final-answer quality was not assessed. This is a bounded execution smoke, not a bitwise comparison, branch-coverage proof, long-context matrix or speed benchmark. The owned process was stopped, `/dev/kfd` was free and the exclusive hardware lock was released. Drivers, power policy, models and DSpark setup were unchanged.

[Portable live record](halo/live-smoke.json) binds tested engine `fd77fb67d97f1b40279793dc856af92af71267c9`, companion `c1ecb6b7927789751c1b790c6961b5278fa84ee1`, package identity, model and executable hashes. Subsequent documentation commits do not change the tested code. The published tag remains unchanged.

## Build dependencies

The successful build used AMD clang23/HIP7.15, rocBLAS5.6.0 at rocm-libraries commit `8d1ae90eff7d022f26019ec55b2ec6a7674b3112`, hipBLASLt1.4.1, hipCUB4.6, rocPRIM4.6 and the frozen rocWMMA2.2.1 headers. The driver and clang hashes are in the build record. A full existing SDK can provide these dependencies; the recorded build used a core SDK plus an isolated math/header overlay. No SDK or model is bundled here.

For that split layout, set `CORE_SDK`, `MATH_SDK` and `WMMA_INCLUDE` to existing absolute paths; `WMMA_INCLUDE` is the directory containing the rocwmma folder. Keep the recorded rocWMMA headers first:

```sh
export ROCM_PATH="$CORE_SDK" HIP_PATH="$CORE_SDK"
export HIP_CLANG_PATH="$CORE_SDK/lib/llvm/bin"
export HIPCC_COMPILE_FLAGS_APPEND="-isystem $WMMA_INCLUDE -isystem $MATH_SDK/include -isystem $CORE_SDK/include"
export LD_LIBRARY_PATH="$MATH_SDK/lib:$CORE_SDK/lib:$CORE_SDK/lib/llvm/lib:$CORE_SDK/lib/rocm_sysdeps/lib"
export ROCM_LDLIBS="-L$MATH_SDK/lib -Wl,-rpath,$MATH_SDK/lib -Wl,-rpath,$CORE_SDK/lib -lm -pthread -lhipblas -lhipblaslt -lrocblas"
make rocm HIPCC="$CORE_SDK/bin/hipcc" ROCM_ARCH=gfx1151 -j2
```

Normal C++20/O3/fast-math flags and the native MMQ C++17 recipe are preserved. Source and license provenance is recorded in [HALO_THIRD_PARTY.md](HALO_THIRD_PARTY.md). The [qualification protocol](HALO_QUALIFICATION.md) remains available for future investigations; unexecuted GPU and other-platform tests are not presented as new passes.

## Final source cleanup under distribution review

The local release candidate retains the three functional patches (cache layout rebuilding, pure-prefill warmup controls and explicit BLAS preparation). The fourth measured-parent patch contained optional runtime tracing and is excluded. The BLAS rationale comment is corrected without changing executable tokens. Measured parent source/binary identities in the portable record remain historical qualification inputs, not hashes of this cleaned binary. Final installer-built artifact acceptance is pending; no new performance benchmark is claimed for the cleanup.
