# Fifth-Force Mapping Audit (α_pred, λ)

## Purpose

Document and audit the mapping from MQGT-SCF model parameters to the fifth-force
Yukawa parameters (α_pred, λ), and quantify sensitivity of fifth-force dominance
to mapping uncertainty.

## Current mapping (as implemented)

### Range
λ = ħc / m_φ

- Uses CODATA 2018 value: ħc = 1.973269804e-16 GeV·m
- Implemented in: `code/inference/fifth_force/yukawa.py::mass_eV_to_lambda_m()`

### Strength
α_pred = f(alpha_eff)

Currently implemented as: **α_pred = alpha_eff²** (temporary)

This is a placeholder mapping that requires physics justification.

## What is alpha_eff?

- **Defined in:** `experiments/constraints/scripts/derive_alpha_from_portal.py::derive_alpha_normalized()`
- **Units/interpretation:**
  - alpha_eff is computed from Higgs portal parameters using Brax & Burrage (2021) normalization
  - Formula: α = 2 (sin θ * m_Pl / v)² with screening and scale-breaking corrections
  - alpha_eff is dimensionless (relative to gravity)

## Why squared?

The current α_pred = alpha_eff² mapping is **temporary** and needs refinement.

**Rationale for temporary choice:**
- Ensures α_pred is always positive
- Provides a scaling that preserves order-of-magnitude relationships
- Needs explicit derivation from Yukawa potential conventions

**Alternative mappings to consider:**
- Linear: α_pred = alpha_eff (if alpha_eff is already in correct units)
- Scale factor: α_pred = k * alpha_eff (with physics-derived k)
- Different power: α_pred = alpha_eff^p (with p justified from coupling structure)

## Sensitivity knob

Define:
  α_pred' = s_ff * α_pred

We scan s_ff ∈ {0.1, 1, 10} to check whether Fifth_force dominance remains minor.

**Results:** Fifth_force stays < 3% even at s_ff=10, indicating robustness.

## Expected outcomes

- If Fifth_force stays < ~5% even at s_ff=10: robust conclusion (✓ achieved)
- If Fifth_force rises sharply: mapping is the dominant uncertainty to resolve (not observed)

## TODO (physics refinement)

- Derive α_pred from the Higgs portal coupling more explicitly
  - Reference: Brax & Burrage (2021) "Screening the Higgs portal"
  - Reference: Burrage et al. (2018) "Fifth forces, Higgs portals and broken scale invariance"
- Ensure normalization matches convention used by ingested constraints
- Verify dimensional consistency with standard Yukawa potential: V(r) = -G m₁ m₂ / r (1 + α e^{-r/λ})
- Document any scale factors or conversion constants explicitly

