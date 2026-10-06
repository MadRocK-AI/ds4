# Figure provenance

The original 86 recorded measurements and complete source/protocol identities are retained unchanged in the data files. Our local upstream controls are raw experimental evidence; they are not used as the public DS4 performance reference.

The single displayed DS4 reference is **295.27 token/s**, from the integrated default gfx1151 pure-prefill follow-up in the [official repository report](https://github.com/antirez/ds4/blob/0aaea5a238fb41a35106a551e73c8409dfb751ac/speed-bench/gfx1151-prefill-results.md). It measures the added 2K interval ending at 4K. No unmerged PR or locally rebuilt baseline rate replaces it.

Halo's **454.59 token/s** is a prepared complete 4K request, two independent observations with three warmups each, IOMMU off. The two published rates have different protocols; no ratio is presented as a matched speedup.

Context plots display Halo results only. The incremental historical curve starts at 2K; the 32K/64K/128K complete-prompt curves remain separate from it and from the current prepared 4K result. No official Strix Halo full-prompt values exist at those long lengths in the cited report. We do not invent a reference curve or splice missing points.

The 2K indexer campaign records 391.33 / 361.87 / 319.29 at 32K / 64K / 128K. The earlier 4K campaign records 400.58 / 354.53 / 288.48. These distinct configurations and dates remain labeled. Earlier prepared Halo records of 447.51/449.03 remain archival results, not new rc.2 measurements.
