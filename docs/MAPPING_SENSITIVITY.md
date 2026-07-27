# Mapping Sensitivity Analysis

**Date:** 2026-01-19  
**Repository:** MQGT-SCF  
**Status:** **Canonical (Mapping Modes Documentation)** ⭐

---

## Purpose

This document explains the α_pred mapping modes (A/B/C), their assumptions and limitations, how to run sensitivity sweeps, and how to interpret results across modes.

---

## Background

The mapping from internal model parameters to fifth-force coupling strength α_pred is **not fully derived** and uses placeholder modes. This is the framework's biggest physics vulnerability, but making it explicit and testable turns "arbitrary mapping" into "explicit assumptions with robustness checks."

## Automated Sensitivity Sweep

A mapping sensitivity sweep can be run automatically to test robustness across all modes:

```bash
make fifth-mapping-sensitivity SEED=42 NPTS=2000 REAL_ONLY=1
```

Or with custom S_FF values:

```bash
make fifth-mapping-sensitivity SEED=42 NPTS=2000 REAL_ONLY=1 S_FF_VALUES="0.1,1.0,10.0,100.0,1000.0"
```

This generates:
- `results/mapping_sensitivity_summary.md` - Human-readable summary table
- `results/mapping_sensitivity_summary.json` - Machine-readable results with full statistics
- `results/mapping_sensitivity_plot.png` - Log-log plot of r_max vs S_FF for modes B/C (if matplotlib available)

**Key Feature:** The sweep uses the **same fixed point set** across all modes (A/B/C/D), ensuring differences arise solely from mapping variations, not Monte Carlo sampling noise. Mode D uses converted ToE parameters for the full ToE-native chain.

---

## Mapping Modes

### Mode A: Legacy Placeholder

**Formula:** `α_pred = α_eff²`

**Status:** Temporary surrogate, kept for backward compatibility

**Assumption:** Squared coupling provides reasonable proxy for fifth-force strength

**Limitation:** Not derived from first principles; no physical justification beyond dimensional consistency

**Usage:**
```bash
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=A
```

**When to use:**
- Backward compatibility with existing results
- Initial exploration of parameter space
- Baseline for comparing other modes

---

### Mode B: Portal-Derived Proxy

**Formula:** `α_pred = 2(κ α_eff)²`

**Status:** Based on Higgs portal literature approximations (e.g., arXiv:1804.07180)

**Parameters:**
- `kappa` (κ): Portal coupling factor (default: 1.0)

**Assumptions:**
- Portal coupling factor κ ≈ 1.0 provides reasonable approximation
- Based on Higgs portal screening mechanisms in scalar-tensor theories
- Derived from approximate matching to portal literature

**Limitations:**
- Not derived from first principles for MQGT-SCF
- Portal coupling factor κ is an approximation, not measured
- Specific prefactor (2.0) is literature-informed but not unique

**Usage:**
```bash
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=B KAPPA=1.0
```

**When to use:**
- Testing robustness to portal-based assumptions
- Comparing with Higgs portal literature
- Exploring sensitivity to portal coupling

**Literature reference:**
- Fifth forces, Higgs portals and broken scale invariance (arXiv:1804.07180)
- Higgs-induced screening mechanisms in scalar-tensor theories (NYAS)

---

### Mode C: Agnostic Scaling

**Formula:** `α_pred = s_ff α_eff²` with optional `λ → s_lambda λ`

**Status:** Explicit scaling knobs for sensitivity analysis

**Parameters:**
- `s_ff`: Scaling factor for alpha (default: 1.0)
- `s_lambda`: Scaling factor for lambda (default: 1.0)

**Assumptions:**
- Scaling factors can be varied to test robustness
- Order-of-magnitude variations (±×10) probe uncertainty

**Limitations:**
- No physical justification for specific scaling values
- Scaling is agnostic (no physics input)
- Used only for sensitivity analysis, not canonical mapping

