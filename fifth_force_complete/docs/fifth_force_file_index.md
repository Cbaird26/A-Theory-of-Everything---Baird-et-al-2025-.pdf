# Fifth-Force & Detectability File Index

**Complete inventory of all files related to fifth-force constraints and detectability analysis**

**Date:** 2026-01-08

---

## Documentation Files

### Canonical Summaries (Reviewer-Safe)

1. **`docs/fifth_force_summary.md`**
   - Purpose: Fifth-force constraint dominance analysis summary
   - Content: Dominance percentages, envelope analysis, mapping sensitivity
   - Status: Canonical, empirical

2. **`docs/fifth_force_detectability_summary.md`**
   - Purpose: Detectability analysis summary (where scalar would be detectable)
   - Content: Hunt band identification, r-ratio statistics, mm-cm regime analysis
   - Status: Canonical, empirical

3. **`docs/fifth_force_start_here.md`**
   - Purpose: Quick start guide for fifth-force pipeline
   - Content: Validation, ingestion, scanning instructions
   - Status: User guide

4. **`docs/fifth_force_data_contract.md`**
   - Purpose: Data contract specification for constraint curves
   - Content: Schema, validation rules, required/optional columns
   - Status: Technical specification

### Detailed Memos (Narrative, Interpretive)

5. **`docs/notes/2026-01-08_scalar_detectability_hunt_band.md`**
   - Purpose: Detailed narrative memo on detectability analysis
   - Content: Context, implementation, interpretation, citations, future proposals
   - Status: Lab notebook entry

### Development Guides

6. **`docs/dev/eotwash_digitization_guide.md`**
   - Purpose: Step-by-step guide for digitizing Eöt-Wash constraint curves
   - Content: WebPlotDigitizer instructions, axis calibration, CSV formatting
   - Status: User guide

7. **`docs/dev/eotwash_digitization_quickref.md`**
   - Purpose: One-page quick reference for digitization
   - Content: Commands, sanity checks, essential info
   - Status: Quick reference

8. **`docs/dev/fifth_force_mapping_audit.md`**
   - Purpose: Documentation of model-to-Yukawa parameter mapping
   - Content: Mapping formulas, physics justification, sensitivity analysis
   - Status: Technical documentation

---

## Code Files

### Core Implementation

9. **`code/inference/fifth_force/detectability.py`**
   - Purpose: Detectability map computation
   - Function: Samples points, computes r = alpha_pred / alpha_max, generates summary
   - Usage: `make fifth-detectability SEED=42 NPTS=2000`

10. **`code/inference/fifth_force/yukawa.py`**
    - Purpose: Model-to-Yukawa parameter mapping
    - Function: Converts (m_phi, theta, mu_sb) → (alpha_pred, lambda_m)
    - Key: Uses CODATA ħc, includes scale-breaking suppression

11. **`code/inference/fifth_force/constraints.py`**
    - Purpose: Constraint curve loading and evaluation
    - Function: `load_curve()`, `max_alpha_allowed()`, `is_excluded()`

12. **`code/inference/fifth_force/envelope.py`**
    - Purpose: Envelope computation (tightest bound across curves)
    - Function: `alpha_max_envelope()` takes minimum at each lambda_m

13. **`code/inference/fifth_force/slack.py`**
    - Purpose: Slack computation for dominance analysis
    - Function: `fifth_force_slack()` computes normalized slack

14. **`code/inference/fifth_force/ingest.py`**
    - Purpose: CSV validation and provenance generation
    - Function: Validates against contract, generates provenance manifests

15. **`code/inference/fifth_force/registry.py`**
    - Purpose: Discovers available constraint curves
    - Function: `list_curves()` finds validated CSV files

16. **`code/inference/fifth_force/curve_registry.py`**
    - Purpose: Selects default curve for analysis
    - Function: Prefers zenodo, falls back to placeholder

### Importers

