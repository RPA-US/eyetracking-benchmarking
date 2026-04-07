import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


INPUT_CSV = os.path.join("output", "statistics_summary.csv")
OUTPUT_DIR = os.path.join("output", "statistics_figs")

FAMILY_ORDER = ["RQ1", "RQ2", "RQ3", "RQ4"]
FAMILY_LABELS = {
    "RQ1": "SQ1 (TC1,TC2)",
    "RQ2": "SQ2 (TC3)",
    "RQ3": "SQ3 (TC4,TC5,TC6)",
    "RQ4": "SQ4 (TC7)",
}
METRIC_ORDER = {"STMF": 0, "MTMF": 0, "EIF": 1, "EITOF": 1, "MAE": 2}

POS_COLOR = "#E97132"
NEG_COLOR = "#156082"
GRID_COLOR = "#d0d0d0"
TEXT_COLOR = "#444444"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_results():
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"Missing {INPUT_CSV}. Run python statistics.py first.")
    return pd.read_csv(INPUT_CSV)


def format_ci(mean, low, high):
    if pd.isna(low) or pd.isna(high):
        return f"{mean:.1f}"
    return f"{mean:.1f} [{low:.1f}, {high:.1f}]"


def make_family_plot(frame, family):
    rows = frame[frame["family"] == family].copy()
    if rows.empty:
        return None

    rows = rows.assign(
        contrast_num=rows["contrast"].str.replace("TC", "", regex=False).astype(int),
        metric_rank=rows["metric"].map(METRIC_ORDER).fillna(99).astype(int),
    ).sort_values(["contrast_num", "metric_rank", "metric"])

    n_rows = len(rows)
    fig_h = max(5.0, 1.05 * n_rows + 2.0)
    fig, ax = plt.subplots(figsize=(15, fig_h), dpi=300)

    y_positions = np.arange(n_rows)[::-1]
    x_min = np.nanmin(rows["paired_difference_ci95_low"].to_numpy(dtype=float))
    x_max = np.nanmax(rows["paired_difference_ci95_high"].to_numpy(dtype=float))
    x_pad = max(5.0, 0.15 * max(abs(x_min), abs(x_max), 1.0))

    for y, (_, row) in zip(y_positions, rows.iterrows()):
        diff = float(row["paired_difference_mean"])
        low = float(row["paired_difference_ci95_low"])
        high = float(row["paired_difference_ci95_high"])
        color = POS_COLOR if diff >= 0 else NEG_COLOR
        ax.errorbar(
            diff,
            y,
            xerr=[[diff - low], [high - diff]],
            fmt="o",
            markersize=9,
            color=color,
            ecolor=color,
            elinewidth=2.2,
            capsize=5,
            markerfacecolor=color if float(row["p_value_holm"]) < 0.05 else "white",
            markeredgecolor=color,
            markeredgewidth=1.4,
        )

    ax.axvline(0, color="#666666", linestyle="--", linewidth=1)
    ax.set_xlim(x_min - x_pad, x_max + x_pad)
    ax.set_ylim(-0.8, n_rows - 0.2)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f"{row['contrast']} · {row['metric']}" for _, row in rows.iterrows()], fontsize=22, color=TEXT_COLOR)
    ax.set_xlabel("Positive values favor Infrared Device (Tobii Spark Pro); negative values favor Webcam Device (WebGazer).", fontsize=16, color=TEXT_COLOR)
    ax.tick_params(axis="x", labelsize=16, colors=TEXT_COLOR)
    ax.grid(axis="x", linestyle="--", alpha=0.35, color=GRID_COLOR)


    out_path = os.path.join(OUTPUT_DIR, f"{family}_paired_differences.png")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main():
    ensure_output_dir()
    results = load_results()
    outputs = []
    for family in FAMILY_ORDER:
        out = make_family_plot(results, family)
        if out:
            outputs.append(out)
            print(f"Wrote {out}")
    print(f"Generated {len(outputs)} statistical figures")


if __name__ == "__main__":
    main()
