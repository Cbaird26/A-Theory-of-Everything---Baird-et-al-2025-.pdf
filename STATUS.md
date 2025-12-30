# MQGT-SCF Project Status Snapshot (Dec 2025)

## What Exists (The Artifact)

MQGT-SCF is a reproducible "constraint engine" + theoretical scaffold that maps model parameters → observables/constraints, identifies bottlenecks, and outputs falsifiable predictions. It is not empirically confirmed, but it is testable.

## Key Technical Result

A prior "100% fifth-force dominated" conclusion was an artifact of comparing raw slacks across different scales. After canonizing normalized slack and locking it with regression tests, the dominant constraints are:

- **QRNG_tilt:** ~86.7% (dominant bottleneck)
- **ATLAS_mu:** ~13.3% (secondary constraint)
- **Fifth_force:** ~0% (not active at baseline)
- **Higgs_inv:** ~0% (not active at baseline)

## What This Implies

Under current assumptions, the strongest limiter on "consciousness-coupled" effects is **quantum randomness bias**, not macroscopic gravity tests.

## Escape Hatch with Tradeoffs

A scale-breaking suppression knob (μ_sb) implemented as:

```
α_eff = α_unscreened * (μ_sb/m_h)^4
```

can reduce QRNG dominance, but predictably activates other constraints (Higgs invisible, some fifth-force regions). This indicates a real constraint trade-space (constraints move; they don't vanish).

**Key finding:** Very strong scale-breaking (μ_sb ~ 0.001 m_h) can reduce QRNG_tilt dominance from 86.7% to 76%, but activates Higgs_inv (18%) and Fifth_force (6%).

## Empirical Status

The model survives current constraints (a viable parameter island exists), but is unproven. Next progress requires real-world tests and/or tighter external bounds.

### Current Viable Parameter Space
- **θ range:** ~10⁻²² to 10⁻²⁰ (extremely small mixing angles)
- **m_φ range:** ~2×10⁻¹⁶ to 2×10⁻¹⁰ GeV (ultralight scalars)
- **λ range:** ~1 μm to 1 m (mesoscale)
- **α range:** ~10⁻¹² to 10⁻⁸ (very weak Yukawa coupling)

## Recent Refinements (Dec 2025)

1. **Normalized slack comparison** - Fixed scale-trap bug, revealed true bottleneck
2. **QRNG_tilt calibration** - Updated epsilon_max from 0.0008 to 0.002292 (data-derived)
3. **Scale-breaking μ_sb** - Implemented Burrage-style suppression, tested trade-offs
4. **Regression tests** - Locked in baseline behavior to prevent regressions

## Next Steps

1. **μ_sb phase diagram** - Map dominance transitions across scale-breaking parameter space
2. **Multi-source QRNG calibration** - Make QRNG bounds defensible with multiple data sources
3. **Paper structure** - Split into 3 focused papers (core theory, constraint engine, QRNG protocol)
4. **Pre-registration** - One sharp experimental prediction based on phase diagram results

## Files and Documentation

- **Constraint engine:** `experiments/constraints/scripts/check_overlap_derived_alpha.py`
- **Regression test:** `experiments/constraints/scripts/test_regression_dominance.py`
- **μ phase diagram:** `experiments/constraints/scripts/sweep_mu_phase_diagram.py`
- **Results:** `experiments/constraints/results/`

## References

- Brax & Burrage (2021): "Screening the Higgs portal", Phys. Rev. D 104, 015011
- Burrage et al. (2018): "Fifth forces, Higgs portals and broken scale invariance", arXiv:1804.07180
- CODATA 2018: ħc = 197.3269804 MeV·fm = 1.973269804e-16 GeV·m