17. **`code/inference/fifth_force/importers/zenodo5080965_fig3.py`**
    - Purpose: Automated importer for Heacock & Huber Zenodo dataset
    - Function: Downloads Data.zip, extracts Fig3.xls, converts to contract CSV
    - Usage: `make fifth-fetch-zenodo5080965`

---

## Data Files

### Raw Data (Input)

18. **`data/raw/fifth_force/README.md`**
    - Purpose: Documentation of all raw datasets
    - Content: Dataset descriptions, digitization process, provenance guidelines

19. **`data/raw/fifth_force/placeholder_eotwash_style.csv`**
    - Type: Synthetic placeholder
    - Purpose: Initial pipeline testing
    - Range: λ ~ 10⁻⁶ to 10⁻³ m

20. **`data/raw/fifth_force/eotwash_style_synthetic_contract.csv`**
    - Type: Synthetic Eöt-Wash-style curve
    - Purpose: Testing envelope logic
    - Range: λ ~ 10⁻⁴ to 10⁻² m

21. **`data/raw/fifth_force/eotwash_tighter_synthetic_contract.csv`**
    - Type: Tighter synthetic curve (10× tighter than placeholder)
    - Purpose: Stress-testing detectability pipeline
    - Range: λ ~ 10⁻⁴ to 10⁻² m

22. **`data/raw/fifth_force/zenodo5080965_fig3_contract.csv`**
    - Type: Real experimental data
    - Source: Heacock & Huber, DOI: 10.5281/zenodo.5080965
    - Range: Picometer-nanometer scale
    - Status: Real constraint data

23. **`data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv.template`**
    - Type: Template for digitized curve
    - Purpose: Guide for manual digitization
    - Status: Template (not ingested)

24. **`data/raw/fifth_force/Data.zip`**
    - Type: Raw Zenodo dataset
    - Source: Heacock & Huber Zenodo archive
    - Contains: Fig3.xls and other data files

### Processed Data (Validated)

25. **`data/processed/placeholder_eotwash_style_validated.csv`**
    - Type: Validated constraint curve
    - Source: Validated from placeholder_eotwash_style.csv
    - Status: Ready for analysis

26. **`data/processed/eotwash_style_synthetic_contract_validated.csv`**
    - Type: Validated constraint curve
    - Source: Validated from eotwash_style_synthetic_contract.csv
    - Status: Ready for analysis

27. **`data/processed/eotwash_tighter_synthetic_contract_validated.csv`**
    - Type: Validated constraint curve
    - Source: Validated from eotwash_tighter_synthetic_contract.csv
    - Status: Ready for analysis

28. **`data/processed/zenodo5080965_fig3_contract_validated.csv`**
    - Type: Validated constraint curve
    - Source: Validated from zenodo5080965_fig3_contract.csv
    - Status: Real experimental data, ready for analysis

---

## Results Files

### Analysis Outputs

29. **`results/fifth_force/detectability_summary.md`**
    - Purpose: Raw detectability analysis output
    - Content: Full tables, statistics, top 25 points by r
    - Status: Generated by `make fifth-detectability`

### Provenance Manifests

30. **`results/fifth_force/placeholder_eotwash_style_provenance.json`**
    - Purpose: Provenance manifest for placeholder curve
    - Content: SHA256 hash, row count, timestamp, source info

31. **`results/fifth_force/eotwash_style_synthetic_contract_provenance.json`**
    - Purpose: Provenance manifest for synthetic curve
    - Content: SHA256 hash, row count, timestamp, source info

32. **`results/fifth_force/eotwash_tighter_synthetic_contract_provenance.json`**
    - Purpose: Provenance manifest for tighter synthetic curve
    - Content: SHA256 hash, row count, timestamp, source info

33. **`results/fifth_force/zenodo5080965_fig3_contract_provenance.json`**
    - Purpose: Provenance manifest for Zenodo curve
    - Content: SHA256 hash, row count, timestamp, DOI, source info

---

## Test Files

