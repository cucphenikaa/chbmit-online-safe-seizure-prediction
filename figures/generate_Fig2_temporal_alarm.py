"""Generate the temporal-label and online-safe alarm schematic used as Fig. 2."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "Fig2.png"

NAVY = "#173F5F"
TEAL = "#148F83"
RED = "#CF3338"
PURPLE = "#7651A8"
ORANGE = "#E67E22"
GREY = "#536975"


def segment(ax, x, width, label, color, *, text_color="#1F2933", hatch=None, weight="normal"):
    patch = Rectangle(
        (x, 0.53), width, 0.17, facecolor=color, edgecolor=GREY,
        linewidth=1.1, hatch=hatch, zorder=2,
    )
    ax.add_patch(patch)
    ax.text(x + width / 2, 0.615, label, ha="center", va="center",
            fontsize=9.2, color=text_color, fontweight=weight, linespacing=1.05)


def panel_a(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.01, 0.94, "(a)", fontsize=13, fontweight="bold", color="#111827")
    ax.text(0.50, 0.95, "Retrospective temporal states used only for scoring",
            ha="center", va="center", fontsize=12.5, fontweight="bold", color="#111827")

    x0 = 0.03
    widths = [0.16, 0.13, 0.19, 0.075, 0.12, 0.12, 0.075, 0.08]
    labels = [
        "Eligible\ninterictal", "Excluded", "Preictal\n30 min", "Ictal",
        "Postictal\n1 h", "Excluded", "Recording\ngap", "Eligible\ninterictal",
    ]
    colors = ["#BFE3D8", "#D9DEE3", "#F4C4C7", "#DF4B50",
              "#F2B79E", "#D9DEE3", "white", "#BFE3D8"]
    hatches = [None, None, None, None, None, None, "///", None]
    text_colors = ["#1F2933", "#1F2933", "#1F2933", "white",
                   "#1F2933", "#1F2933", "#1F2933", "#1F2933"]
    weights = ["normal", "normal", "bold", "bold", "normal", "normal", "normal", "normal"]

    xs = []
    x = x0
    for w, label, color, hatch, tc, fw in zip(widths, labels, colors, hatches, text_colors, weights):
        xs.append(x)
        segment(ax, x, w, label, color, text_color=tc, hatch=hatch, weight=fw)
        x += w

    # Exact temporal criteria, shown outside the blocks to keep the state labels legible.
    ax.text(xs[0] + widths[0] / 2, 0.46, r"$\leq$ onset $-$ 4 h",
            ha="center", fontsize=8.8, color=TEAL, fontweight="bold")
    ax.text(xs[1] + widths[1] / 2, 0.46, "4 h to 30 min\nbefore onset",
            ha="center", va="top", fontsize=8.2, color=GREY, linespacing=1.05)
    ax.text(xs[4] + widths[4] / 2, 0.46, "first hour\nafter offset",
            ha="center", va="top", fontsize=8.2, color=GREY, linespacing=1.05)
    ax.text(xs[5] + widths[5] / 2, 0.46, "1--4 h\nafter offset",
            ha="center", va="top", fontsize=8.2, color=GREY, linespacing=1.05)
    ax.text(xs[7] + widths[7] / 2, 0.46, r"$\geq$ offset $+$ 4 h",
            ha="center", fontsize=8.8, color=TEAL, fontweight="bold")

    # SOP arrow above the preictal block.
    pre_l, pre_r = xs[2], xs[2] + widths[2]
    ax.annotate("", xy=(pre_l, 0.79), xytext=(pre_r, 0.79),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
    ax.text((pre_l + pre_r) / 2, 0.84, "SOP = 30 min; SPH = 0",
            ha="center", fontsize=10, color="#374151")

    # FAR eligibility bars.
    for left, width in ((xs[0], widths[0]), (xs[7], widths[7])):
        ax.plot([left, left + width], [0.31, 0.31], color=TEAL, lw=4,
                solid_capstyle="round")
        ax.text(left + width / 2, 0.245, "EligibleForFAR = 1",
                ha="center", fontsize=8.8, color=TEAL)

    ax.text(0.50, 0.11,
            "Excluded = recorded EEG inside the 4-h seizure-proximity margins that is not preictal, ictal, or postictal.",
            ha="center", fontsize=8.6, color=GREY)
    ax.text(0.98, 0.04, "Schematic not to scale", ha="right", fontsize=8.2,
            color="#6B7280", style="italic")


def panel_b(ax):
    ax.set_xlim(-8, 46)
    ax.set_ylim(-0.05, 1.0)
    ax.spines[["left", "right", "top"]].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0.10))
    ax.spines["bottom"].set_linewidth(1.2)
    ax.set_yticks([])
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.tick_params(axis="x", labelsize=10, length=6, width=1.1)
    ax.set_xlabel("Monitoring time (min)", fontsize=11.5, labelpad=7)
    ax.text(-7.8, 0.93, "(b)", fontsize=13, fontweight="bold", color="#111827")
    ax.text(19, 0.94, "Causal alarm generation and retrospective scoring",
            ha="center", fontsize=12.5, fontweight="bold", color="#111827")

    alarm_t, onset_t, rearm_t = 5, 25, 35
    # Thirty binary predictions preceding the alarm; orange marks positive epochs.
    for i in range(30):
        x = alarm_t - 5 + i / 6
        color = ORANGE if i in {0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 16, 17, 19, 20, 22, 23, 25, 27, 29} else "#D9DEE3"
        ax.vlines(x, 0.52, 0.66, color=color, lw=2.0)

    ax.text(-1.9, 0.75, "5-min causal window: 21/30 positive epochs",
            fontsize=9.6, color="#374151", fontweight="bold", ha="left")

    ax.axvline(alarm_t, ymin=0.14, ymax=0.84, color=NAVY, lw=2.4)
    ax.text(alarm_t, 0.82, "ALARM", ha="center", fontsize=13,
            color=NAVY, fontweight="bold")
    ax.axvline(onset_t, ymin=0.14, ymax=0.84, color=RED, lw=2.6)
    ax.scatter([onset_t], [0.66], marker="^", s=120, color=RED, zorder=4)
    ax.text(onset_t, 0.82, "SEIZURE ONSET", ha="center", fontsize=13,
            color=RED, fontweight="bold")

    ax.add_patch(Rectangle((alarm_t, 0.52), rearm_t - alarm_t, 0.14,
                           facecolor="#DDF0D7", edgecolor="#62B968", lw=1.2))
    ax.text((alarm_t + rearm_t) / 2, 0.59,
            "30-min refractory lockout; alarm history reset",
            ha="center", va="center", fontsize=9.2, color="#3F8A49")
    ax.add_patch(Rectangle((rearm_t, 0.52), 5, 0.14,
                           facecolor="#FFF3D3", edgecolor="#D89B00", lw=1.2))
    ax.text(37.5, 0.59, "Re-arm", ha="center", va="center", fontsize=9.2,
            color="#374151")

    ax.annotate("", xy=(alarm_t, 0.38), xytext=(onset_t, 0.38),
                arrowprops=dict(arrowstyle="<->", color=PURPLE, lw=1.8))
    ax.text((alarm_t + onset_t) / 2, 0.31,
            "TTW = onset $-$ first valid alarm", ha="center", fontsize=9.8,
            color=PURPLE)
    ax.text(-2.7, 0.18,
            "A trigger is a false alarm only when it occurs during eligible interictal time",
            fontsize=8.8, color=GREY, ha="left")


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#20262E",
        "savefig.facecolor": "white",
    })
    fig = plt.figure(figsize=(12.2, 8.0), constrained_layout=False)
    gs = fig.add_gridspec(2, 1, height_ratios=[1.03, 1.10], hspace=0.04,
                          left=0.055, right=0.985, top=0.985, bottom=0.08)
    panel_a(fig.add_subplot(gs[0]))
    panel_b(fig.add_subplot(gs[1]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=320, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(OUT)


if __name__ == "__main__":
    main()
