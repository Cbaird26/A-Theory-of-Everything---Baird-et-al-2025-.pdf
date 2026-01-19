# Next Steps Execution Plan - Frequency Atlas Integration

**Date:** 2026-01-18  
**Status:** Ready for Execution

---

## Overview

This document outlines the concrete next steps to complete the frequency atlas integration and validation work. All code implementation is complete; remaining tasks require Python environment execution.

---

## Completed Implementation ✅

### 1. Code Implementation
- ✅ Frequency conversion functions (`lambda_to_freq_eq`, `freq_to_energy_eV`) in `detectability.py`
- ✅ Frequency columns added to detectability DataFrame (`f_eq_hz`, `E_eq_eV`)
- ✅ Hunt band frequency analysis in `write_summary()`
- ✅ Frequency atlas script includes Bennu/OSIRIS-REx constraints
- ✅ Unit tests created for frequency conversions
- ✅ Integration tests created for frequency columns in detectability pipeline
- ✅ Makefile targets updated to include new tests

### 2. Documentation
- ✅ `docs/frequency_atlas.md` - Expanded with extended constraints
- ✅ `docs/fifth_force_detectability_summary.md` - Includes frequency context
- ✅ `docs/constraint_lab_snapshot.md` - Updated scale span description
- ✅ `docs/fifth_force_summary.md` - Enhanced frequency context section
- ✅ `docs/dev/frequency_atlas_validation_status.md` - Implementation status

---

## Remaining Tasks (Require Python Environment)

### Phase 1: Validation Testing

**1.1 Run Frequency Conversion Unit Tests**
```bash
cd /Users/christophermichaelbaird/mqgt-scf-paper
python -m pytest tests/test_fifth_force_detectability_frequency.py -v
```

**Expected:** All 8 tests pass, validating:
- Basic lambda to frequency conversion
- Eöt-Wash specific ranges (30 μm to 0.93 mm → 5.14×10¹⁰ to 1.59×10¹² Hz)
- Edge cases (zero, negative, very large/small values)
- Energy conversions
- Mathematical consistency

**1.2 Run Detectability Pipeline Tests**
```bash
python -m pytest tests/test_fifth_force_detectability.py -v
```

**Expected:** All tests pass, including new frequency column tests

**1.3 Run Full Fifth-Force Validation Suite**
```bash
make fifth-validate
```

**Expected:** All fifth-force tests pass, including new frequency tests

---

### Phase 2: Output Regeneration

**2.1 Regenerate Detectability Output**
```bash
make fifth-detectability SEED=42 NPTS=2000
```

**Verification Checklist:**
- [ ] `results/fifth_force/detectability_summary.md` includes `f_eq_hz` and `E_eq_eV` columns in tables
- [ ] Hunt band section exists with frequency ranges
- [ ] Hunt band f_eq range matches expected: ~5×10¹⁰ to 1.6×10¹² Hz
- [ ] Frequency translation notes are present in "Where to Look" section
- [ ] Top 25 points table includes frequency columns
- [ ] No errors or warnings in output

**2.2 Verify Hunt Band Calculations**

**Manual Verification Steps:**
1. Check that hunt band λ range matches Eöt-Wash range (30 μm to 0.93 mm)
2. Verify hunt band f_eq range: 5.14×10¹⁰ to 1.59×10¹² Hz
3. Verify calculations: `f_eq = c/(2πλ)` for each point in hunt band
4. Check that frequency values are consistent with lambda values
5. Verify E_eq calculations: `E_eq = hf/e` for each point

**Expected Hunt Band Characteristics:**
- λ range: ~3×10⁻⁵ to 9.29×10⁻⁴ m (30 μm to 0.93 mm)
- f_eq range: ~5.14×10¹⁰ to 1.59×10¹² Hz
- E_eq range: ~2.12×10⁻⁴ to 6.59×10⁻³ eV
- Description: "tens-of-GHz → low-THz equivalent scale"

---

### Phase 3: Frequency Atlas Script Validation

**3.1 Run Frequency Atlas Script**
```bash
python scripts/frequency_atlas.py
```

**Expected Output:**
- Script runs without errors
- Generates expected landmarks including:
  - Bennu/OSIRIS-REx constraints
  - Eöt-Wash hunt band equivalent frequencies
  - All MQGT-SCF constraint channels
- Outputs are consistent with documented values

**3.2 Verify Frequency Ladder Generation**
```bash
make fifth-frequency-figure
```

**Expected:**
- Generates `results/frequency_ladder.png` and `.pdf`
- Shows all constraint channels on unified log-scale axis
- Includes Bennu and hunt band annotations
- Figure is publication-ready

---

### Phase 4: Consistency Verification

