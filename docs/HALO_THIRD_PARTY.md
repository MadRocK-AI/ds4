# Halo source credits

The fork retains the upstream DS4 license, history, `AGENT.md` and `CONTRIBUTING.md`. The private mixed-hardware project overlay is not copied.

The frozen GEMM template headers under `rocm/halo/output_a`, `rocm/halo/shared_gu/kernel` and `rocm/halo/q2/prepared` preserve the MIT notices of Adel Johar (2024). Their qualified WMMA orders differ: Q2 prepared retains the native K8 correction; shared-GU retains its qualified unpatched order. Separate namespaces prevent accidental substitution at link time. Output-B assembly carries the corresponding MIT license in `rocm/halo/output_b/LICENSE`.

IQ2 tables/codecs and original operator helpers derive from the pinned DS4/ggml sources and retain their existing notices. HIP/rocWMMA are external build dependencies with their own licenses. Generated output-B code is ignored by Git and rebuilt from source. Source provenance and every original/ported SHA256 are in [sources.json](halo/sources.json). No model weights or additional prompt corpus are redistributed.
