# Release v1.4.0 - Ready for Publication

**Date:** 2026-01-20  
**Status:** ✅ **All Automated Steps Complete**  
**Next:** Manual steps (GitHub Release + Zenodo DOI)

---

## ✅ Completed Automated Tasks

### Infrastructure
- ✅ `.zenodo.json` created with metadata for Zenodo integration
- ✅ `CITATION.cff` updated to version 1.4.0 and date 2026-01-20
- ✅ Release preparation script ready and tested
- ✅ Integration instructions created for all file types

### Documentation
- ✅ GitHub Release instructions created: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
- ✅ Zenodo DOI update template created: `docs/publishing/ZENODO_DOI_UPDATE_TEMPLATE.md`
- ✅ Integration checklist updated with detailed instructions
- ✅ Integration status document created: `docs/publishing/INTEGRATION_STATUS.md`
- ✅ Complete summary created: `INTEGRATION_COMPLETE_SUMMARY.md`

### File Organization
- ✅ Eöt-Wash variant integration instructions: `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`
- ✅ Digitization visual placement checklist: `docs/dev/digitization_visuals/FILE_PLACEMENT_CHECKLIST.md`
- ✅ Frequency atlas comparison guide: `docs/FREQUENCY_ATLAS_COMPARISON.md`

---

## ⏳ Manual Steps Required

### Step 1: Place Downloaded Files (5 minutes)

**Eöt-Wash CSV Variants:**
- Download files from fresh links
- Place in `data/raw/fifth_force/variants/`
- Follow: `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`

**Digitization Visuals:**
- Download PNG files from fresh links
- Rename and place in `docs/dev/digitization_visuals/`
- Follow: `docs/dev/digitization_visuals/FILE_PLACEMENT_CHECKLIST.md`

**Frequency Atlas:**
- Compare downloaded files with existing versions
- Update if improvements found
- Follow: `docs/FREQUENCY_ATLAS_COMPARISON.md`

### Step 2: Verify Integration (2 minutes)

```bash
make fifth-data-ledger
make test
```

### Step 3: Prepare Release Bundle (3 minutes)

```bash
make prepare-release VERSION=v1.4.0
```

This will create:
- `mqgt_scf_release_v1.4.0.zip` - Release bundle
- `mqgt_scf_release_v1.4.0.zip.sha256` - Hash file

### Step 4: Create GitHub Release (5 minutes)

**Follow:** `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`

**Quick Steps:**
1. Go to: https://github.com/Cbaird26/MQGT-SCF/releases/new
2. Tag: `v1.4.0`
3. Title: `v1.4.0 — Constraint Lab: File Integration and Permanent Artifact Storage`
4. Description: Use template from `docs/publishing/RELEASE_TEMPLATE.md`
5. Attach: `mqgt_scf_release_v1.4.0.zip`
6. Publish

### Step 5: Mint Zenodo DOI (3 minutes)

**Follow:** `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md` Step 3

**Quick Steps:**
1. Wait 2-5 minutes for Zenodo draft
2. Go to: https://zenodo.org/account/settings/github/
3. Find draft for v1.4.0
4. Review metadata
5. Publish to mint DOI
6. Copy DOI (format: `10.5281/zenodo.XXXXXXX`)

### Step 6: Update with DOI (2 minutes)

**Update GitHub Release:**
1. Edit release description
2. Add DOI section with link

**Update CITATION.cff:**
1. Add `doi: "10.5281/zenodo.XXXXXXX"` field
2. Commit and push

**Follow:** `docs/publishing/ZENODO_DOI_UPDATE_TEMPLATE.md`

---

## Quick Reference

**Integration Instructions:**
- Eöt-Wash: `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`
- Visuals: `docs/dev/digitization_visuals/FILE_PLACEMENT_CHECKLIST.md`
- Frequency: `docs/FREQUENCY_ATLAS_COMPARISON.md`

**Release Instructions:**
- Complete guide: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
- Quick start: `docs/publishing/QUICK_START_RELEASE.md`
- Full workflow: `docs/publishing/GITHUB_RELEASE_ZENODO_WORKFLOW.md`

**Templates:**
- Release description: `docs/publishing/RELEASE_TEMPLATE.md`
- DOI update: `docs/publishing/ZENODO_DOI_UPDATE_TEMPLATE.md`

---

## Verification Checklist

After completing all steps:

- [ ] Files placed in correct locations
- [ ] `make test` passes
- [ ] Release bundle created successfully
- [ ] GitHub Release published
- [ ] Zenodo DOI minted
- [ ] DOI added to GitHub Release
- [ ] DOI added to CITATION.cff
- [ ] All links resolve correctly

---

## Estimated Total Time

- File placement: 5 minutes
- Verification: 2 minutes
- Release preparation: 3 minutes
- GitHub Release: 5 minutes
- Zenodo DOI: 3 minutes
- DOI updates: 2 minutes

**Total: ~20 minutes**

---

**All automated infrastructure is complete. Ready for file placement and release creation!**
