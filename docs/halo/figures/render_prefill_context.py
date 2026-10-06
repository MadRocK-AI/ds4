"""Publication charts from archived data. No engine or hardware execution.

Requires Python 3.11+ and matplotlib; run from any directory.
"""
from pathlib import Path
import argparse
import json
import statistics
import hashlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

HERE = Path(__file__).resolve().parent
BLUE = "#0868B2"
ORANGE = "#A75B20"
GRAY = "#8499AB"
INK = "#182D42"
MUTED = "#586D80"


def style(ax, ticks, xmax):
    ax.set_xlim(2048 if ticks[0] == 2048 else 30000, xmax)
    ax.set_ylim(0, 450)
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1024:g}K"))
    ax.set_yticks([0, 100, 200, 300, 400])
    ax.grid(axis="y", color="#DEE6ED", lw=.8)
    ax.set_axisbelow(True)
    for name in ["top", "right", "left"]:
        ax.spines[name].set_visible(False)
    ax.spines["bottom"].set_color("#B9C8D4")
    ax.tick_params(axis="both", length=0, pad=9, colors=MUTED, labelsize=10)
    ax.set_xlabel("Context (tokens)", labelpad=15, color=MUTED, fontsize=10)


def header(fig, title, subtitle):
    fig.text(.07, .925, title, fontsize=23, weight="bold", color=INK)
    fig.text(.07, .866, subtitle, fontsize=11, color=MUTED)


def save(fig, output):
    # Publication layout check: direct curve labels must fit and stay distinct.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes = [text.get_window_extent(renderer) for ax in fig.axes for text in ax.texts]
    for i, box in enumerate(boxes):
        assert fig.bbox.contains(box.x0, box.y0) and fig.bbox.contains(box.x1, box.y1), "Clipped curve label"
        assert not any(box.overlaps(other) for other in boxes[i + 1:]), "Overlapping curve labels"
    for label in fig.texts:
        box = label.get_window_extent(renderer)
        assert fig.bbox.contains(box.x0, box.y0) and fig.bbox.contains(box.x1, box.y1), "Clipped figure caption"
        for ax in fig.axes:
            if ax.xaxis.label.get_text():
                assert not box.overlaps(ax.xaxis.label.get_window_extent(renderer)), "Caption overlaps axis label"
    for extension in ["png", "svg", "pdf"]:
        path = output.with_suffix("." + extension)
        fig.savefig(path, dpi=240, facecolor="white")
        if extension == "svg":
            path.write_bytes(b"\n".join(line.rstrip(b" \t\r") for line in path.read_bytes().splitlines()) + b"\n")
    plt.close(fig)


def selected(data, protocol, series, chunk):
    return sorted([p for p in data["points"] if p["protocol"] == protocol
                   and p["series"] == series and p["chunk_tokens"] == chunk],
                  key=lambda p: p["context_tokens"])


def end_label(ax, p, label, color, fontsize=11, compact=False):
    text = f"{label}  {p['prefill_tps']:.2f}" if compact else f"{label}\n{p['prefill_tps']:.2f} token/s"
    ax.annotate(text,
                (p["context_tokens"], p["prefill_tps"]), xytext=(14, 0),
                textcoords="offset points", ha="left", va="center",
                fontsize=fontsize, linespacing=1.4, color=color,
                annotation_clip=False)


def render_incremental(data, output):
    fig = plt.figure(figsize=(11.8, 6.1))
    ax = fig.add_axes([.07, .23, .73, .54])
    header(fig, "Prefill as context grows",
           "DeepSeek V4 Flash 0731  ·  AMD Strix Halo, 128 GB  ·  2K → 64K")
    style(ax, [2048, 8192, 16384, 32768, 49152, 65536], 65536)
    ax.set_ylabel("Prefill (token/s)", labelpad=14, color=MUTED, fontsize=10)
    for series, color, label in [("C", BLUE, "DS4 Halo"), ("P", ORANGE, "DS4 8db1d1d")]:
        pp = selected(data, "incremental", series, 2048)
        assert [p["context_tokens"] for p in pp] == list(range(2048, 65537, 2048))
        ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp],
                color=color, lw=2.6, solid_capstyle="round")
        end_label(ax, pp[-1], label, color)
    fig.text(.07, .075, "Incremental prefill: each measurement adds 2,048 tokens. Loading, decode and restore are excluded.",
             fontsize=9.5, color=MUTED)
    fig.text(.07, .035, "32 frontiers per curve. Original DS4 code measured by us; upstream 8db1d1d. K = 1,024 tokens.",
             fontsize=9.5, color=MUTED)
    save(fig, output)


