# Next Steps: Complete v1.4.0 Release

**Current Status:** ✅ All automated infrastructure complete  
**Time to Complete:** ~20 minutes

---

## Immediate Next Steps

### 1. Place Downloaded Files (5 minutes)

**Eöt-Wash CSV Variants:**
```bash
# Download and place in:
data/raw/fifth_force/variants/
# Files:
# - eotwash_prl2016_digitized_contract_READY.csv
# - eotwash_prl2016_digitized_contract_sorted.csv
# - eotwash_prl2016_digitized_contract_monotone_conservative.csv
```
**Instructions:** `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`

**Digitization Visuals:**
```bash
# Download, rename, and place in:
docs/dev/digitization_visuals/
# Files (after renaming):
# - eotwash_raw_vs_monotone.png (from eotwash_digitized_compare.png)
# - eotwash_webplotdigitizer_guide.png (from eotwash_digitization_where_to_click_orange.png)
```
**Instructions:** `docs/dev/digitization_visuals/FILE_PLACEMENT_CHECKLIST.md`

**Frequency Atlas:**
- Compare downloaded files with existing versions
- Update if improvements found
**Instructions:** `docs/FREQUENCY_ATLAS_COMPARISON.md`

### 2. Verify Integration (2 minutes)

```bash
make fifth-data-ledger
make test
```

### 3. Prepare Release Bundle (3 minutes)

```bash
make prepare-release VERSION=v1.4.0
```

**Output:**
- `mqgt_scf_release_v1.4.0.zip`
- `mqgt_scf_release_v1.4.0.zip.sha256`

### 4. Create GitHub Release (5 minutes)

**URL:** https://github.com/Cbaird26/MQGT-SCF/releases/new

**Details:**
- Tag: `v1.4.0`
- Title: `v1.4.0 — Constraint Lab: File Integration and Permanent Artifact Storage`
- Description: Use template from `docs/publishing/RELEASE_TEMPLATE.md`
- Attach: `mqgt_scf_release_v1.4.0.zip`

**Full Instructions:** `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`

### 5. Mint Zenodo DOI (3 minutes)

1. Wait 2-5 minutes after GitHub Release
2. Go to: https://zenodo.org/account/settings/github/
3. Find draft for v1.4.0
4. Review metadata (auto-populated from `.zenodo.json`)
5. Publish to mint DOI
6. Copy DOI: `10.5281/zenodo.XXXXXXX`

### 6. Update with DOI (2 minutes)

**Update GitHub Release:**
- Edit release description
- Add: `### Zenodo DOI\n\nThis release is archived on Zenodo: [10.5281/zenodo.XXXXXXX](https://zenodo.org/record/XXXXXXX)`

**Update CITATION.cff:**
- Add field: `doi: "10.5281/zenodo.XXXXXXX"`
- Commit and push

**Template:** `docs/publishing/ZENODO_DOI_UPDATE_TEMPLATE.md`

---

## Quick Reference

**All Instructions:**
- Complete release guide: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
- Quick start: `docs/publishing/QUICK_START_RELEASE.md`
- Integration checklist: `docs/publishing/INTEGRATION_CHECKLIST.md`

**Status Documents:**
- This file: `NEXT_STEPS.md`
- Release ready: `RELEASE_READY_v1.4.0.md`
- Implementation complete: `IMPLEMENTATION_COMPLETE.md`

---

**Ready to proceed! All infrastructure is in place.**
