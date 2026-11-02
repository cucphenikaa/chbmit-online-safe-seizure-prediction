"""Generate the publication Fig. 1 pipeline using only Matplotlib primitives."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
PNG_OUT = ROOT / "figures" / "Fig1.png"
PDF_OUT = ROOT / "figures" / "Fig1_pipeline_vector.pdf"

NAVY = "#163B57"
BLUE = "#2F80ED"
TEAL = "#118C82"
ORANGE = "#F2994A"
PURPLE = "#7A5AA6"
RED = "#D64B4B"
INK = "#183247"
MUTED = "#667B8A"
BORDER = "#CAD5DE"
PANEL = "#F6F8FA"
WHITE = "#FFFFFF"


def rounded(ax, x, y, w, h, *, fc=WHITE, ec=BORDER, lw=1.3,
            radius=0.016, linestyle="-", z=1):
    p = FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0.006,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=linestyle, zorder=z,
    )
    ax.add_patch(p)
    return p


def text(ax, x, y, value, *, size=14, color=INK, weight="normal",
         ha="left", va="center", z=5, linespacing=1.08):
    return ax.text(x, y, value, fontsize=size, color=color, fontweight=weight,
                   ha=ha, va=va, zorder=z, linespacing=linespacing)


def header(ax, x, y, w, number, title, color):
    ax.plot([x + 0.018, x + w - 0.018], [y, y], color=color, lw=4,
            solid_capstyle="round", zorder=4)
    ax.add_patch(Circle((x + 0.034, y - 0.044), 0.022, facecolor=color,
                        edgecolor=color, zorder=5))
    text(ax, x + 0.034, y - 0.044, number, size=13, color=WHITE,
         weight="bold", ha="center")
    text(ax, x + 0.068, y - 0.044, title, size=17, weight="bold")


def arrow(ax, start, end, color=NAVY, style="-|>", lw=2.0, scale=16):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style,
                                mutation_scale=scale, linewidth=lw,
                                color=color, zorder=10))


def pill(ax, x, y, w, h, label, color, *, fill=WHITE, size=11.5):
    rounded(ax, x, y, w, h, fc=fill, ec=color, lw=1.2, radius=0.012, z=3)
    text(ax, x + w / 2, y + h / 2, label, size=size, color=color,
         weight="bold", ha="center")


def waveform(ax, x, y, w, h):
    t = np.linspace(0, 1, 250)
    sig = (0.70 * np.sin(2 * np.pi * 3.1 * t) +
           0.20 * np.sin(2 * np.pi * 8.3 * t + 0.4) +
           0.10 * np.sin(2 * np.pi * 17.0 * t))
    sig /= np.max(np.abs(sig))
    ax.plot(x + w * t, y + h / 2 + 0.36 * h * sig, color=BLUE,
            lw=2.2, solid_capstyle="round", zorder=5)


def temporal_bar(ax, x, y, w, h=0.043):
    proportions = [0.23, 0.17, 0.28, 0.10, 0.14, 0.08]
    colors = ["#BFE3D8", "#D9DEE3", "#F4C4C7", "#E55256", "#F1B49A", WHITE]
    labels = ["Interictal", "Excluded", "Preictal", "Ictal", "Post", "Gap"]
    cursor = x
    for frac, color, label in zip(proportions, colors, labels):
        sw = w * frac
        ax.add_patch(Rectangle((cursor, y), sw, h, facecolor=color,
                               edgecolor=MUTED, linewidth=0.8,
                               hatch="///" if label == "Gap" else None, zorder=3))
        text(ax, cursor + sw / 2, y + h / 2, label, size=8.7,
             color=WHITE if label == "Ictal" else INK,
             weight="bold" if label in {"Preictal", "Ictal"} else "normal",
             ha="center")
        cursor += sw


def data_card(ax, x, y, w, h):
    rounded(ax, x, y, w, h)
    header(ax, x, y + h - 0.014, w, "1", "EEG & labels", BLUE)
    rounded(ax, x + 0.018, y + 0.145, w - 0.036, 0.102,
            fc="#F1F6FD", ec="#D8E8FA", lw=1.0, radius=0.012)
    text(ax, x + w / 2, y + 0.222, "CHB-MIT scalp EEG", size=12.5,
         weight="bold", ha="center")
    waveform(ax, x + 0.043, y + 0.151, w - 0.086, 0.055)
    pill(ax, x + 0.022, y + 0.095, 0.098, 0.037, "10 patients", BLUE, size=9.8)
    pill(ax, x + 0.130, y + 0.095, 0.098, 0.037, "43 seizures", BLUE, size=9.8)
    temporal_bar(ax, x + 0.022, y + 0.040, w - 0.044, h=0.039)
    text(ax, x + w / 2, y + 0.014,
         "10-s epochs  •  preictal 30 min  •  SPH 0",
         size=8.2, color=MUTED, weight="bold", ha="center")


def representations_card(ax, x, y, w, h):
    rounded(ax, x, y, w, h)
    header(ax, x, y + h - 0.014, w, "2", "Representations", TEAL)
    rows = [
        ("F1", "Handcrafted local EEG", "900", BLUE, "#F1F6FD"),
        ("F2", "PLI graph", "485", TEAL, "#EEF8F6"),
        ("F3", "pd-wPLI graph", "485", TEAL, "#EEF8F6"),
        ("F4–F7", "Block-balanced fusion", "970–1870", PURPLE, "#F6F1FA"),
    ]
    start = y + h - 0.128
    for i, (code, name, count, color, fill) in enumerate(rows):
        yy = start - i * 0.060
        rounded(ax, x + 0.018, yy, w - 0.036, 0.047, fc=fill, ec=fill,
                lw=0.5, radius=0.009)
        text(ax, x + 0.030, yy + 0.024, code, size=10.8, color=color,
             weight="bold")
        name_x = x + (0.094 if code == "F4–F7" else 0.074)
        text(ax, name_x, yy + 0.024, name, size=9.1, weight="bold")
    pill(ax, x + 0.035, y + 0.002, w - 0.070, 0.030,
         "Training-only MI  •  top 20 per fold", TEAL, size=7.7)


def learning_card(ax, x, y, w, h):
    rounded(ax, x, y, w, h)
    header(ax, x, y + h - 0.014, w, "3", "Leakage control", ORANGE)
    text(ax, x + 0.020, y + h - 0.102, "Outer seizure-wise LOSO", size=12.5,
         weight="bold")
    block_x = x + 0.020
    for i, name in enumerate(["1", "2", "3", "4", "test"]):
        held = name == "test"
        bw = 0.052
        rounded(ax, block_x + i * 0.060, y + h - 0.172, bw, 0.047,
                fc=ORANGE if held else PANEL, ec=ORANGE, lw=1.1, radius=0.007)
        text(ax, block_x + i * 0.060 + bw / 2, y + h - 0.148, name,
             size=10.5, color=WHITE if held else MUTED, weight="bold", ha="center")
    rounded(ax, x + 0.018, y + 0.050, w - 0.036, 0.095,
            fc="#FFF7EF", ec="#F5C28D", lw=1.0, radius=0.012)
    text(ax, x + 0.032, y + 0.128, "TRAINING FOLDS ONLY", size=9.3,
         color=ORANGE, weight="bold")
    labels = ["Balance 1:1", "Scale", "MI top 20", "Grouped CV"]
    widths = [0.074, 0.055, 0.075, 0.080]
    cursor = x + 0.030
    for i, (lab, pw) in enumerate(zip(labels, widths)):
        pill(ax, cursor, y + 0.069, pw, 0.037, lab, ORANGE, size=7.3)
        cursor += pw + 0.010
        if i < len(labels) - 1:
            arrow(ax, (cursor - 0.008, y + 0.087), (cursor + 0.002, y + 0.087),
                  color=ORANGE, lw=1.1, scale=10)

    text(ax, x + w / 2, y + 0.021,
         "RF  •  XGB  •  SVM-RBF  •  cross-fitted streams",
         size=8.0, color=PURPLE, weight="bold", ha="center")


def metric_boxes(ax, x, y, total_w, labels, color):
    gap = 0.012
    bw = (total_w - gap * (len(labels) - 1)) / len(labels)
    for i, lab in enumerate(labels):
        pill(ax, x + i * (bw + gap), y, bw, 0.048, lab, color, size=12)


def evaluation_panel(ax, x, y, w, h):
    rounded(ax, x, y, w, h, fc=WHITE, ec=BORDER, lw=1.3, radius=0.018)
    ax.plot([x + 0.018, x + w - 0.018], [y + h - 0.014, y + h - 0.014],
            color=PURPLE, lw=4, solid_capstyle="round", zorder=4)
    ax.add_patch(Circle((x + 0.034, y + h - 0.058), 0.022,
                        facecolor=PURPLE, edgecolor=PURPLE, zorder=5))
    text(ax, x + 0.034, y + h - 0.058, "4", size=13, color=WHITE,
         weight="bold", ha="center")
    text(ax, x + 0.068, y + h - 0.058, "Dual evaluation", size=17,
         weight="bold")

    lane_y, lane_h = y + 0.025, h - 0.105
    lane_w = (w - 0.070) / 2
    left_x, right_x = x + 0.022, x + 0.048 + lane_w

    rounded(ax, left_x, lane_y, lane_w, lane_h, fc="#F1F6FD", ec=BLUE,
            lw=1.3, radius=0.013)
    text(ax, left_x + lane_w / 2, lane_y + lane_h - 0.038,
         "CONTROLLED EPOCH TEST", size=12.5, color=BLUE, weight="bold", ha="center")
    text(ax, left_x + lane_w / 2, lane_y + lane_h - 0.084,
         "180 preictal + 540 interictal  •  fixed 1:3 test",
         size=9.1, color=MUTED, weight="bold", ha="center")
    metric_boxes(ax, left_x + 0.036, lane_y + 0.031, lane_w - 0.072,
                 ["BAcc", "MCC"], BLUE)

    rounded(ax, right_x, lane_y, lane_w, lane_h, fc="#EEF8F6", ec=TEAL,
            lw=1.3, radius=0.013)
    text(ax, right_x + lane_w / 2, lane_y + lane_h - 0.038,
         "ONLINE-SAFE CONTINUOUS STREAM", size=12.5, color=TEAL,
         weight="bold", ha="center")
    text(ax, right_x + lane_w / 2, lane_y + lane_h - 0.083,
         "21/30 positives  •  30-min refractory  •  no phase labels",
         size=8.8, color=MUTED, weight="bold", ha="center")
    metric_boxes(ax, right_x + 0.030, lane_y + 0.031, lane_w - 0.060,
                 ["SS", "FAR/h", "TTW"], TEAL)


def audit_band(ax, x, y, w, h):
    rounded(ax, x, y, w, h, fc=PANEL, ec=BORDER, lw=1.2, radius=0.014)
    text(ax, x + 0.020, y + h - 0.026, "ROBUSTNESS & AUDIT TRAIL", size=10.5,
         color=NAVY, weight="bold")
    items = [
        ("All 21 configurations", PURPLE, 0.122),
        ("Rate-matched chance", PURPLE, 0.116),
        (r"$\geq$5-min warning", RED, 0.100),
        ("10-min guard", ORANGE, 0.090),
        ("Forward chaining", ORANGE, 0.103),
        ("No gamma", TEAL, 0.075),
        ("Seeds 42–46", BLUE, 0.084),
    ]
    cursor = x + 0.020
    for lab, color, pw in items:
        pill(ax, cursor, y + 0.013, pw, 0.042, lab, color, size=7.6)
        cursor += pw + 0.008


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "pdf.fonttype": 42,
        "savefig.facecolor": WHITE,
    })
    fig, ax = plt.subplots(figsize=(13.2, 8.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    text(ax, 0.035, 0.965,
         "Leakage-controlled evaluation of patient-specific seizure prediction",
         size=20, color=NAVY, weight="bold")
    text(ax, 0.035, 0.928,
         "From retrospective EEG states to label-blind, continuous-stream alarms",
         size=12.5, color=MUTED)

    top_y, top_h = 0.545, 0.345
    data_card(ax, 0.035, top_y, 0.250, top_h)
    representations_card(ax, 0.310, top_y, 0.250, top_h)
    learning_card(ax, 0.585, top_y, 0.380, top_h)
    arrow(ax, (0.289, 0.705), (0.306, 0.705))
    arrow(ax, (0.564, 0.705), (0.581, 0.705))

    evaluation_panel(ax, 0.085, 0.190, 0.830, 0.285)
    arrow(ax, (0.775, 0.540), (0.775, 0.482), color=PURPLE)
    text(ax, 0.775, 0.505, "same held-out seizure", size=9.2,
         color=PURPLE, weight="bold", ha="center")

    audit_band(ax, 0.035, 0.045, 0.930, 0.105)

    PNG_OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_OUT, dpi=360, bbox_inches="tight", pad_inches=0.08)
    fig.savefig(PDF_OUT, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(PNG_OUT)
    print(PDF_OUT)


if __name__ == "__main__":
    main()