**Usage:**
```bash
# Default scaling
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=C S_FF=1.0 S_LAMBDA=1.0

# Order-of-magnitude variations
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=C S_FF=0.1 S_LAMBDA=1.0
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=C S_FF=10.0 S_LAMBDA=1.0
```

**When to use:**
- Sensitivity analysis to mapping uncertainty
- Testing robustness of conclusions
- Demonstrating stability across order-of-magnitude variations

---

### Mode D: ToE-Native Higgs-Mixing Bridge

**Formula:** Uses explicit ToE equations: κ_cH, v_c → θ_hc (Eq. 13) → α (ToE normalization)

**Status:** Exact mapping from ToE parameters to Yukawa strength using ToE paper's equations

**Parameters:**
- `kappa_cH`: Portal coupling constant (dimensionless)
- `v_c_GeV`: Scalar VEV in GeV
- `m_c_GeV`: Scalar mass in GeV (or derived from m_phi)
- `f_n`: Nucleon scalar form factor (default: 0.30, can be swept)

**Equations Used:**
- **ToE Eq. (13):** θ_hc ≃ κ_cH v v_c / (m_c² - m_h²)
  - For m_c << m_h: θ_hc ≈ -κ_cH v v_c / m_h²
- **Yukawa strength:** α = 2 f_N² (M_Pl/v)² sin²θ
  - Numerically: K_ToE ≈ 1.76×10³¹ (for f_N=0.30)
  - Uses ToE's reduced Planck mass: M_Pl² = (8πG)⁻¹

**Assumptions:**
- Unscreened Higgs-mixed scalar
- Small mixing angle (sin θ ≈ θ)
- Standard Higgs-portal coupling structure
- Nucleon scalar form factor f_N ≈ 0.30 (with uncertainty)

**Limitations:**
- Requires explicit ToE parameter values (κ_cH, v_c)
- Assumes v_c ≠ 0 (symmetric vacuum v_c=0 gives no tree-level mixing)
- Hadronic uncertainty in f_N (typically 0.25-0.35)

**Usage:**
```bash
# Mode D with ToE parameters (requires model points with kappa_cH, v_c_GeV, m_c_GeV)
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=D

# Mode D with custom f_N
# (Note: f_n is set in model points, not via Makefile parameter)
```

**When to use:**
- Exact falsification tests using ToE's own equations
- Converting experimental bounds to ToE parameter constraints
- Reviewer-proof mapping that uses explicit ToE formulas
- Testing parameter fork: v_c=0 vs v_c≠0 implications

**Parameter Fork:**
- **If v_c = 0:** No tree-level Higgs mixing via Eq. (13) → Eöt-Wash may not constrain this channel
- **If v_c ≠ 0:** Eöt-Wash forces |κ_cH v_c| to be extremely small (typically < 10⁻¹¹ GeV)

**Inverse Mapping:**
Mode D enables conversion of experimental bounds to ToE parameters:
- Eöt-Wash α_max(λ) → θ_max(λ) → |κ_cH v_c| bounds
- See `code/inference/fifth_force/toe_bounds.py` for utilities

**Example: Converting Eöt-Wash to ToE Bounds:**
```python
from code.inference.fifth_force.toe_bounds import compute_full_toe_bounds
import pandas as pd

# Load digitized Eöt-Wash curve
eotwash = pd.read_csv('data/raw/eotwash_prl2016_digitized_contract.csv')

# Convert to ToE parameter bounds
toe_bounds = compute_full_toe_bounds(eotwash, f_n=0.30)

# Result: DataFrame with columns:
# - lambda_m, alpha_max, theta_max, mphi_eV, mphi_GeV, kappa_vc_max_GeV
print(toe_bounds[['lambda_m', 'theta_max', 'kappa_vc_max_GeV']])
```

**Reference:**
- ToE paper Eq. (13) for mixing angle
- ToE normalization: M_Pl (reduced) = 2.435×10¹⁸ GeV

---

