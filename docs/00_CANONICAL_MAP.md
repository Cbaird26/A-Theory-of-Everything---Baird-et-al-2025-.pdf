# Canonical Map of the MQGT-SCF / Zora Research Corpus

This document defines the authoritative structure, purpose, and relationships
between all major components of the repository.

Nothing in this repository is "miscellaneous."
Every artifact exists for a reason.

## Speculative and Downstream Extensions

The following components represent speculative, downstream, or exploratory
extensions of the core MQGT-SCF framework.

These elements are logically dependent on the core theory but are not required
for its validity, internal consistency, or primary experimental predictions.

Examples include:
- Artificial intelligence architectures informed by the framework
- Ethical weighting fields (E) applied to agentic systems
- Superluminal or extended group-velocity constructs (e.g. Warp-10 series)
- Conceptual integrations with consciousness or cognition models

All such extensions are explicitly labeled where they appear and should be
understood as exploratory research directions rather than settled components
of the core theory.

---

## QRNG Pipeline (Validated & Contracted)

The QRNG bias-detection pipeline is a calibrated, regression-locked, schema-validated instrument:

- **Start here:** `docs/qrng_start_here.md` — Quick start guide
- **Calibration certificate:** `docs/qrng_pipeline_validation.md` — Empirical validation on synthetic controls
- **Data contract:** `docs/qrng_data_contract.md` — Input schema + provenance requirements
- **Discussion notes:** `docs/notes/qrng_pipeline_validation_discussion.md` — Interpretive discussion (non-canonical)
- **Engineering plan:** `docs/dev/qrng_regression_lock_plan.md` — Regression lock + data contract implementation

**Key components:**
- `code/inference/qrng_ingest.py` — Validator + provenance generator
- `experiments/constraints/scripts/calibrate_qrng_physics.py` — BF10/CI computation + calibration
- `tests/test_qrng_controls_regression.py` — Regression tests (locks calibration)
- `tests/test_qrng_ingest_contract.py` — Contract enforcement tests

**Status:** Publication-ready (calibrated, locked, contracted, provenanced)

