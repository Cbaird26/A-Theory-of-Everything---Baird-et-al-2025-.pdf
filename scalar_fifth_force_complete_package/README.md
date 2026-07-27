# Fifth-Force & Detectability Complete Package

**Everything you need in one place!**

This folder contains all files related to fifth-force constraints and detectability analysis for MQGT-SCF.

## Folder Structure

```
fifth_force_complete/
├── README.md (this file - master index)
├── docs/          # All documentation
├── code/          # All Python code
├── data_raw/      # Raw constraint curves (CSV files)
├── data_processed/ # Validated curves ready for analysis
├── results/       # Analysis outputs and provenance
└── tests/         # Test files
```

## Quick Start

### View Key Summaries
```bash
cat docs/fifth_force_detectability_summary.md    # Detectability results
cat docs/fifth_force_summary.md                  # Constraint dominance
cat docs/notes/2026-01-08_scalar_detectability_hunt_band.md  # Detailed memo
```

### View Results
```bash
cat results/detectability_summary.md             # Full analysis output
```

### View Data
```bash
ls -lh data_raw/                                # Raw constraint curves
ls -lh data_processed/                           # Validated curves
```

### Run Analysis (from repo root)
```bash
make fifth-detectability SEED=42 NPTS=2000
make fifth-ingest INPUT=data/raw/fifth_force/zenodo5080965_fig3_contract.csv
```

## Key Files

### Documentation
- **`docs/fifth_force_detectability_summary.md`** - Canonical detectability results (5.6 KB)
- **`docs/fifth_force_summary.md`** - Canonical constraint dominance (4.4 KB)
- **`docs/notes/2026-01-08_scalar_detectability_hunt_band.md`** - Detailed narrative memo (10 KB)
- **`docs/dev/eotwash_digitization_guide.md`** - How to digitize real curves (6.5 KB)

### Code
- **`code/detectability.py`** - Main detectability computation (12 KB)
- **`code/yukawa.py`** - Model-to-Yukawa mapping (4.0 KB)
- **`code/envelope.py`** - Envelope computation
- **`code/constraints.py`** - Constraint evaluation

### Data
- **`data_raw/zenodo5080965_fig3_contract.csv`** - Real experimental data
- **`data_raw/eotwash_*.csv`** - Synthetic test curves
- **`data_processed/*validated.csv`** - Validated curves ready for analysis

### Results
- **`results/detectability_summary.md`** - Full detectability analysis output
- **`results/*_provenance.json`** - Provenance manifests for all curves

## What's Here

- ✅ All documentation (8 files)
- ✅ All code (9 Python files)
- ✅ All data files (raw + processed)
- ✅ All results (summary + provenance)
- ✅ All tests (3 test files)

**Total: 41+ files, all organized in one place!**

## Next Steps

1. **Digitize real mm-cm curve:** See `docs/dev/eotwash_digitization_guide.md`
2. **Ingest digitized curve:** `make fifth-ingest INPUT=...`
3. **Rerun detectability:** `make fifth-detectability SEED=42 NPTS=2000`

---

**Created:** 2026-01-08
**Purpose:** Complete package of all fifth-force and detectability files for easy access

---

## NEW: Real Curve Processing (2026-01-08)

### Quick Start

Once you have digitized `eotwash_prl2016_digitized_contract.csv`:

```bash
./process_real_eotwash_curve.sh
```

### Files Added

- **`process_real_eotwash_curve.sh`** - Automation script for Steps 2-5
- **`docs/canonical_statement_template.md`** - Template for updating canonical statement
- **`docs/real_curve_workflow.md`** - Complete workflow checklist
- **`REAL_CURVE_QUICKSTART.md`** - Quick reference guide

### Workflow

1. **Digitize curve** (manual): Use `docs/eotwash_digitization_guide.md`
2. **Run automation**: `./process_real_eotwash_curve.sh`
3. **Update canonical statement**: Follow `docs/canonical_statement_template.md`
4. **Update related docs**: Follow `docs/real_curve_workflow.md`

See `REAL_CURVE_QUICKSTART.md` for one-page summary.

