# Claims, Limits, and Falsifiers for MQGT-SCF

**Date:** 2026-01-19  
**Repository:** MQGT-SCF  
**Status:** **Canonical (Scientific Contract)** ⭐

---

## Purpose

This document draws bright lines between what MQGT-SCF **claims**, what it **assumes**, and what would **falsify** the hypothesis. It serves as a "scientific contract" that enables critics to engage with the work on method and evidence rather than speculation.

---

## What MQGT-SCF Is

An **operational constraint lab** for testing a parameterized hypothesis class (effective field theory extension with scalar consciousness and ethical fields) against public experimental constraints across multiple independent channels:

- QRNG (quantum random number generator) bias tests
- Fifth-force experiments (short-range gravity tests)
- Higgs portal constraints (collider experiments)
- Cosmological constraints (large-scale structure)

The framework is designed to be **falsifiable** through operational constraints that quantify where the hypothesis would be excluded, near-detectable, or unconstrained under explicitly stated mapping assumptions.

---

## What MQGT-SCF Is Not

**Not a validated discovery** of new physics. The framework does not claim:
- That consciousness fields exist
- That ethical weighting in quantum measurement is real
- That the modified Born rule has been experimentally confirmed
- That any experimental deviations have been observed

**Not a complete Theory of Everything** in the sense of a validated, empirically confirmed unified theory. The framework is:
- A speculative hypothesis
- An instrumented constraint analysis
- A falsifiable prediction generator

**Not mystical or psychological** in its core claims. The framework:
- Uses frequency scales as translation tools (not as physical assertions about "emotion Hz")
- Treats synthetic curves as scaffolding/plumbing (not as experimental truth)
- Separates visualization aids from physical claims

---

## Core Claims (Falsifiable)

These are the claims that can be tested empirically:

### 1. Modified Born Rule Predictions

**Claim:** If consciousness and ethical fields exist as described, quantum measurement probabilities would be deformed:

```
P(i) ∝ |⟨i|Ψ⟩|² exp(η E_i)
```

where E_i is an ethical energy and η is a small coupling ensuring macroscopic decoupling.

**Testability:**
- QRNG bias tests can detect deviations from true randomness
- Current bound: ε_max = 0.010887 (conservative pooled, N=54,434 bits from NIST Beacon v2)
- Falsifiable if no deviations observed as sample size increases

**Falsifiers:**
- No anomalous biases in QRNG under ethical intent conditions
- Biases observed are consistent with known systematic effects
- Statistical bounds tighten below detectable thresholds

### 2. Fifth-Force Detectability Predictions

**Claim:** If scalar fields exist as described, they would appear as Yukawa-type fifth forces with specific coupling strengths α and interaction ranges λ.

**Testability:**
- Fifth-force experiments (torsion balances, micro-mechanical detectors) can constrain (α, λ) parameter space
- Current analysis identifies hunt bands: λ ~ 0.3-1.3 mm, f_eq ~ 5×10¹⁰–1.6×10¹² Hz
- Falsifiable through targeted experiments in these parameter ranges

**Falsifiers:**
- No deviations observed in hunt band parameter ranges
- Experiments rule out parameter space where framework predicts detectability
- Constraints inconsistent with framework's mapping assumptions

### 3. Multi-Channel Consistency

**Claim:** If the framework is valid, it must be consistent across all constraint channels (QRNG, fifth-force, Higgs, cosmology).

**Testability:**
- Dominance analysis shows which channels matter where in parameter space
- Current analysis: QRNG ~80%, fifth-force ~1.2%, Higgs ~5%, cosmology (not yet integrated)
- Falsifiable if channels give inconsistent constraints

**Falsifiers:**
- Channel constraints are mutually incompatible
- No parameter space exists that satisfies all channels simultaneously
- Experimental updates rule out all viable parameter islands

---

## Limits and Assumptions

These are explicit assumptions and placeholders that limit the current framework:

### 1. α_pred Mapping Modes (Explicit Placeholders)

The mapping from internal model parameters to fifth-force coupling strength α_pred is **not fully derived** and uses placeholder modes:

