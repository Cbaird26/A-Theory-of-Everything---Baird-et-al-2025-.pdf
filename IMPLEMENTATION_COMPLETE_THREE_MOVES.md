# Implementation Complete: Three Robustness Moves

**Date:** 2026-01-21  
**Status:** ✅ **All Three Moves Implemented**

---

## Summary

All three robustness enhancements have been implemented and are ready for use:

1. ✅ **Mapping Sensitivity Sweep** - Automated cross-mode analysis
2. ✅ **Enhanced Mixture Sampling** - 50/50 default with improved coverage reporting  
3. ✅ **Constraint Expansion Infrastructure** - Ready for mm-cm range data integration

---

## Move 1: Mapping Sensitivity Sweep ✅

### What Was Implemented

**New Script:** `scripts/mapping_sensitivity_sweep.py`
- Runs detectability analysis across modes A, B, C using **identical point sets**
- Sweeps S_FF values for mode C (default: [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0])
- Generates comprehensive summary with statistics:
  - max_r, median_r, p99_r, p99.9_r
  - Required scaling factors to reach r=0.1 and r=1.0
  - Fraction statistics (excluded, hunt band, safe)
- Outputs both JSON (machine-readable) and Markdown (human-readable)

**Makefile Target:**
```bash
make fifth-mapping-sensitivity SEED=42 NPTS=2000 REAL_ONLY=1
```

**Documentation Updated:**
- `docs/MAPPING_SENSITIVITY.md` - Added automated sweep instructions

### Key Features

- **Fixed Point Set:** Critical feature - uses same model points across all modes
- **Comprehensive Metrics:** Not just max_r, but tail percentiles and scaling factors
- **Reproducible:** Includes seed and git commit hash in outputs
- **Reviewer-Proof:** Transforms "arbitrary mapping" into "explicit assumptions with robustness checks"

### Output Files

- `results/mapping_sensitivity_summary.md` - Summary table
- `results/mapping_sensitivity_summary.json` - Full results with metadata

---

## Move 2: Constraint Expansion Infrastructure ✅

### What Was Implemented

**New Importers:**
- `code/inference/fifth_force/importers/kapner_prl2007.py`
- `code/inference/fifth_force/importers/lee_arxiv2020.py`

Both follow the same pattern:
- Validate manually-digitized CSV files
- Check data ranges and format
- Generate provenance JSON
- Create validated CSVs in `data/processed/`

**Makefile Targets:**
```bash
make fifth-ingest-kapner   # After digitizing Kapner 2007
make fifth-ingest-lee      # After digitizing Lee 2020
```

**Directory Structure:**
- `data/raw/fifth_force/mm_cm_constraints/` - Storage for digitized CSVs
- `data/raw/fifth_force/mm_cm_constraints/README.md` - Documentation

**Digitization Guide:**
- `docs/dev/mm_cm_constraints_digitization_guide.md` - Complete step-by-step instructions
- Covers WebPlotDigitizer workflow
- CSV format requirements
- Processing and validation steps

**Documentation Updates:**
- `docs/DATA_GROUND_TRUTH.md` - Added Kapner and Lee entries (marked as "To be digitized")
- Updated file naming convention table

### Expected Coverage Extension

After digitization:
- **Kapner 2007:** Extends coverage to ~9.53 mm
- **Lee 2020:** Extends coverage to ~3.0 mm
- **Combined:** Real-only envelope now covers mm-cm range, eliminating synthetic "hunt band" reliance

### Next Steps (Manual)

1. Digitize Kapner 2007 Figure 6 using WebPlotDigitizer
2. Place CSV at: `data/raw/fifth_force/mm_cm_constraints/kapner_prl2007_digitized_contract.csv`
3. Run: `make fifth-ingest-kapner`
4. Repeat for Lee 2020 Figure 5 (bottom panel)

---

## Move 3: Enhanced Mixture Sampling ✅

### What Was Implemented

**Enhanced `sample_model_points()` Function:**
- Added `target_lambda_ranges` parameter for constrained sampling
- When provided, samples points such that lambda_m falls within specified ranges
- Enables true targeted sampling within real constraint windows

**Improved Sampling Logic:**
- **Default Behavior:** When `real_only=True`, automatically uses 50/50 mixture sampling
  - 50% targeted within real curve lambda ranges
  - 50% uniform across full prior range
- Can be overridden with `--target-frac` parameter

