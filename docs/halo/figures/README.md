# Prefill figures

Publication figures display **Halo measurements** and use **295.27 token/s from the official DS4 report** as the only original-DS4 reference. That published rate is a 2K interval ending at 4K; Halo's 454.59 is a complete prepared 4K request. The protocols differ, so no percentage is inferred. [Source audit](PROVENANCE_AUDIT.md).

- [Announcement figure](prefill-4k-release.png): latest 454.59 and the separately labeled official reference.
- [Context overview](prefill-context-overview.png): historical incremental curve starting at **2K**, latest complete prepared 4K result, and historical long prompts with fixed 2K chunks plus indexer. No line joins protocols or campaigns.
- [2K/4K long prompts](prefill-context-four-variants.png): earlier Halo configurations shown separately.
- [Indexer update](prefill-context-indexer-update.png): Halo 391.33 / 361.87 / 319.29 at 32K / 64K / 128K.
- [Incremental context](prefill-context-incremental.png): historical Halo 2K additions through 64K.
- [Best recorded long prompts](prefill-context-best-recorded.png): best Halo chunk at each length, labeled at each point.

[CSV](prefill-context-data.csv) and [JSON](prefill-context-data.json) preserve all 86 original observations, including raw archived experimental controls, unchanged. The renderer omits locally measured original-DS4 curves from public charts. It uses no new benchmark, smoothing, interpolation or invented measurements. Historical and current records stay separate. [Current qualification](../halo2-qualification.json) · [Official source record](official-ds4-published-context.json).

```sh
python -m pip install matplotlib
python docs/halo/figures/render_prefill_context.py
```

Use `--release-only` for the announcement figure or `--overview-only` for the main overview. PNG, SVG and PDF are generated from the same records. K means 1,024 tokens.