## Running Sensitivity Sweeps

### Single Mode Sweep

Test different parameter values within a single mode:

```bash
# Mode B: Vary kappa
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=B KAPPA=0.1
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=B KAPPA=1.0
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=B KAPPA=10.0

# Mode C: Vary s_ff
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=C S_FF=0.1 S_LAMBDA=1.0
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=C S_FF=1.0 S_LAMBDA=1.0
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=C S_FF=10.0 S_LAMBDA=1.0
```

### Cross-Mode Comparison

Compare results across different modes:

```bash
# Same seed for fair comparison
SEED=42
NPTS=2000

# Mode A
make fifth-detectability SEED=$SEED NPTS=$NPTS ALPHA_MODE=A

# Mode B
make fifth-detectability SEED=$SEED NPTS=$NPTS ALPHA_MODE=B KAPPA=1.0

# Mode C (baseline)
make fifth-detectability SEED=$SEED NPTS=$NPTS ALPHA_MODE=C S_FF=1.0 S_LAMBDA=1.0

# Mode C (×10 scaling)
make fifth-detectability SEED=$SEED NPTS=$NPTS ALPHA_MODE=C S_FF=10.0 S_LAMBDA=1.0
```

### Automated Sensitivity Script

Example script for automated sweeps:

```python
#!/usr/bin/env python3
"""Run mapping sensitivity sweep."""

import subprocess
import sys

SEED = 42
NPTS = 2000

# Mode A
subprocess.run([
    "make", "fifth-detectability",
    f"SEED={SEED}", f"NPTS={NPTS}",
    "ALPHA_MODE=A"
])

# Mode B with different kappa
for kappa in [0.1, 1.0, 10.0]:
    subprocess.run([
        "make", "fifth-detectability",
        f"SEED={SEED}", f"NPTS={NPTS}",
        "ALPHA_MODE=B", f"KAPPA={kappa}"
    ])

# Mode C with different s_ff
for s_ff in [0.1, 1.0, 10.0]:
    subprocess.run([
        "make", "fifth-detectability",
        f"SEED={SEED}", f"NPTS={NPTS}",
        "ALPHA_MODE=C", f"S_FF={s_ff}", "S_LAMBDA=1.0"
    ])
```

---

## Interpreting Results Across Modes

### Stability Indicators

**Robust conclusions:**
- Hunt band location (λ range) remains similar across modes
- Excluded fraction remains small (<5%) across modes
- Dominance analysis shows QRNG remains primary constraint

**Sensitive conclusions:**
- Hunt band location shifts significantly across modes
- Excluded fraction varies by >50% across modes
- Fifth-force dominance changes dramatically

### Example Interpretation

**Scenario: Mode A vs. Mode C (×10 scaling)**

**Mode A (baseline):**
- Excluded: 1.3% of points
- Hunt band: λ ~ 0.3-1.3 mm
- Fifth-force dominance: 1.2%

**Mode C (×10 scaling):**
- Excluded: 2.8% of points
- Hunt band: λ ~ 0.3-1.3 mm (similar)
- Fifth-force dominance: 2.8%

