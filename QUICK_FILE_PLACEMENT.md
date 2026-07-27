# Quick File Placement Guide

**Date:** 2026-01-21  
**Purpose:** Fast reference for placing freshly downloaded files

---

## Download the Bundle

**Bundle:** `mqgt_scf_reissue_2026-01-21_155709_UTC.zip`  
**SHA256:** `dbf3f1149ffa8ced837c60c0b4961602171bb509406876ef049c83e694097091`

**Verify after download:**
```bash
shasum -a 256 mqgt_scf_reissue_2026-01-21_155709_UTC.zip
# Should match: dbf3f1149ffa8ced837c60c0b4961602171bb509406876ef049c83e694097091
```

---

## File Placement (5 minutes)

### 1. Eöt-Wash Canonical CSV

**Source:** `eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv`  
**Destination:** `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv`

```bash
# Compare with existing (if you want to verify)
diff data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv \
     eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv

# If new version is better, replace canonical
cp eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
```

### 2. Eöt-Wash Variants

**Place in:** `data/raw/fifth_force/variants/`

```bash
# Rename and place variants
cp eotwash_prl2016_digitized_contract_READY_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_READY.csv

cp eotwash_prl2016_digitized_contract_sorted_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_sorted.csv

cp eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_monotone_conservative.csv
```

### 3. Digitization Visuals

**Place in:** `docs/dev/digitization_visuals/`

```bash
# Rename and place images
cp eotwash_digitized_compare_2026-01-21_155709_UTC.png \
   docs/dev/digitization_visuals/eotwash_raw_vs_monotone.png

cp eotwash_digitization_where_to_click_orange_2026-01-21_155709_UTC.png \
   docs/dev/digitization_visuals/eotwash_webplotdigitizer_guide.png
```

### 4. Frequency Atlas (Optional - Compare First)

**Compare with existing:**
```bash
# Compare Python script
diff scripts/frequency_atlas.py frequency_atlas_2026-01-21_155709_UTC.py

# Compare markdown
diff docs/frequency_atlas.md frequency_atlas_2026-01-21_155709_UTC.md
```

**If improvements found, update:**
```bash
cp frequency_atlas_2026-01-21_155709_UTC.py scripts/frequency_atlas.py
cp frequency_atlas_2026-01-21_155709_UTC.md docs/frequency_atlas.md
```

**Instructions:** See `docs/FREQUENCY_ATLAS_COMPARISON.md`

---

## Verify Placement

```bash
# Check files exist
ls -lh data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
ls -lh data/raw/fifth_force/variants/*.csv
ls -lh docs/dev/digitization_visuals/*.png

# Verify data integrity
make fifth-data-ledger
make test
```

---

## Next: Run the Science

Once files are placed, run the verdict:

```bash
# 1) Ingest canonical curve
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv

# 2) Big-N real-only scan (the verdict run)
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7

# 3) Check results
cat results/fifth_force/detectability_summary.md
```

---

## Make It Permanent (After Science Run)

Once you have results you want to preserve:

1. **Prepare release:**
   ```bash
   make prepare-release VERSION=v1.4.0
   ```

2. **Create GitHub Release:**
   - Upload `mqgt_scf_release_v1.4.0.zip` as release asset
   - Follow: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`

3. **Mint Zenodo DOI:**
   - Enable Zenodo integration (one-time)
   - Publish draft to get permanent DOI

**That's it - no more expiring links!**

---

**Quick reference for detailed instructions:**
- Integration: `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`
- Visuals: `docs/dev/digitization_visuals/FILE_PLACEMENT_CHECKLIST.md`
- Release: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
