# Fifth-Force Detectability Summary

**Note:** This is the raw output from the detectability analysis. For a canonical summary, see `docs/fifth_force_detectability_summary.md`. For detailed interpretation and citations, see `docs/notes/2026-01-08_scalar_detectability_hunt_band.md`.

## Purpose

This report quantifies where the scalar would be detectable if it exists by computing
r = alpha_pred / alpha_max_envelope(lambda_m) for sampled model points.

## Curve Used

Envelope across: placeholder_eotwash_style, eotwash_style_synthetic, zenodo5080965_fig3, eotwash_tighter_synthetic

Curves used: 4 curves
  - placeholder_eotwash_style: data/processed/placeholder_eotwash_style_validated.csv
  - eotwash_style_synthetic: data/processed/eotwash_style_synthetic_contract_validated.csv
  - zenodo5080965_fig3: data/processed/zenodo5080965_fig3_contract_validated.csv
  - eotwash_tighter_synthetic: data/processed/eotwash_tighter_synthetic_contract_validated.csv

**Note:** Synthetic curves are for plumbing validation only; canonical detectability conclusions require real envelope curves with full provenance.

## Statistics

Total points computed: 679

| Threshold | Count | Fraction |
|-----------|-------|----------|
| r > 1.0   |    11 | 1.6% |
| r > 0.1  |    15 | 2.2% |
| r > 0.01 |    23 | 3.4% |
| r > 0.001|    41 | 6.0% |

## Top 25 Points by Detectability Ratio (r)

These are the points closest to detection threshold:

| m_phi_GeV | theta | mu_sb/m_h | alpha_pred | lambda_m (m) | alpha_max | r | excluded | source |
|-----------|-------|-----------|------------|--------------|-----------|---|----------|--------|
| 2.216e-14 | 8.051e-19 | 7.311e-01 | 1.317e-09 | 8.906e-03 | 3.763e-13 | 3.501e+03 | True | eotwash_tighter_synthetic |
| 3.708e-14 | 7.356e-19 | 7.778e-01 | 1.505e-09 | 5.322e-03 | 8.145e-13 | 1.848e+03 | True | eotwash_tighter_synthetic |
| 1.863e-13 | 8.683e-19 | 6.489e-01 | 6.860e-10 | 1.059e-03 | 9.172e-12 | 7.480e+01 | True | eotwash_tighter_synthetic |
| 1.553e-13 | 3.122e-19 | 9.699e-01 | 2.857e-10 | 1.270e-03 | 6.983e-12 | 4.091e+01 | True | eotwash_tighter_synthetic |
| 1.187e-12 | 5.333e-19 | 9.791e-01 | 2.624e-09 | 1.663e-04 | 1.475e-10 | 1.779e+01 | True | eotwash_tighter_synthetic |
| 2.909e-13 | 2.899e-19 | 8.754e-01 | 9.360e-11 | 6.784e-04 | 1.789e-11 | 5.231e+00 | True | eotwash_tighter_synthetic |
| 2.164e-14 | 3.546e-19 | 4.806e-01 | 1.728e-12 | 9.119e-03 | 3.632e-13 | 4.758e+00 | True | eotwash_tighter_synthetic |
| 5.821e-13 | 3.124e-19 | 8.959e-01 | 1.518e-10 | 3.390e-04 | 5.067e-11 | 2.995e+00 | True | eotwash_tighter_synthetic |
| 8.003e-14 | 3.892e-19 | 5.288e-01 | 5.384e-12 | 2.466e-03 | 2.583e-12 | 2.084e+00 | True | eotwash_tighter_synthetic |
| 1.700e-13 | 9.301e-19 | 3.738e-01 | 1.095e-11 | 1.161e-03 | 7.994e-12 | 1.369e+00 | True | eotwash_tighter_synthetic |
| 1.081e-13 | 5.814e-19 | 4.256e-01 | 4.720e-12 | 1.825e-03 | 4.054e-12 | 1.164e+00 | True | eotwash_tighter_synthetic |
| 7.721e-14 | 1.733e-19 | 7.106e-01 | 2.249e-12 | 2.556e-03 | 2.447e-12 | 9.187e-01 | False | eotwash_tighter_synthetic |
| 4.146e-13 | 2.027e-19 | 8.954e-01 | 2.679e-11 | 4.759e-04 | 3.046e-11 | 8.795e-01 | False | eotwash_tighter_synthetic |
| 2.925e-14 | 2.288e-19 | 5.013e-01 | 4.194e-13 | 6.746e-03 | 5.708e-13 | 7.348e-01 | False | eotwash_tighter_synthetic |
| 5.402e-13 | 2.815e-19 | 7.056e-01 | 1.481e-11 | 3.653e-04 | 4.529e-11 | 3.271e-01 | False | eotwash_tighter_synthetic |
| 3.506e-14 | 8.826e-20 | 6.355e-01 | 6.198e-14 | 5.629e-03 | 7.489e-13 | 8.276e-02 | False | eotwash_tighter_synthetic |
| 3.784e-14 | 3.097e-19 | 3.356e-01 | 5.681e-14 | 5.215e-03 | 8.397e-13 | 6.765e-02 | False | eotwash_tighter_synthetic |
| 8.298e-13 | 5.665e-19 | 4.108e-01 | 3.207e-12 | 2.378e-04 | 8.624e-11 | 3.719e-02 | False | eotwash_tighter_synthetic |
| 3.228e-14 | 1.069e-19 | 4.942e-01 | 1.786e-14 | 6.114e-03 | 6.615e-13 | 2.701e-02 | False | eotwash_tighter_synthetic |
| 1.431e-12 | 2.251e-19 | 6.821e-01 | 4.623e-12 | 1.379e-04 | 1.954e-10 | 2.366e-02 | False | eotwash_tighter_synthetic |
| 5.711e-14 | 1.381e-19 | 4.745e-01 | 3.586e-14 | 3.455e-03 | 1.557e-12 | 2.303e-02 | False | eotwash_tighter_synthetic |
| 3.155e-14 | 1.944e-19 | 3.557e-01 | 1.405e-14 | 6.254e-03 | 6.394e-13 | 2.197e-02 | False | eotwash_tighter_synthetic |
| 1.063e-12 | 1.666e-19 | 6.923e-01 | 1.561e-12 | 1.856e-04 | 1.250e-10 | 1.248e-02 | False | eotwash_tighter_synthetic |
| 1.437e-12 | 8.563e-20 | 9.689e-01 | 1.603e-12 | 1.373e-04 | 1.965e-10 | 8.158e-03 | False | eotwash_tighter_synthetic |
| 6.677e-13 | 8.024e-20 | 8.464e-01 | 4.190e-13 | 2.955e-04 | 6.224e-11 | 6.732e-03 | False | eotwash_tighter_synthetic |

## Where to Look

The highest detectability ratio is r = 3.501e+03 at λ = 8.906e-03 m.

Across the central 80% of the λ range (1.509e-04 to 6.352e-03 m),
the average detectability ratio is r = 3.678e+00.

**Interpretation:**
- r ≪ 1: scalar is well below current experimental sensitivity
- r ≈ 0.1–1: scalar is in the detectable range; near-future experiments could see it
- r > 1: scalar is excluded by current constraints

---

## Related Documents

- **Canonical summary:** `docs/fifth_force_detectability_summary.md` (empirical results, reviewer-safe)
- **Detailed memo:** `docs/notes/2026-01-08_scalar_detectability_hunt_band.md` (narrative, interpretation, citations)
- **Implementation:** `code/inference/fifth_force/detectability.py` (detectability computation code)
- **Fifth-force summary:** `docs/fifth_force_summary.md` (constraint dominance analysis)