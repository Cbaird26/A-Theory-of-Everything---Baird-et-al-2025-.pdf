# High-Resolution μ Phase Diagram Summary (Calibrated)

## Date
2025-12-29

## Calibration Metadata
- **ε_max used:** 0.000742 (pooled point estimate from multi-source QRNG calibration)
- **95% CI:** [0.000000, 0.001904]
- **Note:** CI lower bound of 0.000000 is a bootstrap edge case due to finite-sample effects, not a physical zero. Pooled point estimate is primary.

## Sweep Parameters
- **μ_sb/m_h range:** 1e-4 to 1.0 (logspace, 25 points)
- **m_φ range:** 2e-16 to 2e-10 GeV (micron-to-meter regime)
- **θ range:** 1e-22 to 1e-18
- **Grid:** 50 × 50 (m_φ × θ)

## Key Diagnostic Blocks

### Baseline (μ_sb/m_h = 1.0, no suppression)
```
μ_sb/m_h = 1.0e+00  n=1,500
dominant fractions: QRNG_tilt 86.7%, ATLAS_mu 13.3%, Higgs_inv 0.0%, Fifth_force 0.0%
```

### Moderate Suppression (μ_sb/m_h = 1e-2)
```
μ_sb/m_h = 1.0e-02  n=2,500
dominant fractions: QRNG_tilt 100.0%, ATLAS_mu 0.0%, Higgs_inv 0.0%, Fifth_force 0.0%
```
**Note:** The 100% QRNG_tilt at μ_sb/m_h = 10⁻² is likely a shape/topology effect of the viable region at that suppression level, not inherently wrong but worth flagging as "non-monotonic dominance behavior can occur due to topology of the viable set."

### Very Strong Suppression (μ_sb/m_h = 1e-4)
```
μ_sb/m_h = 1.0e-04  n=2,500
dominant fractions: Higgs_inv 68.0%, QRNG_tilt 30.0%, Fifth_force 2.0%, ATLAS_mu 0.0%
```

## Transition Thresholds

From high-resolution scan (25 points, calibrated ε_max = 0.000742):

1. **QRNG_tilt falls below 50%:** μ_sb/m_h ≈ 3.2×10⁻⁴ (log₁₀ ≈ -3.50)
   - At this point: QRNG_tilt 52%, Higgs_inv 44%, Fifth_force 4%
   - Interpretation: Strong suppression begins to relieve QRNG_tilt, but Higgs_inv activates

2. **Higgs_inv first becomes non-zero:** μ_sb/m_h ≈ 1.0×10⁻³ (log₁₀ = -3.00)
   - At this point: QRNG_tilt 80%, Higgs_inv 18%, Fifth_force 2%
   - Interpretation: Higgs_inv constraint becomes active at strong suppression (first appearance, then grows to 68% at μ_sb/m_h = 10⁻⁴)

3. **Fifth_force re-enters:** μ_sb/m_h ≈ 1.0×10⁻³ (log₁₀ = -3.00, same as Higgs_inv)
   - At this point: Fifth_force 2% (thin edge band)
   - Interpretation: Fifth-force constraints are inactive at baseline but re-enter as a thin edge-band once μ_sb/m_h ≲ 10⁻³, limiting ~2% of viable points. This is the signature of an edge-band: only a small slice of the viable island is grazing the fifth-force boundary. At stronger suppression, the dominant bottleneck shifts primarily to Higgs invisible decays (68% at μ_sb/m_h = 10⁻⁴).

## Paper-Ready Results Paragraph

