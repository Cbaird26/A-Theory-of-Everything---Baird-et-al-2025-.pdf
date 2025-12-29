# Derived Alpha Analysis: Tying α to Fundamental Parameters

## Summary

This analysis implements derived-α mapping (tying Yukawa strength α to Higgs portal mixing parameters) and active constraint labeling to identify which constraint is actually limiting each viable point. This prevents α from being a free "dial to zero" parameter and reveals whether the island is collider-limited, fifth-force-limited, or QRNG-limited.

## Methodology

### Derived-α Mapping

Instead of scanning (λ, α) directly, we now scan fundamental parameters:
- **m_φ**: Scalar mass (GeV) → determines λ = ħ/(m_φ c)
- **θ**: Mixing angle with Higgs → determines α = θ² (simple model)

This prevents the "dial α to zero" escape because α is now tied to θ, which is constrained by collider measurements.

### Active Constraint Labeling

For each viable point, we compute slack (distance to violation) for each constraint:
1. **ATLAS μ**: Signal strength deviation (μ = 1.023 ± 0.056)
2. **Higgs invisible width**: BR(H→inv) < 0.145 @ 95% CL
3. **Fifth-force envelope**: α < α_max_allowed
4. **QRNG tilt**: |ε| < 0.0008

Each point is labeled with the constraint that has the smallest slack (is tightest).

## Results

### Island Coordinates (Derived α)

| Parameter | p05 | p50 | p95 |
|-----------|-----|-----|-----|
| λ (m) | [TBD] | [TBD] | [TBD] |
| α | [TBD] | [TBD] | [TBD] |
| m_φ (GeV) | [TBD] | [TBD] | [TBD] |
| θ | [TBD] | [TBD] | [TBD] |

### Constraint Dominance

| Constraint | Percentage | Interpretation |
|------------|------------|----------------|
| ATLAS μ | [TBD]% | Collider-limited |
| Higgs inv | [TBD]% | Collider-limited |
| Fifth-force | [TBD]% | Gravity-limited |
| QRNG tilt | [TBD]% | Tilt-limited |

## Interpretation

### If Island Shrinks

- Derived α prevents "dial to zero" escape
- Joint constraints from multiple channels cut space
- Island becomes more compact and credible
- Shows theory is actually constrained

### If Island Doesn't Shrink Much

- Active constraint map reveals why
- If 90% collider-limited: need better portal mapping or tighter collider bounds
- If 90% fifth-force-limited: need tighter gravity constraints (but we've already added many)
- If 90% QRNG-limited: need better tilt parameter mapping

### Active Constraint Insights

- Reveals which measurements would actually bite
- Guides future experimental priorities
- Shows where theory needs refinement
- Prevents infinite "add more curves" without progress

## Comparison: Free α vs Derived α

### Free α (Previous Analysis)
- Island at tiny α (~10^-9 to 10^-6)
- Can always "turn down" α to survive
- Fifth-force constraints don't bite (α too small)
- Island percentiles stable despite adding constraints

### Derived α (This Analysis)
- α tied to θ (mixing angle)
- Can't dial α independently
- Collider constraints on θ → constraints on α
- Joint constraints from multiple channels
- Island should shrink or reveal what's limiting

## Technical Details

### Model: Simple Higgs Portal

- **α = θ²**: Universal mass-proportional coupling
- **λ = ħ/(m_φ c)**: Range from scalar mass
- **Constraints**: ATLAS μ, Higgs inv, fifth-force, QRNG tilt

### Future Extensions

- **Scale breaking**: α = θ² (μ/m_h)²
- **Portal coupling**: α = θ² g_Hφ²
- **More complete models**: Include mass ratios, phase space factors

## Files Generated

- `overlap_pass3_derived_alpha.json` - Island summary with derived α
- `active_constraint_heatmap_derived.png` - Constraint map in (m_φ, θ) space
- `constraint_dominance_histogram.png` - Constraint dominance histogram
- `DERIVED_ALPHA_ANALYSIS.md` - This document

## Next Steps

1. **Review constraint dominance**: Identify which constraint is limiting
2. **Refine portal mapping**: If collider-limited, improve α(θ) relationship
3. **Extend models**: Add scale breaking, portal couplings
4. **Compare with free α**: Quantify shrinkage from derived α
5. **Document implications**: Update paper with derived-α results

## Conclusion

Derived-α mapping and active constraint labeling provide the "killer insight" that reveals what's actually limiting the island. This prevents infinite "add more curves" without progress and ties the theory to constraints in a physically meaningful way. The island either shrinks significantly (showing it's constrained) or reveals exactly which constraint dominates (guiding next steps).

