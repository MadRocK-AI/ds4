# Changelog

## 0.1.0-rc.1

- Opt-in single-device gfx1151 prefill paths for routed MoE, attention, projections and resident-key indexer scoring.
- Source-built output-B assembly, component identities and third-party provenance.
- Archived benchmark and bitwise evidence, with separate protocols and a context overview starting at 2K.
- Normal ROCm build/link checked for ds4, ds4-server, ds4-bench, ds4-eval and ds4-agent in WSL.
- Pinned installation and launcher provided by [ds4-on-halo](https://github.com/MadRocK-AI/ds4-on-halo).

Historical checkpoints reached 447.51 token/s in a matched prepared-4K comparison (+43.78%) and 449.03 token/s in a separate best recorded mean. These are not new measurements of the integrated release executable. Bitwise equality is scoped to the documented historical test cases. Native dispatch remains the default; Halo paths require DS4_ROCM_HALO_PREFILL=1.

The integrated executable has not had a new GPU model run. See [build and validation scope](docs/HALO_RELEASE.md).
