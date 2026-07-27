# Eöt-Wash Digitization Quick Reference

**One-page reference for digitizing mm-cm fifth-force constraints**

---

## Which Plot?

**Eöt-Wash / Tan et al. PRL 2016**  
Search: "PRL 116, 131102 (2016) fifth force" or "Eöt-Wash inverse square law Yukawa constraints"

---

## Tool

**WebPlotDigitizer:** https://apps.automeris.io/wpd/

---

## Axis Conventions

- **X-axis:** λ (meters), **LOG scale**
- **Y-axis:** α (dimensionless), **LOG scale**
- **Target range:** λ ≈ 10⁻⁴ → 10⁻² m (mm to cm)

---

## Steps

1. Load plot → WebPlotDigitizer
2. Calibrate axes (LOG scale, two points each)
3. Digitize ~30-50 points along exclusion curve
4. Export CSV: `lambda_m`, `alpha_max`
5. Add columns: `source_id=eotwash_prl2016_digitized`, `ref="PRL 116, 131102 (2016)"`
6. Save as: `eotwash_prl2016_digitized_contract.csv`

---

## CSV Format

```csv
lambda_m,alpha_max,source_id,ref
1.2e-4,3.5e-6,eotwash_prl2016_digitized,"PRL 116, 131102 (2016) - Eöt-Wash Group"
```

**Units:** `lambda_m` in meters, `alpha_max` dimensionless

---

## Commands

```bash
# Ingest digitized curve
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv

# Rerun detectability analysis
make fifth-detectability SEED=42 NPTS=2000
```

---

## Sanity Checks

- ✅ `alpha_max` decreases as `lambda_m` decreases
- ✅ `lambda_m` in mm-cm range (0.0001 → 0.01 m)
- ✅ All values positive
- ✅ `lambda_m` strictly increasing

---

## Expected Time

**~10 minutes**

---

## Full Guide

See `docs/dev/eotwash_digitization_guide.md` for detailed instructions.

