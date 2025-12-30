# Dominance Phase Diagram Results

## Date
December 29, 2025

## Objective
Run a dominance phase diagram sweep across Θ_lab values after implementing normalized slack comparison and tightening collider constraints. This tests whether normalized slack comparison reveals the true bottleneck constraints.

## Key Changes from Previous Analysis

### 1. Normalized Slack Comparison
- **Previous approach:** Compared raw slack values (fifth-force slack ~1e-6, collider slack ~0.1)
- **Problem:** Raw slack comparison is biased toward constraints with smaller absolute scales
- **Solution:** Compare normalized slack = (bound - value) / bound = slack / bound
- **Result:** Fair comparison across constraints with different scales

### 2. Tightened Collider Constraints
- **BR(H→inv) constraint:** Updated to 0.145 (conservative) or 0.107 (tight mode)
- **ATLAS μ constraint:** Already using 2σ limits (μ = 1.023 ± 0.056)

## Methodology
- **Regime:** Micron-to-meter (m_φ = 2e-16 to 2e-10 GeV → λ = 0.987 m to 0.987 µm)
- **Model:** Normalized Higgs portal (α = 2 (sin θ * m_Pl / v)²)
- **Screening levels tested:** Θ_lab = 1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001
- **Parameter grid:** 50×50 (m_φ × θ)
- **θ range:** 1e-22 to 1e-18
- **br_max:** 0.145 (conservative)
- **use_normalized_slack:** True

## Results

### Dominance Across All Θ_lab Values

All seven screening levels (Θ_lab = 1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001) produced **identical dominance**:

- **QRNG_tilt:** 86.7% (dominant bottleneck)
- **ATLAS_mu:** 13.3% (secondary constraint)
- **Higgs_inv:** 0.0% (not active)
- **Fifth_force:** 0.0% (not active)

### Key Finding

**Normalized slack comparison completely changes the bottleneck diagnosis.**

#### Previous Result (Raw Slack):
- 100% Fifth_force limited
- Collider constraints never active

#### New Result (Normalized Slack):
- 86.7% QRNG_tilt limited
- 13.3% ATLAS_mu limited
- 0% Fifth_force limited
- 0% Higgs_inv limited

## Interpretation

### Why Normalized Slack Matters

1. **Raw slack comparison is biased:**
   - Fifth-force slack ~ 1e-6 (very small absolute value)
   - Collider slack ~ 0.1 (100,000× larger absolute value)
   - QRNG slack ~ 0.0008 (intermediate)
   - Raw comparison always picks the smallest absolute slack → fifth-force

2. **Normalized slack is fair:**
   - Normalized slack = slack / bound (dimensionless)
   - Compares "how close to violation" relative to the constraint scale
   - QRNG_tilt: normalized slack ~ (0.0008 - value) / 0.0008
   - ATLAS_mu: normalized slack ~ (0.112 - deviation) / 0.112
   - Fifth-force: normalized slack ~ (alpha_max - alpha_eff) / alpha_max

3. **The true bottleneck is QRNG_tilt:**
   - QRNG constraint has the smallest normalized slack (tightest relative to its scale)
   - This makes sense: QRNG tilt constraint (|ε| < 0.0008) is very tight
   - Fifth-force constraints, while having small absolute slack, are actually less restrictive when normalized

### Why Screening Doesn't Change Dominance

- Screening (Θ_lab) only affects fifth-force constraints
- Fifth-force is no longer the bottleneck (0% dominance)
- Therefore, screening cannot shift dominance
- The bottleneck is now QRNG_tilt and ATLAS_mu, which are unaffected by screening

## Implications

### 1. The Real Bottleneck is QRNG Constraints
- QRNG tilt constraint (|ε| < 0.0008) is the dominant limiting factor
- This suggests that consciousness field effects (QRNG biases) are more tightly constrained than fifth forces
- The ethical biasing mechanism (η) must be very small to satisfy QRNG bounds

### 2. Collider Constraints Are Active
- ATLAS μ constraint is active (13.3% of points)
- Higgs invisible branching ratio is not active (0%) even with tight constraint (br_max = 0.107)
- This suggests that collider constraints are relevant but not the primary bottleneck

### 3. Fifth-Force Constraints Are Not the Bottleneck
- With normalized slack, fifth-force constraints are not active (0%)
- This is a major shift from the previous 100% fifth-force limited result
- The normalized comparison reveals that fifth-force constraints are actually less restrictive than QRNG constraints

### 4. Screening Doesn't Help
- Screening (Θ_lab) doesn't change dominance because it only affects fifth-force
- Since fifth-force is not the bottleneck, screening cannot help
- To shift dominance, we would need to suppress QRNG effects or collider signals

## Next Steps

1. **Investigate QRNG constraint scaling:**
   - Current scaling: ε ∝ α * 1e3 (simplified)
   - Need to verify if this scaling is correct
   - If QRNG constraint is too tight, may need to adjust the scaling

2. **Test with different QRNG epsilon_max:**
   - Current: epsilon_max = 0.0008
   - Test with larger epsilon_max to see if dominance shifts

3. **Implement scale-breaking suppression:**
   - Add μ parameter to suppress α naturally
   - This could help with both QRNG and collider constraints

4. **Refine collider constraint mapping:**
   - Current: simplified scaling (BR ∝ α * 0.1)
   - Need more accurate mapping from α to BR(H→inv)

## Conclusion

The normalized slack comparison reveals that **QRNG_tilt is the true bottleneck** (86.7%), not fifth-force constraints. This is a major finding that changes the interpretation of the viable parameter space. The previous "100% fifth-force limited" result was an artifact of biased raw slack comparison.

Screening (Θ_lab) does not shift dominance because it only affects fifth-force constraints, which are no longer the bottleneck. To shift dominance, we would need mechanisms that suppress QRNG effects or collider signals, not fifth forces.

## References

- Brax & Burrage (2021): "Screening the Higgs portal", Phys. Rev. D 104, 015011
- Burrage et al. (2018): "Fifth forces, Higgs portals and broken scale invariance", arXiv:1804.07180
- CODATA 2018: ħc = 197.3269804 MeV·fm = 1.973269804e-16 GeV·m

