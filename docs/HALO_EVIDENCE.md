# Halo evidence and numerical coverage

[Performance and quality summary](HALO_PERFORMANCE.md). The detailed historical controls, source/harness attribution and exact values remain in [baseline-attribution.json](halo/baseline-attribution.json); the peak and controlled headline figures are bound in [peak-performance.json](halo/peak-performance.json). The secondary incremental comparison remains in [published-performance.json](halo/published-performance.json).

The source/evidence matrix binds the documented measurements to their implementation. [sources.json](halo/sources.json) binds each component to its original source SHA256, port path/SHA256, historical checkpoint and upstream base. A bounded live installer/launcher/API smoke passed for the pinned RC. The latest unpublished candidate subsequently passed fresh paired 4K numerical and cache-lifetime gates on a second Halo system; its wider matrix and final package acceptance remain open. [Build and qualification status](HALO_RELEASE.md) distinguishes these candidate checks from historical evidence and the unchanged pinned package. Whole-file hash differences are expected for the recorded source and host bindings.

## Historical chain

The retained chain is historical public8db -> qualified public prefill upgrades -> compatible B/D and Q2/attention contributions -> shared-GU bridge -> longcontext -> resident-key indexer. The measured public core is based on `8db1d1d155cb0400a86a86b9c62d0defb3a6148b`; its executable, diagnostics and environmental composition must also match before identifying a new control with that archived binary. Current upstream documentation was inspected without merging its newer source into the old qualified base.

Checkpoint SHA256s: longcontext-final `cfcf4c62e7f7c00d255dd9ab694b57e2d083cbeec12096762285f6f07d6a05d7`, public-shared-bridge `964069ed749d158e93401d7db6a188b5c2ec7efff84f3b5b4f5e1d93111272b6`, indexer32/64/128 `a024a0a00a7d11178eac4c973cbefa40948c88ce91af8f957a243a6f31253d66`.

The tested model is DeepSeek V4 Flash0731 IQ2_XXS/w2Q2_K/AProjQ8/SExpQ8/OutQ8 chat-v2 imatrix,86,720,111,488B, SHA256 `ca22ae2f838e14077c22bc1c1417b71b45b5e5a3687bd96c2ac6e17fdb6261c0`. The historical campaign used its frozen full hash and checked current stat identity; it did not repeat an87GB hash during every timing observation. Hardware was Ryzen AI Max+395,128GB unified RAM,gfx1151; Linux7.0.0-31-generic, core10/HIP7.15, IOMMU off, GPU auto, NPU auto/suspended, exclusive GPU. These are recorded conditions, not configuration commands.

The 31 longcontext checkpoint entries remain individually recorded in [longcontext-cases.json](halo/longcontext-cases.json). They include fresh32/64/128K with2K/4K chunks and public2K incremental coverage through64K. On compared cases, full frontier FP32 logits, serialized state (raw/compressed/indexer/compressor state), prompt IDs,16 greedy IDs and post-decode state/logits were identical. Incremental intermediate frontiers exercised restoration. A final fresh frontier with `snapshot_bytes=0` did not exercise restore, regardless of its historical `restore_exact_checked` marker. Equality is on these tested inputs/capacities/chunks, with no cross-chunk or universal model-quality claim.

## Historical indexer comparison

Here A is the preceding optimized longcontext chain and B adds the resident-key indexer. Neither arm is the cleaned fork, and A is not the clean public upstream baseline. Each length has two timed observations per arm, in A0/B0/B1/A1 order, with zero warmups. Necessary first-use/recurring work is included in complete prefill; loading/initialization is separate. Readback/observer conditions are archived and differ from other ordinary public protocols.

| Fresh tokens; chunk2048 | A prefill mean; min..max (s) | B prefill mean; min..max (s) | Throughput gain from mean times |
|---|---|---|---|
|32768|87.56;87.39..87.73|83.73;83.69..83.78|4.57%|
|65536|195.29;195.04..195.55|181.10;180.92..181.28|7.84%|
|131072|469.85;469.47..470.24|410.51;410.39..410.63|14.46%|

Use [all18 observations](halo/indexer-observations.csv), including initialization/decode, qualification-only and short4K fallback control rows. [Original official CSVs](halo/historical-csv/) retain their rounded upstream fields; [provenance](halo/historical-provenance.json) binds the original records/CSV/config/environment hashes. [Numerical hashes](halo/historical-numeric-hashes.json) contain hashes/extents only. The decisive pool excludes separate32K/64K qualification runs and the short fallback control. Ranges are not confidence intervals. The16-token decode checks are regressions after readbacks, not an optimized decode claim.

Do not pool this table with incremental suffix, resident4K, first-load, ordinary public or profiling campaigns. Do not combine their percentages or a267->450 claim across protocols. Failed IQ2/arithmetic variants, the unstable later dense cohort, Gufo/shared-down quality-pending work, R9700, DSpark and NPU contributions are excluded.

## New integrated candidate

On 2026-10-06, fresh original-DS4 and patched-candidate runs matched all six complete token/logit/state payloads at 4K/chunk4K with capacities 65,665 and 4,352, including after 16 generated tokens. The 4K → 32-token continuation → fresh 4K lifetime sequence matched nine paired payloads and first/final payloads within each engine; existing four-layer layout witnesses confirmed DonorW → native Wt → DonorW. Manifests and actual byte extents were checked. [Candidate identities and scope](halo/halo2-qualification.json).

The reference was freshly generated on the second system. Both arms differ from the old short-B oracle in four tensor payloads, while token IDs match; that old oracle was not substituted for the fresh reference. The frontier FP32 logit hash matches the historical Structural9 frontier. No new full long-context, snapshot or universal quality claim follows.

Initial IOMMU-on timing averaged 429.79 token/s, below 440. After the owner-authorized single-parameter IOMMU-off change, every complete prepared-geometry payload and manifest also matched its own retained on-mode reference. The same immutable binary and timing recipe then averaged **454.59 token/s**, **44.12%** above its fresh 315.41 original-DS4 control, passing the retained 440 minimum. The candidate's before/after increase is **5.77%**. The old on-mode record is retained; the package and companion pin remain unchanged.

CPU build, focused CPU checks, ROCm C frontend, production kernel compilation and source/module reconstruction have separate statuses in [qualification](HALO_QUALIFICATION.md). Full SDK linking passed for all five targets in local WSL. Live package execution is recorded separately in [the release record](HALO_RELEASE.md). The historical table describes its frozen executables and configurations; it does not certify the integrated package's numerical equivalence or throughput.
