# Release Notes v0.3.0
## Calibration + Phase Diagrams + Forensic Reproducibility

**Release Date:** 2025-01-XX  
**Tag:** `v0.3.0`  
**Milestone:** Review-proofing complete

---

## What Shipped

### QRNG Calibration System
- Multi-source QRNG calibration with bootstrap confidence intervals
- Pooled meta-analysis (inverse variance weighting)
- Environment metadata (Python/NumPy/Pandas versions, seed) in JSON
- RNG seed control (seed=42 by default) for reproducibility
- **Output:** `experiments/constraints/results/QRNG_CALIBRATION.json`

### μ_sb Phase Diagram
- High-resolution phase diagram (25 points) showing constraint dominance transitions
- Sensitivity analysis with pooled ε_max vs upper CI bound
- Dominance diagnostic blocks with normalized slack values
- **Output:** `experiments/constraints/results/MU_PHASE_DIAGRAM.json`

### Stochastic Invariance Test Suite
- Same seed → identical results (byte-for-byte reproducibility)
- Different seeds → stable ε_max (CV < 1%), CI bounds may vary
- Dominance ordering persistence check
- Explicit per-seed logging for reviewer inspection
- **Script:** `experiments/constraints/scripts/test_stochastic_invariance.py`

### Paper Outlines
- **Paper 1:** Core Theory (Lagrangian, field structure, minimal claims)
- **Paper 2:** Constraint Engine (normalized slack, phase diagrams, reproducibility)
- **Paper 3:** QRNG Protocol (pre-registration-friendly experimental design)

### Pre-registration Protocol
- Primary endpoint, hypothesis, analysis pipeline
- Sensitivity framing (pooled vs upper CI bounds)
- Stopping rule and null result publication plan
- **File:** `prereg/PREREG_QRNG_TILT.md`

### Reproducibility Infrastructure
- Exact CLI commands with script hashes (SHA-256)
- Expected output hashes for verification
- Known non-determinism documentation
- Data dependencies listed
- **Location:** `papers/outline/PAPER_2_CONSTRAINT_ENGINE_OUTLINE.md` Appendix D

---

## What Changed

### Core Improvements
- **Normalized slack comparison:** Fixed bias in constraint dominance (was 100% fifth-force, now 86.7% QRNG_tilt)
- **Derived α mapping:** Upgraded from toy `α = θ²` to Brax-Burrage normalized form `α = 2 (sin θ * m_Pl / v)²`
- **Scale-breaking suppression:** Added `μ_sb` parameter with `(μ_sb/m_h)⁴` suppression factor
- **Differential screening:** `Θ_lab` applied only to fifth-force constraints (collider constraints unscreened)

### Reviewer-Proofing
- Edge-band causal explanation (why suppression increases fifth-force relevance)
- Upper-CI scenario clarification (calibration uncertainty vs model parameter change)
- Known non-determinism documentation (where randomness lives, what's invariant)
- Reproducibility checklist with exact commands and hashes

### Safety Measures
- `private_data/` directory for health/biometric data
- `.gitignore` rules for magnetometer/biometric/health CSVs
- Pre-commit hook protection (working correctly)

---

## What to Run

### Reproduce Calibration
```bash
python experiments/constraints/scripts/calibrate_qrng_multisource.py \
  --seed 42 \
  --output experiments/constraints/results/QRNG_CALIBRATION.json
```

### Generate Phase Diagram
```bash
python experiments/constraints/scripts/sweep_mu_phase_diagram.py \
  --lambda-regime micron-to-meter \
  --n-mu-points 25 \
  --mu-sb-min 1e-4 \
  --mu-sb-max 1.0 \
  --output experiments/constraints/results/MU_PHASE_DIAGRAM.json
```

### Run Stochastic Invariance Tests
```bash
pytest experiments/constraints/scripts/test_stochastic_invariance.py -v
# or
python experiments/constraints/scripts/test_stochastic_invariance.py
```

See `papers/outline/PAPER_2_CONSTRAINT_ENGINE_OUTLINE.md` Appendix D for full reproducibility instructions.

---

## What NOT to Commit

The following files are correctly blocked by pre-commit hooks and should remain local-only:

- `PRIVATE_VAULT_SAFETY_RULES.md` - Private vault content
- `VAULT_POLICY.md` - Private vault content
- `experiments/constraints/results/envelope_vs_geraci_diagnostic.*` - False positive (researcher name)
- `experiments/grok_qrng/results/*/summary.csv` - Not in allowlisted path (if you want these in-repo, we can tweak the hook)

**Health/biometric data:**
- Raw magnetometer/heart/coherence data → `private_data/`
- Use derived artifacts (plots, summary stats) in repo instead

---

## Key Findings

### Constraint Dominance (Baseline, μ_sb/m_h = 1.0)
- **QRNG_tilt:** 86.7% (primary bottleneck)
- **ATLAS_mu:** 13.3% (secondary)
- **Fifth_force:** 0% (inactive - not the limiting wall)
- **Higgs_inv:** 0% (inactive)

### Phase Diagram Transitions
- **μ_sb/m_h ≈ 10⁻³:** Higgs_inv activates (18% at onset), Fifth_force re-enters as edge-band (2%)
- **μ_sb/m_h = 10⁻⁴:** Higgs_inv dominant (68%), QRNG_tilt secondary (30%), Fifth_force edge-band (2%)

### Calibration Results
- **Pooled ε_max:** 0.000742 (point estimate)
- **95% CI:** [0.000000, 0.001904] (lower bound is bootstrap edge case, not physical zero)
- **Sensitivity:** Upper CI (0.001904) flips baseline dominance to Fifth_force (83.3%)

---

## Files Changed

- **92 files changed, 7,484 insertions**
- See commit `98bc1d2` for full diff

---

## Next Steps

1. **Review:** Paper outlines ready for expansion into full drafts
2. **Pre-registration:** Protocol ready for registration (e.g., OSF, AsPredicted)
3. **Experiments:** QRNG protocol ready for implementation
4. **Optional:** Tweak pre-commit allowlist for summary.csv files if desired

---

## Questions?

See:
- `papers/outline/PAPER_2_CONSTRAINT_ENGINE_OUTLINE.md` for methodology
- `experiments/constraints/results/HIGH_RES_PHASE_DIAGRAM_SUMMARY.md` for phase diagram interpretation
- `prereg/PREREG_QRNG_TILT.md` for experimental protocol

