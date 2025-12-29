# Execution Checklist: Steps 1-3

## Pre-flight

- [x] Placeholder CSV backed up: `fifth_force_exclusion_PLACEHOLDER.csv`
- [x] Sanity check script ready: `scripts/sanity_check_csv.py`
- [x] Digitization instructions ready: `DIGITIZATION_INSTRUCTIONS.md`

---

## Step 1: Digitize Kapner 2007

- [ ] Find Kapner 2007 paper (exclusion curve plot)
- [ ] Load in WebPlotDigitizer
- [ ] Calibrate axes (log-log)
- [ ] Digitize ~40-80 points along exclusion contour
- [ ] Export as CSV
- [ ] Convert to schema:
  - `lambda` in meters
  - `alpha` dimensionless
  - All rows: `excluded=1`
- [ ] Replace: `experiments/constraints/data/fifth_force_exclusion.csv`
- [ ] **Sanity check:** `python scripts/sanity_check_csv.py`
- [ ] **Paste first 5 rows here for verification** (before proceeding)
- [ ] Regenerate:
  ```bash
  python scripts/fifth_force_yukawa.py
  python scripts/make_global_constraints.py
  ```
- [ ] Visual check: plot matches published figure

---

## Step 2: Replace Higgs Placeholder

- [ ] Find ATLAS-CMS combined Run 2 invisible width limit
- [ ] Extract:
  - `invisible_width_limit_mev` (typically 0.1-0.2 MeV)
  - `signal_strength_deviation` (typically 0.05)
- [ ] Update: `experiments/constraints/data/higgs_limits.json`
- [ ] Update `source` with exact citation
- [ ] Regenerate:
  ```bash
  python scripts/higgs_portal_bounds.py
  python scripts/make_global_constraints.py
  ```
- [ ] Visual check: bounds are reasonable

---

## Step 3: Overlap Check (The Payoff)

- [ ] Run:
  ```bash
  python scripts/check_overlap_region.py
  ```
- [ ] Check output:
  - **Overlap exists** → Viable parameter space → Publish allowed region
  - **No overlap** → Falsified parameterization → Publish inconsistency
- [ ] Review `overlap_region_summary.json`

---

## Step 3.5: Finalize in Paper

- [ ] Copy figures:
  ```bash
  cp results/*.png ../../papers/toe_closed_core/figures/
  ```
- [ ] Compile paper:
  ```bash
  cd ../../papers/toe_closed_core
  pdflatex main.tex
  pdflatex main.tex
  ```
- [ ] Verify citations match exact sources used
- [ ] Commit:
  ```bash
  cd ../../
  git add experiments/constraints papers/toe_closed_core
  git commit -m "Replace placeholders with digitized bounds; regenerate global constraints; run overlap check"
  git push
  ```

---

## Quick Commands Reference

```bash
# Sanity check CSV
python experiments/constraints/scripts/sanity_check_csv.py

# Regenerate all figures
python experiments/constraints/scripts/fifth_force_yukawa.py
python experiments/constraints/scripts/higgs_portal_bounds.py
python experiments/constraints/scripts/make_global_constraints.py

# Overlap check
python experiments/constraints/scripts/check_overlap_region.py

# Copy to paper
cp experiments/constraints/results/*.png papers/toe_closed_core/figures/
```

---

## Expected Outcomes

**Step 1:** Real exclusion curve in plot (matches published figure)

**Step 2:** Real collider bounds in plot (reasonable limits)

**Step 3:** Either:
- ✅ Viable parameter space exists → Publish allowed region map
- ✅ No viable space → Publish falsification → Revise model

**Either way: Science. Either way: Forward.** ✅

