# Fifth-Force Constraint Datasets

This directory contains raw fifth-force constraint curves used by the MQGT-SCF detectability pipeline.

---

## Datasets

### Synthetic / Placeholder Curves

#### `placeholder_eotwash_style.csv`
- **Type:** Synthetic placeholder
- **Purpose:** Initial testing and pipeline validation
- **Range:** mm-cm scale (λ ≈ 10⁻⁴ → 10⁻² m)
- **Note:** Looser than real experimental constraints

#### `eotwash_style_synthetic_contract.csv`
- **Type:** Synthetic Eöt-Wash-style curve
- **Purpose:** Testing envelope logic and detectability analysis
- **Range:** mm-cm scale
- **Note:** Based on Eöt-Wash constraint patterns but not from real data

#### `eotwash_tighter_synthetic_contract.csv`
- **Type:** Tighter synthetic Eöt-Wash-style curve
- **Purpose:** Stress-testing detectability pipeline under tighter constraints
- **Range:** mm-cm scale
- **Note:** 10× tighter than placeholder to test hunt band persistence

### Real Experimental Curves

#### `zenodo5080965_fig3_contract.csv`
- **Source:** Heacock & Huber (2021), Zenodo DOI: 10.5281/zenodo.5080965
- **Type:** Machine-readable experimental data
- **Range:** Picometer-nanometer scale (λ ≈ 10⁻¹² → 10⁻⁹ m)
- **Ingestion:** Automated via `code/inference/fifth_force/importers/zenodo5080965_fig3.py`
- **Note:** Different regime than mm-cm hunt band; used for envelope completeness

#### `eotwash_prl2016_digitized_contract.csv` ✅ **CANONICAL**
- **Source:** Eöt-Wash Group / Tan et al. PRL 116, 131102 (2016)
- **Type:** Digitized from published plot (monotone_conservative version)
- **Range:** Millimeter-centimeter scale (λ ≈ 3×10⁻⁵ → 9×10⁻⁴ m, 29 points)
- **Purpose:** **Critical for mm-cm hunt band analysis**
- **Status:** ✅ **Completed** - Uses monotone_conservative processing (running-minimum algorithm)
- **Processing:** Conservative smoothing prevents fake-tight exclusions from digitization noise
- **Variants:** See `variants/` directory for alternate versions (READY, sorted)
- **Digitization Visuals:** See `docs/dev/digitization_visuals/` for process documentation

---

## Digitization Process

### For `eotwash_prl2016_digitized_contract.csv`

This curve is the **critical missing piece** for anchoring the mm-cm detectability analysis to real experimental constraints.

#### Steps

1. **Locate the plot:**
   - Eöt-Wash Group / Tan et al. PRL 2016
   - Search: "PRL 116, 131102 (2016) fifth force"
   - Look for Yukawa (α, λ) exclusion plot in mm-cm range

2. **Digitize using WebPlotDigitizer:**
   - Tool: https://apps.automeris.io/wpd/
   - See full guide: `docs/dev/eotwash_digitization_guide.md`
   - Quick reference: `docs/dev/eotwash_digitization_quickref.md`

3. **Format the CSV:**
   - Use template: `eotwash_prl2016_digitized_contract.csv.template`
   - Required columns: `lambda_m`, `alpha_max`, `source_id`
   - Optional: `ref` (paper citation)
   - Units: `lambda_m` in meters, `alpha_max` dimensionless

4. **Ingest:**
   ```bash
   make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
   ```

5. **Rerun detectability:**
   ```bash
   make fifth-detectability SEED=42 NPTS=2000
   ```

#### Expected Provenance

When digitized, record:
- **Plot source:** Paper citation and figure number
- **Digitization date:** When the digitization was performed
- **Tool:** WebPlotDigitizer version/URL
- **Digitizer:** Name/identifier of person who digitized
- **Verification:** Sanity checks passed (monotonic, correct units, etc.)

---

## Data Contract

All constraint curves must conform to the fifth-force data contract:

- **Schema:** See `docs/fifth_force_data_contract.md`
- **Validation:** Enforced by `code/inference/fifth_force/ingest.py`
- **Provenance:** Generated automatically during ingestion

### Key Requirements

- `lambda_m`: meters, positive, strictly increasing
- `alpha_max`: dimensionless, positive
- `source_id`: unique identifier string
- Exclusion curves: `alpha_max` generally decreases as `lambda_m` decreases

---

## File Naming Convention

- **Synthetic:** `*_synthetic*.csv` or `placeholder_*.csv`
- **Real automated:** `*_contract.csv` (from importers)
- **Real digitized:** `*_digitized_contract.csv` (manual digitization)
- **Templates:** `*.template` (not ingested, for reference)
- **Variants:** Stored in `variants/` subdirectory with descriptive suffixes:
  - `*_READY.csv` - Raw digitized (no processing)
  - `*_sorted.csv` - Pre-sorted for efficiency
  - `*_monotone_conservative.csv` - Conservative running-minimum version (canonical)

---

## Related Documentation

- **Data Contract:** `docs/fifth_force_data_contract.md`
- **Digitization Guide:** `docs/dev/eotwash_digitization_guide.md`
- **Quick Reference:** `docs/dev/eotwash_digitization_quickref.md`
- **Start Here:** `docs/fifth_force_start_here.md`
- **Summary:** `docs/fifth_force_summary.md`

---

## Notes

- **Synthetic curves** are for pipeline testing and should not be used for final conclusions
- **Real curves** are required for world-facing physics results
- The **mm-cm digitized curve** is the critical missing piece for the hunt band analysis
- Envelope logic combines all curves to find the tightest bound at each λ

