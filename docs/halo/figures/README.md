# Prefill charts and recorded campaigns

The overview includes the latest October 6 prepared-4K result and separately labeled September 25–26 historical context curves. The renderer uses local recorded data only. **Original DS4** means pinned upstream `8db1d1d` measured by us on the corresponding system, not an upstream-published number or today's main. [Historical provenance audit](PROVENANCE_AUDIT.md) · [Latest candidate source and samples](../halo2-qualification.json).

- [Main overview](prefill-context-overview.png): three independent panels. Historical incremental prefill starts at **2K context**; latest prepared complete-4K shows **315.41 → 454.59 (+44.12%)**, two independent processes per engine with three pure warmups each, IOMMU off; historical full prompts retain **fixed 2K chunks**. No line joins protocols or machines. Historical prepared **311.24 → 447.51** and the unpaired **449.03** remain in the overview JSON and their original evidence.
- [Fixed 2K + indexer](prefill-context-indexer-update.png): **391.33 / 361.87 / 319.29** at 32K / 64K / 128K, against the original engine's recorded same-chunk full-prompt rates. Different archived days; not contemporary alternating A/B.
- [Earlier incremental](prefill-context-incremental.png): 32 frontiers from 2K to 64K, two ordinary observations per engine/frontier. Each measurement adds 2K tokens. This preceding checkpoint has no indexer upgrade.
- [Preceding four-variant comparison](prefill-context-four-variants.png): the same full-prompt campaign, with separate 2K- and 4K-chunk panels. The 4K campaign reached **400.58 / 354.53 / 288.48**.
- [Best recorded selection](prefill-context-best-recorded.png): supplementary changing-configuration summary, choosing 4K chunks at 32K and 2K + indexer at 64K/128K. It is not a fixed-configuration scaling result or a same-chunk A/B. [Selection records](best-recorded-selection.json).

The old overview joined official published interval rates with our prepared and first-use complete-prompt rates. That presentation is withdrawn. [The official recorded values](official-ds4-published-context.json) remain separate reference material; none populates the new comparative panels.

## Reading the measurements

P is original DS4 code; C is the preceding optimized checkpoint. Indexer B adds the resident-key update; indexer A is its contemporary optimized control. Full-prompt reference observations are from September 25 and the indexer upgrade from September 26. They match model, chunk, prompt length and allocation rule, but the whole-fork comparison is not contemporary alternating A/B.

Archived rates use token count divided by arithmetic mean seconds. The latest prepared panel uses the mean of two per-process rates; its aggregate-time rate rounds to the same 454.59. Incremental rates count added tokens; full-prompt rates count the complete empty-context request. Loading is excluded. First-use preparation is included in historical long-prompt curves; latest 4K timing follows explicit pure warmups. Decode, snapshot and restore are outside prefill timers. Long prompts allocate length+129 slots. Bitwise identity is verified at matching chunks, not across different chunks.

[CSV](prefill-context-data.csv) and [JSON](prefill-context-data.json) retain all 86 original records unchanged. [Latest evidence](../halo2-qualification.json) retains current and IOMMU-on samples separately. Short controls are not spliced into full-prompt curves; no smoothing, extrapolation or missing points are inferred. [Overview schema 4](prefill-context-overview.json) binds both sources by SHA256 and retains the former historical prepared panel.

## Reproduce the figures

With Python 3.11+ and matplotlib already installed:

```sh
python3 docs/halo/figures/render_prefill_context.py
```

Optional `--output-dir /path/to/exports` writes all five figures in PNG, SVG and PDF. The renderer checks rate arithmetic, source bindings and label layout. No model, ROCm installation or remote host is needed.

Use `--overview-only` to update the latest overview without rewriting the four archived plots.

## Provenance

Portable archived inputs are in [inputs](inputs/). The JSON manifest binds original source IDs and SHA256 to portable filenames and SHA256; portable text uses UTF-8 and LF. For the short 4K control, only two selected ordinary rows are copied, with the original CSV hash and selection rule retained.

[Long-context cases](../longcontext-cases.json) and [indexer observations](../indexer-observations.csv) preserve numerical checks and observation identities. [Quality evidence](../../HALO_EVIDENCE.md) scopes the bitwise claim. Diagnostics, rejected candidates and other hardware are not plotted as Halo performance.

The [rc.2 announcement figure](prefill-4k-release.png) isolates the latest paired prepared-4K result. Reproduce it with `--release-only`; SVG/PDF exports retain the same values and tested scope.