**Interpretation:**
- Hunt band location is **robust** (doesn't shift across modes)
- Excluded fraction increases but remains small
- Fifth-force dominance increases but stays subdominant
- **Conclusion:** Results are moderately sensitive but robust at order-of-magnitude level

### Sensitivity Reporting Format

Each detectability run records mapping mode in output:

```markdown
## Run Metadata

**Seed:** 42
**Alpha Mapping Mode:** C
**s_ff:** 10.0
**s_lambda:** 1.0
```

Compare across modes in a sensitivity summary table:

| Mode | Parameters | Excluded % | Hunt Band λ (mm) | Fifth-Force Dominance % |
|------|-----------|------------|------------------|------------------------|
| A | (baseline) | 1.3% | 0.3-1.3 | 1.2% |
| B | κ=1.0 | 1.4% | 0.3-1.3 | 1.3% |
| C | s_ff=0.1 | 0.2% | 0.3-1.3 | 0.2% |
| C | s_ff=1.0 | 1.3% | 0.3-1.3 | 1.2% |
| C | s_ff=10.0 | 2.8% | 0.3-1.3 | 2.8% |

**Interpretation:** Hunt band location is robust; excluded fraction and dominance are moderately sensitive.

---

## Current Sensitivity Analysis Results

**From [`docs/fifth_force_summary.md`](fifth_force_summary.md):**

Dominance percentages across order-of-magnitude mapping uncertainty (s_ff scaling factor):

| s_ff | Fifth_force % | QRNG_tilt % | ATLAS_mu % | Higgs_inv % | Notes |
|------|---------------|-------------|------------|-------------|-------|
| 0.1  | 0.2%          | 83.1%       | 12.3%      | 4.4%        | Fifth_force negligible; QRNG dominant |
| 1.0  | 1.2%          | 81.3%       | 11.8%      | 4.5%        | Baseline: minor edge trim |
| 10.0 | 2.8%          | 79.2%       | 11.5%      | 4.2%        | Fifth_force rises but stays subdominant; no collapse |

**Conclusion:** Fifth_force remains subdominant (< 3%) even when the mapping is scaled by ×10. The conclusion is robust across an order-of-magnitude mapping uncertainty.

---

## Best Practices

### For Canonical Analysis

1. **Use real-only mode:** Exclude synthetic curves
   ```bash
   make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1 ALPHA_MODE=A
   ```

2. **Document mapping assumptions:** State which mode is used and why
   - Mode A: Legacy placeholder (baseline)
   - Mode B: Portal-derived proxy (if comparing with literature)
   - Mode C: Agnostic scaling (for sensitivity analysis only)

3. **Report sensitivity:** Include mapping sensitivity in results
   - Show results across modes or order-of-magnitude variations
   - Identify which conclusions are robust vs. sensitive

### For Sensitivity Analysis

1. **Use fixed seed:** Ensure fair comparison across modes
   ```bash
   SEED=42  # Same seed for all runs
   ```

2. **Vary systematically:** Test order-of-magnitude variations
   - s_ff ∈ {0.1, 1.0, 10.0}
   - kappa ∈ {0.1, 1.0, 10.0}

3. **Compare metrics:**
   - Excluded fraction
   - Hunt band location (λ range)
   - Constraint dominance percentages

4. **Report stability:** Clearly state which conclusions are robust

---

## Limitations and Future Work

### Current Limitations

1. **No first-principles derivation:** All modes are placeholders
2. **Portal literature approximations:** Mode B relies on approximate matching
3. **Agnostic scaling:** Mode C has no physics input

### Future Work

1. **Derive mapping from first principles:**
   - Compute α_pred from MQGT-SCF Lagrangian
   - Match to portal literature with explicit matching conditions
   - Validate against known limits (GR, SM recovery)

2. **Improve portal matching:**
   - Refine κ factor based on detailed portal analysis
   - Include screening effects explicitly
   - Match to Higgs portal constraints directly

3. **Sensitivity analysis:**
   - Systematic sweep across parameter space
   - Identify optimal mapping through constraint fitting
   - Quantify uncertainty in mapping

---

## References

- Claims/limits/falsifiers: [`docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`](CLAIMS_LIMITS_AND_FALSIFIERS.md)
- Fifth-force summary: [`docs/fifth_force_summary.md`](fifth_force_summary.md)
- Mapping audit: [`docs/dev/fifth_force_mapping_audit.md`](dev/fifth_force_mapping_audit.md)
- Portal literature:
  - Fifth forces, Higgs portals and broken scale invariance (arXiv:1804.07180)
  - Higgs-induced screening mechanisms in scalar-tensor theories (NYAS)

---

**Making mapping assumptions explicit and testable turns "arbitrary mapping" into "explicit assumptions with robustness checks."**
