# Fifth-Force Constraint Analysis Summary

**Date:** 2026-01-01  
**Repository:** MQGT-SCF  
**Commit:** `bb7189a`  
**Python:** `Python 3.14.1`  
**OS:** `Darwin 24.6.0`

---

## Purpose

This document summarizes fifth-force constraint analysis results for the MQGT-SCF parameter space scans. It reports dominance percentages, boundary regimes, and sensitivity to mapping uncertainty.

---

## Curve Sources

The analysis uses constraint curves from the following sources:

1. **zenodo5080965_fig3** (real data)
   - Source: Heacock & Huber, DOI: 10.5281/zenodo.5080965
   - Range: λ ~ 10⁻⁴ to 10⁻² m
   - Status: Real experimental constraint data

2. **placeholder_eotwash_style** (synthetic regression)
   - Source: Synthetic monotonic curve for regression testing
   - Range: λ ~ 10⁻⁶ to 10⁻³ m
   - Status: Placeholder for pipeline validation

---

## Single-Curve Dominance (zenodo5080965_fig3)

Constraint dominance percentages when using the real Zenodo curve:

| Constraint | Dominance % |
|------------|-------------|
| QRNG_tilt  | 82.4%       |
| ATLAS_mu   | 12.1%       |
| Higgs_inv  | 4.8%        |
| Fifth_force| 0.7%        |

**Conclusion:** Fifth_force is a minor constraint (0.7% dominance) when evaluated against the Zenodo curve. QRNG_tilt remains the primary bottleneck.

---

## Envelope Dominance (Tightest Bound Across Curves)

Constraint dominance when using the envelope (minimum alpha_max at each λ):

| Constraint | Dominance % |
|------------|-------------|
| QRNG_tilt  | 81.3%       |
| ATLAS_mu   | 11.8%       |
| Higgs_inv  | 4.5%        |
| Fifth_force| 1.2%        |

**Conclusion:** Even under the tightest available bounds (envelope), Fifth_force remains subdominant (1.2%). The open zone persists.

---

## Mapping Sensitivity

Dominance percentages across order-of-magnitude mapping uncertainty (s_ff scaling factor):

| s_ff | Fifth_force % | QRNG_tilt % | ATLAS_mu % | Higgs_inv % | Notes |
|------|---------------|-------------|------------|-------------|-------|
| 0.1  | 0.2%          | 83.1%       | 12.3%      | 4.4%        | Fifth_force negligible; QRNG dominant |
| 1.0  | 1.2%          | 81.3%       | 11.8%      | 4.5%        | Baseline: minor edge trim |
| 10.0 | 2.8%          | 79.2%       | 11.5%      | 4.2%        | Fifth_force rises but stays subdominant; no collapse |

**Conclusion:** Fifth_force remains subdominant (< 3%) even when the mapping is scaled by ×10. The conclusion is robust across an order-of-magnitude mapping uncertainty.

---

## Boundary Regime

Fifth_force constraints primarily affect parameter space at:

- **Range:** λ ~ 10⁻³ to 10⁻² m (millimeter to centimeter scales)
- **Regime:** Strong μ_sb suppression (μ_sb/m_h ~ 0.001–0.01)
- **Effect:** Edge trimming rather than bulk exclusion

The most constrained points show α_pred exceeding α_max by factors of ~1.2–2.4, concentrated in narrow bands rather than collapsing the viable islands.

---

## Interpretation

**Fifth_force is an edge constraint, not a bottleneck, under the current constraint set.**

- Single-curve analysis: 0.7% dominance
- Envelope analysis: 1.2% dominance  
- Mapping sensitivity: < 3% even at ×10 scaling

The viable parameter islands persist, with QRNG_tilt remaining the primary limiter (~80%+). Fifth_force acts as a boundary layer that trims edges without fundamentally reshaping the constraint landscape.

---

## Detectability Analysis

A complementary analysis quantifies where the scalar would be **detectable** if it exists by computing `r = alpha_pred / alpha_max_envelope(lambda_m)` for sampled model points.

**Key findings:**
- **Hunt band:** Narrow regime around λ ≈ 0.3–1.3 mm where r ≈ 0.1–1 (scalar approaches but does not exceed bounds)
- **Exclusions:** 1.6% of points excluded (r > 1), primarily at longer ranges (λ ~ 5–9 mm)
- **Safe regions:** 94.0% of points far from detection (r < 0.001)

The structured clustering of high-r points in the mm-cm regime suggests this is a model feature, not sampling noise. This identifies a **target regime for experimental probes**.

**See:** `docs/fifth_force_detectability_summary.md` for full detectability analysis.

---

## References

- Mapping audit and physics justification: `docs/dev/fifth_force_mapping_audit.md`
- Data contract specification: `docs/fifth_force_data_contract.md`
- Quick start guide: `docs/fifth_force_start_here.md`
- Detectability analysis: `docs/fifth_force_detectability_summary.md`

