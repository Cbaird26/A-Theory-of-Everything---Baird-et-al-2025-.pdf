# Island Tomography Insights

## Key Takeaways from Pass 1 & Pass 2

### 1. The Island is Real and Structured

**Evidence:**
- Pass 1: 62,250 viable points (250×250 grid)
- Pass 2: 159,600 viable points (400×400 grid, higher resolution in smaller region)
- Stable medians: ~1 mm for λ, ~1e-9 for α

**Interpretation:** This is a coherent overlap patch, not numerical noise. The island has structure and volume.

### 2. High-λ Tail is Shrinking with Refinement

**Evidence:**
- Pass 1: λ p95 = 51.4 cm
- Pass 2: λ p95 = 26.9 cm (tighter!)

**Interpretation:** The "safe zone" is concentrating toward shorter ranges under constraints + grid focus. This is expected and good - refinement is working.

### 3. Low-λ Boundary is Perfect for Sushkov

**Evidence:**
- Pass 2: λ p05 = 3.72 µm
- Sushkov 2011 strongest window: 0.4-4 µm

**Interpretation:** The low-λ boundary sits exactly where Sushkov can bite hardest. This is the perfect next constraint to add.

### What Sushkov Will Do

Adding Sushkov 2011 will either:
- ✅ Shave off the low-λ edge (most likely)
- ✅ Kill the micro-end entirely (if Sushkov is very restrictive)
- ✅ Force the viable region upward in λ (if island survives but shifts)

**All three outcomes are informative.** The goal is to see how the island responds to stronger constraints.

---

## Strategy: Sushkov > More Resolution

**Decision:** Prioritize adding Sushkov 2011 over Pass 3 (500×500 refinement).

**Reasoning:**
- The Sushkov constraint will move the island more than another grid refinement
- Pass 3 can wait until after we see how Sushkov affects the island
- Better to have a "before Sushkov" baseline at current resolution, then refine after

**Workflow:**
1. ✅ Pass 1 & Pass 2 complete (baseline established)
2. ⏳ Digitize Sushkov 2011
3. ⏳ Merge with envelope
4. ⏳ Rerun Pass 2 zoom box (same bounds for fair comparison)
5. ⏳ Compare before/after
6. ⏳ Optional: Pass 3 after Sushkov if needed

---

## Current Island Coordinates (Pass 2)

**Lambda (range):**
- p05 = 3.72 µm
- p50 = 1.00 mm (median)
- p95 = 26.9 cm

**Alpha (Yukawa strength):**
- p05 = 3.29e-12
- p50 = 1.30e-09 (median)
- p95 = 5.15e-07

**Viable points:** 159,600 (400×400 grid)

---

## Next Steps

1. **Digitize Sushkov 2011** (30-60 minutes)
   - Fill `sushkov2011_exclusion.csv`
   - Validate with `validate_digitized_curve.py`
   - Paste first 6 rows for sanity check

2. **Merge with envelope**
   - Use `add_fifth_force_curve.py --merge`
   - Generate comparison plot

3. **Rerun Pass 2 with same zoom bounds**
   - Keep same λ/α ranges for fair comparison
   - Compare island sizes

4. **Interpret results**
   - Did λ p05 increase? (island shrunk at low-λ)
   - Did island survive? (still viable or killed)
   - How much did it shrink? (quantify tightening)

---

## Files

- `overlap_pass1.json` - Coarse baseline
- `overlap_pass2.json` - Refined baseline (before Sushkov)
- `overlap_pass2_with_sushkov.json` - (After Sushkov, to be created)
- `island_comparison.png` - (Before/after plot, to be created)

