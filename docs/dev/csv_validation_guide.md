# CSV Validation Guide for Digitized Eöt-Wash Curve

**Purpose:** Manual validation checklist for digitized constraint curves before ingestion.

---

## Quick Validation (30 seconds)

Run the automated check:
```bash
./check_digitized_csv.sh data_raw/eotwash_prl2016_digitized_contract.csv
```

If all checks pass → proceed to ingestion.
If any fail → fix before proceeding.

---

## Manual Validation Checklist

### 1. File Location

- [ ] File exists at expected path:
  - Package folder: `data_raw/eotwash_prl2016_digitized_contract.csv`
  - Repo root: `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv`

### 2. Header Format

- [ ] First line is: `lambda_m,alpha_max,source_id,ref`
- [ ] No extra headers or comments in header row
- [ ] Commas used as separators (not semicolons or tabs)

### 3. Lambda Values (lambda_m)

- [ ] All values are **positive** (no zeros or negatives)
- [ ] Values are in **meters** (not mm, cm, or other units)
- [ ] Values are **strictly increasing** (each row > previous row)
- [ ] Range is appropriate for mm-cm: ~10⁻⁴ to 10⁻² m
- [ ] Format is numeric (scientific notation OK: `1.2e-4`)

**Common errors:**
- ❌ Using mm instead of meters (multiply by 10⁻³)
- ❌ Using cm instead of meters (multiply by 10⁻²)
- ❌ Non-monotonic (check for sorting errors)
- ❌ Negative values (check axis calibration)

### 4. Alpha Values (alpha_max)

- [ ] All values are **positive** (no zeros or negatives)
- [ ] Values are **dimensionless** (no units)
- [ ] Values generally **decrease** as lambda_m decreases (exclusion curve slopes down)
- [ ] Format is numeric (scientific notation OK: `1.5e-6`)

**Common errors:**
- ❌ Including units (should be dimensionless)
- ❌ Reversed axis (alpha increasing instead of decreasing)
- ❌ Wrong curve traced (traced lower bound instead of upper bound)

### 5. Source ID

- [ ] Column `source_id` has value: `eotwash_prl2016_digitized`
- [ ] Consistent across all rows
- [ ] No typos or variations

### 6. Reference

- [ ] Column `ref` contains paper citation
- [ ] Format: `"PRL 116, 131102 (2016) - Eöt-Wash Group"` or similar
- [ ] Quoted if contains commas
- [ ] Consistent across all rows

### 7. Data Quality

- [ ] No empty rows
- [ ] No missing values (all 4 columns populated)
- [ ] Reasonable number of points (30-50 recommended)
- [ ] Points cover the mm-cm range (~10⁻⁴ to 10⁻² m)

### 8. Sanity Checks

- [ ] Lambda range makes sense:
  - 0.0001 m = 0.1 mm ✓
  - 0.001 m = 1 mm ✓
  - 0.01 m = 1 cm ✓
- [ ] Alpha values reasonable:
  - Typical: 10⁻⁶ to 10⁻² for mm-cm constraints
  - Not too large (>1) or too small (<10⁻¹²)
- [ ] Curve shape:
  - Alpha decreases as lambda decreases (exclusion curve)
  - No reversals or jumps

---

## Example Valid CSV

```csv
lambda_m,alpha_max,source_id,ref
1.0e-4,1.5e-5,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
2.0e-4,1.2e-5,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
5.0e-4,8.5e-6,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
1.0e-3,5.0e-6,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
2.0e-3,2.5e-6,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
5.0e-3,1.0e-6,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
1.0e-2,5.0e-7,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
```

**Key points:**
- Lambda in meters (1e-4 = 0.1 mm)
- Alpha dimensionless, decreasing
- Source ID consistent
- Reference quoted (contains comma)

---

## Common Issues and Fixes

### Issue: "Lambda values not increasing"

**Fix:** Sort CSV by lambda_m column:
```bash
(head -1 file.csv && tail -n +2 file.csv | sort -t',' -k1 -n) > sorted.csv
```

### Issue: "Units wrong (mm instead of meters)"

**Fix:** Multiply lambda_m column by 10⁻³:
```python
# Python one-liner
import pandas as pd
df = pd.read_csv('file.csv')
df['lambda_m'] = df['lambda_m'] * 1e-3  # mm to m
df.to_csv('fixed.csv', index=False)
```

### Issue: "Alpha increasing instead of decreasing"

**Fix:** You traced the wrong curve. Re-digitize, tracing the **upper bound** (exclusion curve), not the lower bound.

### Issue: "Negative values"

**Fix:** Check axis calibration in WebPlotDigitizer. Verify you clicked the correct points for axis calibration.

---

## Pre-Ingestion Checklist

Before running `make fifth-ingest`:

- [ ] Automated check passes: `./check_digitized_csv.sh [file]`
- [ ] Manual validation complete (all items above checked)
- [ ] File saved at correct path
- [ ] Backup copy saved (just in case)

---

## After Ingestion

Verify:
- [ ] Provenance manifest created: `results/fifth_force/eotwash_prl2016_digitized_contract_provenance.json`
- [ ] Validated CSV created: `data/processed/eotwash_prl2016_digitized_contract_validated.csv`
- [ ] No errors in ingestion output

---

**This validation ensures the digitized curve is ready for canonical analysis.**