**Mode A (Legacy Placeholder):**
- `α_pred = α_eff²`
- Status: Temporary surrogate, kept for backward compatibility
- Assumption: Squared coupling provides reasonable proxy

**Mode B (Portal-Derived Proxy):**
- `α_pred = 2(κ α_eff)²`
- Status: Based on Higgs portal literature approximations
- Assumption: Portal coupling factor κ ≈ 1.0 provides reasonable approximation
- Limitation: Not derived from first principles

**Mode C (Agnostic Scaling):**
- `α_pred = s_ff α_eff²` with optional `λ → s_λ λ`
- Status: Explicit scaling knobs for sensitivity analysis
- Assumption: Scaling factors s_ff and s_λ can be varied to test robustness
- Limitation: No physical justification for specific scaling values

**Sensitivity Analysis:**
- Current analysis shows fifth-force remains subdominant (< 3%) even at ×10 mapping scaling
- This suggests robustness to mapping uncertainty, but does not eliminate the placeholder nature

### 2. Real vs. Synthetic Constraints

**Real Constraints (Experimental Data):**
- `eotwash_prl2016_digitized_contract.csv`: Digitized from PRL 116, 161101 (2016)
- `zenodo5080965_fig3_contract.csv`: From Heacock & Huber (Zenodo 5080965)
- These represent actual experimental bounds

**Synthetic Constraints (Scaffolding):**
- `placeholder_eotwash_style.csv`: Regression/validation curve
- `eotwash_style_synthetic_contract.csv`: Plumbing for testing
- `eotwash_tighter_synthetic_contract.csv`: Validation curve

**Guardrails:**
- Synthetic curves are **explicitly labeled** as scaffolding/plumbing
- Real-only mode (`--real-only`) excludes synthetics from canonical analysis
- Coverage reporting shows fraction of sampled points within real curve λ ranges
- Points outside real coverage are **not** marked as "excluded" in real-only mode

### 3. Frequency Translation Tools

The frequency atlas (`docs/frequency_atlas.md`) provides conversion formulas:

- `f_eq ≈ c/(2πλ)` for Yukawa range → equivalent frequency
- `f = E/h` for energy → frequency
- `f = 1/T` for timescale → frequency

**Status:** Translation tools for organizing multi-scale constraints, **not** physical assertions.

**Limitation:** These are unit conversions and scale labels, not literal oscillations or "emotion frequencies."

---

## Measured/Computed vs. Assumed/Mapped

### Measured/Computed (Empirical)

These are direct calculations from data:

- **Constraint dominance percentages:** QRNG ~80%, fifth-force ~1.2%, Higgs ~5%
- **Detectability ratios:** r = α_pred / α_max for sampled model points
- **Hunt band locations:** λ ~ 0.3-1.3 mm where r ≈ 0.1-1 (near-detectable)
- **Exclusion fractions:** ~1.3% of points excluded (r > 1), ~1.8% near-detectable (0.1 < r ≤ 1)
- **Coverage fractions:** Fraction of sampled points within real curve λ ranges
- **QRNG bounds:** ε_max = 0.010887 from pooled multi-source analysis

### Assumed/Mapped (Explicit Assumptions)

These require explicit assumptions:

- **α_pred mapping modes:** Mode A/B/C are placeholders, not derived from first principles
- **Coupling parameterizations:** ξ, λ_c, λ_e values assumed but not measured
- **Ethical energy E_i:** Operational definition assumed but not independently measured
- **Consciousness field Φ_c:** Existence assumed but not experimentally confirmed
- **Portal coupling factors:** κ and other portal parameters are approximations

---

## Falsifiers (What Would Disprove the Hypothesis)

### Strong Falsifiers

If any of these occur, the framework would be falsified:

1. **No deviations in hunt bands:** Targeted experiments in λ ~ 0.3-1.3 mm show no fifth-force deviations where framework predicts detectability

2. **QRNG bounds tighten below detectable:** Statistical bounds on QRNG bias decrease below framework's predicted thresholds as sample size increases

