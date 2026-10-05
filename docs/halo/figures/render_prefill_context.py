"""Publication charts from archived data. No engine or hardware execution.

Requires Python 3.11+ and matplotlib; run from any directory.
"""
from pathlib import Path
import argparse
import json
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

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
    for series, color, label in [("C", BLUE, "Halo"), ("P", ORANGE, "Local upstream")]:
        pp = selected(data, "incremental", series, 2048)
        assert [p["context_tokens"] for p in pp] == list(range(2048, 65537, 2048))
        ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp],
                color=color, lw=2.6, solid_capstyle="round")
        end_label(ax, pp[-1], label, color)
    fig.text(.07, .075, "Incremental prefill: each measurement adds 2,048 tokens. Loading, decode and restore are excluded.",
             fontsize=9.5, color=MUTED)
    fig.text(.07, .035, "32 measured frontiers per curve. Local upstream = rebuilt upstream8db. K = 1,024 tokens.",
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
        specs = [("fresh", "P", ORANGE, "Local upstream", "-"),
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
    note = "Pre-indexer campaign: matching-chunk local upstream and Halo measurements."
    fig.text(.07, .035, note + " K = 1,024 tokens.", fontsize=9.5, color=MUTED)
    save(fig, output)


def render_current(data, output):
    fig = plt.figure(figsize=(11.8, 6.1))
    ax = fig.add_axes([.07, .23, .73, .54])
    header(fig, "Full-prompt prefill with the indexer upgrade",
           "DeepSeek V4 Flash 0731  ·  AMD Strix Halo, 128 GB  ·  2K chunks")
    style(ax, [32768, 65536, 131072], 131072)
    ax.set_ylabel("Prefill (token/s)", labelpad=14, color=MUTED, fontsize=10)
    for protocol, series, color, label in [("indexer_fresh", "indexer_B", BLUE, "Halo + indexer"),
                                         ("fresh", "P", ORANGE, "Local upstream")]:
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
    for key, color, label in [("halo", BLUE, "Halo best recorded"), ("upstream", ORANGE, "Local upstream")]:
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

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    data = json.loads((HERE / "prefill-context-data.json").read_text(encoding="utf-8"))
    for p in data["points"]:
        assert abs(p["mean_seconds"] - statistics.mean(p["individual_seconds"])) < 1e-9
        assert abs(p["prefill_tps"] - p["added_tokens"] / p["mean_seconds"]) < 1e-9
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "svg.fonttype": "none", "pdf.fonttype": 42})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    render_incremental(data, args.output_dir / "prefill-context-incremental")
    selection = json.loads((HERE / "best-recorded-selection.json").read_text(encoding="utf-8"))
    for row in selection["points"]:
        for key in ["halo", "upstream"]:
            assert row[key] in data["points"]
    render_previous(data, args.output_dir / "prefill-context-four-variants")
    render_current(data, args.output_dir / "prefill-context-indexer-update")
    render_best(selection, args.output_dir / "prefill-context-best-recorded")


if __name__ == "__main__":
    main()