**Enhanced Coverage Reporting:**
- **Intersection Coverage:** Reports points covered by ALL real curves
- **Uncovered Points:** Explicitly tracks and reports points outside all real supports
- **Per-Curve Statistics:** Shows coverage fraction for each individual curve
- **Warning Indicators:** Visual flags if uncovered fraction > 0 in real-only mode

### Key Improvements

1. **Structural Guarantee:** 50/50 mixture ensures good resolution where data exists
2. **Auditable:** Coverage report shows exactly which lambda ranges are real-supported
3. **Conservative:** Uncovered points are explicitly flagged, not silently ignored

### Updated Functions

- `sample_model_points()` - Added lambda range targeting
- `compute_coverage_report()` - Added intersection and uncovered statistics
- `write_summary()` - Enhanced coverage report section with warnings

---

## Usage Examples

### Run Mapping Sensitivity Sweep

```bash
# Default sweep (all modes, S_FF = [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0])
make fifth-mapping-sensitivity SEED=42 NPTS=2000 REAL_ONLY=1

# Custom S_FF values
make fifth-mapping-sensitivity SEED=42 NPTS=2000 REAL_ONLY=1 S_FF_VALUES="0.1,1.0,10.0,100.0"

# View results
cat results/mapping_sensitivity_summary.md
```

### Enhanced Sampling (Automatic)

```bash
# Real-only mode now uses 50/50 mixture by default
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A

# Custom targeted fraction (e.g., 70% targeted)
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7
```

### Integrate New Constraints (After Digitization)

```bash
# After digitizing and placing CSV files:
make fifth-ingest-kapner
make fifth-ingest-lee

# Verify in detectability run
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1
# Check coverage report includes extended lambda range
```

---

## Files Created/Modified

### New Files
- `scripts/mapping_sensitivity_sweep.py` - Automated sweep script
- `code/inference/fifth_force/importers/kapner_prl2007.py` - Kapner importer
- `code/inference/fifth_force/importers/lee_arxiv2020.py` - Lee importer
- `docs/dev/mm_cm_constraints_digitization_guide.md` - Digitization guide
- `data/raw/fifth_force/mm_cm_constraints/README.md` - Directory documentation

### Modified Files
- `code/inference/fifth_force/detectability.py` - Enhanced sampling and coverage reporting
- `Makefile` - Added `fifth-mapping-sensitivity`, `fifth-ingest-kapner`, `fifth-ingest-lee` targets
- `docs/MAPPING_SENSITIVITY.md` - Added automated sweep section
- `docs/DATA_GROUND_TRUTH.md` - Added Kapner and Lee entries

---

## Testing Recommendations

### Mapping Sensitivity
```bash
# Quick test (small NPTS)
make fifth-mapping-sensitivity SEED=42 NPTS=100 REAL_ONLY=1

# Full sweep
make fifth-mapping-sensitivity SEED=42 NPTS=2000 REAL_ONLY=1
```

### Enhanced Sampling
```bash
# Test 50/50 mixture
make fifth-detectability SEED=42 NPTS=1000 REAL_ONLY=1

# Check coverage report includes intersection/uncovered stats
cat results/fifth_force/detectability_summary.md
```

### Constraint Integration (After Digitization)
```bash
# Test importer with dummy CSV (verify it validates correctly)
# Then test with real digitized data
make fifth-ingest-kapner
make fifth-ingest-lee

# Verify envelope includes new curves
python -c "from code.inference.fifth_force.registry import list_curves; print([c['source_id'] for c in list_curves(real_only=True)])"
```

---

## Key Design Decisions

1. **Fixed Point Sets:** Mapping sensitivity sweep uses identical points across modes to isolate mapping effects
2. **50/50 Default:** Mixture sampling defaults to balanced approach when real_only=True for optimal coverage
3. **Infrastructure First:** Constraint expansion infrastructure ready before digitization (can test with dummy data)
4. **Backward Compatible:** All changes maintain compatibility with existing workflows

---

## What's Next

### Immediate
- **Digitize curves:** Follow `docs/dev/mm_cm_constraints_digitization_guide.md` to create Kapner and Lee CSVs
- **Run sensitivity sweep:** Execute `make fifth-mapping-sensitivity` to verify robustness

### After Digitization
- **Ingest new curves:** Run `make fifth-ingest-kapner` and `make fifth-ingest-lee`
- **Re-run detectability:** Verify extended coverage in mm-cm range
- **Check envelope merging:** Ensure conservative minimum bound works correctly

---

**All three moves are complete and ready for use!** 🎉
