"""Render archived measurements; does not run the engine or access hardware.

Requires Python 3.11+ and matplotlib. Run from any directory.
"""
from pathlib import Path
import argparse
import json
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

HERE = Path(__file__).resolve().parent
BLUE, ORANGE, GRAY = "#136CB0", "#A95513", "#7890A4"


def render(data, peak, updated, output):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "svg.fonttype": "none", "pdf.fonttype": 42})
    fig, axes = plt.subplots(2, 1, figsize=(12, 10.8))
    fig.subplots_adjust(left=.09, right=.96, top=.76, bottom=.14, hspace=.56)
    fig.text(.09, .958, "Prefill on AMD Strix Halo", size=25, weight="bold", color="#172B40")
    fig.text(.09, .92, "DeepSeek V4 Flash 0731  ·  Single device, 128 GB unified memory", color="#526377", size=12)
    fig.text(.09, .878,
             f"Peak recorded mean: {peak['highest_recorded_mean']['prefill_tps']:.2f} token/s",
             color=BLUE, size=17, weight="bold")
    fig.text(.09, .852, "Resident 4K after native preparation / warmup; separate from the first-use curves below.",
             color="#526377", size=10)
    fig.text(.09, .82, "Bitwise logits, complete state and tokens preserved in the verified cases.",
             color="#263B50", size=11)
    points = data["points"]

    for ax, xmax in zip(axes, [131072, 65536]):
        ax.set_xscale("log", base=2)
        ticks = [2048 * 2**i for i in range(7) if 2048 * 2**i <= xmax]
        ax.xaxis.set_major_locator(FixedLocator(ticks))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x / 1024:g}K"))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.set_xlim(2048 / 1.14, xmax * 1.14)
        ax.set_ylim(0, 475)
        ax.set_yticks([0, 100, 200, 300, 400])
        ax.set_ylabel("Prefill (token/s)")
        ax.grid(axis="y", color="#DCE4EC", linewidth=.8)
        ax.grid(axis="x", color="#EDF1F5", linewidth=.7)
        ax.set_axisbelow(True)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["bottom", "left"]:
            ax.spines[spine].set_color("#B7C4D1")
        ax.tick_params(colors="#354B60", labelsize=10)

    ax = axes[0]
    ax.set_title("Full prompt from empty context", loc="left", weight="bold", pad=13)
    ax.set_xlabel("Full prompt / context length (tokens)")
    specs = [("fresh", "P", 2048, ORANGE, "o", "--", "Local upstream · 2K chunks"),
             ("fresh", "P", 4096, ORANGE, "s", "-", "Local upstream · 4K chunks"),
             ("fresh", "C", 2048, GRAY if updated else BLUE, "o", "--",
              "Halo · previous 2K" if updated else "Halo · 2K chunks"),
             ("fresh", "C", 4096, BLUE, "s", "-",
              "Halo · previous 4K" if updated else "Halo · 4K chunks")]
    if updated:
        specs.append(("indexer_fresh", "indexer_B", 2048, BLUE, "o", "--", "Halo · 2K + indexer"))
    for protocol, series, chunk, color, marker, style, label in specs:
        pp = sorted([p for p in points if p["protocol"] == protocol and p["series"] == series
                     and p["chunk_tokens"] == chunk], key=lambda p: p["context_tokens"])
        ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp],
                color=color, marker=marker, linestyle=style, lw=2.3, markersize=6,
                markerfacecolor="white" if marker == "o" else color, label=label)
        # Label the updated and 4K curves, avoiding overlapping old 2K values.
        if not updated or color != GRAY:
            for p in pp:
                offset = 12 if marker == "s" and series == "C" else -18
                if protocol == "indexer_fresh": offset = -22 if p["context_tokens"] == 32768 else 13
                if series == "P": offset = 12 if marker == "o" else -18
                # At 64K the current 2K and preceding 4K differ by only7.34 token/s.
                if updated and series == "C" and p["context_tokens"] == 65536: offset = -20
                position = (-30, 0) if not updated and series == "C" and marker == "o" else (0, offset)
                ax.annotate(f"{p['prefill_tps']:.2f}", (p["context_tokens"], p["prefill_tps"]),
                            xytext=position, textcoords="offset points", ha="center", fontsize=9,
                            color=color, bbox={"facecolor": "white", "edgecolor": "none", "pad": .2})
    ax.axvspan(2048 / 1.14, 4096 * 1.14, color="#F3F6F9", zorder=0)
    for arm, color in [("P", ORANGE), ("C", BLUE)]:
        for p in [p for p in points if p["protocol"] == "short_fresh" and p["series"] == arm]:
            ax.scatter(p["context_tokens"], p["prefill_tps"], marker="D", s=36,
                       facecolors="white", edgecolors=color, linewidths=1.8, zorder=5)
            ax.annotate(f"{p['prefill_tps']:.2f}", (p["context_tokens"], p["prefill_tps"]),
                        xytext=(0, 12 if arm == "C" else -18), textcoords="offset points",
                        ha="center", fontsize=9, color=color)
    ax.text(.015, .04, "◇ Short-prompt controls\nFixed 64K context allocation", transform=ax.transAxes,
            fontsize=9, color="#526377")
    ax.legend(loc="upper left", bbox_to_anchor=(.30, .96), ncol=1, fontsize=8.6,
              frameon=False, handlelength=2.5)

    ax = axes[1]
    ax.set_title("Incremental prefill · 2K tokens added at each frontier", loc="left", weight="bold", pad=13)
    ax.set_xlabel("Context frontier after the 2K increment (tokens)")
    for arm, color, label in [("P", ORANGE, "Local upstream"), ("C", BLUE, "Halo · preceding long-context chain")]:
        pp = sorted([p for p in points if p["protocol"] == "incremental" and p["series"] == arm],
                    key=lambda p: p["context_tokens"])
        ax.plot([p["context_tokens"] for p in pp], [p["prefill_tps"] for p in pp],
                color=color, marker="o", markersize=3, lw=2.1, label=label)
        for p in [pp[0], pp[1], pp[-1]]:
            ax.annotate(f"{p['prefill_tps']:.2f}", (p["context_tokens"], p["prefill_tps"]),
                        xytext=(0, 12 if arm == "C" else -18), textcoords="offset points",
                        ha="center", fontsize=9, color=color)
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    fig.text(.09, .063, "Model loading excluded; first-use preparation included. Incremental rates count only the added 2K tokens.",
             size=9, color="#526377")
    fig.text(.09, .04, "K = 1,024 tokens. Logarithmic context axis. Markers are archived measurements; lines only connect measured points.",
             size=9, color="#526377")
    fig.text(.09, .018, "Local upstream = rebuilt upstream8db control. Campaigns: September 25–26, 2026. No new benchmark.",
             size=9, color="#526377")
    for extension in ["png", "svg", "pdf"]:
        fig.savefig(output.with_suffix("." + extension), dpi=200, facecolor="white",
                    metadata={"Creator": "DS4 Halo archived measurements"} if extension != "png" else None)
        if extension == "svg":
            path = output.with_suffix(".svg")
            path.write_bytes(b"\n".join(line.rstrip(b" \t\r") for line in path.read_bytes().splitlines()) + b"\n")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    data = json.loads((HERE / "prefill-context-data.json").read_text(encoding="utf-8"))
    peak = json.loads((HERE.parent / "peak-performance.json").read_text(encoding="utf-8"))
    for p in data["points"]:
        assert abs(p["mean_seconds"] - statistics.mean(p["individual_seconds"])) < 1e-9
        assert abs(p["prefill_tps"] - p["added_tokens"] / p["mean_seconds"]) < 1e-9
    args.output_dir.mkdir(parents=True, exist_ok=True)
    render(data, peak, False, args.output_dir / "prefill-context-four-variants")
    render(data, peak, True, args.output_dir / "prefill-context-indexer-update")


if __name__ == "__main__":
    main()
