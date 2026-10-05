# Archived prefill charts

Reconstructed from recorded September 25–26 measurements. The renderer uses local data only.

- [Main overview: DS4 Halo versus official DS4](prefill-context-overview.png): starts at 2K; includes Halo prepared 4K **449.03 / 447.51** and long-context **400.58 / 361.87 / 319.29**. The official curve uses only [antirez/ds4 main](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md): **231.91 / 295.27 / 268.51** at 2K / 4K / 16K. It stops at 16K; no local rebuilt control is relabelled official. [Official reference](official-ds4-published-context.json) and [overview records](prefill-context-overview.json) bind every plotted value to its source. Official rates count 2K increments, while Halo preparation and complete-prompt conditions vary. These cross-campaign curves do not establish a controlled A/B or scaling result.

- [Best recorded full-prompt chart](prefill-context-best-recorded.png): 400.58 / 361.87 / 319.29 token/s at 32K / 64K / 128K. It selects 4K chunks at 32K and 2K + indexer at 64K/128K. [Selection and source records](best-recorded-selection.json) bind every chosen point to the full-precision data. This is a best-result curve across archived configurations, not a fixed-chunk A/B.
- [Fixed 2K + indexer chart](prefill-context-indexer-update.png): 391.33 / 361.87 / 319.29 token/s at 32K / 64K / 128K. Only the measured indexer-upgraded Halo series and its recorded 2K upstream control are shown.
- [Earlier incremental chart](prefill-context-incremental.png): two continuous curves from 2K to 64K, before the indexer upgrade. Each frontier adds 2K tokens. Every one of the 32 frontiers per engine uses two ordinary observations. These are interval rates, not updated complete-prompt rates.
- [Preceding four-variant comparison](prefill-context-four-variants.png): retained supplementary pre-indexer 2K/4K comparison; it is not the headline result.

Series names and final rates are placed at the ends of the curves. The current full-prompt charts label the earlier context values above the measured points; the best-result chart also identifies each chosen chunk. Incremental curves have no point symbols; full-prompt curves mark each of their three actual measurements. The main overview uses a base-2 logarithmic context axis to keep 2K and 4K readable alongside 128K; the supplementary charts use linear axes. Connecting segments do not add observations or estimate missing results. No smoothing or extrapolation is applied. PNG, SVG and PDF are available for every chart.

[CSV](prefill-context-data.csv) and [JSON](prefill-context-data.json) retain all 86 records with full precision, including the short-prompt controls and contemporary indexer A observations. Those supplementary records remain available without being mixed into the plotted curves. JSON retains individual observations, protocols, allocations, source IDs and SHA256 bindings.

## Reading the measurements

In supplementary internal-control figures, P is the local rebuilt upstream8db reference and C the qualified preceding Halo chain. Those figures are labelled DS4 control and are separate from the official published comparison. Local upstream is not the remote official DS4 published speed figure. Indexer A/B measures the resident-key upgrade relative to its contemporary optimized control. Updated 2K and preceding 4K belong to different campaigns; the latter has no measured indexer update.

Each rate is tokens divided by the arithmetic mean complete-prefill seconds. Incremental rates count only the added 2K tokens; decode, snapshot and restore remain outside the timer. Model loading is excluded, required first-use preparation is included. Long prompts allocate length+129 context slots. The archived short 2K/4K controls allocate 65,665 slots and are retained only in the data files; the short 2K control is the first incremental frontier, not an independent measurement.

The prepared resident 4K peak and controlled result are shown together at 4K in the main overview, bound to the [peak record](../peak-performance.json) and [controlled attribution](../baseline-attribution.json). Numerical identity is scoped to the documented same-chunk full-logit/state/token checks. See [quality evidence](../../HALO_EVIDENCE.md).

## Reproduce the figures

With Python 3.11+ and matplotlib already installed:

```sh
python3 docs/halo/figures/render_prefill_context.py
```

Optional `--output-dir /path/to/exports` writes all five figures in PNG, SVG and PDF. The renderer checks rate arithmetic before rendering. No model, ROCm installation or remote host is needed.

## Provenance

Portable archived inputs are in [inputs](inputs/). The JSON manifest binds each original source ID and SHA256 to its portable filename and SHA256. Portable text uses UTF-8 and LF line endings. For the short 4K control, only the two selected ordinary rows are copied; the original CSV hash and selection rule are retained.

Timing diagnostics, profiler observations, rejected intermediate candidates and other hardware are excluded from the curves. The retained [long-context cases](../longcontext-cases.json) and [indexer observations](../indexer-observations.csv) preserve verification and per-observation identities.
