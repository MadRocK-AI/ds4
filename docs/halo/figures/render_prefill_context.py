"""Recorded Halo curves and separately labeled official DS4 reference. No hardware execution.
Requires Python 3.11+ and matplotlib.
"""
from pathlib import Path
import argparse, json, statistics, hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FixedLocator, FuncFormatter

HERE = Path(__file__).resolve().parent
BLUE, ORANGE, INK, MUTED = "#0868B2", "#A75B20", "#182D42", "#586D80"

def save(fig, output):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for label in [*fig.texts, *(t for ax in fig.axes for t in ax.texts)]:
        box = label.get_window_extent(renderer)
        assert fig.bbox.contains(box.x0, box.y0) and fig.bbox.contains(box.x1, box.y1), "Clipped text"
    for ax in fig.axes:
        boxes = [t.get_window_extent(renderer) for t in ax.texts]
        for i,box in enumerate(boxes):
            assert not any(box.overlaps(other) for other in boxes[i+1:]), "Overlapping labels"
    for extension in ("png", "svg", "pdf"):
        path = output.with_suffix("."+extension)
        fig.savefig(path, dpi=240, facecolor="white")
        if extension == "svg":
            path.write_bytes(b"\n".join(line.rstrip(b" \t\r") for line in path.read_bytes().splitlines())+b"\n")
    plt.close(fig)

def selected(data, protocol, series, chunk):
    return sorted([p for p in data["points"] if p["protocol"]==protocol and p["series"]==series and p["chunk_tokens"]==chunk],key=lambda p:p["context_tokens"])

def style(ax, ticks):
    ax.set_xlim(ticks[0], ticks[-1]); ax.set_ylim(0,500)
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,_:f"{x/1024:g}K"))
    ax.set_yticks([0,100,200,300,400,500])
    ax.grid(axis="y",color="#DEE6ED",lw=.8);ax.set_axisbelow(True)
    for name in ("top","right","left"):ax.spines[name].set_visible(False)
    ax.spines["bottom"].set_color("#B9C8D4")
    ax.tick_params(axis="both",length=0,pad=9,colors=MUTED,labelsize=10)
    ax.set_xlabel("Context (tokens)",labelpad=15,color=MUTED,fontsize=10)
    ax.set_ylabel("Prefill (token/s)",labelpad=14,color=MUTED,fontsize=10)

def curve(ax, pp, label, markers=True):
    ax.plot([p["context_tokens"] for p in pp],[p["prefill_tps"] for p in pp],color=BLUE,lw=2.6,
            marker="o" if markers else None,markersize=5,markerfacecolor="white",markeredgewidth=1.5,clip_on=False)
    last=pp[-1]
    ax.annotate(f"{label}\n{last['prefill_tps']:.2f} token/s",(last["context_tokens"],last["prefill_tps"]),
                xytext=(14,0),textcoords="offset points",va="center",fontsize=10,color=BLUE,annotation_clip=False)
    if markers:
        for index,p in enumerate(pp[:-1]):
            ax.annotate(f"{p['prefill_tps']:.2f}",(p["context_tokens"],p["prefill_tps"]),xytext=(6 if index==0 else 0,12),textcoords="offset points",ha="left" if index==0 else "center",color=BLUE,fontsize=10)

def simple(data, output, protocol, series, chunk, title, note):
    fig=plt.figure(figsize=(11.8,6.1));ax=fig.add_axes([.07,.23,.73,.54])
    fig.text(.07,.925,title,fontsize=23,weight="bold",color=INK)
    fig.text(.07,.866,"DeepSeek V4 Flash 0731 · Strix Halo, 128 GB · Historical measurements",fontsize=11,color=MUTED)
    pp=selected(data,protocol,series,chunk)
    ticks=[2048,8192,16384,32768,49152,65536] if protocol=="incremental" else [32768,65536,131072]
    style(ax,ticks);curve(ax,pp,"DS4 Halo",protocol!="incremental")
    fig.text(.07,.075,note,fontsize=9.5,color=MUTED)
    fig.text(.07,.035,"Halo results only. Official DS4 reference is reported separately. K = 1,024 tokens.",fontsize=9.5,color=MUTED)
    save(fig,output)

