# WebPlotDigitizer Pre-Export Checklist

**Critical checks before exporting CSV (prevents 90% of screwups):**

## 1. Axes Configuration
- [ ] **Both axes set to log scale** (not linear)
- [ ] X-axis: log
- [ ] Y-axis: log

## 2. Calibration
- [ ] **Two calibration points per axis** that match the plot's tick labels
- [ ] X-axis: Two known lambda values from plot ticks
- [ ] Y-axis: Two known alpha values from plot ticks
- [ ] Verify calibration by checking a few digitized points match plot values

## 3. Units Conversion
- [ ] **Lambda values in meters** (not mm, not cm)
- [ ] If plot shows mm: multiply by 1e-3
- [ ] If plot shows cm: multiply by 1e-2
- [ ] If plot shows μm: multiply by 1e-6
- [ ] Verify: lambda should be ~1e-6 to ~1e0 meters for EP tests

## 4. Export Format
- [ ] Export as CSV
- [ ] Columns: `lambda,alpha` (or rename to match)
- [ ] Add `excluded` column: set all values to `1` (boundary points)

## 5. Post-Export Verification
After replacing CSV, run:
```bash
python experiments/constraints/scripts/sanity_check_csv.py
head -n 6 experiments/constraints/data/fifth_force_exclusion.csv
```

**Paste the 6 lines here for verification:**
- Units (meters, not mm)
- Monotonicity of lambda
- Alpha magnitude plausibility
- Excluded flag all 1s

---

## Common Mistakes to Avoid

❌ **Linear axes instead of log** → Curve will be wrong shape
❌ **Wrong units (mm instead of m)** → Lambda values 1000x too small
❌ **Only one calibration point** → Scale will be wrong
❌ **Mixed excluded flags** → Should all be 1 for boundary curve
❌ **Not checking monotonicity** → Indicates calibration issue

✅ **All checks pass** → Ready to regenerate figures and run overlap check

