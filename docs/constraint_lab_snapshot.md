# Constraint Lab Snapshot

**Date:** 2026-01-01  
**Repository:** MQGT-SCF

---

## Purpose

This document provides a one-page overview of the constraint evaluation instruments in the MQGT-SCF repository. It summarizes instrument status, current dominance results, and links to detailed canonical summaries.

---

## QRNG Instrument Status

**Status:** ✅ Calibrated, regression-locked, contracted, multi-source, fixed-point comparator

- **Calibration:** Validated on synthetic controls (fair and biased datasets)
- **Data Contract:** Strict schema validation with provenance tracking
- **Multi-Source:** Conservative and weighted pooling modes implemented
- **Fixed-Point Comparison:** Identical-point dominance comparison available
- **Regression Tests:** Locked via `tests/test_qrng_controls_regression.py` and `tests/test_qrng_ingest_contract.py`

**Current Bound:** ε_max = 0.010887 (conservative pooled, N=54,434 bits from NIST Beacon v2)  
**Note:** Sample size below 200k target; bound expected to tighten with full 400-pulse cache.

**Canonical Summary:** [`docs/qrng_multisource_summary.md`](docs/qrng_multisource_summary.md)  
**Validation Certificate:** [`docs/qrng_pipeline_validation.md`](docs/qrng_pipeline_validation.md)

---

## Fifth-Force Instrument Status

**Status:** ✅ Contracted, provenanced, envelope analysis, mapping sensitivity

- **Data Contract:** Schema validation for constraint curves (lambda_m, alpha_max, source_id)
- **Provenance:** Full manifest tracking for ingested curves
- **Envelope Analysis:** Multi-curve tightest-bound computation
- **Mapping Sensitivity:** Robustness checks across order-of-magnitude uncertainty (s_ff ∈ {0.1, 1.0, 10.0})
- **Regression Tests:** Locked via `tests/test_fifth_force_*`

**Current Dominance:** 1.2% (envelope mode), < 3% even at ×10 mapping scaling  
**Boundary Regime:** λ ~ 10⁻³ to 10⁻² m (millimeter to centimeter scales)

**Canonical Summary:** [`docs/fifth_force_summary.md`](docs/fifth_force_summary.md)

---

## Current Dominance Headline

**Note:** Dominance percentages depend on epsilon_max source (baseline vs pooled) and point set sampling.

### With Pooled Multi-Source QRNG Bound

| Constraint | Dominance % | Notes |
|------------|-------------|-------|
| QRNG_tilt | ~80% | Primary bottleneck |
| ATLAS_mu | ~12% | Secondary |
| Higgs_inv | ~5% | Secondary |
| Fifth_force | ~1% | Edge trimmer (subdominant) |

**Interpretation:** QRNG_tilt remains the primary constraint. Fifth_force acts as a boundary layer trimming edges without fundamentally reshaping the viable parameter islands.

---

## Quick Links

### QRNG Instrumentation
- [`docs/qrng_multisource_summary.md`](docs/qrng_multisource_summary.md) - Multi-source calibration results
- [`docs/qrng_pipeline_validation.md`](docs/qrng_pipeline_validation.md) - Validation certificate
- [`docs/qrng_multisource_start_here.md`](docs/qrng_multisource_start_here.md) - Quick start guide
- [`docs/qrng_data_contract.md`](docs/qrng_data_contract.md) - Data contract specification

### Fifth-Force Instrumentation
- [`docs/fifth_force_summary.md`](docs/fifth_force_summary.md) - Constraint analysis results
- [`docs/fifth_force_start_here.md`](docs/fifth_force_start_here.md) - Quick start guide
- [`docs/fifth_force_data_contract.md`](docs/fifth_force_data_contract.md) - Data contract specification
- [`docs/dev/fifth_force_mapping_audit.md`](docs/dev/fifth_force_mapping_audit.md) - Mapping physics justification

---

## Validation Commands

To ensure CI remains green:

```bash
make qrng-validate      # Run QRNG regression tests
make fifth-validate     # Run fifth-force regression tests
```

---

## Reproducibility

All constraint instruments are:
- **Provenanced:** Full data lineage tracking
- **Regression-Locked:** Tests prevent breaking changes
- **Contract-Validated:** Strict schema enforcement
- **One-Command:** Makefile targets for full pipelines

See individual canonical summaries for detailed reproduction instructions.

