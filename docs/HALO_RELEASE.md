# Halo release validation

**0.1.0-rc.2 passed actual installation, complete-payload numerical verification and bounded launcher/API execution on AMD Strix Halo.** Native dispatch remains the source-build default; the companion enables admitted Halo paths. This is a release candidate with explicitly tested scope.

## Performance

**Halo prepared complete 4K prefill: 454.59 token/s mean**, samples **454.52 / 454.65**. Two independent Halo processes each performed three pure position-zero warmups then one measured complete 4,096-token request, capacity 4,352, generation disabled. Loading is excluded; timing had no profiler, trace, payload readback or private preload.

The single original-DS4 reference shown in public performance tables is **295.27 token/s**, copied from the [official gfx1151 report](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md). It is a 2K incremental interval ending at 4K, so no percentage speedup is inferred against Halo's complete prepared 4K result. [Samples and identities](halo/halo2-qualification.json).

The measured configuration used Ryzen AI Max+395/Radeon 8060S (`gfx1151`), 128 GB RAM, Ubuntu 26.04.1/kernel 7.0.0-38, a 106 GiB shared GPU ceiling, IOMMU off and GPU policy auto. The installer does not change these host settings. Complete compared on/off payloads remained bitwise identical.

## Source and installed-package binding

The companion pins engine `c077b9c634d126275035efb8dbd4007f56a45be7`, upstream base `8db1d1d155cb0400a86a86b9c62d0defb3a6148b`. This source retains qualified cache layout rebuilding, optional pure-prefill warmups and explicit BLAS preparation. It removes only the measured parent's optional runtime trace hooks and corrects an explanatory comment without changing executable tokens, kernels, arithmetic, selectors or reserve policy. The 454.59 timing record identifies the measured parent executable; the cleaned installer-built executable has distinct recorded hashes and matched its complete reference payloads. No new speed campaign was run for the cleanup.

| Validation | Result and scope |
| --- | --- |
| Normal ROCm build/link | PASS, all five executables and relocation checks |
| Actual library closure | PASS, all 22 pinned SDK providers plus 8 host ABI libraries recorded |
| Fresh complete numerical comparison | PASS, six token/logit/full-state payloads and manifests, 4K prefill plus 16 generated tokens |
| On/off comparison | PASS, both engines' complete prepared-geometry payloads unchanged bitwise |
| Cache lifetime | PASS on measured parent: 4K → +32 → reset → fresh 4K, nine paired payloads and layout witnesses; functional cache code retained |
| Actual unchanged installer | PASS, one complete supported-model hash, clean exact source pin, normal build and managed launcher |
| Installed clean executable | PASS, all six complete payloads and API extents match both retained original-DS4 and measured-parent off-mode references |
| Launcher and API | PASS, version/status/doctor/preview and HTTP 200 for models plus two requests: 14 / 4,214 prompt tokens, 8 generated each |
| Release and resource cleanup | PASS, owned processes stopped, KFD idle, exclusive lock released, loopback listener closed |

[Portable installed acceptance record](halo/distribution-acceptance.json) binds tested source, package identity, all five installed binary hashes and numerical/API evidence. The original approved pre-execution snapshot remains separate. Publication metadata records the completed outcome without changing inference code, installer scripts, version or engine pin. The installed test companion was 0afd451ee06d57ee03edfae09872edc8219e90e9; later publication edits are documentation and unused qualification metadata only.

## Coverage and historical evidence

Bitwise equality describes the recorded inputs/geometries, not universal model quality. The API smoke is bounded generation, not a broad answer-quality panel. New long-context/snapshot, other-model, multi-GPU, SSD and other-platform matrices are not claimed. Accepted historical 32K/64K/128K, incremental and restoration records remain separately labeled in [HALO_EVIDENCE.md](HALO_EVIDENCE.md). Historical 447.51/449.03 rates and the earlier rc.1 installer smoke remain valid for their own source/protocol identities. [Earlier live record](halo/live-smoke.json).

## Build dependencies

The successful build used AMD clang 23 / HIP 7.15, rocBLAS 5.6.0 at rocm-libraries commit `8d1ae90eff7d022f26019ec55b2ec6a7674b3112`, hipBLASLt 1.4.1, hipCUB 4.6, rocPRIM 4.6 and the frozen rocWMMA 2.2.1 headers. The driver and clang hashes are in the build record. A full existing SDK can provide these dependencies; the recorded build used a core SDK plus an isolated math/header overlay. No SDK or model is bundled here.

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

[Published package provenance](halo/release-provenance.json) records the tested package identity, published metadata identity and unchanged executable inputs.
