# Fifth-Force Detectability Summary

## Run Metadata

**Seed:** 42
**Git Commit:** a8c1419cd15e70fd2e6cac7794ee8776d4512756
**Real-Only Mode:** Enabled (synthetic curves excluded)
**Alpha Mapping Mode:** A

## Real-Curve Coverage Report

**Purpose:** Shows what fraction of sampled points fall within real experimental coverage.

**Rule:** In real-only mode, points outside real curve coverage are NOT marked as 'excluded'.

### Coverage by Real Curve

| Curve | λ_min (m) | λ_max (m) | Points Covered | Fraction |
|-------|-----------|-----------|----------------|----------|
| zenodo5080965_fig3 | 2.922e-11 | 8.448e-09 | 0/131 | 0.00% |
| eotwash_prl2016_digitized | 2.995e-05 | 9.289e-04 | 131/131 | 100.00% |

**Total Coverage:** 131/131 points (100.00%) covered by at least one real curve

**Intersection Coverage:** 0/131 points (0.00%) covered by all real curves

✅ **Uncovered Points:** 0/131 (0.00%) - all points within real experimental coverage

---

## Purpose

This report quantifies where the scalar would be detectable if it exists by computing
r = alpha_pred / alpha_max_envelope(lambda_m) for sampled model points.

## Curve Used

{'source_id': 'eotwash_prl2016_digitized', 'lambda_min': 2.99528567943e-05, 'lambda_max': 0.0009288694666433, 'fraction_covered': 1.0, 'count_covered': 131, 'count_total': 131}

**Note:** Real-only mode enabled. Synthetic curves excluded from envelope.

## Statistics

Total points computed: 131

| Threshold | Count | Fraction |
|-----------|-------|----------|
| r > 1.0   |     0 | 0.0% |
| r > 0.1  |     0 | 0.0% |
| r > 0.01 |     0 | 0.0% |
| r > 0.001|     0 | 0.0% |

## Top 25 Points by Detectability Ratio (r)

These are the points closest to detection threshold:

