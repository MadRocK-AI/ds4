# Changelog

## Unreleased qualification update — 2026-10-06

- The patched integration candidate passed fresh paired 4K token/logit/full-state, prepared-geometry and cache-lifetime checks on a second Strix Halo system.
- Prepared IOMMU-off mean: **454.59 token/s** versus fresh upstream 315.41 (**+44.12%**), passing the unchanged 440 minimum. The owner-authorized IOMMU contrast improved candidate mean by 5.77% from 429.79, with all complete compared on/off payloads bitwise unchanged.
- Candidate source/artifact identities, all bounded samples and tested limits are recorded in [the qualification summary](docs/halo/halo2-qualification.json). The published RC, companion pin and installer remain unchanged.

## 0.1.0-rc.1

- Opt-in single-device gfx1151 prefill paths for routed MoE, attention, projections and resident-key indexer scoring.
- Source-built output-B assembly, component identities and third-party provenance.
- Archived benchmark and bitwise evidence, with separate protocols and a context overview starting at 2K.
- Normal ROCm build/link checked for ds4, ds4-server, ds4-bench, ds4-eval and ds4-agent in WSL.
- Pinned installation and launcher provided by [ds4-on-halo](https://github.com/MadRocK-AI/ds4-on-halo).

Historical checkpoints reached 447.51 token/s in a matched prepared-4K comparison (+43.78%) and 449.03 token/s in a separate best recorded mean. These are not new measurements of the integrated release executable. Bitwise equality is scoped to the documented historical test cases. Native dispatch remains the default; Halo paths require DS4_ROCM_HALO_PREFILL=1.

Post-publication validation on 2026-10-05: installation, live launcher/API generation and hardware release passed on Halo for the pinned RC. The two requests used 14- and 4,214-token prompts with eight generated tokens each; the generation budget ended during thinking. This adds no new answer-quality, bitwise or throughput claim. See [validation scope](docs/HALO_RELEASE.md).
