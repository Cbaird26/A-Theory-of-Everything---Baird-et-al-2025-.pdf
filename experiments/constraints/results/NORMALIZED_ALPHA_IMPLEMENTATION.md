# Normalized Alpha Implementation - Summary

## Overview

This document summarizes the implementation of the properly normalized derived-α mapping from Brax & Burrage (2021), replacing the incorrect toy normalization that produced unrealistically small α values.

## Implementation Date

December 29, 2025

## Key Changes

### 1. Fixed Normalization Formula

**Before (incorrect):**
```python
α = (θ / v)² * (m_N / m_Pl)²  # Produced α ~ 10^-54 (absurdly tiny)
```

**After (correct, Brax & Burrage Eq. 26 + 21):**
```python
β_φ = (m_Pl / v) * sin θ
α = 2 * β_φ² = 2 * (sin θ * m_Pl / v)²
```

**Impact:**
- For θ = 10^-4: α ≈ 4.9e25 (huge, excluded)
- For θ = 10^-17: α ≈ 1 (just at bound)
- Need θ < 10^-20 to survive typical fifth-force bounds (α < 1e-6)

### 2. Fixed Unit Conversion

**Before:**
```python
HBAR_C = 197.3e-15  # Approximate
```

**After (CODATA 2018):**
```python
HBAR_C_GeV_m = 1.973269804e-16  # CODATA 2018, exact
```

**Verification:**
- m_φ = 2e-10 GeV → λ ≈ 0.987 µm ✓
- m_φ = 2e-16 GeV → λ ≈ 0.987 m ✓

### 3. Fixed Planck Mass

**Before:**
```python
M_PL = 2.435e18  # Wrong value
```

**After:**
```python
M_PL = 1.22e19  # Reduced Planck mass (correct)
```

### 4. Added Screening Support

**Implementation:**
```python
α_eff = Θ² * α_unscreened  # Multiplicative (Brax & Burrage Eq. 97-98)
```

**Usage:**
- `--screening` flag to enable
- `--Theta` parameter (default 1.0 = unscreened)
- For Θ = 0.1: α_eff = 0.01 * α (100× suppression)

### 5. Added Lambda-Regime Selection

**Options:**
- `--lambda-regime sub-nm`: m_φ in MeV-GeV range (default)
- `--lambda-regime micron-to-meter`: m_φ ultralight (2e-16 to 2e-10 GeV)

## Results Comparison

### Incorrect Normalization (Before Fix)

- **Viable points:** 40,000
- **θ range:** 1.8e-6 to 5.6e-2
- **α range:** 7.8e-54 to 7.8e-45 (absurdly tiny)
- **Issue:** Used (m_N/m_Pl)² which divides by m_Pl twice

### Correct Normalization (After Fix)

**Unscreened (Θ=1.0):**
- **Viable points:** 1,100-1,700 (depending on scan range)
- **θ range:** 1.2e-22 to 4.3e-21 (extremely small!)
- **α range:** 7.2e-11 to 9.1e-8 (within bounds)
- **Constraint dominance:** 100% fifth-force limited

**Screened (Θ=0.1):**
- **Viable points:** 1,700
- **θ range:** 1.2e-22 to 4.1e-20 (slightly larger)
- **α range:** 7.2e-13 to 8.2e-8
- **Constraint dominance:** 100% fifth-force limited

## Key Physics Insight

The proper normalization from Brax & Burrage introduces a huge factor (m_Pl / v)² ≈ 2.45 × 10^32, making α extremely large for any reasonable θ. This means:

1. **Higgs portal fifth forces are extremely constrained** - this is correct physics
2. **The "no viable region" result with larger θ is physically correct** - not a bug
3. **Only extremely small θ (< 10^-20) can survive** - this is the reality of the model
4. **Screening can help** - but even with Θ = 0.1, θ must still be < 10^-19

## Files Modified

1. `experiments/constraints/scripts/derive_alpha_from_portal.py`
   - Fixed constants (CODATA ħc, correct m_Pl)
   - Replaced `derive_alpha_normalized` with correct formula
   - Added `Theta` parameter for screening

2. `experiments/constraints/scripts/check_overlap_derived_alpha.py`
   - Added `Theta` parameter support
   - Added `--lambda-regime` argument
   - Updated to pass `Theta` to mapping function

## Verification Tests

All tests passed:
- ✅ Unit conversion (CODATA)
- ✅ Normalization formula (α = 2 β²)
- ✅ Screening mechanism (α_eff = Θ² α)
- ✅ Lambda-regime selection
- ✅ Constraint labeling (still 100% fifth-force limited)

## References

- Brax & Burrage (2021): "Screening the Higgs portal", Phys. Rev. D 104, 015011
  - Eq. 26: β_φ / m_Pl = sin θ / v
  - Eq. 21: V(r) = 2 β_φ(φ_bg)² V_N(r) e^{-m_φ r}
  - Eq. 97-98: Screening factor Θ

- CODATA 2018: ħc = 197.3269804 MeV·fm = 1.973269804e-16 GeV·m

## Conclusion

The implementation is complete and verified. The normalized model correctly shows that Higgs portal fifth forces are extremely constrained, requiring θ < 10^-20 to survive experimental bounds. This is the correct physics from Brax & Burrage (2021), not a bug. The dramatic shrinkage from 40,000 to ~1,100 viable points demonstrates the power of proper normalization in eliminating unphysical parameter space.