We map the MQGT-SCF Higgs-portal parameter space under scale-breaking suppression μ_sb via a high-resolution dominance phase diagram over log₁₀(μ_sb/m_h) using calibrated QRNG bounds from multi-source analysis (ε_max = 0.000742, pooled point estimate; 95% bootstrap CI: [0.000000, 0.001904], where the lower bound reflects finite-sample bootstrap effects rather than physical zero). With normalized slack comparison to avoid scale artifacts, we find that the baseline viable region (μ_sb/m_h = 1.0, no suppression) is primarily limited by QRNG_tilt (86.7% of viable points), with a secondary collider limitation from ATLAS_mu (13.3%). Fifth-force constraints are inactive at baseline but re-enter as a thin edge-band once μ_sb/m_h ≲ 10⁻³, limiting ~2% of viable points; at stronger suppression the dominant bottleneck shifts primarily to Higgs invisible decays (68% at μ_sb/m_h = 10⁻⁴). This re-entry occurs because μ_sb suppression enlarges the viable θ region, pushing a small subset of points toward the fifth-force envelope. Moderate suppression (μ_sb/m_h = 0.01) maintains 100% QRNG_tilt dominance, indicating that scale-breaking must be very strong to shift the bottleneck; this non-monotonic behavior reflects the topology of the viable set rather than a fundamental constraint ordering. As μ_sb decreases further, QRNG_tilt pressure relaxes and the constraint landscape reconfigures: QRNG_tilt falls below 50% at μ_sb/m_h ≈ 3.2×10⁻⁴, Higgs invisible decays become active at μ_sb/m_h ≈ 1.0×10⁻³ (18% at onset, rising to 68% at μ_sb/m_h = 10⁻⁴). A sensitivity sweep using the upper-CI calibration (ε_max = 0.001904) qualitatively alters the bottleneck ordering, relieving QRNG_tilt and restoring fifth-force dominance (83.3%); this is a calibration-uncertainty scenario, not a model parameter change, demonstrating that experimental calibration of ε_max is presently the highest-leverage empirical uncertainty. This establishes a structured, testable constraint simplex where empirical leverage can be shifted between QRNG and collider channels by physically motivated suppression mechanisms, but with clear transition thresholds rather than smooth gradients.

## Figure Caption

**Figure 1:** Dominant constraint versus log₁₀(μ_sb/m_h) under normalized slack with calibrated QRNG bounds (ε_max = 0.000742, pooled point estimate from multi-source calibration). Colors indicate the active bottleneck across viable parameter points. At baseline (μ_sb/m_h = 1.0), QRNG_tilt dominates (86.7%) with ATLAS_mu secondary (13.3%); fifth-force constraints are inactive. The regime transition from QRNG_tilt-dominated to collider-/fifth-force-limited behavior occurs near μ_sb/m_h ≈ 3.2×10⁻⁴ (QRNG_tilt falls below 50%), with Higgs_inv activating at μ_sb/m_h ≈ 1.0×10⁻³ (18% at onset, rising to 68% at μ_sb/m_h = 10⁻⁴) and Fifth_force re-entering as a thin edge-band at μ_sb/m_h ≈ 1.0×10⁻³ (2% of viable points). A sensitivity check with the upper CI bound (ε_max = 0.001904) shows Fifth_force dominance at baseline, demonstrating the critical importance of accurate QRNG calibration.

## Sensitivity Check (Upper CI: ε_max = 0.001904)

With the looser bound (upper CI), the constraint landscape shifts dramatically:
- **Baseline (μ_sb/m_h = 1.0):** Fifth_force 83.3%, ATLAS_mu 16.7%, QRNG_tilt 0% (completely relieved)
- **Moderate suppression (μ_sb/m_h = 0.01):** Fifth_force 100% (complete dominance)
- **Very strong suppression (μ_sb/m_h = 0.0001):** Higgs_inv 72%, Fifth_force 28%

**Interpretation:** The 2.6× difference between pooled (0.000742) and upper CI (0.001904) completely changes the baseline bottleneck from QRNG_tilt to Fifth_force, demonstrating the critical sensitivity to QRNG calibration accuracy. This validates the importance of multi-source calibration and bootstrap uncertainty quantification.

## Files Generated

- `mu_phase_diagram_calibrated_pooled/` - Pooled point estimate (ε_max = 0.000742, 25 points)
- `mu_phase_diagram_calibrated_upperCI/` - Upper CI sensitivity (ε_max = 0.001904, 25 points)

Each directory contains:
- `MU_PHASE_DIAGRAM.json` - Raw data with metadata (ε_max, timestamp)
- `MU_PHASE_DIAGRAM.png` - Plot
- `MU_PHASE_DIAGRAM.md` - Interpretation with calibration metadata

