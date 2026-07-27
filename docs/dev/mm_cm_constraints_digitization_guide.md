# mm-cm Range Constraint Digitization Guide

**Date:** 2026-01-21  
**Purpose:** Step-by-step guide for digitizing Kapner 2007 and Lee 2020 fifth-force constraint curves

---

## Overview

This guide walks through digitizing constraint curves from Kapner et al. (2007) and Lee et al. (2020) to extend real-only coverage into the mm-cm range (1 mm to 10 mm), eliminating reliance on synthetic "hunt band" assumptions.

---

## Prerequisites

1. **WebPlotDigitizer** (web-based tool)
   - URL: https://apps.automeris.io/wpd/
   - Alternative: Desktop version available for download

2. **PDF Access**
   - Kapner 2007: https://arxiv.org/abs/hep-ph/0611184 or PRL publication
   - Lee 2020: https://arxiv.org/abs/2002.11761

3. **Reference Example**
   - See `docs/dev/eotwash_digitization_guide.md` for the Eöt-Wash PRL 2016 workflow

---

## Kapner et al. (2007) - PRL Figure 6

### Source Information
- **Paper:** "Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale"
- **PRL:** 98, 021101 (2007)
- **arXiv:** hep-ph/0611184
- **Coverage:** λ ≈ 10 μm to 10 mm

### Figure Details
- **Target:** Figure 6 (composite exclusion plot showing multiple experiments)
- **Axes:** 
  - X-axis: λ (range in meters), log scale
  - Y-axis: α (Yukawa coupling strength), log scale
- **Curve to digitize:** Boundary of excluded region (upper envelope)

### Digitization Steps

1. **Open WebPlotDigitizer**
   - Load PDF or screenshot of Figure 6
   - Select "2D (X-Y) Plot" mode

2. **Calibrate Axes**
   - Click on two points on the X-axis (λ) to set scale
   - Click on two points on the Y-axis (α) to set scale
   - Ensure log scale is selected for both axes

3. **Digitize Exclusion Boundary**
   - Click along the exclusion boundary curve
   - Focus on the smooth envelope (avoid experimental scatter)
   - Target ~20-30 points spanning the full λ range
   - Prioritize accuracy in the mm range (1-10 mm)

4. **Export Data**
   - Export as CSV
   - Verify columns: `x` (lambda_m), `y` (alpha_max)

5. **Post-Processing**
   - Rename: `kapner_prl2007_digitized_contract.csv`
   - Ensure columns are: `lambda_m,alpha_max,source_id`
   - Add `source_id` column with value `kapner_prl2007_digitized`
   - Sort by `lambda_m` (ascending)
   - Place in: `data/raw/fifth_force/mm_cm_constraints/`

6. **Create Variants** (optional, following Eöt-Wash pattern)
   - `_READY.csv`: Raw digitized points
   - `_sorted.csv`: Pre-sorted for fast interpolation
   - `_monotone_conservative.csv`: Running-minimum conservative envelope

---

## Lee et al. (2020) - arXiv Figure 5

### Source Information
- **Paper:** "Test of the Gravitational Inverse-Square Law at Millimeter Ranges"
- **PRL:** 124, 101101 (2020)
- **arXiv:** 2002.11761
- **Coverage:** λ ≈ 52 μm to 3.0 mm

### Figure Details
- **Target:** Figure 5, **bottom panel** (95% CL upper limits on |α|)
- **Axes:**
  - X-axis: λ (range in meters), log scale
  - Y-axis: |α| (upper limit), log scale
- **Curve to digitize:** The upper limit curve (boundary of allowed region)

### Digitization Steps

1. **Open WebPlotDigitizer**
   - Load PDF or screenshot of Figure 5
   - Select bottom panel only (ignore top panel if shown)
   - Select "2D (X-Y) Plot" mode

2. **Calibrate Axes**
   - X-axis: λ (meters), log scale
   - Y-axis: |α| (upper limit), log scale
   - Ensure both axes are logarithmic

