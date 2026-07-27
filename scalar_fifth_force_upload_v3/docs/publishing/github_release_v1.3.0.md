# GitHub Release v1.3.0

**Release Title:**
```
v1.3.0 — Constraint Lab: QRNG Multisource + Scalar Fifth-Force Detectability
```

---

## Release Description

This release publishes a fully reproducible constraint-lab framework integrating multisource QRNG calibration (including NIST Beacon data) and a fifth-force detectability instrument for the Merged Quantum Gauge Theory and Scalar Consciousness Framework (MQGT-SCF).

### What's Included

**QRNG Multisource Instrument:**
- Multi-source QRNG calibration pipeline
- Real cached NIST Beacon v2 stream (≈200k bits)
- Conservative and weighted pooling modes
- Fixed-point dominance comparison (baseline vs pooled)
- Full provenance tracking

**Fifth-Force Detectability Instrument:**
- Yukawa mapping pipeline (model → α_pred, λ)
- Constraint registry + envelope logic
- Detectability map computation (r = α_pred / α_max)
- Sensitivity scans (mapping uncertainty s_ff ∈ {0.1, 1, 10})
- Real experimental constraint support (Zenodo 5080965)

**Documentation Suite:**
- Canonical summaries (reviewer-safe, empirical)
- Detailed narrative memos (interpretation, citations)
- Raw results (tables, statistics, provenance)
- Complete file index

### Key Results

**QRNG Multisource:**
- NIST stream consistent with fair randomness (ε ≈ 0)
- Conservative pooling loosens ε_max by design
- QRNG_tilt dominance shifts only a few percent with pooling
- Islands persist → no collapse, no artifact

**Fifth-Force Detectability:**
- Identifies sub-mm to mm regime (λ ≈ 0.5 mm) where scalar would approach detectability
- Fifth_force stays <3% dominant even at s_ff=10 (mapping uncertainty)
- No island collapse under sensitivity scans
- Structured hunt band, not random noise

### Important Notes

- **No detection is claimed.** This is a constraint-analysis framework.
- The framework identifies where a scalar of this class would appear first if it exists.
- All results are reproducible with fixed seeds (SEED=42).
- The pipeline is explicitly falsifiable: ingestion of real Eöt-Wash mm–cm bounds will either collapse or preserve the identified regime.

### Reproducibility

All results can be reproduced with:

```bash
# QRNG multisource
make qrng-multisource-validate
make qrng-multisource-report

# Fifth-force detectability
make fifth-detectability SEED=42 NPTS=2000

# Full constraint lab
make fifth-report
```

### Package Contents

The attached `scalar_fifth_force_upload_v3.zip` contains:
- 49 files (docs, code, data, results, tests)
- Complete constraint-lab infrastructure
- All documentation and provenance
- Automation scripts

### Next Steps

The framework is ready for real experimental bounds. To complete the analysis:
1. Digitize Eöt-Wash mm–cm constraint curve
2. Ingest via `make fifth-ingest INPUT=...`
3. Rerun detectability to determine if hunt band persists or collapses

See `docs/dev/eotwash_digitization_guide.md` for digitization instructions.

---

## Files Changed

- Added QRNG multisource calibration instrument
- Added fifth-force detectability instrument
- Added constraint lab snapshot documentation
- Added canonical summaries and detailed memos
- Added real curve ingestion pipeline
- Added automation scripts and validation tools

## Documentation

- **Constraint Lab Overview:** `docs/constraint_lab_snapshot.md`
- **QRNG Multisource Summary:** `docs/qrng_multisource_summary.md`
- **Fifth-Force Summary:** `docs/fifth_force_summary.md`
- **Detectability Summary:** `docs/fifth_force_detectability_summary.md`
- **File Index:** `docs/fifth_force_file_index.md`

## Citation

If you use this work, please cite:
- GitHub Release: [URL]
- Zenodo DOI: [DOI - to be added]

---

**This release establishes timestamped priority and auditability for the constraint-lab framework.**

