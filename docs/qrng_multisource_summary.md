# Multi-Source QRNG Calibration Summary

## Purpose

Multi-source QRNG calibration pools independent bitstream sources to compute a conservative pooled `epsilon_max` bound for the QRNG_tilt constraint, enhancing credibility through cross-checks.

## Pooled Epsilon Max

**Mode A (Conservative - Default)**: `max over sources of |epsilon_hat| + CI_radius`

This method can only loosen or stay the same as more sources are added (worst-case bound for credibility).

**Mode B (Weighted - Sensitivity)**: `inverse-variance weighted average + max CI_radius`

This method can tighten with more independent data (statistical meta-analysis).

Both modes are computed when `--compute-both-modes` is used.

## Results

### Pooled Epsilon Max (Snapshot)

| Mode | Pooled ε_max | Notes |
|------|-------------|-------|
| Conservative | 0.010887 | credibility-first (worst-case bound) |
| Weighted | 0.010887 | sensitivity check (same as conservative with single source) |

**Note**: With a single source, both modes yield identical results. As additional independent sources are added, weighted mode may tighten while conservative mode can only loosen or stay the same.

### Per-Source Statistics

| Source ID | N | epsilon_hat | BF10 | 95% CI for ε |
|-----------|------|-------------|------|--------------|
| nist_beacon_v2 | 54,434 | 0.003343 | 0.018 | [-0.000857, 0.007543] |

### Interpretation

We executed the multi-source QRNG calibration instrument using a real cached NIST Beacon v2 stream (N=54,434 bits). The NIST stream was consistent with fair behavior (ε̂ ≈ 3.3×10⁻³, BF10 ≈ 0.018, and a 95% credible interval spanning zero), providing an independent cross-check under full provenance. Under the conservative pooling rule (worst-case across sources), the pooled bound was ε_max = 0.010887, which is looser than the single-source baseline ε_max = 0.002292 by design, reflecting conservative uncertainty aggregation. Under the weighted sensitivity mode (inverse-variance weighting by N), ε_max = 0.010887, identical to the conservative bound with a single source; as additional independent sources are added, the weighted mode may yield a smaller pooled estimate than the conservative bound when sources are mutually consistent. Dominance scans using the pooled bound yielded QRNG_tilt as the primary bottleneck (~80%), with collider and Higgs-invisible constraints secondary and fifth-force subdominant. Modest differences in dominance percentages relative to earlier baselines may reflect scan sampling and source composition; comparisons are most meaningful when evaluated on an identical point set. Overall, multi-source integration increases robustness and auditability, while maintaining the viability of the parameter island.

**Note on sample size**: This snapshot uses N=54,434 bits from cached NIST; conservative ε_max is expected to be loose at this N. A 400-pulse cache (≈204,800 bits) is the minimum target for stable bounds.

**Note on dominance comparison**: Dominance percentages are most meaningful when computed on an identical parameter point set (same stored sample or fixed seed). Comparisons across different scan runs may reflect sampling variation in addition to constraint changes.

See `results/qrng/multisource_epsilon_summary.md` for full details and provenance references.

## Usage

1. Fetch sources: `make qrng-fetch-nist` (or add manual CSVs to `data/raw/qrng_sources/`)
2. Generate report: `make qrng-multisource-report`
3. Re-run dominance: `make qrng-dominance-with-multisource`

The pooled epsilon_max is automatically used by dominance scans when `results/qrng/multisource_epsilon_max.json` exists.

## See Also

- `docs/qrng_multisource_start_here.md` - Quick start guide
- `docs/qrng_multisource_contract.md` - Data contract specification
- `docs/qrng_data_contract.md` - Base QRNG data contract

