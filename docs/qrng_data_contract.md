# QRNG Data Contract (Input Schema + Provenance)

This document defines the canonical schema for QRNG bitstream logs used by the MQGT-SCF
QRNG pipeline. All real-world QRNG datasets must conform to this contract before analysis.

The goal is strict reproducibility: identical inputs must produce identical outputs.

---

## Canonical Format

Preferred file format: **CSV** (UTF-8), one record per row.

### Required columns

- `timestamp` — ISO 8601 timestamp (UTC strongly recommended)
- `bit` — integer in {0, 1}
- `source_id` — short string identifying the source (e.g., `nist_beacon`, `anu_qrng`, `grok_qrng`, `lab_qrng`)

### Optional columns (recommended)

- `run_id` — identifier for a run/session/batch
- `device_id` — identifier for the device (if applicable)
- `meta` — freeform JSON string for extra metadata

---

## Validation Rules

A dataset is valid if:

1) All required columns exist.
2) `bit` is strictly 0 or 1 (no blanks, no floats, no booleans).
3) `timestamp` parses as ISO 8601.
4) `source_id` is non-empty and <= 64 chars.
5) Rows are not silently dropped; all filtering must be explicit and logged.
6) File must be stable under re-read (no nondeterministic parsing).

---

## Provenance Requirements

For each dataset analyzed, record:

- filename
- SHA256 hash
- row count
- time range
- source_id distribution
- any validation warnings/errors

This provenance record is produced automatically by `qrng_ingest.py`.

---

## Directory Convention

- `data/raw/` — raw input logs (immutable once analyzed)
- `data/processed/` — validated and normalized logs
- `results/qrng/` — analysis outputs and provenance manifests

---

## Notes

This contract enforces clarity. It does not assume any particular interpretation
of QRNG bias, consciousness effects, or causality. Those interpretations are downstream.

