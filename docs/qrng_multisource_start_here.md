# Multi-Source QRNG Calibration Quick Start

This guide explains how to use the multi-source QRNG calibration instrument to compute a pooled `epsilon_max` bound from multiple independent bitstream sources.

## Overview

The multi-source QRNG calibration pipeline:
1. Ingests multiple independent QRNG sources (from `data/raw/qrng_sources/`)
2. Validates each source against the QRNG data contract
3. Computes per-source `epsilon_hat`, BF10, and credible intervals
4. Pools results conservatively to produce a single `epsilon_max` bound
5. Integrates with dominance scans to use the pooled bound automatically

## Adding a Source

### Option 1: Fetch NIST Beacon (Recommended)
Run `make qrng-fetch-nist` to cache a real NIST Beacon source locally (raw data is gitignored).

This fetches the last 400 pulses (~204,800 bits) from NIST Beacon v2.0 and converts to contract format.

### Option 2: Manual CSV
1. Place your source CSV file in `data/raw/qrng_sources/`
2. Ensure it conforms to the QRNG data contract (see `docs/qrng_data_contract.md`):
   - Required columns: `timestamp`, `bit`, `source_id`
   - Optional columns: `run_id`, `device_id`, `meta`
3. The file will be automatically discovered during ingest

Example source CSV:
```csv
timestamp,bit,source_id
2025-01-01T00:00:00Z,0,nist_beacon
2025-01-01T00:00:01Z,1,nist_beacon
...
```

## Running the Pipeline

### Step 1: Validate Tests
```bash
make qrng-multisource-validate
```

### Step 2: Generate Report
```bash
make qrng-multisource-report
```

This will:
- Ingest all sources from `data/raw/qrng_sources/`
- Compute per-source statistics
- Compute pooled `epsilon_max`
- Write summary to `results/qrng/multisource_epsilon_summary.md`
- Write JSON to `results/qrng/multisource_epsilon_max.json`

### Step 3: Re-run Dominance with Pooled Bound
```bash
make qrng-dominance-with-multisource
```

Or manually update your dominance scan script to use `--epsilon-max=None` (it will auto-load from the pooled file).

## Output Files

- `results/qrng/multisource_epsilon_summary.md` - Human-readable summary with per-source table
- `results/qrng/multisource_epsilon_max.json` - Machine-readable pooled epsilon_max (used by dominance scans)
- `results/qrng/multisource_manifest.json` - Combined manifest listing all sources
- `results/qrng/provenance/*.json` - Per-source provenance manifests

## Pooling Method

The default pooling method is **conservative max**:
```
epsilon_max_pooled = max over sources of |epsilon_hat| + CI_radius
```

Where `CI_radius = max(|CI_low|, |CI_high|)` for each source's 95% credible interval.

This ensures the pooled bound is at least as tight as the tightest individual source bound.

## Integration with Dominance Scans

The dominance scan script (`active_constraint_labeling.py`) automatically loads the pooled `epsilon_max` if available:

- If `results/qrng/multisource_epsilon_max.json` exists, it uses that value
- Otherwise, it falls back to the default single-source `epsilon_max = 0.002292`

The scan outputs record which `epsilon_max` source was used in the summary JSON.

## Offline-First Design

All source adapters are **offline-first**:
- No network calls in adapters or tests
- Sources must be cached locally in `data/raw/qrng_sources/`
- Fetching/updating sources (e.g., from NIST Beacon) is a separate optional script
- Tests use synthetic sources created in temporary directories

This ensures reproducible builds and prevents CI failures from network issues.

## See Also

- `docs/qrng_multisource_contract.md` - Full data contract specification
- `docs/qrng_data_contract.md` - Base QRNG data contract
- `code/inference/qrng_multisource_ingest.py` - Ingest implementation
- `code/inference/qrng_pooled_epsilon.py` - Pooling implementation

