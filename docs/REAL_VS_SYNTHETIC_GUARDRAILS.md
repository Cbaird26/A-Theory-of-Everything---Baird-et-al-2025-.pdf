# Real vs. Synthetic Guardrails

**Date:** 2026-01-19  
**Repository:** MQGT-SCF  
**Status:** **Canonical (Guardrail Policy)** ⭐

---

## Purpose

This document defines clear guardrails for distinguishing real experimental data from synthetic/placeholder curves, preventing overinterpretation and ensuring credibility.

---

## Labeling Convention

### Real Curves (Experimental Data)

**Real curves are experimental constraints from published sources:**

**Filename patterns:**
- Contain source identifiers: `zenodo5080965`, `eotwash_prl2016`, `bennu_osiris_rex`
- **Do not** contain `synthetic` or `placeholder`

**Examples:**
- `zenodo5080965_fig3_contract.csv` - Real data from Zenodo
- `eotwash_prl2016_digitized_contract.csv` - Real data from PRL 2016
- `bennu_osiris_rex_2024_contract.csv` - Real data from OSIRIS-REx

**Provenance:**
- Include scientific reference (DOI, paper citation)
- Generated automatically during ingestion
- Stored in `results/fifth_force/<source_id>_provenance.json`

**Usage:**
- Used in canonical analysis
- Included in real-only mode (`--real-only`)
- Reported in coverage reports

### Synthetic Curves (Scaffolding/Plumbing)

**Synthetic curves are validation/testing curves, NOT experimental data:**

**Filename patterns:**
- Contain `synthetic` or `placeholder`
- May contain `style` (e.g., "Eöt-Wash-style") indicating approximation

**Examples:**
- `placeholder_eotwash_style.csv` - Placeholder for testing
- `eotwash_style_synthetic_contract.csv` - Synthetic Eöt-Wash-style curve
- `eotwash_tighter_synthetic_contract.csv` - Tighter synthetic for stress-testing

