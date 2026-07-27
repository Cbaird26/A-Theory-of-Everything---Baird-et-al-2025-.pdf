# Eöt-Wash Digitization Guide: From Plot to Pipeline

## Objective

Extract **one real experimental exclusion curve** in the mm-cm regime and feed it into the detectability pipeline to answer:

**"Is the scalar still alive here, or is it dead?"**

This is the critical step that moves us from synthetic constraints to real experimental bounds.

---

## What Curve to Digitize

Use a torsion-balance / inverse-square-law test that explicitly reports Yukawa (α, λ) bounds in the millimeter range.

### Recommended Source

**Eöt-Wash / Kapner et al. / Tan et al. (PRL 2016)**

These are the gold-standard mm-cm fifth-force bounds. Search for:
- "Eöt-Wash inverse square law Yukawa constraints"
- "PRL 116, 131102 (2016) fifth force"

### What You're Looking For

A plot with:
- **x-axis:** λ (meters), **log scale**
- **y-axis:** α (dimensionless), **log scale**
- **A descending exclusion curve** in the mm-cm region (λ ≈ 10⁻⁴ → 10⁻² m)

The curve represents the **upper limit** α_max(λ) — points above the curve are excluded.

---

## Tool: WebPlotDigitizer

**URL:** https://apps.automeris.io/wpd/

- No install required
- Works in browser
- Handles log-scale axes correctly

---

## Step-by-Step Instructions

### 1. Open the Plot

1. Screenshot or download the PDF page with the curve
2. Crop to just the graph (axes must be visible)

### 2. Load into WebPlotDigitizer

1. Launch WebPlotDigitizer → **Load Image**
2. Select your cropped plot image

### 3. Set Axes (Critical Step)

1. Choose **2D (X-Y) Plot**
2. Set **both axes to LOG scale**

#### Axis Calibration

**X-axis (λ in meters):**
- Click two known points on the x-axis
- Example: 1e-4 m and 1e-2 m
- Enter the actual values when prompted

**Y-axis (α dimensionless):**
- Click two known points on the y-axis
- Example: 1e-6 and 1e-2
- Enter the actual values when prompted

**⚠️ Take your time here. This is the only "precision" step.**
- Mis-calibrated axes will produce incorrect data
- Double-check by verifying a few known points on the curve

### 4. Digitize the Curve

1. Choose **Manual Mode**
2. Click along the **exclusion curve** (the upper bound)
3. **~30-50 points** is more than enough
4. **Focus on λ ≈ 10⁻⁴ → 10⁻² m** (mm to cm range)

**Tips:**
- Trace the curve smoothly, not too densely
- Include points at both ends of your target range
- The curve should be **monotonically decreasing** (α_max decreases as λ decreases)

### 5. Export CSV

1. Export as CSV with two columns: `lambda_m`, `alpha_max`
2. Save as: `eotwash_prl2016_mm_digitized.csv`

---

## Contract Format (Drop-In Ready)

Edit the CSV to match the fifth-force data contract schema:

```csv
lambda_m,alpha_max,source_id,ref
1.2e-4,3.5e-6,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
2.5e-4,2.1e-6,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
...
```

### Required Columns

- `lambda_m` — range in **meters** (float, positive, strictly increasing)
- `alpha_max` — maximum allowed strength (dimensionless, positive)
- `source_id` — use: `eotwash_prl2016_digitized`

### Optional Columns

- `ref` — paper citation (e.g., `"PRL 116, 131102 (2016) - Eöt-Wash Group"`)

### Units

- **lambda_m:** meters (e.g., 0.001 = 1 mm)
- **alpha_max:** dimensionless (relative to gravity)

### Validation Rules

The CSV must satisfy:
- `lambda_m` values are **strictly increasing**
- All `lambda_m` > 0
- All `alpha_max` > 0
- `alpha_max` generally **decreases** as `lambda_m` decreases (exclusion curve)

---

## Sanity Checks (Before Ingestion)

Ask yourself:

1. ✅ Does `alpha_max` decrease as `lambda_m` decreases? (Exclusion curves slope down)
2. ✅ Is `lambda_m` in mm-cm range? (0.0001 m to 0.01 m)
3. ✅ Does this look tighter than the placeholder? (Should exclude more parameter space)
4. ✅ Are units correct? (meters, not mm or cm)
5. ✅ Is the curve monotonic? (No reversals)

If **all yes** → you're golden.

---

## Ingestion & Hunt

Once the CSV is ready:

```bash
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
make fifth-detectability SEED=42 NPTS=2000
```

This will:
1. Validate the CSV against the contract
2. Generate provenance manifest
3. Update the envelope (combining with existing curves)
4. Recompute `r = alpha_pred / alpha_max_envelope`
5. Tell us if the hunt band survives or collapses

---

## How We Interpret the Result

### Case A — Hunt Band Survives (r ≈ 0.1-1)

We can honestly say:

> "This scalar is not detected, but remains maximally constrained near λ ≈ ___ mm. A targeted experiment here would decisively test it."

**That is world-facing physics.**

### Case B — Hunt Band Collapses (r ≪ 1 everywhere)

We say:

> "This class of scalar is ruled out at mm-cm scales under existing constraints."

**That is still a win — clean falsification.**

Either way, we're done guessing.

---

## Expected Time

**~10 minutes** for the digitization step.

Most of the time is spent:
- Calibrating axes correctly (2-3 minutes)
- Tracing the curve smoothly (3-5 minutes)
- Formatting the CSV (1-2 minutes)

---

## Troubleshooting

### "My alpha_max values are increasing"
- You're tracing the wrong curve (trace the **upper bound**, not lower)
- Or axes are reversed

### "Lambda values are negative or zero"
- Check axis calibration (units and scale)
- Verify you're reading meters, not mm/cm

### "The curve has reversals"
- Re-trace more carefully
- Exclusion curves should be monotonic

### "Ingestion fails validation"
- Check `lambda_m` is strictly increasing
- Verify all values are positive
- Ensure CSV has no extra headers or formatting

---

## Next Steps After Digitization

1. **Ingest:** Run `make fifth-ingest` (validates and creates provenance)
2. **Rerun detectability:** Run `make fifth-detectability` (computes r ratios)
3. **Compare results:** Check if hunt band persists or collapses
4. **Write canonical conclusion:** Based on the outcome

See `docs/dev/eotwash_digitization_quickref.md` for a one-page quick reference.

---

## Why This Matters

You were right to pull us away from:
- ❌ Stale RNG
- ❌ Coin-flip mysticism  
- ❌ Statistical self-harm

This is how discovery actually happens:
- ✅ Geometry
- ✅ Force laws
- ✅ Exclusion curves
- ✅ Narrow pressure zones

You didn't slow us down. You aimed us.

---

## References

- **Eöt-Wash Group:** Standard mm-cm fifth-force constraints
- **PRL 116, 131102 (2016):** Tan et al. inverse-square-law test
- **WebPlotDigitizer:** https://apps.automeris.io/wpd/
- **Fifth-Force Data Contract:** `docs/fifth_force_data_contract.md`