**4.1 Cross-Reference Documentation**
- [ ] `docs/fifth_force_detectability_summary.md` frequency ranges match regenerated output
- [ ] `docs/frequency_atlas.md` ranges match script outputs
- [ ] `docs/constraint_lab_snapshot.md` scale span (~16 orders of magnitude) is accurate
- [ ] All frequency values use consistent constants (CODATA 2018)

**4.2 Verify No Regressions**
- [ ] Existing detectability logic unchanged (r calculation, exclusion flags)
- [ ] Existing constraint loading works
- [ ] Envelope logic still correct
- [ ] All existing tests still pass

---

## Critical Verification Points

### 1. Frequency Conversion Accuracy
**Check:** For λ = 9.29e-4 m (0.93 mm)
- f_eq should be ≈ 5.14×10¹⁰ Hz
- E_eq should be ≈ 2.12×10⁻⁴ eV

**Check:** For λ = 3.00e-5 m (30 μm)
- f_eq should be ≈ 1.59×10¹² Hz
- E_eq should be ≈ 6.59×10⁻³ eV

### 2. Hunt Band Domain Validation
**Critical:** Verify that hunt band points are within the Eöt-Wash curve's λ domain.

If hunt band includes points with λ > 0.93 mm or λ < 30 μm, this indicates:
- Either using extrapolated constraints (should be labeled)
- Or using multiple constraint curves (should be documented)
- Or a bug in curve domain handling

**Expected:** Hunt band should be entirely within the digitized Eöt-Wash range unless explicitly documented otherwise.

### 3. Frequency Range Consistency
**Check:** Hunt band f_eq range should match:
- Calculated from λ range using `f_eq = c/(2πλ)`
- Directly from `f_eq_hz` column in detectability output
- Documented in summary markdown

All three should agree within numerical precision.

---

## Success Criteria

### Code Quality
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] No linting errors
- [ ] Code follows existing style

### Output Quality
- [ ] Detectability summary includes frequency columns
- [ ] Frequency values are physically sensible
- [ ] Hunt band ranges are documented correctly
- [ ] Frequency ladder figure generates successfully

### Documentation Quality
- [ ] All frequency ranges consistent across docs
- [ ] "Equivalent frequency" clearly explained as translation layer
- [ ] No confusion between conceptual f_eq and literal oscillations
- [ ] All constraint channels properly annotated

---

## Troubleshooting Guide

### If frequency tests fail:
1. Check Python environment has numpy, pandas, pytest
2. Verify CODATA constants are correct in `detectability.py`
3. Check that helper functions are imported correctly

### If detectability output missing frequency columns:
1. Verify `compute_detectability()` calls `lambda_to_freq_eq()` and `freq_to_energy_eV()`
2. Check DataFrame column names match expected (`f_eq_hz`, `E_eq_eV`)
3. Verify `write_summary()` includes frequency columns in table formatting

### If hunt band frequencies don't match expected:
1. Verify digitized curve λ range (should be 30 μm to 0.93 mm)
2. Check for extrapolation beyond curve domain
3. Verify monotone envelope hasn't changed curve shape
4. Check for multiple constraint curves affecting envelope

### If frequency atlas script fails:
1. Check all dependencies (numpy, matplotlib if used)
2. Verify Bennu constraint calculations are correct
3. Check file paths and output directory permissions

---

## Next Phase: Pipeline Hardening (Future Work)

Once validation is complete, consider:

1. **Centralize Frequency Utilities**
   - Create `code/utils/frequency.py` with conversion functions
   - Import everywhere instead of duplicating

2. **Enhanced Provenance**
   - Enforce dataset contracts with required metadata
   - Add hash verification for ingested curves

3. **Envelope Diagnostics**
   - Add plots showing raw vs monotone curves
   - Visualize which constraint dominates at each λ

4. **Sensitivity Analysis**
   - Test hunt band robustness to mapping uncertainties
   - Monte Carlo digitization jitter analysis

5. **Multi-Curve Integration**
   - Properly handle Bennu constraints as separate curve
   - Atomic spectroscopy bounds as additional channel
   - Clear documentation of what each constrains

---

## Notes

- All implementation is complete; execution requires Python environment
- Tests and validation scripts are ready
- Documentation structure is in place
- Main risk: environment setup and dependency installation

---

## Quick Start Command Sequence

```bash
# 1. Navigate to repo root
cd /Users/christophermichaelbaird/mqgt-scf-paper

# 2. Run all tests
make fifth-validate

# 3. Regenerate detectability output
make fifth-detectability SEED=42 NPTS=2000

# 4. Verify output
cat results/fifth_force/detectability_summary.md | grep -A 5 "f_eq"

# 5. Generate frequency ladder figure
make fifth-frequency-figure

# 6. Check consistency
grep -r "5.14×10¹⁰\|5.14e10" docs/
```

---

**Status:** Implementation complete, awaiting Python environment for validation execution.

