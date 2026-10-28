# Page fitting

**Hard rules (from the approved process):** never reduce font size below 10 pt body text; never delete content to make it fit unless the user approves.

## What was done by hand originally (exact process, not automated)
When a resume ran over one page, I (1) trimmed spacing values by a few twips at a time, (2) trimmed top and bottom margins (the lowest used was 0.32 in), and only then, with the user's approval, (3) cut a bullet.
The amounts were tuned per resume by eye, re-rendering after each change.

## What `scripts/build.py` does (CODIFIED version, not the original)
The ladder below turns that manual loop into fixed steps. The numbers are a codification chosen for this package, not the exact values used on each past resume.

| Level | Spacing (all `spacing_pt` values) | Top/bottom margin |
|---|---|---|
| L0 | as approved | 0.55 in |
| L1 | x 0.85 | 0.55 in |
| L2 | x 0.70 | 0.55 in |
| L3 | x 0.70 | 0.45 in |
| L4 | x 0.60 | 0.40 in |
| L5 (floor) | x 0.60 | 0.35 in |

The script builds, converts, counts pages, and stops at the first level that reaches `--target-pages` (default 1). The level used is saved as `<name>.style_used.json`.
If L5 still overflows it **stops with exit code 2 and does not cut content**. Tell the user which bullets you would cut and ask.

Demonstration: `input/sample_dense.json` needs 2 pages at L0 and fits at L1 (`output/Sample_Dense.build_log.txt`).

## Left and right margins
They stay at 0.7 in. If you ever change them, update `tab_stop_in` (see STYLE_SPEC.md).

## Photo variant
The photo makes the header taller, so a resume that fits without a photo can overflow with one. Run the ladder separately for each variant. Never change wording to fit.

## Two-page resumes
Use `--target-pages 2`. The approved two-page master used 0.6 in top/bottom margins and a page break before its second-page section (not automated here; split by content).
