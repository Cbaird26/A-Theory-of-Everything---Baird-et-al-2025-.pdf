# Ready for Release v1.4.0

**Date:** 2026-01-21  
**Status:** ✅ **All Automated Infrastructure Complete**

---

## ✅ What's Complete

### Infrastructure
- ✅ `.zenodo.json` - Zenodo metadata configured
- ✅ `CITATION.cff` - Updated to v1.4.0, date 2026-01-20
- ✅ Release preparation script - `scripts/prepare_release.sh`
- ✅ Makefile targets - `fifth-ingest`, `fifth-detectability`, `prepare-release`

### Documentation
- ✅ Complete GitHub Release guide
- ✅ Zenodo DOI workflow
- ✅ File integration instructions
- ✅ Science run instructions
- ✅ Quick reference guides

### File Organization
- ✅ Directory structure ready
- ✅ Integration instructions created
- ✅ Canonical CSV already in place

---

## ⏳ What You Need to Do

### Step 1: Place Downloaded Files (5 minutes)

**Download:** `mqgt_scf_reissue_2026-01-21_155709_UTC.zip`  
**SHA256:** `dbf3f1149ffa8ced837c60c0b4961602171bb509406876ef049c83e694097091`

**Quick placement commands:**
```bash
# Extract bundle first
unzip mqgt_scf_reissue_2026-01-21_155709_UTC.zip

# Canonical (if updating)
cp eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv

# Variants
cp eotwash_prl2016_digitized_contract_READY_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_READY.csv
cp eotwash_prl2016_digitized_contract_sorted_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_sorted.csv
cp eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_monotone_conservative.csv

# Visuals
cp eotwash_digitized_compare_2026-01-21_155709_UTC.png \
   docs/dev/digitization_visuals/eotwash_raw_vs_monotone.png
cp eotwash_digitization_where_to_click_orange_2026-01-21_155709_UTC.png \
   docs/dev/digitization_visuals/eotwash_webplotdigitizer_guide.png
```

**Detailed:** See `QUICK_FILE_PLACEMENT.md`

---

### Step 2: Run the Science (10-30 minutes)

**The Verdict Run - Prove/Kill the Scalar:**

```bash
# 1) Ingest canonical curve
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv

# 2) Big-N real-only scan (THE VERDICT)
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7

# 3) Check results
cat results/fifth_force/detectability_summary.md
```

**What this answers:**
- Is the scalar ruled out? (excluded fraction)
- Is it near detection? (hunt band fraction)  
- Where should future experiments focus? (target band)

**Expected results (based on previous runs):**
- Small excluded fraction (~1.3%)
- Small hunt band (~1.8%)
- Most parameter space survives (not ruled out, not detected)

**Detailed:** See `SCIENCE_RUN_INSTRUCTIONS.md`

---

### Step 3: Make It Permanent (20 minutes)

**Stop the expiring link treadmill forever:**

```bash
# Prepare release bundle
make prepare-release VERSION=v1.4.0
```

**Then:**

1. **Create GitHub Release** (5 min)
   - Go to: https://github.com/Cbaird26/MQGT-SCF/releases/new
   - Tag: `v1.4.0`
   - Upload: `mqgt_scf_release_v1.4.0.zip`
   - Use template from `docs/publishing/RELEASE_TEMPLATE.md`
   - Publish

2. **Mint Zenodo DOI** (3 min)
   - Wait 2-5 minutes for Zenodo draft
   - Go to: https://zenodo.org/account/settings/github/
   - Find draft for v1.4.0
   - Review and publish
   - Copy DOI: `10.5281/zenodo.XXXXXXX`

3. **Update with DOI** (2 min)
   - Add DOI to GitHub Release description
   - Add DOI to `CITATION.cff`
   - Commit and push

**Detailed:** See `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`

---

## Complete Workflow

```bash
# === PART 1: FILES (5 min) ===
# [Download and place files - see Step 1 above]

# === PART 2: SCIENCE (10-30 min) ===
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7
cat results/fifth_force/detectability_summary.md

# === PART 3: PERMANENT (20 min) ===
make prepare-release VERSION=v1.4.0
# [Create GitHub Release + Zenodo DOI - see Step 3 above]
```

**Total time: ~35-55 minutes**

---

## Quick Reference

**Start Here:**
- `START_HERE_NOW.md` - 3-step quick start
- `ALL_IN_ONE_GUIDE.md` - Complete workflow

**File Placement:**
- `QUICK_FILE_PLACEMENT.md` - Fast file placement
- `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md` - Detailed CSV guide
- `docs/dev/digitization_visuals/FILE_PLACEMENT_CHECKLIST.md` - Visual placement

**Science Run:**
- `SCIENCE_RUN_INSTRUCTIONS.md` - Complete science guide
- `docs/fifth_force_start_here.md` - Fifth-force pipeline overview

**Release:**
- `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md` - Step-by-step release
- `docs/publishing/QUICK_START_RELEASE.md` - 15-minute quick start
- `docs/publishing/ZENODO_DOI_UPDATE_TEMPLATE.md` - DOI update template

---

## Verification

**Before starting:**
- [x] `.zenodo.json` exists and is valid
- [x] `CITATION.cff` updated to v1.4.0
- [x] Makefile targets ready
- [x] All documentation created

**After file placement:**
- [ ] Files in correct locations
- [ ] `make test` passes
- [ ] `make fifth-data-ledger` includes all files

**After science run:**
- [ ] `results/fifth_force/detectability_summary.md` exists
- [ ] Results make sense (check excluded/hunt band fractions)

**After release:**
- [ ] GitHub Release published
- [ ] Zenodo DOI minted
- [ ] DOI added to GitHub Release
- [ ] DOI added to `CITATION.cff`

---

## Key Points

1. **All automated work is complete** - Infrastructure ready
2. **Files need manual placement** - Follow quick guides
3. **Science run is straightforward** - Three make commands
4. **Permanent release is simple** - GitHub + Zenodo workflow documented
5. **No more expiring links** - Once on GitHub Release + Zenodo, it's permanent

---

**Everything is ready. Proceed with file placement → science run → permanent release!**
