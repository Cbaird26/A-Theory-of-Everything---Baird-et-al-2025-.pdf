# QRNG Pipeline — Start Here

This guide walks you through the complete QRNG bias-detection pipeline from raw data to calibrated results.

**Time:** ~10 minutes for a first run  
**Prerequisites:** Python 3.8+, pytest (for tests)

---

## Quick Start (3 Steps)

### 1. Validate the Pipeline

Run the regression tests to ensure everything works:

```bash
make qrng-validate
```

Or directly:

```bash
pytest -q tests/test_qrng_controls_regression.py tests/test_qrng_ingest_contract.py
```

**Expected:** All tests pass. This confirms:
- Fair controls correctly reject bias (BF10 < 1/3)
- Biased controls correctly detect bias (BF10 > 10)
- Data contract validation works

---

### 2. Ingest Raw QRNG Data

Place your raw QRNG CSV in `data/raw/`, then validate and ingest:

```bash
make qrng-ingest INPUT=data/raw/my_qrng.csv
```

Or directly:

```bash
python -m code.inference.qrng_ingest data/raw/my_qrng.csv
```

**What this does:**
- Validates schema (timestamp, bit, source_id)
- Normalizes format
- Generates provenance manifest (SHA256, row counts, time ranges)
- Writes validated CSV to `data/processed/`
- Writes provenance to `results/qrng/`

**Output:**
- `data/processed/my_qrng_validated.csv` — normalized, validated data
- `results/qrng/my_qrng_provenance.json` — audit trail

---

### 3. Run Analysis

#### Option A: Calibration (Control Datasets)

If you have control datasets (fair + biased):

```bash
make qrng-calibrate FAIR=CONTROL_random_200k.csv BIASED=CONTROL_bias_p505_200k.csv
```

Or directly:

```bash
cd experiments/constraints/scripts
python calibrate_qrng_physics.py \
  --fair CONTROL_random_200k.csv \
  --biased CONTROL_bias_p505_200k.csv \
  --priors 0.5,1.0,2.0
```

**Output:** Calibration report showing:
- Fair control: BF10 < 1/3 (no bias detected)
- Biased control: BF10 > 10 (bias detected)
- Prior robustness check

#### Option B: Mixed Dataset Analysis

For combined datasets:

```bash
make qrng-mixed MIXED=file1.csv,file2.csv
```

Or directly:

```bash
cd experiments/constraints/scripts
python calibrate_qrng_physics.py --mixed file1.csv,file2.csv
```

---

## Where Outputs Land

### Validated Data
- **Location:** `data/processed/`
- **Format:** Normalized CSV (timestamp, bit, source_id)
- **Naming:** `{original_name}_validated.csv`

### Provenance Manifests
- **Location:** `results/qrng/`
- **Format:** JSON with SHA256, row counts, time ranges, source distribution
- **Naming:** `{original_name}_provenance.json`

### Analysis Results
- **Location:** `experiments/constraints/results/`
- **Format:** JSON summaries, plots, calibration reports
- **Files:** `QRNG_CALIBRATION.json`, `QRNG_CALIBRATION.png`, etc.

---

## Data Contract

All QRNG logs must conform to the schema defined in `docs/qrng_data_contract.md`:

**Required columns:**
- `timestamp` — ISO 8601 (UTC recommended)
- `bit` — integer in {0, 1}
- `source_id` — string identifier (≤64 chars)

**Validation rules:**
- No missing required columns
- No invalid bit values
- No unparseable timestamps
- No empty source_ids

See `docs/qrng_data_contract.md` for full specification.

---

## Troubleshooting

### "Missing required column"
→ Check that your CSV has `timestamp`, `bit`, and `source_id` columns.

### "Invalid bit value"
→ Ensure `bit` column contains only `0` or `1` (not booleans, floats, or other values).

### "Empty timestamp" or "Empty source_id"
→ Remove rows with blank values, or fill them explicitly.

### Tests fail
→ Run `make qrng-validate` to see which test fails. Check that:
- `calibrate_qrng_physics.py` is import-safe
- Required dependencies are installed (scipy, numpy)

---

## Next Steps

- **Calibration certificate:** See `docs/qrng_pipeline_validation.md`
- **Discussion notes:** See `docs/notes/qrng_pipeline_validation_discussion.md`
- **Engineering plan:** See `docs/dev/qrng_regression_lock_plan.md`
- **Data contract:** See `docs/qrng_data_contract.md`

---

## Full Workflow Example

```bash
# 1. Validate pipeline
make qrng-validate

# 2. Ingest raw data
make qrng-ingest INPUT=data/raw/my_qrng.csv

# 3. Run analysis (if you have control datasets)
make qrng-calibrate FAIR=CONTROL_random_200k.csv BIASED=CONTROL_bias_p505_200k.csv

# 4. Check outputs
ls -lh data/processed/
ls -lh results/qrng/
```

---

**Questions?** See the full documentation in `docs/` or check the test files in `tests/` for examples.

