# Archived prefill charts

Reconstructed from recorded September 25–26 measurements. The renderer uses local data only.

- [Incremental chart](prefill-context-incremental.png): two continuous curves from 2K to 64K. Each frontier adds 2K tokens; rates measure that increment. Every one of the 32 frontiers per engine uses two ordinary observations.
- [Full-prompt chart with indexer update](prefill-context-indexer-update.png): complete empty-context prefill at 32K, 64K and 128K. Separate panels for 2K and 4K chunks, with equal linear axes. Updated indexer observations appear only in the 2K panel.
- [Preceding four-variant comparison](prefill-context-four-variants.png): the same layout using only the preceding matched campaign.

Series names and final rates are placed at the ends of the curves. Incremental curves have no point symbols; full-prompt curves mark each of their three actual measurements. Axes are linear. Connecting segments do not add observations or estimate missing results. No smoothing or extrapolation is applied. PNG, SVG and PDF are available for every chart.

[CSV](prefill-context-data.csv) and [JSON](prefill-context-data.json) retain all 86 records with full precision, including the short-prompt controls and contemporary indexer A observations. Those supplementary records remain available without being mixed into the plotted curves. JSON retains individual observations, protocols, allocations, source IDs and SHA256 bindings.

## Reading the measurements

P is the local rebuilt upstream8db reference, C the qualified preceding Halo chain. Local upstream is not the remote official DS4 published speed figure. Indexer A/B measures the resident-key upgrade relative to its contemporary optimized control. Updated 2K and preceding 4K belong to different campaigns; the latter has no measured indexer update.

Each rate is tokens divided by the arithmetic mean complete-prefill seconds. Incremental rates count only the added 2K tokens; decode, snapshot and restore remain outside the timer. Model loading is excluded, required first-use preparation is included. Long prompts allocate length+129 context slots. The archived short 2K/4K controls allocate 65,665 slots and are retained only in the data files; the short 2K control is the first incremental frontier, not an independent measurement.

The separate resident peak of 449.03 token/s remains in the [performance page](../../HALO_PERFORMANCE.md) and [peak record](../peak-performance.json). Numerical identity is scoped to the documented same-chunk full-logit/state/token checks. See [quality evidence](../../HALO_EVIDENCE.md).

## Reproduce the figures

With Python 3.11+ and matplotlib already installed:

```sh
python3 docs/halo/figures/render_prefill_context.py
```

Optional `--output-dir /path/to/exports` writes all three figures in PNG, SVG and PDF. The renderer checks rate arithmetic before rendering. No model, ROCm installation or remote host is needed.

## Provenance

Portable archived inputs are in [inputs](inputs/). The JSON manifest binds each original source ID and SHA256 to its portable filename and SHA256. Portable text uses UTF-8 and LF line endings. For the short 4K control, only the two selected ordinary rows are copied; the original CSV hash and selection rule are retained.

Timing diagnostics, profiler observations, rejected intermediate candidates and other hardware are excluded from the curves. The retained [long-context cases](../longcontext-cases.json) and [indexer observations](../indexer-observations.csv) preserve verification and per-observation identities.
