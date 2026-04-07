# Statistics Summary Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a reusable `statistics.py` script that computes paired within-subject comparisons, uncertainty intervals, and effect sizes for all comparison families, then exports a CSV summary and a paper-ready table.

**Architecture:** Read `data/combined_data.csv`, reshape per `Subject` and `Filename`, and compute paired statistics for each metric family already present in the repo. Keep the analysis reusable by centralizing the logic in small helper functions for pairing, confidence intervals, Wilcoxon/t-test selection, and effect size calculation. Write outputs to `output/` so the script can be rerun without touching the plotting code.

**Tech Stack:** Python, pandas, NumPy, SciPy, matplotlib (for optional table formatting if needed).

---

### Task 1: Define the statistical outputs and comparison map

**Files:**
- Create: `statistics.py`
- Modify: none

**Step 1: Write the output schema first**

Define the columns the CSV must contain, at minimum:
- `family`
- `contrast`
- `metric`
- `n_pairs`
- `condition_a_mean`
- `condition_a_ci95_low`
- `condition_a_ci95_high`
- `condition_b_mean`
- `condition_b_ci95_low`
- `condition_b_ci95_high`
- `test_name`
- `statistic`
- `p_value`
- `effect_size_name`
- `effect_size_value`

**Step 2: Define the comparison map**

Hard-code a small mapping from comparison family to filenames and metric column names, for example:
- `RQ1`: `TC1`, `TC2`, `%MatchingFixations`
- `RQ2`: `TC3`, `%MatchingFixations` and `%EventsWithFixations`
- `RQ3`: `TC4`, `TC5`, `TC6`, `%MatchingFixations`, `%EventsWithFixations`, `MAE`
- `RQ4`: `TC7`, `%RelevantFixations`, `PercentageEventsWithTestObjectTrue`

**Step 3: Add a tiny smoke test by running the script shape-only later**

No test file is required yet; the first verification will be a script run on the real CSV.

### Task 2: Implement pairing, uncertainty, and effect-size helpers

**Files:**
- Create: `statistics.py`

**Step 1: Add helper functions**

Implement helpers for:
- loading `data/combined_data.csv`
- filtering rows by `Filename`
- aggregating per `Subject` with `mean()`
- computing a 95% confidence interval over subject-level values
- computing paired differences
- choosing a paired test (`Wilcoxon` as default, with safe fallback to paired t-test only if needed)
- computing an effect size from the paired differences

Suggested helper shape:

```python
def summarize_by_subject(df, metric):
    return df.groupby('Subject')[metric].mean().sort_index()

def mean_ci95(values):
    ...

def paired_wilcoxon(a, b):
    ...

def rank_biserial_from_diffs(diffs):
    ...
```

**Step 2: Decide how to handle missing or unmatched subjects**

Use the intersection of subject IDs for each paired comparison and drop incomplete pairs explicitly.

### Task 3: Generate the reusable statistics CSV

**Files:**
- Create: `statistics.py`

**Step 1: Build the comparison loop**

Iterate over all families and metrics, construct paired subject vectors for each contrast, run the statistical helpers, and append one result row per comparison.

**Step 2: Write the CSV output**

Save the results to:
- `output/statistics_summary.csv`

**Step 3: Run the script once**

Run: `python statistics.py`

Expected: the CSV is created and populated with one row per comparison.

### Task 4: Generate a paper-ready table

**Files:**
- Create: `statistics.py`

**Step 1: Format a Markdown table**

Create `output/statistics_summary.md` with a compact table grouped by family and contrast.

**Step 2: Keep the table readable**

Round values consistently and keep columns narrow enough for direct copy/paste into the manuscript.

**Step 3: Re-run the script**

Run: `python statistics.py`

Expected: both CSV and Markdown outputs are refreshed.

### Task 5: Verify the analysis end to end

**Files:**
- Inspect: `output/statistics_summary.csv`
- Inspect: `output/statistics_summary.md`

**Step 1: Check basic sanity**

Confirm every expected family/contrast appears and that `n_pairs` is 10 for the within-subject comparisons.

**Step 2: Check statistical values**

Confirm p-values, confidence intervals, and effect sizes are finite and sensible.

**Step 3: Optional lightweight export sanity**

If needed, add a short printout at script end summarizing how many comparisons were processed successfully.

### Task 6: Final verification

**Files:**
- Modify: `statistics.py` if any last-minute cleanup is needed

**Step 1: Run syntax check**

Run: `python -m py_compile statistics.py`

Expected: exit code 0.

**Step 2: Run the full analysis**

Run: `python statistics.py`

Expected: outputs are created in `output/` without errors.
