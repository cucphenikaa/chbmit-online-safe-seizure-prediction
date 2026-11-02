"""Reproduce ESM Fig. S1 from saved V11B alarm-sensitivity results."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "figure_source_data" / "v11b_targeted_alarm_sensitivity_folds.csv"
OUTPUT = ROOT / "supplementary_figures" / "FigS1.png"

NAVY = "#173B57"
TEAL = "#168C80"
GRID = "#D8DDE2"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8.4,
        "axes.titlesize": 9.5,
        "axes.labelsize": 8.6,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "axes.linewidth": 0.8,
        "savefig.facecolor": "white",
    }
)

RULES = [
    ("Legacy_90_consecutive", "90 consecutive", "X"),
    ("FP_10min_theta_0.70", "10 min / 0.70", "v"),
    ("FP_5min_theta_0.80", "5 min / 0.80", "D"),
    ("FP_5min_theta_0.70", "5 min / 0.70 (primary)", "o"),
    ("FP_2min_theta_0.70", "2 min / 0.70", "^"),
    ("FP_5min_theta_0.50", "5 min / 0.50", "s"),
]

CONFIGURATIONS = [
    ("RandomForest", "F1_Handcrafted", "RF-F1"),
    ("RandomForest", "F7_All", "RF-F7"),
    ("XGBoost", "F1_Handcrafted", "XGB-F1"),
    ("XGBoost", "F6_Handcrafted_wPLI", "XGB-F6"),
]


def operating_points(data: pd.DataFrame, model: str, feature: str):
    subset = data[
        (data["Model"] == model)
        & (data["FeatureSet"] == feature)
        & (data["AlarmGenerationMode"] == "online_safe_gap_only")
    ]
    points = []
    for rule, label, marker in RULES:
        rows = subset[subset["AlarmRule"] == rule]
        points.append(
            {
                "rule": rule,
                "label": label,
                "marker": marker,
                "far": rows["FalseAlarms"].sum()
                / rows["EligibleInterictalHours"].sum(),
                "ss": rows["SeizurePredicted"].sum() / len(rows),
            }
        )
    return points


def main() -> None:
    data = pd.read_csv(SOURCE)
    figure, axes = plt.subplots(
        2, 2, figsize=(7.05, 5.25), sharex=True, sharey=True
    )

    for panel, (axis, (model, feature, title)) in enumerate(
        zip(axes.flat, CONFIGURATIONS)
    ):
        points = operating_points(data, model, feature)
        axis.plot(
            [point["far"] for point in points],
            [point["ss"] for point in points],
            color=TEAL,
            linewidth=1.25,
            zorder=1,
        )
        for point in points:
            is_primary = point["rule"] == "FP_5min_theta_0.70"
            axis.scatter(
                point["far"],
                point["ss"],
                s=64 if is_primary else 40,
                marker=point["marker"],
                facecolor="white" if is_primary else TEAL,
                edgecolor=NAVY if is_primary else "white",
                linewidth=1.3 if is_primary else 0.7,
                zorder=3,
            )

        axis.set_title(title, fontweight="bold")
        axis.set_xlim(-0.015, 0.43)
        axis.set_ylim(0.05, 0.78)
        axis.grid(color=GRID, linewidth=0.7)
        axis.spines[["top", "right"]].set_visible(False)
        axis.text(
            -0.12,
            1.04,
            f"({chr(ord('a') + panel)})",
            transform=axis.transAxes,
            fontsize=9.5,
            fontweight="bold",
            ha="left",
            va="bottom",
        )

    for axis in axes[:, 0]:
        axis.set_ylabel("Seizure sensitivity")
    for axis in axes[1, :]:
        axis.set_xlabel("FAR (alarms/h)")

    handles = []
    for rule, label, marker in RULES:
        is_primary = rule == "FP_5min_theta_0.70"
        handles.append(
            Line2D(
                [0],
                [0],
                marker=marker,
                linestyle="none",
                markerfacecolor="white" if is_primary else TEAL,
                markeredgecolor=NAVY if is_primary else "white",
                markeredgewidth=1.3 if is_primary else 0.7,
                markersize=7.0,
                label=label,
            )
        )
    figure.legend(
        handles=handles,
        loc="lower center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, 0.015),
        columnspacing=1.5,
        handletextpad=0.5,
    )
    figure.subplots_adjust(
        left=0.095, right=0.985, top=0.94, bottom=0.20, hspace=0.30, wspace=0.20
    )
    figure.savefig(OUTPUT, dpi=450, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
