# Fifth-Force Pipeline — Start Here

This guide walks you through the complete fifth-force constraint pipeline from raw curves to dominance analysis.

**Time:** ~10 minutes for a first run  
**Prerequisites:** Python 3.8+, pytest (for tests)

---

## Quick Start (3 Steps)

### 1. Validate the Pipeline

Run the regression tests to ensure everything works:

```bash
make fifth-validate
```

Or directly:

```bash
pytest -q tests/test_fifth_force_contract.py tests/test_fifth_force_constraints_regression.py
```

**Expected:** All tests pass. This confirms:
- Schema validation works
- Constraint evaluation correctly identifies excluded/allowed points
- Synthetic curves produce expected behavior

---

### 2. Ingest Raw Constraint Curves

Place your raw constraint CSV in `data/raw/fifth_force/`, then validate and ingest:

```bash
make fifth-ingest INPUT=data/raw/fifth_force/my_constraint.csv
```

Or directly:

```bash
python -m code.inference.fifth_force.ingest data/raw/fifth_force/my_constraint.csv
```

**What this does:**
- Validates schema (lambda_m, alpha_max, source_id)
- Enforces monotonicity (lambda_m strictly increasing)
- Generates provenance manifest (SHA256, row counts, ranges)
- Writes validated CSV to `data/processed/`
- Writes provenance to `results/fifth_force/`

**Output:**
- `data/processed/my_constraint_validated.csv` — normalized, validated data
- `results/fifth_force/my_constraint_provenance.json` — audit trail

---

### 3. Run Dominance Analysis

Run a full dominance scan including fifth-force constraints:

```bash
make fifth-scan
```

Or for envelope (tightest bound across curves):

```bash
make fifth-scan-envelope
```

**Output:** Dominance summaries showing constraint percentages and boundary points.

---

## Where Outputs Land

### Validated Curves
- **Location:** `data/processed/`
- **Format:** Normalized CSV (lambda_m, alpha_max, source_id, ref)
- **Naming:** `{original_name}_validated.csv`

### Provenance Manifests
- **Location:** `results/fifth_force/`
- **Format:** JSON with SHA256, row counts, lambda ranges, source distribution
- **Naming:** `{original_name}_provenance.json`

### Analysis Results
- **Location:** `results/fifth_force/`
- **Format:** JSON summaries, markdown reports
- **Files:** `fifth_force_dominance.json`, `fifth_force_dominance_summary.md`, etc.

---

## Data Contract

All constraint curves must conform to the schema defined in `docs/fifth_force_data_contract.md`:

**Required columns:**
- `lambda_m` — range in meters (float, positive, strictly increasing)
- `alpha_max` — maximum allowed strength (dimensionless, positive)
- `source_id` — string identifier (≤64 chars)

**Validation rules:**
- No missing required columns
- lambda_m must be strictly monotonic increasing
- alpha_max must be positive for all rows

See `docs/fifth_force_data_contract.md` for full specification.

---

## Troubleshooting

### "Missing required column"
→ Check that your CSV has `lambda_m`, `alpha_max`, and `source_id` columns.

### "lambda_m not monotonic"
→ Ensure `lambda_m` values increase strictly (no duplicates, no decreases).

### "alpha_max must be positive"
→ Ensure all `alpha_max` values are > 0.

### Tests fail
→ Run `make fifth-validate` to see which test fails. Check that:
- Required dependencies are installed (scipy, numpy, pandas)
- Data files are in expected locations

---

## Next Steps

- **Results summary:** See `docs/fifth_force_summary.md`
- **Data contract:** See `docs/fifth_force_data_contract.md`
- **Mapping audit:** See `docs/dev/fifth_force_mapping_audit.md`

---

## Full Workflow Example

```bash
# 1. Validate pipeline
make fifth-validate

# 2. Ingest raw constraint curve
make fifth-ingest INPUT=data/raw/fifth_force/zenodo5080965_fig3_contract.csv

# 3. Run dominance scan
make fifth-scan

# 4. Run envelope scan (if multiple curves)
make fifth-scan-envelope

# 5. Generate full report
make fifth-report
```

---

**Questions?** See the full documentation in `docs/` or check the test files in `tests/` for examples.

