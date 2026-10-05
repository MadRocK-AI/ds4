# Initial private Halo release

Prepared on 2026-10-02 for the private repositories [msala9/ds4](https://github.com/msala9/ds4) and [msala9/ds4-on-halo](https://github.com/msala9/ds4-on-halo). The planned official home is the madrock organization. No transfer or public publication is included in this initial upload.

## Acceptance and validation

The owner accepted the existing internal numerical and performance evidence for this preparation. Those observations retain their original executables, model, inputs and measurement boundaries. No new GPU inference or benchmark of the integrated release executable is claimed. The source remains opt-in with `DS4_ROCM_HALO_PREFILL=1`; native dispatch is the default.

The normal `make rocm` path built **ds4, ds4-server, ds4-bench, ds4-eval and ds4-agent** in local WSL for gfx1151. All five ELF relocation checks passed, with 29 real shared-library files resolved and no missing symbols. The actual runtime object contains a gfx1151 AMD HSA code image. The successful build and source checks took 312.10 seconds. [The portable build record](halo/release-build.json) contains executable, compiler and library hashes and exact SDK package identities.

The compiled engine commit is `34ec09459cc64c1f565dbb2e49744ce7d852d9de`. Publication commits change documentation only. The companion publication updates its engine pin and presentation; its build and benchmark implementations are unchanged. The archived compiler logs and original receipts remain local; this repository contains the path-independent evidence summary.

Historical fresh resident 4096-token prefill reached **447.51 tokens/s** in the frozen controlled comparison (9.15 seconds). A later ordinary profiling bracket reported **449.03 tokens/s**; the observations are kept separate. The frozen structural9 checkpoint SHA256 is `9405793e0ad534c747a2036fc2e807554691031ebc68b8a240bf0805779fac71`. Long-context and indexer evidence, numerical hashes, tested geometry and measurement boundaries are retained in [HALO_EVIDENCE.md](HALO_EVIDENCE.md). These are historical performance observations, not a new binary benchmark.

The [performance overview](HALO_PERFORMANCE.md) explains the added paths, same-protocol gains, distinct upstream/local references and bitwise test coverage.

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
