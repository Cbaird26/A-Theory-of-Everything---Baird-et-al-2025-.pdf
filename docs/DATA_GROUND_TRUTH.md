# Data Ground Truth Protocol

**Date:** 2026-01-19  
**Repository:** MQGT-SCF  
**Status:** **Canonical (Ground Truth Protocol)** ⭐

---

## Purpose

This document specifies the canonical dataset paths, variant labeling convention, ledger generation protocol, and provenance tracking explanation for MQGT-SCF constraint data.

---

## Canonical Datasets

### Fifth-Force Constraints

**Canonical Raw Input:**
- `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv` ✅ **CANONICAL**
  - **Source:** Eöt-Wash Group / Tan et al. PRL 116, 131102 (2016)
  - **Type:** Digitized from published plot (monotone_conservative version)
  - **Range:** Millimeter-centimeter scale (λ ≈ 3×10⁻⁵ → 9×10⁻⁴ m, 29 points)
  - **Purpose:** Primary real experimental constraint for mm-cm hunt band analysis
  - **Status:** ✅ **Completed** - Uses monotone_conservative processing (running-minimum algorithm)
  - **Processing:** Conservative smoothing prevents fake-tight exclusions from digitization noise
  - **Variants:** See `data/raw/fifth_force/variants/` for alternate versions (READY, sorted)
  - **Digitization Visuals:** See [`docs/dev/digitization_visuals/`](dev/digitization_visuals/) for process documentation

**Real Experimental Curves:**
- `data/raw/fifth_force/zenodo5080965_fig3_contract.csv`
  - **Source:** Heacock & Huber (2021), Zenodo DOI: 10.5281/zenodo.5080965
  - **Type:** Machine-readable experimental data
  - **Range:** Picometer-nanometer scale (λ ≈ 10⁻¹² → 10⁻⁹ m)
  - **Ingestion:** Automated via `code/inference/fifth_force/importers/zenodo5080965_fig3.py`

- `data/raw/fifth_force/kapner_prl2007_digitized_contract.csv` ⏳ **To be digitized**
  - **Source:** Kapner et al., "Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale", PRL 98, 021101 (2007)
  - **arXiv:** hep-ph/0611184
  - **Type:** Digitized from published plot (Figure 6)
  - **Range:** 55 μm to 9.53 mm (extends mm-cm coverage)
  - **Purpose:** Expand real-only envelope to mm-cm region
  - **Status:** ⏳ **To be digitized** - See `docs/dev/mm_cm_constraints_digitization_guide.md`
  - **Ingestion:** Manual digitization → `make fifth-ingest-kapner`

- `data/raw/fifth_force/lee_arxiv2020_digitized_contract.csv` ⏳ **To be digitized**
  - **Source:** Lee et al., "Test of the Gravitational Inverse-Square Law at Millimeter Ranges", PRL 124, 101101 (2020)
  - **arXiv:** 2002.11761
  - **Type:** Digitized from published plot (Figure 5, bottom panel)
  - **Range:** 52 μm to 3.0 mm (complements Kapner coverage)
  - **Purpose:** Additional mm-scale constraint for envelope merging
  - **Status:** ⏳ **To be digitized** - See `docs/dev/mm_cm_constraints_digitization_guide.md`
  - **Ingestion:** Manual digitization → `make fifth-ingest-lee`

### QRNG Constraints

**Canonical Raw Input:**
- `data/raw/qrng_sources/nist_beacon_v2_last400.csv`
  - **Source:** NIST Beacon v2.0 (last 400 pulses)
  - **Type:** Public quantum random number generator data
  - **Format:** Binary bitstream (converted to CSV)
  - **Ingestion:** Via `make qrng-fetch-nist` or `scripts/fetch_nist_beacon_v2_cache.py`

---

## Variant Labeling Convention

### Explicit Variant Names

**Variants are stored in dedicated subdirectories and explicitly labeled:**

