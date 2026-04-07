import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


OUTPUT_DIR = "output"
SOURCE_CSV = os.path.join("data", "combined_data.csv")
SUMMARY_CSV = os.path.join(OUTPUT_DIR, "statistics_summary.csv")
PAPER_MD = os.path.join(OUTPUT_DIR, "statistics_paper_table.md")
PAPER_TEX = os.path.join(OUTPUT_DIR, "statistics_paper_table.tex")


@dataclass(frozen=True)
class Comparison:
    family: str
    contrast: str
    metric_column: str
    metric_label: str
    filename_a: str
    filename_b: str
    condition_a: str
    condition_b: str


COMPARISONS = [
    Comparison("RQ1", "TC1", "%MatchingFixations", "STMF", "RQ1_tobii_form_density_low_postprocessed.csv", "RQ1_webgazer_form_density_low_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ1", "TC1", "MAE", "MAE", "RQ1_tobii_form_density_low_postprocessed.csv", "RQ1_webgazer_form_density_low_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ1", "TC2", "%MatchingFixations", "STMF", "RQ1_tobii_form_density_high_postprocessed.csv", "RQ1_webgazer_form_density_high_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ1", "TC2", "MAE", "MAE", "RQ1_tobii_form_density_high_postprocessed.csv", "RQ1_webgazer_form_density_high_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),

    Comparison("RQ2", "TC3", "%MatchingFixations", "STMF", "RQ2_tobii_alternance_buttons_postprocessed.csv", "RQ2_webgazer_alternance_buttons_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ2", "TC3", "%EventsWithFixations", "EIF", "RQ2_tobii_alternance_buttons_postprocessed.csv", "RQ2_webgazer_alternance_buttons_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ2", "TC3", "MAE", "MAE", "RQ2_tobii_alternance_buttons_postprocessed.csv", "RQ2_webgazer_alternance_buttons_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),

    Comparison("RQ3", "TC4", "%MatchingFixations", "STMF", "RQ3_tobii_position_50cm_postprocessed.csv", "RQ3_webgazer_position_50cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ3", "TC4", "%EventsWithFixations", "EIF", "RQ3_tobii_position_50cm_postprocessed.csv", "RQ3_webgazer_position_50cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ3", "TC4", "MAE", "MAE", "RQ3_tobii_position_50cm_postprocessed.csv", "RQ3_webgazer_position_50cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ3", "TC5", "%MatchingFixations", "STMF", "RQ3_tobii_position_70cm_postprocessed.csv", "RQ3_webgazer_position_70cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ3", "TC5", "%EventsWithFixations", "EIF", "RQ3_tobii_position_70cm_postprocessed.csv", "RQ3_webgazer_position_70cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ3", "TC5", "MAE", "MAE", "RQ3_tobii_position_70cm_postprocessed.csv", "RQ3_webgazer_position_70cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ3", "TC6", "%MatchingFixations", "STMF", "RQ3_tobii_position_90cm_postprocessed.csv", "RQ3_webgazer_position_90cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ3", "TC6", "%EventsWithFixations", "EIF", "RQ3_tobii_position_90cm_postprocessed.csv", "RQ3_webgazer_position_90cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),
    Comparison("RQ3", "TC6", "MAE", "MAE", "RQ3_tobii_position_90cm_postprocessed.csv", "RQ3_webgazer_position_90cm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js"),

    Comparison("RQ4", "TC7", "%RelevantFixations", "MTMF", "RQ4_tobii_rpm_postprocessed.csv", "RQ4_webgazer_rpm_postprocessed.csv", "Infrared/Tobii Pro Spark", "Webcam/Webgazer.js")
]

METRIC_ORDER = {"STMF": 0, "MTMF": 0, "EIF": 1, "MAE": 2}


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    return pd.read_csv(SOURCE_CSV)


def summarize_by_subject(df, metric):
    return df.groupby("Subject")[metric].mean().sort_index().dropna()


def paired_vectors(df, filename_a, filename_b, metric):
    a = summarize_by_subject(df[df["Filename"] == filename_a], metric)
    b = summarize_by_subject(df[df["Filename"] == filename_b], metric)
    common = a.index.intersection(b.index)
    return a.loc[common].astype(float), b.loc[common].astype(float)


def mean_ci95(values):
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    n = arr.size
    mean = float(np.mean(arr)) if n else np.nan
    if n < 2:
        return mean, np.nan, np.nan
    sem = stats.sem(arr)
    if not np.isfinite(sem) or sem == 0:
        return mean, mean, mean
    margin = stats.t.ppf(0.975, n - 1) * sem
    return mean, float(mean - margin), float(mean + margin)


def rank_biserial_from_diffs(diffs):
    diffs = np.asarray(diffs, dtype=float)
    diffs = diffs[~np.isnan(diffs)]
    diffs = diffs[diffs != 0]
    if diffs.size == 0:
        return 0.0
    ranks = stats.rankdata(np.abs(diffs))
    positive = ranks[diffs > 0].sum()
    negative = ranks[diffs < 0].sum()
    total = positive + negative
    return float((positive - negative) / total) if total else 0.0


def paired_wilcoxon(a, b):
    diffs = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    diffs = diffs[~np.isnan(diffs)]
    diffs = diffs[diffs != 0]
    if diffs.size == 0:
        return 0.0, 1.0, 0.0
    result = stats.wilcoxon(diffs, zero_method="wilcox", alternative="two-sided", method="auto")
    return float(result.statistic), float(result.pvalue), rank_biserial_from_diffs(diffs)


def holm_adjust(p_values):
    p_values = np.asarray(p_values, dtype=float)
    n = len(p_values)
    order = np.argsort(p_values)
    adjusted = np.empty(n, dtype=float)
    running_max = 0.0
    for rank, idx in enumerate(order):
        adj = (n - rank) * p_values[idx]
        running_max = max(running_max, adj)
        adjusted[idx] = min(running_max, 1.0)
    return adjusted


def build_results(df):
    rows = []
    for item in COMPARISONS:
        a, b = paired_vectors(df, item.filename_a, item.filename_b, item.metric_column)
        common = a.index.intersection(b.index)
        a = a.loc[common]
        b = b.loc[common]
        diff = a.values - b.values
        a_mean, a_low, a_high = mean_ci95(a.values)
        b_mean, b_low, b_high = mean_ci95(b.values)
        diff_mean, diff_low, diff_high = mean_ci95(diff)
        stat, p_value, effect = paired_wilcoxon(a.values, b.values)
        rows.append({
            "family": item.family,
            "contrast": item.contrast,
            "metric": item.metric_label,
            "metric_column": item.metric_column,
            "condition_a": item.condition_a,
            "condition_b": item.condition_b,
            "filename_a": item.filename_a,
            "filename_b": item.filename_b,
            "n_pairs": int(len(common)),
            "condition_a_mean": a_mean,
            "condition_a_ci95_low": a_low,
            "condition_a_ci95_high": a_high,
            "condition_b_mean": b_mean,
            "condition_b_ci95_low": b_low,
            "condition_b_ci95_high": b_high,
            "paired_difference_mean": diff_mean,
            "paired_difference_ci95_low": diff_low,
            "paired_difference_ci95_high": diff_high,
            "test_name": "Wilcoxon signed-rank",
            "statistic": stat,
            "p_value": p_value,
            "effect_size_name": "rank-biserial r",
            "effect_size_value": effect,
        })
    results = pd.DataFrame(rows)
    results["p_value_holm"] = results.groupby("family")["p_value"].transform(lambda s: holm_adjust(s.to_numpy()))
    results["contrast_num"] = results["contrast"].str.replace("TC", "", regex=False).astype(int)
    results["metric_rank"] = results["metric"].map(METRIC_ORDER).fillna(99).astype(int)
    results = results.sort_values(["family", "contrast_num", "metric_rank", "metric"])
    return results.drop(columns=["contrast_num", "metric_rank"])


def format_ci(mean, low, high):
    if pd.isna(low) or pd.isna(high):
        return f"{mean:.2f}"
    return f"{mean:.2f} [{low:.2f}, {high:.2f}]"


def build_paper_table(results):
    table = pd.DataFrame(
        {
            "RQ/TC": results["family"] + "-" + results["contrast"],
            "Metric": results["metric"],
            "Condition A (CI)": [format_ci(m, l, h) for m, l, h in zip(results["condition_a_mean"], results["condition_a_ci95_low"], results["condition_a_ci95_high"])],
            "Condition B (CI)": [format_ci(m, l, h) for m, l, h in zip(results["condition_b_mean"], results["condition_b_ci95_low"], results["condition_b_ci95_high"])],
            "Δ (CI)": [format_ci(m, l, h) for m, l, h in zip(results["paired_difference_mean"], results["paired_difference_ci95_low"], results["paired_difference_ci95_high"])],
            "p": [f"{p:.4f}" for p in results["p_value_holm"]],
            "r": [f"{r:.3f}" for r in results["effect_size_value"]],
        }
    )
    return table


def write_markdown_table(table):
    lines = ["# Statistics Summary", "", "Note: p values are Holm-adjusted within each RQ.", ""]
    lines.append("| " + " | ".join(table.columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(table.columns)) + " |")
    for _, row in table.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in table.columns) + " |")
    return "\n".join(lines) + "\n"


def main():
    ensure_output_dir()
    results = build_results(load_data())
    results.to_csv(SUMMARY_CSV, index=False)
    paper = build_paper_table(results)
    with open(PAPER_MD, "w", encoding="utf-8") as f:
        f.write(write_markdown_table(paper))
    with open(PAPER_TEX, "w", encoding="utf-8") as f:
        f.write(paper.to_latex(index=False, escape=False))
    print(f"Wrote {SUMMARY_CSV}")
    print(f"Wrote {PAPER_MD}")
    print(f"Wrote {PAPER_TEX}")
    print(f"Processed {len(results)} comparisons")


if __name__ == "__main__":
    main()
