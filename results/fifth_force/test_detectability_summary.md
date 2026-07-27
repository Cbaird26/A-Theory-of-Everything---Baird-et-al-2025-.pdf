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
| zenodo5080965_fig3 | 2.922e-11 | 8.448e-09 | 0/31 | 0.00% |
| eotwash_prl2016_digitized | 2.995e-05 | 9.289e-04 | 31/31 | 100.00% |

**Total Coverage:** 31/31 points (100.00%) covered by at least one real curve

**Intersection Coverage:** 0/31 points (0.00%) covered by all real curves

✅ **Uncovered Points:** 0/31 (0.00%) - all points within real experimental coverage

---

## Purpose

This report quantifies where the scalar would be detectable if it exists by computing
r = alpha_pred / alpha_max_envelope(lambda_m) for sampled model points.

## Curve Used

{'source_id': 'eotwash_prl2016_digitized', 'lambda_min': 2.99528567943e-05, 'lambda_max': 0.0009288694666433, 'fraction_covered': 1.0, 'count_covered': 31, 'count_total': 31}

**Note:** Real-only mode enabled. Synthetic curves excluded from envelope.

## Statistics

Total points computed: 31

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
| 6.677e-13 | 8.024e-20 | 8.464e-01 | 4.190e-13 | 2.955e-04 | 1.614e+11 | 6.677e-04 | 3.782e+00 | 1.108e-13 | False | eotwash_prl2016_digitized |
| 6.316e-13 | 3.061e-19 | 2.576e-01 | 6.544e-15 | 3.124e-04 | 1.527e+11 | 6.316e-04 | 3.782e+00 | 1.730e-15 | False | eotwash_prl2016_digitized |
| 2.192e-13 | 5.554e-19 | 1.225e-01 | 1.851e-16 | 9.003e-04 | 5.300e+10 | 2.192e-04 | 2.734e-01 | 6.771e-16 | False | eotwash_prl2016_digitized |
| 4.475e-12 | 5.728e-19 | 4.836e-01 | 1.236e-11 | 4.410e-05 | 1.082e+12 | 4.475e-03 | 2.937e+05 | 4.210e-17 | False | eotwash_prl2016_digitized |
| 6.689e-13 | 3.539e-19 | 2.610e-02 | 1.297e-22 | 2.950e-04 | 1.617e+11 | 6.689e-04 | 3.782e+00 | 3.429e-23 | False | eotwash_prl2016_digitized |
| 1.311e-12 | 6.011e-19 | 3.676e-02 | 1.672e-20 | 1.505e-04 | 3.171e+11 | 1.311e-03 | 6.833e+02 | 2.447e-23 | False | eotwash_prl2016_digitized |
| 2.332e-13 | 1.213e-19 | 3.030e-02 | 5.900e-24 | 8.463e-04 | 5.638e+10 | 2.332e-04 | 6.576e-01 | 8.973e-24 | False | eotwash_prl2016_digitized |
| 6.163e-12 | 3.980e-20 | 1.276e-01 | 6.776e-21 | 3.202e-05 | 1.490e+12 | 6.163e-03 | 4.059e+05 | 1.669e-26 | False | eotwash_prl2016_digitized |
| 3.012e-13 | 3.619e-22 | 2.266e-01 | 4.573e-27 | 6.552e-04 | 7.282e+10 | 3.012e-04 | 3.298e+00 | 1.387e-27 | False | eotwash_prl2016_digitized |
| 1.772e-12 | 1.209e-22 | 8.123e-01 | 1.554e-24 | 1.114e-04 | 4.284e+11 | 1.772e-03 | 1.170e+03 | 1.329e-27 | False | eotwash_prl2016_digitized |
| 7.431e-13 | 4.983e-22 | 1.183e-01 | 9.051e-29 | 2.656e-04 | 1.797e+11 | 7.431e-04 | 3.782e+00 | 2.393e-29 | False | eotwash_prl2016_digitized |
| 2.340e-12 | 2.959e-21 | 7.887e-02 | 4.407e-27 | 8.431e-05 | 5.659e+11 | 2.340e-03 | 1.194e+04 | 3.691e-31 | False | eotwash_prl2016_digitized |
| 5.953e-12 | 3.631e-19 | 1.033e-02 | 8.635e-26 | 3.315e-05 | 1.439e+12 | 5.953e-03 | 3.897e+05 | 2.216e-31 | False | eotwash_prl2016_digitized |
| 1.078e-12 | 1.113e-19 | 5.163e-03 | 2.975e-30 | 1.830e-04 | 2.608e+11 | 1.078e-03 | 1.567e+01 | 1.899e-31 | False | eotwash_prl2016_digitized |
| 5.579e-12 | 2.002e-20 | 4.216e-02 | 6.153e-26 | 3.537e-05 | 1.349e+12 | 5.579e-03 | 3.608e+05 | 1.706e-31 | False | eotwash_prl2016_digitized |
| 9.444e-13 | 1.765e-21 | 3.632e-02 | 1.131e-30 | 2.090e-04 | 2.283e+11 | 9.444e-04 | 7.768e+00 | 1.455e-31 | False | eotwash_prl2016_digitized |
| 2.632e-13 | 2.447e-22 | 6.999e-02 | 7.931e-32 | 7.496e-04 | 6.365e+10 | 2.632e-04 | 8.685e-01 | 9.132e-32 | False | eotwash_prl2016_digitized |
| 3.867e-13 | 4.870e-19 | 1.843e-03 | 2.872e-31 | 5.103e-04 | 9.351e+10 | 3.867e-04 | 3.523e+00 | 8.150e-32 | False | eotwash_prl2016_digitized |
| 2.783e-13 | 2.196e-21 | 1.352e-02 | 9.988e-34 | 7.090e-04 | 6.730e+10 | 2.783e-04 | 2.302e+00 | 4.339e-34 | False | eotwash_prl2016_digitized |
| 1.939e-12 | 4.373e-20 | 6.915e-03 | 7.343e-31 | 1.018e-04 | 4.688e+11 | 1.939e-03 | 3.019e+03 | 2.432e-34 | False | eotwash_prl2016_digitized |
| 1.406e-12 | 1.363e-21 | 2.395e-02 | 1.431e-32 | 1.404e-04 | 3.399e+11 | 1.406e-03 | 6.833e+02 | 2.094e-35 | False | eotwash_prl2016_digitized |
| 6.327e-13 | 1.390e-20 | 1.866e-03 | 2.107e-37 | 3.119e-04 | 1.530e+11 | 6.327e-04 | 3.782e+00 | 5.571e-38 | False | eotwash_prl2016_digitized |
| 2.366e-12 | 1.216e-19 | 1.668e-03 | 5.032e-34 | 8.340e-05 | 5.721e+11 | 2.366e-03 | 1.317e+04 | 3.821e-38 | False | eotwash_prl2016_digitized |
| 1.640e-12 | 2.741e-21 | 7.599e-03 | 2.412e-35 | 1.203e-04 | 3.966e+11 | 1.640e-03 | 6.833e+02 | 3.530e-38 | False | eotwash_prl2016_digitized |
| 1.499e-12 | 4.323e-21 | 3.310e-03 | 1.935e-37 | 1.316e-04 | 3.625e+11 | 1.499e-03 | 6.833e+02 | 2.832e-40 | False | eotwash_prl2016_digitized |

## Where to Look

The highest detectability ratio is r = 1.108e-13 at λ = 2.955e-04 m.

This corresponds to f_eq = 1.614e+11 Hz (equivalent frequency tag).

Across the central 80% of the λ range (4.410e-05 to 7.090e-04 m),
the average detectability ratio is r = 4.502e-15.

**Interpretation:**
- r ≪ 1: scalar is well below current experimental sensitivity
- r ≈ 0.1–1: scalar is in the detectable range; near-future experiments could see it
- r > 1: scalar is excluded by current constraints

**Frequency Translation:**
The equivalent frequency f_eq = c/(2πλ) provides a translation layer to map
fifth-force ranges onto a universal Hz axis, enabling comparison with other
MQGT-SCF constraint channels (cosmology ~10⁻¹⁸ Hz, QRNG ~Hz–GHz, Higgs ~10²⁵ Hz).
This is a unit-conversion tool, not evidence by itself.