def render_previous(data, output):
    fig = plt.figure(figsize=(13, 6.3))
    axes = [fig.add_axes([.07, .23, .295, .51]), fig.add_axes([.57, .23, .275, .51])]
    header(fig, "Full-prompt prefill",
           "DeepSeek V4 Flash 0731  ·  AMD Strix Halo, 128 GB  ·  32K → 128K")
    for ax, chunk in zip(axes, [2048, 4096]):
        style(ax, [32768, 65536, 131072], 131072)
        ax.set_title(f"{chunk // 1024}K chunks", loc="left", fontsize=12, weight="bold", color=INK, pad=16)
        ax.set_ylabel("Prefill (token/s)", labelpad=12, color=MUTED, fontsize=10)
        specs = [("fresh", "P", ORANGE, "DS4 8db1d1d", "-"),
                 ("fresh", "C", BLUE,
                  "Halo preceding", "-")]
        for protocol, series, color, label, line in specs:
            pp = selected(data, protocol, series, chunk)
            assert [p["context_tokens"] for p in pp] == [32768, 65536, 131072]
            ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp],
                    color=color, lw=2.3, linestyle=line, marker="o", markersize=5,
                    markerfacecolor="white", markeredgewidth=1.5, clip_on=False)
            end_label(ax, pp[-1], label, color, fontsize=9.8, compact=True)
    fig.text(.07, .075, "Empty-context requests. Required first-use preparation included; model loading excluded.",
             fontsize=9.5, color=MUTED)
    note = "Pre-indexer campaign: matching-chunk original DS4 and Halo measurements."
    fig.text(.07, .035, note + " K = 1,024 tokens.", fontsize=9.5, color=MUTED)
    save(fig, output)


def render_current(data, output):
    fig = plt.figure(figsize=(11.8, 6.1))
    ax = fig.add_axes([.07, .23, .73, .54])
    header(fig, "Full-prompt prefill with the indexer upgrade",
           "DeepSeek V4 Flash 0731  ·  AMD Strix Halo, 128 GB  ·  2K chunks")
    style(ax, [32768, 65536, 131072], 131072)
    ax.set_ylabel("Prefill (token/s)", labelpad=14, color=MUTED, fontsize=10)
    for protocol, series, color, label in [("indexer_fresh", "indexer_B", BLUE, "DS4 Halo + indexer"),
                                         ("fresh", "P", ORANGE, "DS4 8db1d1d")]:
        pp = selected(data, protocol, series, 2048)
        ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp],
                color=color, lw=2.6, marker="o", markersize=5,
                markerfacecolor="white", markeredgewidth=1.5, clip_on=False)
        end_label(ax, pp[-1], label, color)
        for p in pp[:-1]:
            ax.annotate(f"{p['prefill_tps']:.2f}", (p["context_tokens"], p["prefill_tps"]),
                        xytext=(0, 12), textcoords="offset points", ha="center", color=color, fontsize=10)
    fig.text(.07, .075, "Complete empty-context prompts. First-use preparation included; model loading excluded.", fontsize=9.5, color=MUTED)
    fig.text(.07, .035, "Recorded campaigns: upstream September 25, indexer upgrade September 26. K = 1,024 tokens.", fontsize=9.5, color=MUTED)
    save(fig, output)


