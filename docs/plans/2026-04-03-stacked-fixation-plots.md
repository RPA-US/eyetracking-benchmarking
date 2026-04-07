# Stacked Fixation Plots Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update the summary figures so each device bar shows the matching vs non-matching fixation composition while keeping the current percentage labels and existing aggregation logic.

**Architecture:** Extend `plots.py` with small helpers that derive stacked bar inputs from the existing per-CSV mean metrics already used today. Keep the current plotting structure and output filenames, but render each device as a stacked bar with two segments: matching and non-matching. This preserves the current interpretation of the plots while adding the visual composition requested by the reviewer/user.

**Tech Stack:** Python, pandas, matplotlib, NumPy.

---

### Task 1: Add reusable stacked-bar helpers

**Files:**
- Modify: `plots.py`

**Step 1: Add helper functions**

Create small helpers near the top of the file to:
- compute `matching` and `non_matching` values from an input percentage
- draw one stacked bar pair for two devices
- place a percentage label above each full bar

Example shape:

```python
def split_percentages(matching_pct):
    return matching_pct, 100 - matching_pct

def add_stacked_bar(ax, x, matching, non_matching, color_matching, color_non_matching):
    ax.bar(x, matching, color=color_matching)
    ax.bar(x, non_matching, bottom=matching, color=color_non_matching)
```

**Step 2: Run a quick syntax check**

Run: `python -m py_compile plots.py`

Expected: exit code 0.

### Task 2: Update RQ1–RQ3 STMF figures to stacked bars

**Files:**
- Modify: `plots.py`

**Step 1: Refactor the four STMF figures**

Update these plot blocks:
- `RQ1_TC1_STMF`
- `RQ1_TC2_STMF`
- `RQ2_TC3_STMF`
- `RQ3_TC4_TC5_TC6_STMF_bars`

For each one:
- keep the same underlying source metrics and file filters
- compute one matching value per device exactly as today
- derive the non-matching segment as `100 - matching`
- render a stacked bar for Tobii and Webgazer
- keep the top label showing the matching percentage as a `%`

**Step 2: Verify the plot definitions still execute**

Run: `python plots.py`

Expected: script completes and writes the same JPG files in `output/figs/` without errors.

### Task 3: Update RQ4 MTMF figure to stacked bars

**Files:**
- Modify: `plots.py`

**Step 1: Refactor the RQ4 plot**

Update `RQ4_TC7_MTMF` so each device bar is stacked from:
- matching / relevant fixation percentage
- non-matching remainder

Keep the current label above each bar and preserve the filename `output/figs/RQ4_TC7_MTMF.jpg`.

**Step 2: Run the full plotting script**

Run: `python plots.py`

Expected: no exceptions; the RQ4 figure is regenerated alongside the others.

### Task 4: Check generated outputs for visual consistency

**Files:**
- Inspect: `output/figs/RQ1_TC1_STMF.jpg`
- Inspect: `output/figs/RQ1_TC2_STMF.jpg`
- Inspect: `output/figs/RQ2_TC3_STMF.jpg`
- Inspect: `output/figs/RQ3_TC4_TC5_TC6_STMF_bars.jpg`
- Inspect: `output/figs/RQ4_TC7_MTMF.jpg`

**Step 1: Confirm bar composition**

Verify each plot now shows two stacked color segments per device and the label still reports the matching percentage.

**Step 2: Confirm readability**

Check that axis limits, titles, legend placement, and annotations still fit the figure size.

### Task 5: Final verification and commit

**Files:**
- Modify: any plot file touched in previous tasks

**Step 1: Re-run syntax and plotting**

Run:

```bash
python -m py_compile plots.py
python plots.py
```

Expected: both commands succeed.

**Step 2: Commit the finished change**

```bash
git add plots.py output/figs/*.jpg
git commit -m "feat: show fixation composition in summary plots"
```

Expected: commit records the updated visual summaries.
