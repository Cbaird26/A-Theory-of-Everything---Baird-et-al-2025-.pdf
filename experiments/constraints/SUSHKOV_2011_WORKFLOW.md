# Sushkov 2011 Workflow — Complete Step-by-Step

## Overview

Digitize Sushkov et al. PRL 107, 171101 (2011) exclusion curve and add it to the constraint envelope to tighten the island at the micron end (0.4-4 µm range).

---

## Step 1: Digitize the Curve

1. Open the paper: **PRL 107, 171101 (2011)**
2. Find the exclusion plot (Yukawa α vs λ)
3. Use WebPlotDigitizer or similar to extract ~50-100 points
4. Fill `experiments/constraints/data/sushkov2011_exclusion.csv`:
   - `lambda`: range in **meters** (0.1-10 µm = 1e-7 to 1e-5 m)
   - `alpha`: dimensionless Yukawa strength
   - `excluded`: 1 for points above the curve (excluded region)
   - `source`: "Sushkov2011"

**Template already created:** `experiments/constraints/data/sushkov2011_exclusion.csv`

---

## Step 2: Validate Digitized Data

**Sanity check before merging:**

```bash
python experiments/constraints/scripts/validate_digitized_curve.py \
  --csv experiments/constraints/data/sushkov2011_exclusion.csv \
  --source Sushkov2011 \
  --lambda-min 1e-7 \
  --lambda-max 1e-5 \
  --plot
```

**What it checks:**
- ✅ λ values in expected range (1e-7 to 1e-5 m)
- ✅ α magnitudes plausible (positive, < 1.0, not too small)
- ✅ Monotonicity (curve should increase with λ)
- ✅ No axis flip
- ✅ Proper excluded/allowed labeling

**If validation fails:** Fix issues before proceeding.

---

## Step 3: Merge with Envelope

**Merge Sushkov 2011 with existing Kapner bounds:**

```bash
python experiments/constraints/scripts/add_fifth_force_curve.py \
  --merge \
  --base experiments/constraints/data/fifth_force_exclusion.csv \
  --add experiments/constraints/data/sushkov2011_exclusion.csv \
  --out experiments/constraints/data/fifth_force_exclusion_envelope.csv \
  --plot experiments/constraints/results/fifth_force_envelope_compare.png
```

**What this does:**
- Computes envelope (most restrictive α at each λ)
- Combines Kapner + Sushkov constraints
- Generates comparison plot

---

## Step 4: Update Overlap Check to Use Envelope

**Option A:** Replace the base file (simplest)
```bash
cp experiments/constraints/data/fifth_force_exclusion_envelope.csv \
   experiments/constraints/data/fifth_force_exclusion.csv
```

**Option B:** Update `check_overlap_region.py` to load envelope CSV directly

---

## Step 5: Rerun Overlap with Envelope

**Pass 1: Coarse scan**
```bash
python experiments/constraints/scripts/check_overlap_region.py \
  --n-lambda 300 \
  --n-alpha 300 \
  --out-json experiments/constraints/results/overlap_pass1_with_sushkov.json
```

**Extract p05/p95, then Pass 2: Zoomed scan**
```bash
python experiments/constraints/scripts/check_overlap_region.py \
  --lambda-min <p05_lambda> \
  --lambda-max <p95_lambda> \
  --alpha-min <p05_alpha> \
  --alpha-max <p95_alpha> \
  --n-lambda 500 \
  --n-alpha 500 \
  --out-json experiments/constraints/results/overlap_pass2_with_sushkov.json
```

---

## Step 6: Compare Before/After

**Compare island coordinates:**

```bash
python experiments/constraints/scripts/compare_islands.py \
  --before experiments/constraints/results/overlap_pass2.json \
  --after experiments/constraints/results/overlap_pass2_with_sushkov.json \
  --plot experiments/constraints/results/island_comparison.png
```

**Expected result:**
- ✅ Lambda p05 should **increase** (island shrunk at low-λ end)
- ✅ Lambda p95 may tighten slightly
- ✅ Alpha bounds should remain similar or tighten

**If island doesn't shrink:**
- Check digitization (units, axis flip)
- Verify Sushkov curve is actually more restrictive in 0.4-4 µm range
- Island might mostly live at larger λ (also informative)

---

## Quick Reference

**Files:**
- Template: `experiments/constraints/data/sushkov2011_exclusion.csv`
- Validation: `experiments/constraints/scripts/validate_digitized_curve.py`
- Merge: `experiments/constraints/scripts/add_fifth_force_curve.py`
- Compare: `experiments/constraints/scripts/compare_islands.py`

**Expected range:**
- Lambda: 1e-7 to 1e-5 m (0.1-10 µm)
- Alpha: ~1e-12 to ~1e-6 (check paper for exact range)

**Time estimate:** 30-60 minutes for digitization + validation + merge + rerun

---

## Troubleshooting

**Validation fails:**
- Check units (λ in meters, not microns)
- Verify axis labels weren't flipped
- Ensure α values are positive and reasonable

**Island doesn't shrink:**
- Sushkov might not be more restrictive in your island's λ range
- Check if digitized curve is actually above/below existing bounds
- Verify envelope computation worked correctly

**Merge fails:**
- Check CSV format (columns: lambda, alpha, excluded, source)
- Ensure all values are numeric
- Check file paths are correct

