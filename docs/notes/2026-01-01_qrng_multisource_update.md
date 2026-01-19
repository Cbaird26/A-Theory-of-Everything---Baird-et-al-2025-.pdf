# 2026-01-01 — Multi-Source QRNG Calibration Update (Non-canonical memo)

This memo summarizes the implementation and initial results of the multi-source QRNG calibration instrument.

## Implementation Status

The multi-source QRNG calibration instrument was successfully implemented with:
- Data contract extension (`docs/qrng_multisource_contract.md`)
- Source adapter infrastructure (`code/inference/qrng_sources/`)
- Multi-source ingest pipeline (`code/inference/qrng_multisource_ingest.py`)
- Pooled epsilon computation (`code/inference/qrng_pooled_epsilon.py`)
- Pipeline integration hook (auto-loads pooled epsilon_max in dominance scans)
- Regression tests (`tests/test_qrng_multisource.py`)
- Makefile targets for one-command workflows
- NIST Beacon fetcher (`scripts/fetch_nist_beacon_v2_cache.py`)

## Initial Results (Synthetic Test)

Initial test run with synthetic NIST-like source:
- **Pooled epsilon_max**: 0.025679 (Mode A - Conservative)
- **Method**: max over sources of |epsilon_hat| + CI_radius
- **Per-source (synthetic NIST)**: N=6400, epsilon_hat=0.006719, CI=[-0.005531, 0.018960], BF10=0.028

**Note**: This was a pipeline verification run with synthetic data. Real NIST Beacon data will be used when API is available.

## Interpretation

### Conservative Pooling Behavior

With conservative pooling (Mode A - max-of-CI), adding sources can only:
- **Loosen** the bound (if a new source has a wider CI)
- **Stay the same** (if all sources have similar CIs)
- **Never tighten** (by design - it's a worst-case bound)

This is expected and correct: conservative pooling prioritizes credibility over tightness.

### Weighted Pooling (Mode B - Sensitivity)

Weighted pooling (inverse-variance weighted average) can:
- **Tighten** with more independent data (statistical meta-analysis)
- Provide a sensitivity check against conservative mode

Both modes are now computed when `--compute-both-modes` is used.

## Next Steps

1. Fetch real NIST Beacon data when API is available
2. Add additional independent sources (ANU QRNG, etc.)
3. Compare conservative vs weighted pooling results
4. Re-run dominance scans with pooled epsilon_max
5. Document impact on viable parameter islands

## Key Insights

- Multi-source pooling enhances credibility through cross-checks
- Conservative mode ensures worst-case safety
- Weighted mode provides statistical tightening potential
- Both modes should be reported for robustness story

## References

- NIST Beacon: https://beacon.nist.gov/home
- QRNG Data Contract: `docs/qrng_data_contract.md`
- Multi-Source Contract: `docs/qrng_multisource_contract.md`
- Start Here Guide: `docs/qrng_multisource_start_here.md`

