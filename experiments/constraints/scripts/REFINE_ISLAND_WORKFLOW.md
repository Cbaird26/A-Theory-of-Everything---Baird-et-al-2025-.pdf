# Island Refinement Workflow — Adding Stronger Constraints

This document outlines the workflow to tighten the viable parameter island by adding stronger published fifth-force constraints.

## Overview

The current island is bounded by:
- QRNG bounds (ε < 2.29×10⁻³)
- Kapner 2007 (fifth-force, ~55 µm and above)
- ATLAS Higgs portal constraints

**Goal:** Add stronger constraints in the micron→sub-micron range to tighten the island.

## Step 1: Digitize Sushkov 2011 (0.4-4 µm range)

**Paper:** Sushkov et al., PRL 107, 171101 (2011)  
**Range:** Best bounds in 0.4-4 µm window  
**Why:** Hits the low end of your current island

### Create template:

```bash
python experiments/constraints/scripts/add_fifth_force_curve.py \
  --create-template \
  --source "Sushkov2011" \
  --out experiments/constraints/data/sushkov2011_exclusion.csv
```

### Digitize:

1. Open the paper (PRL 107, 171101)
2. Find the exclusion plot (Yukawa α vs λ)
3. Use WebPlotDigitizer or similar to extract (λ, α) points
4. Replace the `alpha` column in the CSV with digitized values
5. Set `excluded=1` for points above the curve

### Merge with existing bounds:

```bash
python experiments/constraints/scripts/add_fifth_force_curve.py \
  --merge \
  --existing experiments/constraints/data/fifth_force_exclusion.csv \
  --new experiments/constraints/data/sushkov2011_exclusion.csv \
  --out experiments/constraints/data/fifth_force_exclusion_envelope.csv
```

## Step 2: (Optional) Add Decca 2005 (sub-µm)

**Paper:** Decca et al., PRL 94, 240401 (2005)  
**Range:** Sub-µm constraints using isoelectronic technique  
**Why:** Tightens the sub-µm side, reduces Casimir modeling ambiguity

### Create template:

```bash
python experiments/constraints/scripts/add_fifth_force_curve.py \
  --create-template \
  --source "Decca2005" \
  --out experiments/constraints/data/decca2005_exclusion.csv
```

### Digitize and merge:

Same process as Sushkov 2011, then merge:

```bash
python experiments/constraints/scripts/add_fifth_force_curve.py \
  --merge \
  --existing experiments/constraints/data/fifth_force_exclusion_envelope.csv \
  --new experiments/constraints/data/decca2005_exclusion.csv \
  --out experiments/constraints/data/fifth_force_exclusion_envelope.csv
```

## Step 3: Update Overlap Check to Use Envelope

Update `check_overlap_region.py` to load the envelope CSV instead of the single curve.

## Step 4: Rerun Overlap with Refined Grid

```bash
# Pass 1: Coarse scan with new constraints
python experiments/constraints/scripts/check_overlap_region.py \
  --ff-json experiments/constraints/results/fifth_force_bounds_envelope.json \
  --n-lambda 250 --n-alpha 250

# Extract p05/p95 from JSON, then zoom
python experiments/constraints/scripts/check_overlap_region.py \
  --ff-json experiments/constraints/results/fifth_force_bounds_envelope.json \
  --lambda-min <p05_lambda> --lambda-max <p95_lambda> \
  --alpha-min <p05_alpha> --alpha-max <p95_alpha> \
  --n-lambda 400 --n-alpha 400 \
  --out-json experiments/constraints/results/overlap_island_summary_refined.json
```

## Step 5: Compare Island Sizes

Compare the refined island coordinates:
- Before: λ ∈ [1e-6, 1] m, α ∈ [1e-12, 7.54e-7]
- After: (will be tighter, especially on the low-λ side)

## References

- **Kapner 2007:** PRL 98, 021101 — inverse-square-law tests down to ~55 µm
- **Sushkov 2011:** PRL 107, 171101 — best bounds in 0.4-4 µm range
- **Decca 2005:** PRL 94, 240401 — isoelectronic technique, sub-µm constraints
- **Decca 2007:** PRD 75, 077101 — Casimir pressure Yukawa bounds (optional)

## Notes

- Keep the three "micron→meter" stories separate:
  1. **Fifth-force island** (this workflow) — mainstream Yukawa constraints
  2. **Dark dimension theory** — specific theoretical program (Phys Rev D 111, 046014)
  3. **Microtubules quantum computation** — speculative quantum-biology track (EPJ Plus 2025)

- The goal is to computationally tighten the island, not to claim discovery
- Even if the island shrinks significantly, it's still a valid constraint result