**Provenance:**
- Explicitly labeled as "synthetic/regression/validation" in provenance manifests
- **No scientific reference** (because they're not real data)

**Usage:**
- **Only** for pipeline testing and validation
- **Excluded** from canonical analysis
- **Not used** in real-only mode (`--real-only`)

---

## Real-Only Mode

### Purpose

The `--real-only` flag excludes synthetic curves from detectability analysis, ensuring canonical results use only real experimental constraints.

### Implementation

**In `detectability.py`:**
- `--real-only` flag filters curves using `is_real_curve()` function
- Synthetic curves are excluded from envelope computation
- Coverage reporting shows only real curve coverage

**In Makefile:**
```bash
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1
```

**Behavior:**
- Only real curves are used for constraint envelope
- Points outside real curve λ coverage are **NOT** marked as "excluded"
- Coverage report shows fraction of sampled points within real coverage

### Why Real-Only Mode Matters

**Prevents overinterpretation:**
- Synthetic curves may have tighter bounds than real data
- Using synthetics could create "fake-tight" exclusions
- Real-only mode ensures results reflect actual experimental constraints

**Enables reviewer verification:**
- Reviewers can verify results use only real data
- Coverage report shows where real constraints exist
- Points outside coverage are clearly identified as unconstrained

---

## Coverage Reporting

### Purpose

Coverage reporting shows what fraction of sampled points fall within real experimental coverage, preventing overinterpretation outside data ranges.

### Implementation

**In detectability analysis:**
- Coverage report computed automatically in real-only mode
- Reported in `results/fifth_force/detectability_summary.md`
- Includes per-curve and total coverage statistics

### Coverage Report Format

```
## Real-Curve Coverage Report

**Purpose:** Shows what fraction of sampled points fall within real experimental coverage.

**Rule:** In real-only mode, points outside real curve coverage are NOT marked as 'excluded'.

### Coverage by Real Curve

| Curve | λ_min (m) | λ_max (m) | Points Covered | Fraction |
|-------|-----------|-----------|----------------|----------|
| zenodo5080965_fig3 | 1e-12 | 1e-9 | 50/856 | 5.8% |

**Total Coverage:** 100/856 points (11.7%) covered by at least one real curve
```

### Interpretation

**High coverage (>50%):**
- Most sampled points fall within real experimental coverage
- Results are well-constrained by experimental data
- Hunt band predictions are reliable

**Low coverage (<20%):**
- Most sampled points fall outside real experimental coverage
- Results are less constrained by experimental data
- Hunt band predictions should be interpreted cautiously

**Zero coverage:**
- No sampled points fall within real experimental coverage
- Results cannot be interpreted (no constraints available)
- Requires expanding real curve coverage or adjusting sampling

---

## Hard Rules

### Rule 1: Synthetic Curves Are Not Experimental Truth

**Statement:** Synthetic curves are scaffolding/regression plumbing, never experimental truth.

**Implementation:**
- Synthetic curves are explicitly labeled in filenames
- Provenance manifests explicitly state "synthetic/regression/validation"
- Excluded from canonical analysis via real-only mode

**Consequence of violation:**
- Results would be invalid (using non-experimental constraints)
- Reviewers would correctly dismiss the analysis

### Rule 2: Real-Only Mode Prevents Extrapolation

**Statement:** In real-only mode, points outside real curve coverage are NOT marked as "excluded."

**Implementation:**
- `detectability.py` checks if points are within real curve λ ranges
- Points outside coverage are skipped or marked as unconstrained
- Coverage report shows coverage gaps

**Consequence of violation:**
- Would overclaim constraints outside experimental data
- Would mislead reviewers about experimental coverage

### Rule 3: All Assumptions Must Be Explicit

**Statement:** Any assumption about mapping, coupling, or data interpretation must be documented.

**Implementation:**
- Mapping modes (A/B/C) explicitly documented with assumptions
- Coverage reporting reveals data gaps
- Falsifiers clearly stated in claims/limits document

**Consequence of violation:**
- Would enable "moving goalposts" critique
- Would reduce credibility of results

---

## Examples

### Example 1: Canonical Analysis (Real-Only Mode)

```bash
# Use only real curves
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1 ALPHA_MODE=A

# Output includes coverage report
# Shows: 85/2000 points (4.3%) covered by real curves
# Interpretation: Low coverage, results should be interpreted cautiously
```

### Example 2: Validation Run (Full Envelope)

```bash
# Include synthetic curves for validation
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=0 ALPHA_MODE=A

# Output notes: "Synthetic curves are for plumbing validation only"
# Interpretation: Validation only, not canonical analysis
```

### Example 3: Mapping Sensitivity Sweep

```bash
# Real-only mode with different mapping modes
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1 ALPHA_MODE=A
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1 ALPHA_MODE=B KAPPA=1.0
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1 ALPHA_MODE=C S_FF=0.1 S_LAMBDA=1.0

# Compare results across modes
# Interpretation: Shows robustness to mapping assumptions
```

---

## Checklist for Canonical Analysis

Before running canonical detectability analysis:

- [ ] At least one real curve ingested (`make fifth-ingest`)
- [ ] Real-only mode enabled (`REAL_ONLY=1`)
- [ ] Coverage report generated and reviewed
- [ ] Coverage >20% or explicitly acknowledged as low coverage
- [ ] Mapping mode documented and assumptions stated
- [ ] Synthetic curves explicitly excluded

Before publishing results:

- [ ] All synthetic curves explicitly labeled in provenance
- [ ] Real-only mode used for canonical analysis
- [ ] Coverage report included in summary
- [ ] Mapping assumptions documented in claims/limits doc
- [ ] No overinterpretation outside experimental coverage

---

## References

- Data ground truth: [`docs/DATA_GROUND_TRUTH.md`](DATA_GROUND_TRUTH.md)
- Mapping sensitivity: [`docs/MAPPING_SENSITIVITY.md`](MAPPING_SENSITIVITY.md)
- Claims/limits/falsifiers: [`docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`](CLAIMS_LIMITS_AND_FALSIFIERS.md)
- Fifth-force start guide: [`docs/fifth_force_start_here.md`](fifth_force_start_here.md)
- Digitization visuals: [`docs/dev/digitization_visuals/`](dev/digitization_visuals/)
- Digitization guide: [`docs/dev/eotwash_digitization_guide.md`](dev/eotwash_digitization_guide.md)

---

**These guardrails ensure results are credible, reproducible, and interpretable within experimental data coverage.**
