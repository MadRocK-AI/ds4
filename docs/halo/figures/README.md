# Archived prefill charts

Reconstructed from recorded September 25–26 measurements. The renderer uses local data only. **Original DS4** means the upstream `8db1d1d` engine measured by us on the same Halo, not an upstream-published number or today's main. [Provenance audit](PROVENANCE_AUDIT.md).

- [Main overview](prefill-context-overview.png): three independent panels. Incremental prefill starts at **2K context**; the prepared complete-4K panel shows **311.24 → 447.51 (+43.78%)**, with **449.03** identified separately as an unpaired best mean; the full-prompt panel keeps **fixed 2K chunks**. No line joins different protocols.
- [Fixed 2K + indexer](prefill-context-indexer-update.png): **391.33 / 361.87 / 319.29** at 32K / 64K / 128K, against the original engine's recorded same-chunk full-prompt rates. Different archived days; not contemporary alternating A/B.
- [Earlier incremental](prefill-context-incremental.png): 32 frontiers from 2K to 64K, two ordinary observations per engine/frontier. Each measurement adds 2K tokens. This preceding checkpoint has no indexer upgrade.
- [Preceding four-variant comparison](prefill-context-four-variants.png): the same full-prompt campaign, with separate 2K- and 4K-chunk panels. The 4K campaign reached **400.58 / 354.53 / 288.48**.
- [Best recorded selection](prefill-context-best-recorded.png): supplementary changing-configuration summary, choosing 4K chunks at 32K and 2K + indexer at 64K/128K. It is not a fixed-configuration scaling result or a same-chunk A/B. [Selection records](best-recorded-selection.json).

The old overview joined official published interval rates with our prepared and first-use complete-prompt rates. That presentation is withdrawn. [The official recorded values](official-ds4-published-context.json) remain separate reference material; none populates the new comparative panels.

## Reading the measurements

P is original DS4 code; C is the preceding optimized checkpoint. Indexer B adds the resident-key update; indexer A is its contemporary optimized control. Full-prompt reference observations are from September 25 and the indexer upgrade from September 26. They match model, chunk, prompt length and allocation rule, but the whole-fork comparison is not contemporary alternating A/B.

Each rate is token count divided by arithmetic mean seconds. Incremental rates count only added tokens; full-prompt rates count the complete empty-context request. Model loading is excluded. Required first-use preparation is included in the full-prompt curves; the resident 4K panel explicitly measures after preparation and warmup. Decode, snapshot and restore are outside prefill timers. Long prompts allocate length+129 context slots. Bitwise identity is verified at matching chunks, not between different chunk sizes.

[CSV](prefill-context-data.csv) and [JSON](prefill-context-data.json) retain all 86 original records, individual observations, source IDs, protocols, allocations and SHA256 bindings. The short controls retain their original allocations and are not spliced into full-prompt curves. Connecting segments add no measurements; no smoothing, extrapolation or missing points are inferred. [Overview panel records](prefill-context-overview.json) bind to the canonical data and prepared benchmark attribution.

## Reproduce the figures

With Python 3.11+ and matplotlib already installed:

```sh
python3 docs/halo/figures/render_prefill_context.py
```

Optional `--output-dir /path/to/exports` writes all five figures in PNG, SVG and PDF. The renderer checks rate arithmetic, source bindings and label layout. No model, ROCm installation or remote host is needed.

## Provenance

Portable archived inputs are in [inputs](inputs/). The JSON manifest binds original source IDs and SHA256 to portable filenames and SHA256; portable text uses UTF-8 and LF. For the short 4K control, only two selected ordinary rows are copied, with the original CSV hash and selection rule retained.

[Long-context cases](../longcontext-cases.json) and [indexer observations](../indexer-observations.csv) preserve numerical checks and observation identities. [Quality evidence](../../HALO_EVIDENCE.md) scopes the bitwise claim. Diagnostics, rejected candidates and other hardware are not plotted as Halo performance.
