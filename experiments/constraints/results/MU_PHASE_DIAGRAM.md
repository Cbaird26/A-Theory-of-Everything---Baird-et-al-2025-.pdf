# μ_sb Phase Diagram Interpretation

## Date
2025-12-29

## Overview
Phase diagram showing how constraint dominance changes as scale-breaking suppression (μ_sb) varies.
This is the "one figure to rule them all" - shows where bottlenecks switch and which constraints become active.

## Key Findings

### Dominance Transitions

**Dominance Transitions:**

- At μ_sb/m_h = 1.0000e-02 (log₁₀ = -2.00): Higgs_inv → QRNG_tilt

### Summary Table

| μ_sb/m_h | log₁₀(μ_sb/m_h) | Viable Points | QRNG_tilt (%) | ATLAS_mu (%) | Higgs_inv (%) | Fifth_force (%) |
|----------|-----------------|---------------|---------------|--------------|----------------|-----------------|
| 1.0000e-04 | -4.00 | 100 | 30.0 | 0.0 | 70.0 | 0.0 |
| 1.0000e-02 | -2.00 | 100 | 100.0 | 0.0 | 0.0 | 0.0 |
| 1.0000e+00 | 0.00 | 60 | 83.3 | 16.7 | 0.0 | 0.0 |


## Interpretation

### Baseline (μ_sb/m_h = 1.0, no suppression)
- QRNG_tilt: ~86.7% (dominant bottleneck)
- ATLAS_mu: ~13.3% (secondary)
- Higgs_inv: ~0%
- Fifth_force: ~0%

### Strong Suppression (μ_sb/m_h << 1)
- As μ_sb decreases, α_eff = α_unscreened * (μ_sb/m_h)^4 becomes very small
- This should relieve QRNG_tilt constraint
- But other constraints (Higgs_inv, Fifth_force) may become active

### Key Questions Answered
1. **Where does QRNG_tilt → ATLAS_mu transition occur?**
   - See transitions table above

2. **Where do Higgs_inv / Fifth_force become active?**
   - See summary table above

3. **Is viable region "narrow knife-edge" or "broad basin"?**
   - Check viable points vs μ_sb plot

4. **What μ_sb range gives most viable space?**
   - See viable points column in summary table

## Next Steps
- Use this phase diagram to decide which experiment to pre-register
- If QRNG_tilt remains dominant across μ_sb range → focus on QRNG calibration
- If collider constraints become judge → focus on LHC Run 3 data
