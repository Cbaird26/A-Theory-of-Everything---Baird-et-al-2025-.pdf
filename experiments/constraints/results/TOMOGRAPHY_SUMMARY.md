# Island Tomography Results Summary

## Pass 1: Coarse Scan (250×250 grid)

**Viable points:** 62,250

**Lambda (range):**
- p05 = 1.946e-06 m (1.95 µm)
- p50 = 1.000e-03 m (1 mm, median)
- p95 = 5.139e-01 m (51.4 cm)

**Alpha (Yukawa strength):**
- p05 = 1.946e-12
- p50 = 9.726e-10 (median)
- p95 = 4.861e-07

**Zoom box for Pass 2:**
```bash
python experiments/constraints/scripts/check_overlap_region.py \
  --lambda-min 1.946e-06 \
  --lambda-max 5.139e-01 \
  --alpha-min 1.946e-12 \
  --alpha-max 4.861e-07 \
  --n-lambda 400 --n-alpha 400 \
  --out-json experiments/constraints/results/overlap_pass2.json
```

---

## Pass 2: Refined Scan (400×400 grid, zoomed on p05/p95)

**Viable points:** 159,600 (higher resolution in smaller region)

**Lambda (range):**
- p05 = 3.717e-06 m (3.72 µm)
- p50 = 1.001e-03 m (1 mm, median)
- p95 = 2.693e-01 m (26.9 cm)

**Alpha (Yukawa strength):**
- p05 = 3.286e-12
- p50 = 1.300e-09 (median)
- p95 = 5.145e-07

**Zoom box for Pass 3 (optional):**
```bash
python experiments/constraints/scripts/check_overlap_region.py \
  --lambda-min 3.717e-06 \
  --lambda-max 2.693e-01 \
  --alpha-min 3.286e-12 \
  --alpha-max 5.145e-07 \
  --n-lambda 500 --n-alpha 500 \
  --out-json experiments/constraints/results/overlap_pass3.json
```

---

## Observations

1. **Island is tightening:** Pass 2 shows narrower p95 bounds than Pass 1
   - Lambda p95: 51.4 cm → 26.9 cm (tighter)
   - Alpha p95: 4.86e-07 → 5.15e-07 (similar, slightly higher)

2. **Median remains stable:** ~1 mm for lambda, ~1e-9 for alpha

3. **Low-λ end:** p05 is in the micron range (1.95 µm → 3.72 µm)
   - This is where Sushkov 2011 constraints (0.4-4 µm) will be most impactful

---

## Next Steps

1. **Optional Pass 3:** Further refinement with 500×500 grid
2. **Add Sushkov 2011:** Digitize and merge to test if micron-end survives
3. **Compare island sizes:** Before/after adding stronger constraints

---

## Files

- `overlap_pass1.json` - Coarse scan results
- `overlap_pass2.json` - Refined scan results
- `overlap_pass3.json` - (Optional) Ultra-refined scan

