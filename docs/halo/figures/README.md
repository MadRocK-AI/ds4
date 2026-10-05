# Archived prefill charts

The publication figures reconstruct existing September 25–26 measurements. No engine, GPU, remote host or benchmark is invoked by the renderer.

- [Updated indexer chart](prefill-context-indexer-update.png): preceding 2K/4K curves plus the measured 2K resident-key indexer upgrade.
- [Previous four-variant chart](prefill-context-four-variants.png): original long-context comparison, extended with recorded short-prompt controls and the incremental series.
- [CSV](prefill-context-data.csv) and [JSON](prefill-context-data.json): all 86 reconstructed records, including the contemporary indexer controls. JSON contains individual observations, protocol, allocation, source IDs and SHA256 bindings. CSV preserves measurement precision.

Both charts have separate full-prompt and incremental panels, with context axes beginning at 2K. K = 1,024 tokens. The logarithmic axis gives each context doubling equal space. Markers are actual measurements, straight lines connect available points, and missing full-prompt 8K/16K measurements are not inferred. Only the first incremental request starts empty: that same 2K observation is also shown as a short-prompt diamond. It is not a second independent measurement. Short 2K/4K requests allocate 65,665 context slots; long prompts allocate length+129. These groups are not connected.

P is the local rebuilt upstream8db reference, C the qualified preceding Halo chain. Neither P nor the indexer A control is the official remote published DS4 speed figure. The indexer A/B pair measures only the resident-key upgrade relative to its contemporary optimized control. Updated 2K and preceding 4K curves are different campaigns; the latter has no measured indexer update. The resident peak 449.03 token/s is a separate recorded mean after native preparation/warmup, not a point spliced into a first-use curve.

Every rate is tokens divided by the arithmetic mean complete-prefill seconds. Incremental rows count only the added 2K tokens, not the entire frontier; decode, snapshots and restore are outside that timer. Model loading is outside prefill, required first-use preparation is inside. Numerical identity is scoped to the documented same-chunk full-logit/state/token checks, not universal model quality or equality between chunk sizes. See [quality evidence](../../HALO_EVIDENCE.md).

## Reproduce the images

With Python 3.11+ and matplotlib already installed, run:

```sh
python3 docs/halo/figures/render_prefill_context.py
```

Optional `--output-dir /path/to/exports` writes PNG, SVG and PDF for both charts. The renderer uses only this directory's normalized data and [the peak record](../peak-performance.json). It checks rate arithmetic before rendering. No model or ROCm installation is needed.

## Provenance

Portable archived inputs are in [inputs](inputs/). The JSON manifest binds each original source ID and SHA256, its portable filename and portable SHA256. For the short 4K control, only the two selected ordinary rows are copied; its original full CSV hash and selection rule are retained. Portable text uses UTF-8 and LF line endings; original source hashes preserve the archived byte identity. Full diagnostics, profiler observations and rejected intermediate candidates are excluded from all plotted series. No external Spark or R9700 series is included.

The retained [long-context cases](../longcontext-cases.json) and [indexer observations](../indexer-observations.csv) preserve the corresponding verification and per-observation identities.
