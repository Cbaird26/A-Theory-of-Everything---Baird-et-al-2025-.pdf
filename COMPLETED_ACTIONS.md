# Completed Actions - v1.4.0 Release

**Date:** 2026-01-21  
**Status:** ✅ **All Automated Tasks Complete + Science Run Complete**

---

## ✅ What Was Completed

### 1. File Integration ✅

**Files Placed:**
- ✅ Canonical Eöt-Wash CSV updated: `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv`
- ✅ Variants placed (3 files):
  - `data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_READY.csv`
  - `data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_sorted.csv`
  - `data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_monotone_conservative.csv`
- ✅ Digitization visuals placed (2 files):
  - `docs/dev/digitization_visuals/eotwash_raw_vs_monotone.png`
  - `docs/dev/digitization_visuals/eotwash_webplotdigitizer_guide.png`

**Documentation Updated:**
- ✅ `docs/dev/digitization_visuals/README.md` - Marked files as present
- ✅ `data/raw/fifth_force/variants/README.md` - Marked variants as present

### 2. Code Fixes ✅

**Fixed:**
- ✅ Indentation error in `code/inference/fifth_force/detectability.py` (line 252-254)
- ✅ Unclosed parenthesis in `code/inference/fifth_force/detectability.py` (line 512)
- ✅ Release script syntax error in `scripts/prepare_release.sh`

**Verified:**
- ✅ Python syntax validated
- ✅ Scripts compile correctly

### 3. Science Run ✅

**Verdict Run Completed:**
```bash
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7
```

**Results:**
- **Total points computed:** 2,548
- **Coverage:** 100% of points within real experimental ranges
- **Excluded (r > 1.0):** 0 points (0.0%)
- **Near-detectable (r > 0.1):** 0 points (0.0%)
- **Hunt band (0.1 < r ≤ 1.0):** 0 points (0.0%)
- **All points:** r << 1 (far below detection threshold)

**Interpretation:**
- Scalar is **not ruled out** by current Eöt-Wash constraints
- Scalar is **not near detection** (all r values << 1)
- Scalar survives current constraints but is well below experimental sensitivity
- This is **not** "scalar proven" - it's "scalar not killed yet"

**Output Files:**
- `results/fifth_force/detectability_summary.md` - Complete analysis report
- `results/fifth_force/detectability_run.json` - Run metadata

### 4. Release Preparation ✅

**Release Bundle Created:**
- ✅ `mqgt_scf_release_v1.4.0.zip` (320K)
- ✅ `mqgt_scf_release_v1.4.0.zip.sha256`
- ✅ SHA256: `3621dc7d78345582285cddd7e5d560fd69fbe4ed3523125f2e8df9e8019e3091`

**Data Ledgers Generated:**
- ✅ `results/DATA_LEDGER.csv` - 17 datasets tracked
- ✅ `results/DATA_LEDGER_SHA256.txt` - SHA256 hashes for all data files

**Bundle Contents:**
- Code directory
- Data directory (including variants)
- Documentation (including digitization visuals)
- Scripts
- Tests
- Makefile
- Configuration files (.zenodo.json, CITATION.cff, etc.)

### 5. Infrastructure ✅

**Configuration:**
- ✅ `.zenodo.json` - Ready for Zenodo integration
- ✅ `CITATION.cff` - Updated to v1.4.0, date 2026-01-20

**Documentation:**
- ✅ 29 documentation files created/updated
- ✅ Complete release workflow guides
- ✅ Science run instructions
- ✅ File integration guides

---

## ⏳ Manual Steps Remaining

### Step 1: Create GitHub Release (5 minutes)

**Bundle ready:** `mqgt_scf_release_v1.4.0.zip`

**Steps:**
1. Go to: https://github.com/Cbaird26/MQGT-SCF/releases/new
2. Tag: `v1.4.0`
3. Title: `v1.4.0 — Constraint Lab: File Integration and Science Results`
4. Description: Use template from `docs/publishing/RELEASE_TEMPLATE.md`
5. Attach: `mqgt_scf_release_v1.4.0.zip`
6. Publish

**Instructions:** `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`

### Step 2: Mint Zenodo DOI (3 minutes)

1. Wait 2-5 minutes after GitHub Release
2. Go to: https://zenodo.org/account/settings/github/
3. Find draft for v1.4.0
4. Review metadata (auto-populated from `.zenodo.json`)
5. Publish to mint DOI
6. Copy DOI: `10.5281/zenodo.XXXXXXX`

### Step 3: Update with DOI (2 minutes)

**Update GitHub Release:**
- Edit release description
- Add: `### Zenodo DOI\n\nThis release is archived on Zenodo: [10.5281/zenodo.XXXXXXX](https://zenodo.org/record/XXXXXXX)`

**Update CITATION.cff:**
- Add: `doi: "10.5281/zenodo.XXXXXXX"`
- Commit and push

**Template:** `docs/publishing/ZENODO_DOI_UPDATE_TEMPLATE.md`

---

## Science Results Summary

**The Verdict:**
- ✅ Scalar **not ruled out** (0% excluded)
- ✅ Scalar **not near detection** (all r << 1)
- ✅ Scalar survives current Eöt-Wash constraints
- ✅ Well below experimental sensitivity

**Key Findings:**
- 100% coverage by real experimental data
- All 2,548 sampled points have r << 1
- Highest detectability ratio: r ≈ 2.4×10⁻⁹
- Scalar is alive but undetectable with current constraints

**Next Steps for Science:**
- Consider tighter mapping assumptions (modes B/C)
- Add more constraint channels
- Refine parameter space sampling
- Document mapping sensitivity

---

## Files Summary

**Placed:**
- 1 canonical CSV (updated)
- 3 variant CSVs
- 2 digitization visuals

**Generated:**
- 1 release bundle (320K)
- 1 SHA256 hash file
- 1 detectability summary
- 1 run metadata JSON
- 2 data ledgers

**Created/Updated:**
- 29 documentation files
- 3 code fixes
- 1 release script fix

---

## Quick Reference

**Release Bundle:**
- File: `mqgt_scf_release_v1.4.0.zip`
- Size: 320K
- SHA256: `3621dc7d78345582285cddd7e5d560fd69fbe4ed3523125f2e8df9e8019e3091`

**Science Results:**
- Summary: `results/fifth_force/detectability_summary.md`
- Metadata: `results/fifth_force/detectability_run.json`

**Next Steps:**
- GitHub Release: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
- Zenodo DOI: Same guide, Step 3

---

**All automated work complete. Science run complete. Ready for permanent release!**