def render_best(selection, output):
    fig = plt.figure(figsize=(11.8, 6.1))
    ax = fig.add_axes([.07, .23, .73, .54])
    header(fig, "Best recorded full-prompt prefill",
           "DeepSeek V4 Flash 0731  ·  AMD Strix Halo, 128 GB  ·  Best chunk at each context")
    style(ax, [32768, 65536, 131072], 131072)
    ax.set_ylabel("Prefill (token/s)", labelpad=14, color=MUTED, fontsize=10)
    for key, color, label in [("halo", BLUE, "Halo best recorded"), ("upstream", ORANGE, "DS4 8db1d1d")]:
        pp = [r[key] for r in selection["points"]]
        ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp],
                color=color, lw=2.6, marker="o", markersize=5,
                markerfacecolor="white", markeredgewidth=1.5, clip_on=False)
        end_label(ax, pp[-1], label, color)
        for p in pp[:-1]:
            ax.annotate(f"{p['prefill_tps']:.2f}", (p["context_tokens"], p["prefill_tps"]),
                        xytext=(0, 12), textcoords="offset points", ha="center", color=color, fontsize=10)
    for r in selection["points"]:
        p = r["halo"]
        ax.annotate(r["halo_configuration"], (p["context_tokens"], p["prefill_tps"]),
                    xytext=(0, -22), textcoords="offset points", ha="center", color=BLUE, fontsize=9)
    fig.text(.07, .075, "Complete empty-context prompts. Best results from archived campaigns; chunk selection is shown at each point.", fontsize=9.5, color=MUTED)
    fig.text(.07, .035, "Upstream best setting: 2K chunks. First-use preparation included, model loading excluded. K = 1,024 tokens.", fontsize=9.5, color=MUTED)
    save(fig, output)

