# File Integration Checklist

**Date:** 2026-01-19  
**Purpose:** Checklist for integrating downloaded files into repository

---

## Eöt-Wash CSV Files

### Canonical File (Already in Repo)
- [x] `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv` - Uses monotone_conservative version

### Variants to Add (When Downloaded)
- [ ] `data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_READY.csv` - Raw digitized
- [ ] `data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_sorted.csv` - Pre-sorted version
- [ ] `data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_monotone_conservative.csv` - Backup of canonical

**Note:** If new `monotone_conservative` version differs from existing, compare and update canonical if new version is more conservative.

---

## Digitization Visuals

### Files to Add (When Downloaded)
- [ ] `docs/dev/digitization_visuals/eotwash_raw_vs_monotone.png`
  - Download from: `eotwash_digitized_compare.png`
  - Verify: Shows blue (raw) vs. orange (monotone) curves

- [ ] `docs/dev/digitization_visuals/eotwash_webplotdigitizer_guide.png`
  - Download from: `eotwash_digitization_where_to_click_orange.png`
  - Verify: Shows WebPlotDigitizer with orange guidance overlays

**After adding:**
- [ ] Update `docs/dev/digitization_visuals/README.md` to remove "To Be Added" notes
- [ ] Verify images display in `docs/dev/eotwash_digitization_guide.md`
- [ ] Test image links in documentation

---

## Frequency Atlas Files

### Comparison Required
- [ ] Compare `frequency_atlas.py` (downloaded) with `scripts/frequency_atlas.py` (existing)
- [ ] Compare `frequency_atlas.md` (downloaded) with `docs/frequency_atlas.md` (existing)

### Update Decision
- [ ] If new versions have improvements → Update existing files
- [ ] If versions are identical → Skip update
- [ ] If new versions have issues → Keep existing files

**See:** [`docs/FREQUENCY_ATLAS_UPDATE.md`](../FREQUENCY_ATLAS_UPDATE.md) for detailed instructions

---

## Release Bundle

### Create Release Bundle (When Ready)
- [ ] Run `make prepare-release VERSION=v1.4.0`
- [ ] Verify bundle includes all necessary files
- [ ] Check bundle size (< 50GB for Zenodo)
- [ ] Generate SHA256 hash of bundle

---

## Documentation Updates

### Already Completed
- [x] `.zenodo.json` created
- [x] GitHub Release workflow documentation created
- [x] Release template created
- [x] Citation update instructions created
- [x] Release preparation script created
- [x] `DATA_GROUND_TRUTH.md` updated
- [x] `data/raw/fifth_force/README.md` updated
- [x] `Makefile` updated with `prepare-release` target

### After Adding Files
- [ ] Verify all image references work
- [ ] Test all documentation links
- [ ] Run `make test` to ensure nothing broke
- [ ] Update this checklist to mark items complete

---

## Verification Steps

After integrating all files:

1. **Test Reproducibility:**
   ```bash
   make install
   make test
   make reproduce
   ```

2. **Verify Data Integrity:**
   ```bash
   make fifth-data-ledger
   make fifth-sha256-ledger
   ```

3. **Check Documentation:**
   - All image links work
   - All cross-references valid
   - No broken links

4. **Prepare Release:**
   ```bash
   make prepare-release VERSION=v1.4.0
   ```

---

## Next Steps After Integration

1. **Create GitHub Release:**
   - Tag: `v1.4.0`
   - Upload release bundle
   - Use release template for description

2. **Mint Zenodo DOI:**
   - Wait for Zenodo draft (auto-created from GitHub Release)
   - Review and publish Zenodo record
   - Copy DOI

3. **Update CITATION.cff:**
   - Add DOI to `CITATION.cff`
   - Update version and date
   - Commit and push

4. **Update GitHub Release:**
   - Add Zenodo DOI to release description
   - Update release with DOI link

---

**This checklist ensures all downloaded files are properly integrated and documented.**
