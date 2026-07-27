# All-in-One Guide: Files → Science → Permanent Release

**Date:** 2026-01-21  
**Purpose:** Complete workflow from file placement to science run to permanent release

---

## Part 1: Place Files (5 minutes)

### Download and Verify Bundle

```bash
# Download: mqgt_scf_reissue_2026-01-21_155709_UTC.zip
# Verify SHA256
shasum -a 256 mqgt_scf_reissue_2026-01-21_155709_UTC.zip
# Expected: dbf3f1149ffa8ced837c60c0b4961602171bb509406876ef049c83e694097091
```

### Extract and Place Files

**Canonical Eöt-Wash CSV:**
```bash
cp eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
```

**Variants:**
```bash
cp eotwash_prl2016_digitized_contract_READY_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_READY.csv

cp eotwash_prl2016_digitized_contract_sorted_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_sorted.csv

cp eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_monotone_conservative.csv
```

**Digitization Visuals:**
```bash
cp eotwash_digitized_compare_2026-01-21_155709_UTC.png \
   docs/dev/digitization_visuals/eotwash_raw_vs_monotone.png

cp eotwash_digitization_where_to_click_orange_2026-01-21_155709_UTC.png \
   docs/dev/digitization_visuals/eotwash_webplotdigitizer_guide.png
```

**Frequency Atlas (Optional - Compare First):**
```bash
# Compare before replacing
diff scripts/frequency_atlas.py frequency_atlas_2026-01-21_155709_UTC.py
diff docs/frequency_atlas.md frequency_atlas_2026-01-21_155709_UTC.md

# If improvements, update
cp frequency_atlas_2026-01-21_155709_UTC.py scripts/frequency_atlas.py
cp frequency_atlas_2026-01-21_155709_UTC.md docs/frequency_atlas.md
```

### Verify Placement

```bash
make fifth-data-ledger
make test
```

---

## Part 2: Run the Science (10-30 minutes)

### The Verdict Run

```bash
# 1) Ingest canonical curve
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv

# 2) Big-N real-only scan (the verdict)
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7

# 3) Check results
cat results/fifth_force/detectability_summary.md
```

**What this answers:**
- Is the scalar ruled out? (excluded fraction)
- Is it near detection? (hunt band fraction)
- Where should future experiments focus? (hunt band location)

**Expected output:**
- Summary in `results/fifth_force/detectability_summary.md`
- JSON metadata in `results/fifth_force/detectability_run.json`
- Coverage report (if REAL_ONLY=1)

---

## Part 3: Make It Permanent (20 minutes)

### Step 1: Prepare Release Bundle

```bash
make prepare-release VERSION=v1.4.0
```

**Output:**
- `mqgt_scf_release_v1.4.0.zip`
- `mqgt_scf_release_v1.4.0.zip.sha256`

### Step 2: Create GitHub Release

1. Go to: https://github.com/Cbaird26/MQGT-SCF/releases/new
2. Tag: `v1.4.0`
3. Title: `v1.4.0 — Constraint Lab: File Integration and Science Results`
4. Description: Use template from `docs/publishing/RELEASE_TEMPLATE.md`
5. Attach: `mqgt_scf_release_v1.4.0.zip`
6. Publish

**Full instructions:** `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`

### Step 3: Mint Zenodo DOI

1. Wait 2-5 minutes
2. Go to: https://zenodo.org/account/settings/github/
3. Find draft for v1.4.0
4. Review metadata (from `.zenodo.json`)
5. Publish to mint DOI
6. Copy DOI: `10.5281/zenodo.XXXXXXX`

### Step 4: Update with DOI

**GitHub Release:**
- Edit release description
- Add: `### Zenodo DOI\n\nThis release is archived on Zenodo: [10.5281/zenodo.XXXXXXX](https://zenodo.org/record/XXXXXXX)`

**CITATION.cff:**
- Add: `doi: "10.5281/zenodo.XXXXXXX"`
- Commit and push

**Template:** `docs/publishing/ZENODO_DOI_UPDATE_TEMPLATE.md`

---

## Complete Workflow Summary

```bash
# === PART 1: FILES (5 min) ===
# [Download and place files - see above]

# === PART 2: SCIENCE (10-30 min) ===
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7
cat results/fifth_force/detectability_summary.md

# === PART 3: PERMANENT (20 min) ===
make prepare-release VERSION=v1.4.0
# [Create GitHub Release - manual]
# [Mint Zenodo DOI - manual]
# [Update with DOI - manual]
```

**Total time: ~35-55 minutes**

---

## Quick Reference

**File Placement:**
- Quick guide: `QUICK_FILE_PLACEMENT.md`
- Detailed: `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`

**Science Run:**
- Instructions: `SCIENCE_RUN_INSTRUCTIONS.md`
- Start here: `docs/fifth_force_start_here.md`

**Release:**
- Complete: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
- Quick: `docs/publishing/QUICK_START_RELEASE.md`

---

**Ready to go! Place files → Run science → Make permanent.**
