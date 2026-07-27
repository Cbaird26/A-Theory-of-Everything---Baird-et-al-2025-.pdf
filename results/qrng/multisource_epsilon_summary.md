# Multi-Source QRNG Epsilon Max Summary

**Pooled epsilon_max (Mode A - Conservative)**: `0.010887`
**Method**: max over sources of |epsilon_hat| + CI_radius
**Pooled epsilon_max (Mode B - Weighted)**: `0.010887`

**Sensitivity Analysis**: Both pooling modes computed for comparison.
- Mode A (Conservative): max over sources of |epsilon_hat| + CI_radius (default, credibility-first)
- Mode B (Weighted): inverse-variance weighted average + max CI_radius (sensitivity check)

**Prior scale**: 1.0
**CI mass**: 0.95
**Number of sources**: 1

## Per-Source Results

| Source ID | N | epsilon_hat | BF10 | 95% CI for ε | epsilon_bound |
|-----------|------|-------------|------|--------------|---------------|
| nist_beacon_v2 | 54434 | 0.003343 | 0.018 | [-0.000857, 0.007543] | 0.010887 |

## Provenance

- Combined manifest: `results/qrng/multisource_manifest.json`
- Pooled epsilon_max JSON: `results/qrng/multisource_epsilon_max.json`

## Notes

- epsilon_bound = |epsilon_hat| + CI_radius (where CI_radius = max(|CI_low|, |CI_high|))
- Mode A (Conservative): Can only loosen or stay same as more sources are added (worst-case bound)
- Mode B (Weighted): Can tighten with more independent data (statistical meta-analysis)
- Conservative mode is default for scientific rigor; weighted mode provided for sensitivity analysis