def render_previous(data,output):
    fig=plt.figure(figsize=(13,6.3))
    fig.text(.07,.925,"Halo full-prompt prefill · earlier 2K and 4K chunks",fontsize=23,weight="bold",color=INK)
    fig.text(.07,.866,"DeepSeek V4 Flash 0731 · Strix Halo, 128 GB · Historical pre-indexer campaign",fontsize=11,color=MUTED)
    for rect,chunk in zip(([.07,.23,.295,.51],[.57,.23,.275,.51]),(2048,4096)):
        ax=fig.add_axes(rect);style(ax,[32768,65536,131072]);ax.set_title(f"{chunk//1024}K chunks",loc="left",fontsize=12,color=INK,pad=16)
        curve(ax,selected(data,"fresh","C",chunk),"Halo")
    fig.text(.07,.075,"Empty-context prompts. Required first-use preparation included; loading excluded.",fontsize=9.5,color=MUTED)
    fig.text(.07,.035,"Separate chunk configurations; no substituted original-DS4 baseline curve. K = 1,024 tokens.",fontsize=9.5,color=MUTED)
    save(fig,output)

def render_best(selection,output):
    fig=plt.figure(figsize=(11.8,6.1));ax=fig.add_axes([.07,.23,.73,.54]);style(ax,[32768,65536,131072])
    fig.text(.07,.925,"Best recorded Halo full-prompt prefill",fontsize=23,weight="bold",color=INK)
    fig.text(.07,.866,"DeepSeek V4 Flash 0731 · Strix Halo, 128 GB · Best recorded chunk at each context",fontsize=11,color=MUTED)
    pp=[r["halo"] for r in selection["points"]];curve(ax,pp,"Halo")
    for r in selection["points"]:
        p=r["halo"];ax.annotate(r["halo_configuration"],(p["context_tokens"],p["prefill_tps"]),xytext=(0,-22),textcoords="offset points",ha="center",color=BLUE,fontsize=9)
    fig.text(.07,.075,"Archived campaigns; selected chunk is labeled. First-use preparation included; loading excluded.",fontsize=9.5,color=MUTED)
    fig.text(.07,.035,"Official DS4 reference is reported separately. K = 1,024 tokens.",fontsize=9.5,color=MUTED)
    save(fig,output)

def render_overview(data, latest, output):
    fig=plt.figure(figsize=(12.8,12.8))
    fig.text(.07,.955,"DS4 Halo prefill",fontsize=23,weight="bold",color=INK)
    fig.text(.07,.925,"DeepSeek V4 Flash 0731 · Strix Halo, 128 GB · Recorded September / October campaigns",fontsize=11,color=MUTED)
    fig.text(.07,.902,"Official DS4 reference: 295.27 token/s, 2K→4K interval. Different protocol; no inferred speedup.",fontsize=10,color=MUTED)
    fig.text(.07,.855,"Historical incremental prefill · context starts at 2K",fontsize=15,weight="bold",color=INK)
    ax=fig.add_axes([.07,.655,.72,.165]);style(ax,[2048,8192,16384,32768,49152,65536])
    curve(ax,selected(data,"incremental","C",2048),"Halo",False)
    fig.text(.07,.585,"Each interval adds 2,048 tokens; two observations per frontier. Pre-indexer Halo checkpoint.",fontsize=9.5,color=MUTED)
    fig.text(.07,.545,"454.59 token/s",fontsize=32,weight="bold",color=BLUE)
    fig.text(.07,.510,"Latest complete prepared 4K request · October 6 · IOMMU off",fontsize=15,weight="bold",color=INK)
    fig.text(.07,.475,"Samples 454.52 / 454.65 · 3 pure warmups + 1 measured request per independent process",fontsize=11,color=MUTED)
    fig.text(.07,.440,"106 GiB shared GPU ceiling · Generation disabled · Loading excluded",fontsize=11,color=MUTED)
    fig.text(.07,.400,"Bitwise-identical complete FP32 logits, states and token IDs in verified cases.",fontsize=11,color=INK)
    fig.text(.07,.295,"Historical complete first-use prompts · 2K chunks + indexer",fontsize=15,weight="bold",color=INK)
    ax=fig.add_axes([.07,.125,.72,.135]);style(ax,[32768,65536,131072]);ax.set_xlabel("Complete prompt (tokens)",labelpad=15,color=MUTED,fontsize=10)
    curve(ax,selected(data,"indexer_fresh","indexer_B",2048),"Halo + indexer")
    fig.text(.07,.043,"Required first-use preparation included; loading excluded. Historical context matrix was not rerun for rc.2.",fontsize=9.5,color=MUTED)
    fig.text(.07,.017,"No line connects different protocols or campaigns. Original records are retained. K = 1,024 tokens.",fontsize=9.5,color=MUTED)
    save(fig,output)

