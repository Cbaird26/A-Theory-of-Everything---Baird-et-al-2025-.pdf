# Exact Digitization Instructions for Real Bounds

## Current Script Interpretation

### Fifth-Force CSV (`fifth_force_exclusion.csv`)

**Current format:**
```csv
lambda,alpha,excluded
1e-06,1e-12,0
2e-06,1.5e-12,0
5e-06,2e-12,1
...
```

**How the script interprets it:**
- `excluded=1` → Points on or inside the exclusion boundary (red fill region)
- `excluded=0` → Points in allowed region (below boundary)
- The script uses `fill_between` to shade the excluded region above the boundary curve

**For digitization:**
- **Option A (recommended):** Mark all digitized points as `excluded=1` (treat as boundary curve)
  - Script will fill above the curve as excluded
  - This is the cleanest approach
  
- **Option B:** Mark boundary points as `excluded=1`, allowed points as `excluded=0`
  - Requires digitizing both sides of the boundary
  - More work, but gives explicit allowed region

**Units:**
- `lambda`: **meters** (not cm, not mm)
- `alpha`: **dimensionless** (Yukawa strength parameter)
- Log-spacing recommended but not required

**Example digitized format (Option A - boundary only):**
```csv
lambda,alpha,excluded
1.0e-06,1.2e-12,1
1.5e-06,1.8e-12,1
2.0e-06,2.5e-12,1
...
```

### Higgs Portal JSON (`higgs_limits.json`)

**Current format:**
```json
{
  "invisible_width_limit": 0.1,
  "signal_strength_deviation": 0.05,
  "mass_range_gev": [1.0, 1000.0],
  "coupling_range": [1e-6, 0.01],
  "source": "ATLAS+CMS combined (2023)",
  "note": "..."
}
```

**How the script interprets it:**
- `invisible_width_limit_mev`: Upper bound on invisible Higgs width (MeV)
- `signal_strength_deviation`: Maximum allowed fractional deviation from SM
- `mass_range_gev`: Scalar mass range [min, max] in GeV
- `coupling_range`: Higgs-portal coupling range [min, max]

**For digitization:**
- Extract numerical limits from ATLAS/CMS papers
- Update `invisible_width_limit_mev` with real bound (typically 0.1-1.0 MeV)
- Update `signal_strength_deviation` with real bound (typically 0.01-0.1)
- Keep `mass_range_gev` and `coupling_range` as the range where limits apply
- Update `source` with exact citation

**Example real data format:**
```json
{
  "invisible_width_limit_mev": 0.13,
  "signal_strength_deviation": 0.05,
  "mass_range_gev": [1.0, 1000.0],
  "coupling_range": [1e-6, 0.01],
  "source": "ATLAS-CMS combined Run 2 (2020)",
  "note": "Invisible width limit from Phys. Rev. D 101, 012002 (2020)"
}
```

## Step-by-Step Digitization Workflow

### Step 1: Fifth-Force (Kapner 2007 recommended)

1. **Find the paper:** Kapner et al. (2007) "Tests of the gravitational inverse-square law"
2. **Locate exclusion plot:** Usually Figure 1 or 2 (log-log plot of α vs λ)
3. **Digitize boundary:**
   - Use WebPlotDigitizer (https://apps.automeris.io/wpd/)
   - Extract points along the exclusion boundary
   - Export as CSV
4. **Convert to required format:**
   - Ensure `lambda` is in meters
   - Ensure `alpha` is dimensionless
   - Set all points to `excluded=1` (boundary curve)
5. **Save:** Replace `experiments/constraints/data/fifth_force_exclusion.csv`
6. **Test:** Run script and verify plot matches published figure

### Step 2: Higgs Portal (ATLAS-CMS combined)

1. **Find the paper:** ATLAS-CMS combined invisible width analysis (Run 2)
2. **Extract limits:**
   - Invisible width: typically 0.1-0.2 MeV (check exact number)
   - Signal strength: typically 0.05 fractional deviation
3. **Update JSON:**
   - Replace `invisible_width_limit_mev` with real number
   - Replace `signal_strength_deviation` with real number
   - Update `source` with exact citation
4. **Save:** Replace `experiments/constraints/data/higgs_limits.json`
5. **Test:** Run script and verify bounds are reasonable

### Step 3: Regenerate and Check Overlap

```bash
# Regenerate figures
python experiments/constraints/scripts/fifth_force_yukawa.py
python experiments/constraints/scripts/higgs_portal_bounds.py
python experiments/constraints/scripts/make_global_constraints.py

# Check overlap
python experiments/constraints/scripts/check_overlap_region.py

# Copy to paper
cp experiments/constraints/results/*.png papers/toe_closed_core/figures/
cd papers/toe_closed_core && pdflatex main.tex && pdflatex main.tex
```

## Validation Checklist

After digitization, verify:

- [ ] Fifth-force plot matches published exclusion curve (visual check)
- [ ] Higgs portal bounds are within expected range (0.1-1.0 MeV for invisible width)
- [ ] Citations in paper match exact sources used
- [ ] Overlap check runs without errors
- [ ] Global constraints figure shows all three channels

## Troubleshooting

**If plot doesn't match published figure:**
- Check units (meters vs cm/mm for lambda)
- Check axis scaling (log vs linear)
- Verify you digitized the correct curve (exclusion boundary, not allowed region)

**If script errors:**
- Verify CSV has exactly 3 columns: `lambda,alpha,excluded`
- Verify JSON is valid (use `python -m json.tool` to check)
- Check file paths are correct

