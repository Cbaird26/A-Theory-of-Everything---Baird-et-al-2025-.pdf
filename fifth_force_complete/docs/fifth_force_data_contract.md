# Fifth-Force Constraint Data Contract (Input Schema + Provenance)

This document defines the canonical schema for fifth-force constraint curves used by the MQGT-SCF
fifth-force pipeline. All constraint datasets must conform to this contract before analysis.

The goal is strict reproducibility: identical inputs must produce identical exclusion evaluations.

---

## Canonical Format

Preferred file format: **CSV** (UTF-8), one constraint point per row.

### Required columns

- `lambda_m` — range in meters (float, positive, strictly increasing)
- `alpha_max` — maximum allowed strength (dimensionless, relative to gravity, positive)
- `source_id` — short string identifying the source (e.g., `zenodo5080965_fig3`, `eotwash_2009`)

### Optional columns (recommended)

- `ref` — citation or DOI (e.g., `doi:10.5281/zenodo.5080965`)
- `note` — freeform string for additional context

---

## Validation Rules

A constraint curve is valid if:

1) All required columns exist.
2) `lambda_m` is strictly increasing (monotonic).
3) `alpha_max` is positive for all rows.
4) `source_id` is non-empty and <= 64 chars.
5) Rows are not silently dropped; all filtering must be explicit and logged.
6) File must be stable under re-read (no nondeterministic parsing).

---

## Provenance Requirements

For each constraint curve analyzed, record:

- filename
- SHA256 hash
- row count
- lambda_m range (min, max)
- source_id distribution
- any validation warnings/errors

This metadata is written to `results/fifth_force/<name>_provenance.json`.

---

## Directory Conventions

- Raw data: `data/raw/fifth_force/`
- Processed/validated: `data/processed/`
- Provenance manifests: `results/fifth_force/`