34. **`tests/test_fifth_force_contract.py`**
    - Purpose: Tests for CSV contract validation
    - Content: Valid CSV ingestion, rejection of bad data, missing columns

35. **`tests/test_fifth_force_constraints_regression.py`**
    - Purpose: Regression tests for constraint evaluation
    - Content: `is_excluded()` tests, normalized slack consistency

36. **`tests/test_fifth_force_detectability.py`**
    - Purpose: Regression tests for detectability computation
    - Content: Point sampling, lambda monotonicity, r computation, exclusion logic

---

## Legacy/Experimental Files

37. **`experiments/constraints/data/eotwash_master_exclusion.csv`**
    - Type: Legacy experimental data
    - Status: May be superseded by new pipeline

38. **`experiments/constraints/data/fifth_force_exclusion.csv`**
    - Type: Legacy experimental data
    - Status: May be superseded by new pipeline

39. **`experiments/constraints/data/fifth_force_exclusion_PLACEHOLDER.csv`**
    - Type: Legacy placeholder
    - Status: May be superseded by new pipeline

40. **`experiments/constraints/data/fifth_force_exclusion_envelope.csv`**
    - Type: Legacy envelope data
    - Status: May be superseded by new pipeline

41. **`experiments/constraints/scripts/add_fifth_force_curve.py`**
    - Type: Legacy script
    - Status: May be superseded by new pipeline

42. **`experiments/constraints/scripts/fifth_force_yukawa.py`**
    - Type: Legacy script
    - Status: May be superseded by new pipeline

---

## Quick Access Commands

### View Documentation
```bash
# Canonical summaries
cat docs/fifth_force_summary.md
cat docs/fifth_force_detectability_summary.md

# Detailed memo
cat docs/notes/2026-01-08_scalar_detectability_hunt_band.md

# Digitization guide
cat docs/dev/eotwash_digitization_guide.md
```

### View Data Files
```bash
# Raw constraint curves
ls -lh data/raw/fifth_force/*.csv
head data/raw/fifth_force/zenodo5080965_fig3_contract.csv

# Processed (validated) curves
ls -lh data/processed/*validated.csv
head data/processed/zenodo5080965_fig3_contract_validated.csv
```

### View Results
```bash
# Detectability summary
cat results/fifth_force/detectability_summary.md

# Provenance manifests
cat results/fifth_force/*_provenance.json
```

### Run Analysis
```bash
# Ingest a curve
make fifth-ingest INPUT=data/raw/fifth_force/zenodo5080965_fig3_contract.csv

# Run detectability analysis
make fifth-detectability SEED=42 NPTS=2000

# Fetch Zenodo data
make fifth-fetch-zenodo5080965
```

---

## File Count Summary

- **Documentation:** 8 files
- **Code:** 9 files (core + importers)
- **Raw Data:** 6 files (4 CSVs + 1 template + 1 zip)
- **Processed Data:** 4 validated CSV files
- **Results:** 5 files (1 summary + 4 provenance JSONs)
- **Tests:** 3 files
- **Legacy:** 6 files (experimental directory)

**Total:** 41 files related to fifth-force constraints and detectability

---

## Key Files for Reviewers

1. **`docs/fifth_force_detectability_summary.md`** - Canonical detectability results
2. **`docs/fifth_force_summary.md`** - Canonical constraint dominance results
3. **`docs/notes/2026-01-08_scalar_detectability_hunt_band.md`** - Detailed interpretation
4. **`results/fifth_force/detectability_summary.md`** - Raw analysis output
5. **`code/inference/fifth_force/detectability.py`** - Implementation code

---

## Next Steps

1. **Digitize real mm-cm curve:** Use `docs/dev/eotwash_digitization_guide.md`
2. **Ingest digitized curve:** `make fifth-ingest INPUT=...`
3. **Rerun detectability:** `make fifth-detectability SEED=42 NPTS=2000`
4. **Update summaries:** Refresh canonical documents with real curve results