| m_phi_GeV | theta | mu_sb/m_h | alpha_pred | lambda_m (m) | f_eq (Hz) | E_eq (eV) | alpha_max | r | excluded | source |
|-----------|-------|-----------|------------|--------------|-----------|-----------|-----------|---|----------|--------|
| 5.821e-13 | 3.124e-19 | 8.959e-01 | 1.518e-10 | 3.390e-04 | 1.408e+11 | 5.821e-04 | 3.782e+00 | 4.012e-11 | False | eotwash_prl2016_digitized |
| 5.402e-13 | 2.815e-19 | 7.056e-01 | 1.481e-11 | 3.653e-04 | 1.306e+11 | 5.402e-04 | 3.782e+00 | 3.916e-12 | False | eotwash_prl2016_digitized |
| 6.677e-13 | 8.024e-20 | 8.464e-01 | 4.190e-13 | 2.955e-04 | 1.614e+11 | 6.677e-04 | 3.782e+00 | 1.108e-13 | False | eotwash_prl2016_digitized |
| 2.626e-13 | 1.122e-19 | 4.269e-01 | 6.699e-15 | 7.514e-04 | 6.350e+10 | 2.626e-04 | 8.332e-01 | 8.041e-15 | False | eotwash_prl2016_digitized |
| 6.316e-13 | 3.061e-19 | 2.576e-01 | 6.544e-15 | 3.124e-04 | 1.527e+11 | 6.316e-04 | 3.782e+00 | 1.730e-15 | False | eotwash_prl2016_digitized |
| 2.192e-13 | 5.554e-19 | 1.225e-01 | 1.851e-16 | 9.003e-04 | 5.300e+10 | 2.192e-04 | 2.734e-01 | 6.771e-16 | False | eotwash_prl2016_digitized |
| 4.475e-12 | 5.728e-19 | 4.836e-01 | 1.236e-11 | 4.410e-05 | 1.082e+12 | 4.475e-03 | 2.937e+05 | 4.210e-17 | False | eotwash_prl2016_digitized |
| 4.190e-12 | 1.275e-19 | 9.408e-01 | 6.236e-12 | 4.709e-05 | 1.013e+12 | 4.190e-03 | 2.937e+05 | 2.124e-17 | False | eotwash_prl2016_digitized |
| 8.968e-13 | 5.876e-20 | 3.528e-01 | 1.100e-16 | 2.200e-04 | 2.168e+11 | 8.968e-04 | 7.768e+00 | 1.416e-17 | False | eotwash_prl2016_digitized |
| 5.826e-13 | 2.174e-20 | 5.052e-01 | 3.640e-17 | 3.387e-04 | 1.409e+11 | 5.826e-04 | 3.782e+00 | 9.625e-18 | False | eotwash_prl2016_digitized |
| 4.111e-12 | 6.013e-19 | 3.540e-01 | 1.236e-12 | 4.800e-05 | 9.940e+11 | 4.111e-03 | 2.937e+05 | 4.210e-18 | False | eotwash_prl2016_digitized |
| 5.253e-13 | 1.361e-20 | 4.805e-01 | 3.742e-18 | 3.756e-04 | 1.270e+11 | 5.253e-04 | 3.782e+00 | 9.894e-19 | False | eotwash_prl2016_digitized |
| 1.513e-12 | 4.898e-19 | 1.323e-01 | 2.080e-16 | 1.304e-04 | 3.659e+11 | 1.513e-03 | 6.833e+02 | 3.044e-19 | False | eotwash_prl2016_digitized |
| 4.792e-13 | 4.709e-21 | 6.283e-01 | 4.589e-19 | 4.118e-04 | 1.159e+11 | 4.792e-04 | 3.782e+00 | 1.213e-19 | False | eotwash_prl2016_digitized |
| 3.271e-13 | 5.767e-19 | 5.326e-02 | 2.750e-19 | 6.033e-04 | 7.909e+10 | 3.271e-04 | 3.298e+00 | 8.340e-20 | False | eotwash_prl2016_digitized |
| 1.515e-12 | 3.279e-20 | 4.290e-01 | 5.090e-17 | 1.302e-04 | 3.663e+11 | 1.515e-03 | 6.833e+02 | 7.450e-20 | False | eotwash_prl2016_digitized |
| 2.994e-12 | 2.155e-20 | 7.700e-01 | 1.024e-15 | 6.590e-05 | 7.240e+11 | 2.994e-03 | 3.381e+04 | 3.029e-20 | False | eotwash_prl2016_digitized |
| 3.150e-13 | 4.850e-21 | 4.764e-01 | 5.639e-20 | 6.265e-04 | 7.616e+10 | 3.150e-04 | 3.298e+00 | 1.710e-20 | False | eotwash_prl2016_digitized |
| 2.045e-12 | 3.460e-20 | 3.222e-01 | 6.395e-18 | 9.651e-05 | 4.944e+11 | 2.045e-03 | 5.081e+03 | 1.259e-21 | False | eotwash_prl2016_digitized |
| 4.791e-13 | 4.657e-22 | 9.408e-01 | 1.109e-21 | 4.118e-04 | 1.159e+11 | 4.791e-04 | 3.782e+00 | 2.932e-22 | False | eotwash_prl2016_digitized |
| 6.689e-13 | 3.539e-19 | 2.610e-02 | 1.297e-22 | 2.950e-04 | 1.617e+11 | 6.689e-04 | 3.782e+00 | 3.429e-23 | False | eotwash_prl2016_digitized |
| 2.797e-12 | 1.986e-20 | 3.353e-01 | 9.545e-19 | 7.054e-05 | 6.764e+11 | 2.797e-03 | 3.060e+04 | 3.119e-23 | False | eotwash_prl2016_digitized |
| 9.329e-13 | 1.775e-20 | 1.241e-01 | 2.142e-22 | 2.115e-04 | 2.256e+11 | 9.329e-04 | 7.768e+00 | 2.757e-23 | False | eotwash_prl2016_digitized |
| 1.311e-12 | 6.011e-19 | 3.676e-02 | 1.672e-20 | 1.505e-04 | 3.171e+11 | 1.311e-03 | 6.833e+02 | 2.447e-23 | False | eotwash_prl2016_digitized |
| 2.332e-13 | 1.213e-19 | 3.030e-02 | 5.900e-24 | 8.463e-04 | 5.638e+10 | 2.332e-04 | 6.576e-01 | 8.973e-24 | False | eotwash_prl2016_digitized |

## Where to Look

The highest detectability ratio is r = 4.012e-11 at λ = 3.390e-04 m.

This corresponds to f_eq = 1.408e+11 Hz (equivalent frequency tag).

Across the central 80% of the λ range (3.802e-05 to 6.235e-04 m),
the average detectability ratio is r = 4.205e-13.

**Interpretation:**
- r ≪ 1: scalar is well below current experimental sensitivity
- r ≈ 0.1–1: scalar is in the detectable range; near-future experiments could see it
- r > 1: scalar is excluded by current constraints

**Frequency Translation:**
The equivalent frequency f_eq = c/(2πλ) provides a translation layer to map
fifth-force ranges onto a universal Hz axis, enabling comparison with other
MQGT-SCF constraint channels (cosmology ~10⁻¹⁸ Hz, QRNG ~Hz–GHz, Higgs ~10²⁵ Hz).
This is a unit-conversion tool, not evidence by itself.