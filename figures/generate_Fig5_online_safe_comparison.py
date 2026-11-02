"""Reproduce manuscript Fig. 5 from the saved V11B fold-level results.

This deterministic scientific plot does not use a generative-image model.
Paths are resolved relative to this file.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "figure_source_data" / "v11b_targeted_fold_results.csv"
OUTPUT = ROOT / "figures" / "Fig5.png"
NAVY, BLUE, ORANGE = "#173B57", "#2F80ED", "#F2994A"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8.2,
        "axes.titlesize": 9.5,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "axes.linewidth": 0.8,
        "savefig.facecolor": "white",
    }
)


def aggregate_results(path: Path) -> pd.DataFrame:
    folds = pd.read_csv(path)
    rows = []
    keys = ["Model", "FeatureSet", "AlarmGenerationMode"]
    for (model, feature, mode), group in folds.groupby(keys):
        detected = group["SeizurePredicted"].eq(1)
        rows.append(
            {
                "Model": model,
                "FeatureSet": feature,
                "Mode": mode,
                "SS": group["SeizurePredicted"].sum() / len(group),
                "FAR": group["FalseAlarms"].sum()
                / group["EligibleInterictalHours"].sum(),
                "TTW": group.loc[detected, "TimeToWarning_min"].mean(),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    data = aggregate_results(SOURCE)
    configurations = [
        ("RandomForest", "F1_Handcrafted", "RF-F1"),
        ("RandomForest", "F7_All", "RF-F7"),
        ("XGBoost", "F1_Handcrafted", "XGB-F1"),
        ("XGBoost", "F6_Handcrafted_wPLI", "XGB-F6"),
    ]
    modes = [
        ("label_gated_v10", "Label-gated", "white", BLUE, "o"),
        ("online_safe_gap_only", "Online-safe", ORANGE, ORANGE, "s"),
    ]
    metrics = [
        ("SS", "Seizure sensitivity", (0.40, 0.71)),
        ("FAR", "FAR (alarms/h)", (0.145, 0.215)),
        ("TTW", "Mean TTW (min)", (10, 23.8)),
    ]

    figure, axes = plt.subplots(1, 3, figsize=(7.15, 2.85))
    x_positions = np.arange(len(configurations))
    for panel, (axis, (metric, ylabel, limits)) in enumerate(zip(axes, metrics)):
        for index, (model, feature, _) in enumerate(configurations):
            values = []
            for mode, *_ in modes:
                row = data[
                    (data.Model == model)
                    & (data.FeatureSet == feature)
                    & (data.Mode == mode)
                ].iloc[0]
                values.append(float(row[metric]))

            axis.plot(
                [index - 0.16, index + 0.16],
                values,
                color="#AAB4BC",
                linewidth=1.1,
                zorder=1,
            )
            for mode_index, (offset, value, style) in enumerate(
                zip([-0.16, 0.16], values, modes)
            ):
                _, _, face, edge, marker = style
                axis.scatter(
                    index + offset,
                    value,
                    s=37,
                    marker=marker,
                    facecolor=face,
                    edgecolor=edge,
                    linewidth=1.2,
                    zorder=3,
                )
                label = f"{value:.3f}" if metric != "TTW" else f"{value:.1f}"
                if mode_index == 0:
                    dx, dy, horizontal, vertical = 0, 7, "center", "bottom"
                else:
                    dx, dy, horizontal, vertical = 0, -8, "center", "top"
                axis.annotate(
                    label,
                    (index + offset, value),
                    xytext=(dx, dy),
                    textcoords="offset points",
                    ha=horizontal,
                    va=vertical,
                    fontsize=5.8,
                    color=NAVY,
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.25},
                )

        axis.set_xticks(
            x_positions,
            [configuration[2] for configuration in configurations],
            rotation=25,
            ha="right",
        )
        axis.set_ylabel(ylabel)
        axis.set_ylim(*limits)
        axis.set_xlim(-0.65, len(configurations) - 0.45)
        axis.grid(axis="y", color="#D8DDE2", linewidth=0.7)
        axis.spines[["top", "right"]].set_visible(False)
        axis.text(
            -0.12,
            1.05,
            f"({chr(ord('a') + panel)})",
            transform=axis.transAxes,
            fontsize=9.5,
            fontweight="bold",
            ha="left",
            va="bottom",
        )

    legend = [
        Line2D(
            [0], [0], marker="o", color="none", markerfacecolor="white",
            markeredgecolor=BLUE, markeredgewidth=1.2, label="Label-gated"
        ),
        Line2D(
            [0], [0], marker="s", color="none", markerfacecolor=ORANGE,
            markeredgecolor=ORANGE, label="Online-safe"
        ),
    ]
    figure.legend(
        handles=legend, loc="upper center", ncol=2, frameon=False,
        bbox_to_anchor=(0.5, 1.035)
    )
    figure.subplots_adjust(
        left=0.085, right=0.995, top=0.80, bottom=0.25, wspace=0.48
    )
    figure.savefig(OUTPUT, dpi=450, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