def render_overview(overview, output):
    """Independent protocol panels, never a curve across different workloads."""
    fig = plt.figure(figsize=(12.8, 12.8))
    fig.text(.07, .955, "Original DS4 vs DS4 Halo", fontsize=23, weight="bold", color=INK)
    fig.text(.07, .925, "DeepSeek V4 Flash 0731  ·  Strix Halo, 128 GB  ·  Recorded September / October campaigns", fontsize=11, color=MUTED)
    fig.text(.07, .902, "Original DS4: upstream 8db1d1d. Panels separate protocols, dates and the two Strix Halo systems.", fontsize=10, color=MUTED)
    panels = {p["id"]: p for p in overview["panels"]}

    fig.text(.07, .855, "Historical incremental prefill · context starts at 2K", fontsize=15, weight="bold", color=INK)
    ax = fig.add_axes([.07, .655, .72, .165])
    style(ax, [2048, 8192, 16384, 32768, 49152, 65536], 65536)
    ax.set_ylabel("Prefill (token/s)", labelpad=14, color=MUTED, fontsize=10)
    for series, color, label in [("C", BLUE, "DS4 Halo"), ("P", ORANGE, "DS4 8db1d1d")]:
        pp = sorted([p for p in panels["incremental"]["points"] if p["series"] == series], key=lambda p: p["context_tokens"])
        assert [p["context_tokens"] for p in pp] == list(range(2048, 65537, 2048))
        ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp], color=color, lw=2.5)
        end_label(ax, pp[-1], label, color, fontsize=10)
    fig.text(.07, .585, "Each interval adds 2,048 tokens; two observations per frontier. Pre-indexer Halo checkpoint.", fontsize=9.5, color=MUTED)

    fig.text(.07, .555, "Latest prepared complete 4K request · October 6 · IOMMU off", fontsize=15, weight="bold", color=INK)
    ax = fig.add_axes([.20, .405, .59, .11])
    pair = panels["resident_4k"]["comparison"]
    rates = [pair["control_tps"], pair["halo_tps"]]
    ax.barh([1, 0], rates, height=.42, color=[ORANGE, BLUE])
    ax.set_xlim(0, 510)
    ax.set_ylim(-.5, 1.5)
    ax.set_yticks([1, 0], ["DS4 8db1d1d", "DS4 Halo"])
    ax.set_xticks([0, 100, 200, 300, 400, 500])
    ax.tick_params(axis="both", length=0, pad=9, colors=MUTED, labelsize=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="x", color="#DEE6ED", lw=.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Prefill (token/s)", labelpad=10, color=MUTED, fontsize=10)
    for y, rate, color in zip([1, 0], rates, [ORANGE, BLUE]):
        ax.annotate(f"{rate:.2f}", (rate, y), xytext=(8, 0), textcoords="offset points", va="center", fontsize=11, color=color)
    fig.text(.82, .45, f"+{pair['throughput_gain_percent']:.2f}%", fontsize=16, weight="bold", color=BLUE)
    fig.text(.07, .35, "Second Halo system: two independent processes per engine, each with 3 pure warmups + 1 sample; generation disabled.", fontsize=9.5, color=MUTED)

    fig.text(.07, .295, "Historical complete first-use prompts · 2K chunks + indexer", fontsize=15, weight="bold", color=INK)
    ax = fig.add_axes([.07, .125, .72, .135])
    style(ax, [32768, 65536, 131072], 131072)
    ax.set_xlabel("Complete prompt (tokens)", labelpad=15, color=MUTED, fontsize=10)
    ax.set_ylabel("Prefill (token/s)", labelpad=14, color=MUTED, fontsize=10)
    for series, color, label in [("indexer_B", BLUE, "DS4 Halo + indexer"), ("P", ORANGE, "DS4 8db1d1d")]:
        pp = sorted([p for p in panels["fresh_2k_indexer"]["points"] if p["series"] == series], key=lambda p: p["context_tokens"])
        assert [p["context_tokens"] for p in pp] == [32768, 65536, 131072]
        ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp], color=color, lw=2.5,
                marker="o", markersize=5, markerfacecolor="white", markeredgewidth=1.5, clip_on=False)
        end_label(ax, pp[-1], label, color, fontsize=10)
        for p in pp[:-1]:
            ax.annotate(f"{p['prefill_tps']:.2f}", (p["context_tokens"], p["prefill_tps"]), xytext=(0, 12),
                        textcoords="offset points", ha="center", color=color, fontsize=10)
    fig.text(.07, .043, "Required first-use preparation included; loading excluded. Original DS4 Sep 25, indexer Sep 26; not contemporary A/B.", fontsize=9.5, color=MUTED)
    fig.text(.07, .017, "No line connects different protocols. Full-precision records and source identities accompany the figures. K = 1,024 tokens.", fontsize=9.5, color=MUTED)
    save(fig, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    parser.add_argument("--overview-only", action="store_true", help="update the overview without rewriting archived plots")
    args = parser.parse_args()
    data = json.loads((HERE / "prefill-context-data.json").read_text(encoding="utf-8"))
    for p in data["points"]:
        assert abs(p["mean_seconds"] - statistics.mean(p["individual_seconds"])) < 1e-9
        assert abs(p["prefill_tps"] - p["added_tokens"] / p["mean_seconds"]) < 1e-9
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "svg.fonttype": "none", "pdf.fonttype": 42})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if not args.overview_only:
        render_incremental(data, args.output_dir / "prefill-context-incremental")
    selection = json.loads((HERE / "best-recorded-selection.json").read_text(encoding="utf-8"))
    for row in selection["points"]:
        for key in ["halo", "upstream"]:
            assert row[key] in data["points"]
    if not args.overview_only:
        render_previous(data, args.output_dir / "prefill-context-four-variants")
        render_current(data, args.output_dir / "prefill-context-indexer-update")
        render_best(selection, args.output_dir / "prefill-context-best-recorded")
    overview = json.loads((HERE / "prefill-context-overview.json").read_text(encoding="utf-8"))
    for name, sha in overview["source_bindings"].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == sha
    assert overview["schema"] == 4
    latest = json.loads((HERE.parent / "halo2-qualification.json").read_text(encoding="utf-8"))
    assert latest["timing"]["IOMMU"] == "off" and latest["timing"]["minimum_pass"]
    pair = next(p for p in overview["panels"] if p["id"] == "resident_4k")["comparison"]
    assert pair["control_tps"] == latest["timing"]["summary"]["upstream"]["mean_tok_s"]
    assert pair["halo_tps"] == latest["timing"]["summary"]["fork"]["mean_tok_s"]
    assert pair["throughput_gain_percent"] == latest["timing"]["mean_gain_percent"]
    for panel in overview["panels"]:
        for point in panel.get("points", []):
            assert point in data["points"]
    render_overview(overview, args.output_dir / "prefill-context-overview")


if __name__ == "__main__":
    main()
