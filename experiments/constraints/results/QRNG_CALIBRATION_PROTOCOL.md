# QRNG Calibration Protocol

## Date
2025-12-29

## Overview
Multi-source calibration of QRNG_tilt constraint bound (ε_max) from independent QRNG data sources.

## Data Sources

### lfdr_withinrun
- **Path:** experiments/grok_qrng/results/lfdr_withinrun/global_summary.json
- **Time range:** 2024-01-01 00:00:00 to 2024-01-05 15:06:39
- **n_trials:** 400,000
- **ε_max:** 0.000742
- **95% CI:** [0.000030, 0.002353]
- **Data hash:** e0b59edc45129605...

## Pooled Result

- **Method:** meta_analysis_inverse_variance
- **ε_max (pooled point estimate):** 0.000742
- **95% CI (bootstrap):** [0.000000, 0.001904]
- **Note on CI lower bound:** The lower bound of 0.000000 is a bootstrap edge case due to finite-sample effects in the resampling scheme, not a physical "true zero bias." The pooled point estimate (0.000742) is the primary calibrated value used in constraint analysis.

## Preprocessing

- **Method:** bootstrap_95
- **Bootstrap samples:** 1,000
- **Window size:** None

## Sensitivity Analysis

### Window Size Effects

- **Window size 10000:** ε_max = 0.015300 [0.000035, 0.002350]
- **Window size 50000:** ε_max = 0.005900 [0.000047, 0.002192]
- **Window size 100000:** ε_max = 0.003640 [0.000042, 0.002273]
- **Window size full:** ε_max = 0.000742 [0.000038, 0.002295]


## Assumptions

1. **Stationarity:** QRNG bias is constant over the measurement period
2. **Independence:** Trials are independent (no autocorrelation)
3. **No systematic drift:** No time-dependent bias trends
4. **Representative sampling:** Sources are representative of QRNG behavior under test conditions

## What Would Falsify This Bound

If future QRNG data (with similar or larger sample sizes) produces:
- **ε_max < 0.000000:** Current bound is too conservative; viable region expands
- **ε_max > 0.001904:** Current bound is too optimistic; viable region shrinks significantly

**Quantitative impact:** If ε_max tightens by 10%, the viable parameter island shrinks by approximately X% (to be computed from constraint engine).

## Reproducibility

- **Script:** /Users/christophermichaelbaird/mqgt-scf-paper/experiments/constraints/scripts/calibrate_qrng_multisource.py
- **Script hash:** 14120dc8a8e35e99...
- **Data hashes:** See per-source sections above

## Next Steps

1. Integrate pooled ε_max into constraint engine
2. Re-run μ phase diagram with calibrated bounds
3. Update regression tests if baseline changes
