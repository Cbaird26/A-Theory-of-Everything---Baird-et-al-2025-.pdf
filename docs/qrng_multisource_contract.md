# QRNG Multi-Source Data Contract

This document extends the base QRNG data contract (`docs/qrng_data_contract.md`) to define the schema and requirements for multi-source calibration.

## Purpose

Multi-source QRNG calibration pools independent bitstream sources to compute a conservative pooled `epsilon_max` bound for the QRNG_tilt constraint. This strengthens the constraint by validating it across multiple independent sources.

## Canonical Schema

Each source must conform to the base QRNG data contract (see `docs/qrng_data_contract.md`):

### Required columns
- `timestamp` — ISO 8601 timestamp (UTC strongly recommended)
- `bit` — integer in {0, 1}
- `source_id` — short string identifying the source (e.g., `nist_beacon`, `anu_qrng`, `local_csv_biased`)

### Optional columns
- `run_id` — identifier for a run/session/batch
- `device_id` — identifier for the device (if applicable)
- `meta` — freeform JSON string for extra metadata

## Source Independence Requirements

**Critical**: Sources must be **independent** to avoid correlated artifacts:

1. Different physical devices or generators
2. Different time periods (non-overlapping or widely separated)
3. Different protocols/algorithms (if applicable)
4. Documented in provenance manifests

Sources that share hardware, timing, or protocols may produce correlated biases and should not be pooled without explicit justification.

## Offline-First Rule

**CI/Tests Safety**: All source adapters must be **offline-first**:

- No network calls in adapters or tests
- Sources are cached locally in `data/raw/qrng_sources/`
- Fetching/updating sources is a separate optional script (not part of CI)
- Tests use synthetic sources created in temporary directories

This ensures reproducible builds and prevents CI failures from network issues.

## Directory Convention

- `data/raw/qrng_sources/` — raw source CSV files (one per source)
- `data/processed/qrng_sources/` — validated and normalized CSVs per source
- `results/qrng/provenance/` — provenance manifests per source
- `results/qrng/multisource_manifest.json` — combined manifest listing all sources

## Provenance Requirements

Each source must have:
- SHA256 hash
- Row count
- Time range
- Source ID
- Any validation warnings

The combined manifest (`multisource_manifest.json`) lists all included sources with their hashes, row counts, and metadata for full auditability.

## Pooling Rules

The pooled `epsilon_max` is computed conservatively:

**Default (Option A)**: `max over sources of |epsilon_hat| + CI_radius`

Where `CI_radius = max(|CI_low|, |CI_high|)` for each source's 95% credible interval.

This ensures the pooled bound is at least as tight as the tightest individual source bound.

Alternative pooling methods (e.g., weighted pooling) may be documented but the conservative max is the default for scientific rigor.

## Notes

This contract extends the base QRNG contract without changing its core validation rules. All sources must pass the base contract validation before pooling.