- **Sorted variants:** `data/raw/fifth_force/variants/*_sorted.csv`
  - Purpose: Pre-sorted by lambda_m for interpolation efficiency
  - Label: Filename contains `_sorted`
  - Usage: Optimized for fast lookups

- **Monotone conservative:** `data/raw/fifth_force/variants/*_monotone_conservative.csv`
  - Purpose: Enforced monotonicity for conservative envelope
  - Label: Filename contains `_monotone_conservative`
  - Usage: Prevents accidental "fake-tight" exclusions from digitization artifacts

### Synthetic/Placeholder Labeling

**Synthetic curves are explicitly labeled in filename:**
- Filenames contain `synthetic` or `placeholder`
- Examples: `placeholder_eotwash_style.csv`, `eotwash_style_synthetic_contract.csv`
- **Purpose:** Pipeline testing and validation only
- **Status:** Excluded from canonical analysis via `--real-only` mode

**Real curves are explicitly labeled:**
- Filenames contain source identifiers: `zenodo5080965`, `eotwash_prl2016`, `bennu_osiris_rex`, `kapner_prl2007`, `lee_arxiv2020`
- **Purpose:** Canonical experimental constraints
- **Status:** Used in real-only mode and canonical analysis

---

## Ledger Generation Protocol

### Dataset Ledger

**Generate via:**
```bash
make fifth-data-ledger
```

**Output:** `results/DATA_LEDGER.csv`

**Format:**
```csv
Dataset File,Source,Description,Version,Last Modified,SHA256
data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv,PRL 116 131102 (2016),Canonical Eöt-Wash constraints,1.0,2025-12-28,<SHA256_HASH>
```

**Purpose:**
- Lists all canonical datasets with sources and descriptions
- Provides audit trail for data provenance
- Links raw data to scientific references

### SHA256 Ledger

**Generate via:**
```bash
make fifth-sha256-ledger
```

**Output:** `results/DATA_LEDGER_SHA256.txt`

**Format:**
```
<SHA256_HASH>  data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
<SHA256_HASH>  data/processed/eotwash_prl2016_digitized_contract_validated.csv
```

**Purpose:**
- Provides cryptographic hashes for all data files
- Enables verification of data integrity
- Prevents undetected data manipulation

### Provenance JSON Manifests

**Generated automatically during ingestion:**
- Location: `results/fifth_force/<source_id>_provenance.json`
- Format: JSON with SHA256, row counts, ranges, scientific reference
- Example: `results/fifth_force/zenodo5080965_fig3_provenance.json`

**Contents:**
```json
{
  "source_id": "zenodo5080965_fig3",
  "sha256": "<SHA256_HASH>",
  "row_count": 29,
  "lambda_min": 1e-12,
  "lambda_max": 1e-9,
  "ref": "Heacock & Huber (2021), Zenodo DOI: 10.5281/zenodo.5080965",
  "timestamp": "2026-01-19T12:00:00Z",
  "git_commit": "<COMMIT_HASH>"
}
```

---

## Provenance Tracking Explanation

### Why Provenance Matters

Provenance tracking ensures:
- **Data integrity:** Cryptographic hashes prevent undetected modification
- **Reproducibility:** Exact dataset versions can be identified and recreated
- **Auditability:** Full lineage from raw data to processed results
- **Credibility:** Clear links to scientific sources enable verification

### Provenance Chain

1. **Raw Data:** Original experimental data or digitized plots
   - Location: `data/raw/`
   - Metadata: Source identifier, scientific reference

2. **Ingestion:** Validation and normalization
   - Script: `code/inference/fifth_force/ingest.py`
   - Validation: Schema checks, monotonicity enforcement
   - Output: `data/processed/<source_id>_validated.csv`

3. **Provenance Manifest:** Automatic generation during ingestion
   - Location: `results/fifth_force/<source_id>_provenance.json`
   - Contents: SHA256, metadata, scientific reference

4. **Ledger Generation:** Periodic snapshots
   - Script: `scripts/create_data_ledger.py`
   - Output: `results/DATA_LEDGER.csv`
   - Purpose: Human-readable audit trail

