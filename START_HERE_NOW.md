# START HERE: Files → Science → Permanent

**Status:** ✅ Everything ready  
**Time:** ~40 minutes total

---

## 🚀 Quick Start (3 Commands)

### 1. Place Files (5 min)

**Download bundle:** `mqgt_scf_reissue_2026-01-21_155709_UTC.zip`  
**SHA256:** `dbf3f1149ffa8ced837c60c0b4961602171bb509406876ef049c83e694097091`

```bash
# Canonical (if you want to update)
cp eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv

# Variants
cp eotwash_prl2016_digitized_contract_READY_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_READY.csv
cp eotwash_prl2016_digitized_contract_sorted_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/variants/eotwash_prl2016_digitized_contract_sorted.csv

# Visuals
cp eotwash_digitized_compare_2026-01-21_155709_UTC.png \
   docs/dev/digitization_visuals/eotwash_raw_vs_monotone.png
cp eotwash_digitization_where_to_click_orange_2026-01-21_155709_UTC.png \
   docs/dev/digitization_visuals/eotwash_webplotdigitizer_guide.png
```

**Detailed:** `QUICK_FILE_PLACEMENT.md`

---

### 2. Run the Science (10-30 min)

**The Verdict Run:**

```bash
# Ingest (if not already done)
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv

# Big-N real-only scan (THE VERDICT)
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7

# Check results
cat results/fifth_force/detectability_summary.md
```

**What this answers:**
- ✅ Ruled out? (excluded fraction)
- ✅ Near detection? (hunt band)
- ✅ Where to focus? (target band)

**Expected:** Small excluded (~1.3%), small hunt band (~1.8%), most space survives

**Detailed:** `SCIENCE_RUN_INSTRUCTIONS.md`

---

### 3. Make It Permanent (20 min)

**Stop the expiring link treadmill:**

```bash
# Prepare release
make prepare-release VERSION=v1.4.0
```

Then:
1. **GitHub Release:** Upload `mqgt_scf_release_v1.4.0.zip` → Get stable URL
2. **Zenodo DOI:** Enable integration → Publish draft → Get permanent DOI
3. **Update:** Add DOI to GitHub Release and `CITATION.cff`

**Detailed:** `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`

---

## 📋 Complete Workflow

```bash
# === FILES (5 min) ===
# [Download and place - see above]

# === SCIENCE (10-30 min) ===
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7
cat results/fifth_force/detectability_summary.md

# === PERMANENT (20 min) ===
make prepare-release VERSION=v1.4.0
# [GitHub Release + Zenodo DOI - follow instructions]
```

---

## 📚 Documentation Quick Links

**File Placement:**
- Quick: `QUICK_FILE_PLACEMENT.md`
- Detailed: `data/raw/fifth_force/variants/INTEGRATION_INSTRUCTIONS.md`

**Science Run:**
- Instructions: `SCIENCE_RUN_INSTRUCTIONS.md`
- Start guide: `docs/fifth_force_start_here.md`

**Release:**
- Complete: `docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md`
- Quick: `docs/publishing/QUICK_START_RELEASE.md`
- All-in-one: `ALL_IN_ONE_GUIDE.md`

---

## ✅ Current Status

**Infrastructure:**
- ✅ `.zenodo.json` ready for Zenodo
- ✅ `CITATION.cff` updated to v1.4.0
- ✅ All Makefile targets exist
- ✅ Canonical CSV already in place

**Ready for:**
- ⏳ Place fresh files (if updating)
- ⏳ Run science verdict
- ⏳ Create permanent release

---

**Everything is ready. Download files → Run science → Make permanent!**