def render_release(latest, official, output):
    rate=latest["timing"]["summary"]["fork"]["mean_tok_s"]
    ref=next(p for p in official["points"] if p["context_tokens"]==4096)["prefill_tps"]
    assert ref==295.27
    fig=plt.figure(figsize=(12.8,7.2))
    fig.text(.07,.91,"DS4 Halo on AMD Strix Halo",fontsize=25,weight="bold",color=INK)
    fig.text(.07,.855,"DeepSeek V4 Flash 0731 IQ2 · Single Radeon 8060S · 128 GB RAM",fontsize=12,color=MUTED)
    for x,color in ((.07,ORANGE),(.53,BLUE)):
        fig.add_artist(FancyBboxPatch((x,.39),.40,.34,boxstyle="round,pad=0.015,rounding_size=0.02",transform=fig.transFigure,facecolor="#F3F7FA",edgecolor="#DCE5ED"))
    fig.text(.09,.665,"Original DS4 · official published result",fontsize=12,weight="bold",color=ORANGE)
    fig.text(.09,.555,f"{ref:.2f}",fontsize=40,weight="bold",color=ORANGE)
    fig.text(.09,.505,"token/s · added 2K interval ending at 4K",fontsize=11,color=MUTED)
    fig.text(.09,.435,"Source: antirez/ds4 gfx1151 report",fontsize=10,color=MUTED)
    fig.text(.55,.665,"DS4 Halo · our recorded result",fontsize=12,weight="bold",color=BLUE)
    fig.text(.55,.555,f"{rate:.2f}",fontsize=40,weight="bold",color=BLUE)
    fig.text(.55,.505,"token/s · complete prepared 4K request",fontsize=11,color=MUTED)
    fig.text(.55,.435,"Samples: 454.52 / 454.65 token/s",fontsize=10,color=MUTED)
    fig.text(.07,.31,"Different benchmark protocols. No percentage speedup inferred between these rates.",fontsize=11,color=INK)
    fig.text(.07,.23,"Halo: 3 pure warmups + 1 measured request per process · IOMMU off · 106 GiB GPU ceiling",fontsize=11,color=MUTED)
    fig.text(.07,.16,"FP32 logits, complete serialized state and token IDs bitwise-identical in verified cases.",fontsize=11,color=INK)
    fig.text(.07,.09,"Model loading / generation excluded. No profiler, trace or payload readback during Halo timing.",fontsize=10,color=MUTED)
    fig.text(.07,.038,"Source, installer and evidence: github.com/MadRocK-AI/ds4",fontsize=10,color=MUTED)
    save(fig,output)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--output-dir",type=Path,default=HERE)
    g=p.add_mutually_exclusive_group();g.add_argument("--overview-only",action="store_true");g.add_argument("--release-only",action="store_true")
    args=p.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.fonttype":"none","pdf.fonttype":42})
    data=json.loads((HERE/"prefill-context-data.json").read_text(encoding="utf-8"))
    for point in data["points"]:
        assert abs(point["mean_seconds"]-statistics.mean(point["individual_seconds"]))<1e-9
        assert abs(point["prefill_tps"]-point["added_tokens"]/point["mean_seconds"])<1e-9
    latest=json.loads((HERE.parent/"halo2-qualification.json").read_text(encoding="utf-8"))
    official=json.loads((HERE/"official-ds4-published-context.json").read_text(encoding="utf-8"))
    assert latest["timing"]["IOMMU"]=="off" and latest["timing"]["minimum_pass"]
    overview=json.loads((HERE/"prefill-context-overview.json").read_text(encoding="utf-8"))
    for name,sha in overview["source_bindings"].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==sha
    if not args.overview_only:render_release(latest,official,args.output_dir/"prefill-4k-release")
    if args.release_only:return
    render_overview(data,latest,args.output_dir/"prefill-context-overview")
    if args.overview_only:return
    simple(data,args.output_dir/"prefill-context-incremental","incremental","C",2048,"Halo prefill as context grows","Incremental prefill: each measurement adds 2,048 tokens; loading, decode and restore excluded.")
    simple(data,args.output_dir/"prefill-context-indexer-update","indexer_fresh","indexer_B",2048,"Halo prefill with the indexer upgrade","Complete empty-context prompts, 2K chunks. Required first-use preparation included; loading excluded.")
    render_previous(data,args.output_dir/"prefill-context-four-variants")
    selection=json.loads((HERE/"best-recorded-selection.json").read_text(encoding="utf-8"))
    for row in selection["points"]:assert row["halo"] in data["points"]
    render_best(selection,args.output_dir/"prefill-context-best-recorded")

if __name__=="__main__":main()
