# Calibrated μ Phase Diagram Summary

## Date
2025-12-29

## Overview
Phase diagram results with calibrated QRNG bounds (multi-source calibration, ε_max = 0.000742 pooled point estimate, 95% CI: [0.000000, 0.001888]).

## Key Findings

### Pooled Point Estimate (ε_max = 0.000742)

**Dominance Diagnostic Blocks:**

| μ_sb/m_h | log₁₀(μ_sb/m_h) | Viable Points | QRNG_tilt (%) | ATLAS_mu (%) | Higgs_inv (%) | Fifth_force (%) |
|----------|-----------------|---------------|---------------|--------------|----------------|-----------------|
| 1.0e+00 | 0.00 | 240 | **83.3** | 16.7 | 0.0 | 0.0 |
| 1.0e-01 | -1.00 | 400 | **100.0** | 0.0 | 0.0 | 0.0 |
| 1.0e-02 | -2.00 | 400 | **100.0** | 0.0 | 0.0 | 0.0 |
| 1.0e-03 | -3.00 | 400 | **80.0** | 0.0 | **20.0** | 0.0 |
| 1.0e-04 | -4.00 | 400 | **30.0** | 0.0 | **65.0** | **5.0** |

**Key Transitions:**
- **Baseline (μ_sb/m_h = 1.0):** QRNG_tilt 83.3% (dominant), ATLAS_mu 16.7% (secondary)
- **Moderate suppression (μ_sb/m_h = 0.1-0.01):** QRNG_tilt 100% (complete dominance)
- **Strong suppression (μ_sb/m_h = 0.001):** QRNG_tilt 80%, Higgs_inv 20% (first activation)
- **Very strong suppression (μ_sb/m_h = 0.0001):** Higgs_inv 65% (becomes dominant), QRNG_tilt 30%, Fifth_force 5%

### Upper CI Sensitivity (ε_max = 0.001888)

**Dominance Diagnostic Blocks:**

| μ_sb/m_h | log₁₀(μ_sb/m_h) | Viable Points | QRNG_tilt (%) | ATLAS_mu (%) | Higgs_inv (%) | Fifth_force (%) |
|----------|-----------------|---------------|---------------|--------------|----------------|-----------------|
| 1.0e+00 | 0.00 | 240 | **0.0** | 16.7 | 0.0 | **83.3** |
| 1.0e-01 | -1.00 | 400 | **0.0** | 0.0 | 0.0 | **100.0** |
| 1.0e-02 | -2.00 | 400 | **0.0** | 0.0 | 0.0 | **100.0** |
| 1.0e-03 | -3.00 | 400 | **0.0** | 0.0 | **25.0** | **75.0** |
| 1.0e-04 | -4.00 | 400 | **0.0** | 0.0 | **70.0** | **30.0** |

**Key Transitions:**
- **Baseline (μ_sb/m_h = 1.0):** Fifth_force 83.3% (dominant), ATLAS_mu 16.7% (secondary), **QRNG_tilt 0% (completely relieved)**
- **Moderate suppression (μ_sb/m_h = 0.1-0.01):** Fifth_force 100% (complete dominance)
- **Strong suppression (μ_sb/m_h = 0.001):** Fifth_force 75%, Higgs_inv 25%
- **Very strong suppression (μ_sb/m_h = 0.0001):** Higgs_inv 70%, Fifth_force 30%

## Interpretation

### What the Phase Diagram Says

1. **Calibrated bound (ε_max = 0.000742) reveals QRNG_tilt as primary bottleneck:**
   - At baseline (μ_sb/m_h = 1.0), QRNG_tilt dominates (83.3%)
   - This is ~3× tighter than previous single-source bound (0.002292)
   - The tighter bound makes QRNG_tilt bite significantly harder

2. **Sensitivity check (ε_max = 0.001888) shows critical dependence:**
   - With looser bound, Fifth_force takes over at baseline (83.3%)
   - QRNG_tilt is completely relieved (0%)
   - Demonstrates the critical importance of accurate QRNG calibration

3. **Scale-breaking suppression (μ_sb) provides trade-offs, not escape:**
   - Strong suppression (μ_sb/m_h < 0.001) relieves QRNG_tilt
   - But activates Higgs_inv and Fifth_force
   - No "free lunch": constraints move, they don't vanish

4. **Transition points:**
   - **QRNG_tilt → Higgs_inv:** μ_sb/m_h ≈ 0.001 (with calibrated bound)
   - **Fifth_force activation:** μ_sb/m_h ≈ 0.0001 (with calibrated bound)
   - **Fifth_force dominance:** μ_sb/m_h = 1.0 (with upper CI bound)

## Paper-Ready Summary

**Results Paragraph (for Paper 2):**

We map the MQGT-SCF Higgs-portal parameter space under scale-breaking suppression μ_sb via a dominance phase diagram over log₁₀(μ_sb/m_h), using calibrated QRNG bounds from multi-source analysis (ε_max = 0.000742, 95% CI: [0.000000, 0.001904]). With normalized slack comparison to avoid scale artifacts, we find that the baseline viable region is primarily limited by QRNG_tilt (83.3% of viable points), with a secondary collider limitation from ATLAS_mu (16.7%). As μ_sb decreases, QRNG_tilt pressure relaxes and the constraint landscape reconfigures: Higgs invisible decays become active at μ_sb/m_h ≲ 0.001 (20% at 0.001, 65% at 0.0001), and fifth-force bounds re-enter at μ_sb/m_h ≲ 0.0001 (5%), indicating a trade-off surface rather than a single-constraint escape. A sensitivity check with the upper CI bound (ε_max = 0.001888) shows Fifth_force dominance at baseline (83.3%), demonstrating the critical sensitivity to QRNG calibration accuracy. This establishes a structured, testable constraint simplex where empirical leverage can be shifted between QRNG and collider channels by physically motivated suppression mechanisms.

**Figure Caption:**

Figure 1: Dominant constraint versus log₁₀(μ_sb/m_h) under normalized slack with calibrated QRNG bounds (ε_max = 0.000742, pooled point estimate). Colors indicate the active bottleneck across viable parameter points. The regime transition from QRNG_tilt-dominated to collider-/fifth-force-limited behavior occurs near μ_sb/m_h ≈ 0.001, with Higgs_inv activating below μ_sb/m_h ≈ 0.001 and Fifth_force re-entering below μ_sb/m_h ≈ 0.0001. A sensitivity check with the upper CI bound (ε_max = 0.001888) shows Fifth_force dominance at baseline, demonstrating the critical importance of accurate QRNG calibration.

## Files Generated

- `mu_phase_diagram_calibrated_eps_pooled/` - Pooled point estimate (ε_max = 0.000742)
- `mu_phase_diagram_calibrated_eps_upperCI/` - Upper CI sensitivity (ε_max = 0.001888)

Each directory contains:
- `MU_PHASE_DIAGRAM.json` - Raw data
- `MU_PHASE_DIAGRAM.png` - Plot
- `MU_PHASE_DIAGRAM.md` - Interpretation