3. **Channel incompatibility:** Constraint channels are mutually incompatible, leaving no viable parameter space

4. **Symmetry violations:** Framework violates established symmetries beyond acceptable decoupling limits

5. **Contradictory experimental results:** Experiments directly contradict framework predictions with high confidence

### Weak Falsifiers (Require Interpretation)

These would require careful interpretation:

1. **Mapping sensitivity failure:** Results are highly sensitive to mapping mode choice, suggesting framework is underconstrained

2. **Synthetic curve dependence:** Conclusions depend critically on synthetic curves, indicating lack of real experimental coverage

3. **Coverage gaps:** Sampled parameter space lies mostly outside real experimental coverage, limiting interpretability

---

## Synthetic vs. Real Data (Guardrails)

### Labeling Convention

**Real Curves:**
- Filename contains source identifier (e.g., `eotwash_prl2016`, `zenodo5080965`)
- Provenance manifest includes scientific reference (DOI, paper citation)
- Used in canonical analysis

**Synthetic Curves:**
- Filename contains `synthetic` or `placeholder`
- Provenance manifest explicitly labels as "synthetic/regression/validation"
- Used only for plumbing/validation, not canonical conclusions

### Real-Only Mode

The `--real-only` flag in detectability analysis:

- **Excludes** synthetic curves from constraint envelope
- **Reports** coverage fractions for each real curve
- **Refuses** to mark points as "excluded" outside real experimental coverage
- **Prevents** overinterpretation of results where no real constraints exist

### Coverage Reporting

For each real curve used:
- λ_min, λ_max (interaction range coverage)
- Fraction of sampled points within this range
- Hard rule: Points outside coverage are not "excluded" in real-only mode

---

## Frequency Ladder as Translation Tool

The frequency atlas (`docs/frequency_atlas.md`) provides a translation layer for organizing multi-scale constraints.

**What it is:**
- Unit conversion formulas (λ → f_eq, E → f, T → f)
- Organizational tool for comparing constraints across 43-60 orders of magnitude
- Visualization aid for understanding scale relationships

**What it is not:**
- Physical assertion that frequencies have literal meaning for consciousness/ethics
- Claim that "emotion frequencies" are physical observables
- Mystical or psychological mapping

**Guardrail:** Frequency ladder is a **ruler**, not a physical assertion. It enables cross-channel comparison but does not claim that frequency scales are fundamental to the physics.

---

## Current Status Summary

**Operational Status:**
- ✅ Reproducible constraint lab framework implemented
- ✅ Multi-channel constraint analysis functional
- ✅ Real-only mode available for reviewer-safe analysis
- ✅ Mapping sensitivity modes implemented (A/B/C)
- ✅ Coverage reporting prevents overinterpretation

**Limitations:**
- ⚠️ α_pred mapping is placeholder (not fully derived)
- ⚠️ Limited real experimental coverage (mm-cm scales)
- ⚠️ Framework unvalidated (no experimental confirmations)
- ⚠️ Many assumptions explicit but not independently verified

**Falsifiability:**
- ✅ Framework makes testable predictions (hunt bands, QRNG bounds)
- ✅ Predictions can be tested with existing or near-future experiments
- ✅ Framework can be falsified through multiple channels

---

## References

- Repository: https://github.com/Cbaird26/MQGT-SCF
- Constraint lab snapshot: [`docs/constraint_lab_snapshot.md`](constraint_lab_snapshot.md)
- Fifth-force summary: [`docs/fifth_force_summary.md`](fifth_force_summary.md)
- Frequency atlas: [`docs/frequency_atlas.md`](frequency_atlas.md)
- Data ground truth: [`docs/DATA_GROUND_TRUTH.md`](DATA_GROUND_TRUTH.md) (if exists)
- Mapping sensitivity: [`docs/MAPPING_SENSITIVITY.md`](MAPPING_SENSITIVITY.md) (if exists)

---

**This document is designed to survive scrutiny and enable productive scientific engagement. All assumptions are explicit, all claims are falsifiable, and all limitations are documented.**