3. **Digitize Upper Limit Curve**
   - Click along the upper limit boundary
   - Aim for ~15-25 points covering 52 μm to 3.0 mm
   - Pay attention to any sharp transitions or plateaus

4. **Export Data**
   - Export as CSV
   - Verify columns: `x` (lambda_m), `y` (alpha_max)

5. **Post-Processing**
   - Rename: `lee_arxiv2020_digitized_contract.csv`
   - Ensure columns: `lambda_m,alpha_max,source_id`
   - Add `source_id` column with value `lee_arxiv2020_digitized`
   - Sort by `lambda_m` (ascending)
   - Place in: `data/raw/fifth_force/mm_cm_constraints/`

6. **Create Variants** (optional)
   - Follow same pattern as Kapner (READY, sorted, monotone)

---

## CSV Format Requirements

All digitized curves must follow this contract schema:

```csv
lambda_m,alpha_max,source_id
5.2e-5,1.0e+4,lee_arxiv2020_digitized
6.0e-5,8.0e+3,lee_arxiv2020_digitized
...
```

### Column Definitions

- **lambda_m**: Interaction range in meters (must be positive, monotonically increasing recommended)
- **alpha_max**: Maximum allowed Yukawa coupling strength (dimensionless, must be positive)
- **source_id**: Unique identifier (must match importer expectations)

### Validation

Before ingestion, verify:
- ✅ All lambda_m values are positive
- ✅ All alpha_max values are positive
- ✅ source_id is consistent across all rows
- ✅ File is sorted by lambda_m (for fast interpolation)
- ✅ No duplicate lambda_m values (or handle via monotone processing)

---

## Processing Workflow

After placing raw CSV files:

1. **Validate format:**
   ```bash
   # Check CSV structure
   head -5 data/raw/fifth_force/mm_cm_constraints/kapner_prl2007_digitized_contract.csv
   ```

2. **Ingest via pipeline:**
   ```bash
   make fifth-ingest-kapner
   make fifth-ingest-lee
   ```

3. **Verify processed files:**
   ```bash
   ls -lh data/processed/*kapner*
   ls -lh data/processed/*lee*
   ```

4. **Test envelope integration:**
   ```bash
   make fifth-detectability SEED=42 NPTS=1000 REAL_ONLY=1
   # Check that coverage report includes new curves
   ```

---

## Quality Checklist

- [ ] Figure source clearly identified (paper, figure number, panel)
- [ ] Axes correctly calibrated (log scale for both)
- [ ] ~20-30 points digitized (or sufficient for smooth interpolation)
- [ ] CSV format matches contract schema
- [ ] source_id matches importer expectation
- [ ] File passes ingestion pipeline without errors
- [ ] Coverage report shows new lambda range included
- [ ] Variants created (optional but recommended)

---

## Troubleshooting

**Problem:** WebPlotDigitizer calibration fails
- **Solution:** Ensure you're clicking exact tick marks, not approximate positions. Use grid alignment if available.

**Problem:** Exported data doesn't match figure visually
- **Solution:** Re-check axis calibration. Verify log vs linear scale selection.

**Problem:** Ingestion fails with "source_id mismatch"
- **Solution:** Ensure source_id column matches exactly what the importer expects (check importer source code).

**Problem:** Coverage report doesn't show new curves
- **Solution:** Verify `is_real_curve()` in `registry.py` recognizes the source_id pattern.

---

## References

- Eöt-Wash digitization example: `docs/dev/eotwash_digitization_guide.md`
- Data ground truth documentation: `docs/DATA_GROUND_TRUTH.md`
- Real vs synthetic guardrails: `docs/REAL_VS_SYNTHETIC_GUARDRAILS.md`

---

## Notes

- **Conservatism:** When in doubt, digitize slightly above the exclusion boundary (more conservative = larger alpha_max = less likely to exclude models)
- **Monotone processing:** The monotone conservative variant applies running-minimum to prevent noise-induced fake exclusions
- **Intersection coverage:** After ingesting both curves, check that their lambda ranges overlap appropriately for envelope merging
