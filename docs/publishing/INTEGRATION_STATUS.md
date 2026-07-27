# File Integration Status

**Date:** 2026-01-20  
**Status:** Infrastructure Complete, Files Ready for Placement

---

## Completed Infrastructure

### ✅ Zenodo Integration
- `.zenodo.json` created with metadata for automatic DOI minting
- GitHub Release workflow documentation complete
- Release preparation script ready

### ✅ File Organization Structure
- `data/raw/fifth_force/variants/` directory exists with README
- `docs/dev/digitization_visuals/` directory exists with README
- Integration instructions created for all file types

### ✅ Documentation
- Integration checklist updated with detailed instructions
- GitHub Release instructions created for v1.4.0
- Zenodo DOI update template created
- Frequency atlas comparison guide created

### ✅ Release Preparation
- `CITATION.cff` updated to version 1.4.0 and date 2026-01-20
- Release preparation script tested and ready
- Makefile target `prepare-release` available

---

## Files Ready for Placement

### Eöt-Wash CSV Variants
**Location:** `data/raw/fifth_force/variants/`  
**Instructions:** `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`

**Files to add:**
- `eotwash_prl2016_digitized_contract_READY.csv`
- `eotwash_prl2016_digitized_contract_sorted.csv`
- `eotwash_prl2016_digitized_contract_monotone_conservative.csv`

**Status:** ⏳ Ready for file placement

### Digitization Visuals
**Location:** `docs/dev/digitization_visuals/`  
**Instructions:** `docs/dev/digitization_visuals/FILE_PLACEMENT_CHECKLIST.md`

**Files to add:**
- `eotwash_raw_vs_monotone.png` (rename from `eotwash_digitized_compare.png`)
- `eotwash_webplotdigitizer_guide.png` (rename from `eotwash_digitization_where_to_click_orange.png`)

**Status:** ⏳ Ready for file placement

### Frequency Atlas
**Location:** Compare with existing files  
**Instructions:** `docs/FREQUENCY_ATLAS_COMPARISON.md`

**Action:** Compare downloaded files with existing versions  
**Status:** ⏳ Ready for comparison

---

## Next Steps

### Immediate (File Placement)
1. Download files from fresh links
2. Place Eöt-Wash variants in `data/raw/fifth_force/variants/`
3. Place digitization visuals in `docs/dev/digitization_visuals/` (with correct names)
4. Compare frequency atlas files and update if needed

### After File Placement
1. Run `make fifth-data-ledger` to verify files are tracked
2. Run `make test` to ensure nothing broke
3. Update README files to mark files as present

### Release Creation
1. Run `make prepare-release VERSION=v1.4.0`
2. Follow `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
3. Create GitHub Release
4. Mint Zenodo DOI
5. Update `CITATION.cff` with DOI

---

## Quick Reference

**Integration Instructions:**
- Eöt-Wash variants: `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`
- Digitization visuals: `docs/dev/digitization_visuals/FILE_PLACEMENT_CHECKLIST.md`
- Frequency atlas: `docs/FREQUENCY_ATLAS_COMPARISON.md`

**Release Instructions:**
- GitHub Release: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
- Zenodo DOI update: `docs/publishing/ZENODO_DOI_UPDATE_TEMPLATE.md`

**Checklists:**
- Integration: `docs/publishing/INTEGRATION_CHECKLIST.md`
- This status: `docs/publishing/INTEGRATION_STATUS.md`

---

**All infrastructure is complete. Ready for file placement and release creation.**