5. **SHA256 Ledger:** Cryptographic verification
   - Script: `scripts/create_sha256_ledger.sh`
   - Output: `results/DATA_LEDGER_SHA256.txt`
   - Purpose: Integrity verification

### Real-Only Mode Implications

In `--real-only` mode:
- Only real experimental curves are used
- Synthetic/placeholder curves are excluded
- Coverage reporting shows fraction of sampled points within real curve λ ranges
- Points outside real coverage are **not** marked as "excluded"

**This prevents overinterpretation of results outside experimental data coverage.**

---

## Data Contract Requirements

All constraint curves must conform to the fifth-force data contract:

**Schema:** See [`docs/fifth_force_data_contract.md`](fifth_force_data_contract.md)

**Required columns:**
- `lambda_m`: Interaction range in meters (positive, strictly increasing)
- `alpha_max`: Maximum allowed coupling strength (dimensionless, positive)
- `source_id`: Unique identifier string (consistent across rows)

**Validation:** Enforced by `code/inference/fifth_force/ingest.py`

**Provenance:** Generated automatically during ingestion

---

## Usage

### Ingest Canonical Dataset

```bash
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
```

**Outputs:**
- `data/processed/eotwash_prl2016_digitized_contract_validated.csv`
- `results/fifth_force/eotwash_prl2016_digitized_contract_provenance.json`

### Generate Ledgers

```bash
make fifth-data-ledger
make fifth-sha256-ledger
```

**Outputs:**
- `results/DATA_LEDGER.csv`
- `results/DATA_LEDGER_SHA256.txt`

### Verify Data Integrity

```bash
# Check SHA256 hash matches ledger
sha256sum data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
grep eotwash_prl2016_digitized_contract.csv results/DATA_LEDGER_SHA256.txt
```

---

## File Naming Convention Summary

| Prefix | Type | Example | Usage |
|--------|------|---------|-------|
| `zenodo*` | Real (automated) | `zenodo5080965_fig3_contract.csv` | Canonical |
| `*_prl2016_digitized*` | Real (digitized) | `eotwash_prl2016_digitized_contract.csv` | Canonical |
| `kapner_prl2007*` | Real (digitized) | `kapner_prl2007_digitized_contract.csv` | Canonical (when digitized) |
| `lee_arxiv2020*` | Real (digitized) | `lee_arxiv2020_digitized_contract.csv` | Canonical (when digitized) |
| `bennu_*` | Real (automated) | `bennu_osiris_rex_2024_contract.csv` | Canonical |
| `*_synthetic*` | Synthetic | `eotwash_style_synthetic_contract.csv` | Validation only |
| `placeholder_*` | Synthetic | `placeholder_eotwash_style.csv` | Validation only |
| `*_sorted.csv` | Variant | `*_sorted.csv` | Optimization |
| `*_monotone_*.csv` | Variant | `*_monotone_conservative.csv` | Conservative envelope |

---

## References

- Data contract: [`docs/fifth_force_data_contract.md`](fifth_force_data_contract.md)
- Fifth-force start guide: [`docs/fifth_force_start_here.md`](fifth_force_start_here.md)
- Real vs. synthetic guardrails: [`docs/REAL_VS_SYNTHETIC_GUARDRAILS.md`](REAL_VS_SYNTHETIC_GUARDRAILS.md)
- Raw data directory README: [`data/raw/fifth_force/README.md`](../data/raw/fifth_force/README.md)
- Digitization visuals: [`docs/dev/digitization_visuals/`](dev/digitization_visuals/)
- Digitization guide: [`docs/dev/eotwash_digitization_guide.md`](dev/eotwash_digitization_guide.md)
- mm-cm constraints digitization: [`docs/dev/mm_cm_constraints_digitization_guide.md`](dev/mm_cm_constraints_digitization_guide.md)

---

**This protocol ensures all data inputs are frozen, auditable, and traceable to scientific sources.**
