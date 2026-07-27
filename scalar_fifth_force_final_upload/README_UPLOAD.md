# Scalar Fifth Force Final Upload Package

**Package Name:** `scalar_fifth_force_final_upload`  
**Created:** 2026-01-08  
**Status:** Ready for upload - includes all updates with real curve path specifications

---

## What's In This Package

Complete package of all scalar fifth-force constraint and detectability analysis files.

**Key Files:**
- ✅ All documentation (canonical summaries updated with real curve results)
- ✅ All Python code
- ✅ All data files (raw + processed)
- ✅ All results
- ✅ Automation scripts (updated with correct paths)
- ✅ **EXACT_CSV_PATH.txt** - Shows exact path needed for digitized CSV

---

## Exact CSV Path Required

**For the digitized Eöt-Wash curve CSV:**

If running from REPO ROOT:
```
data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
```

If placing in PACKAGE FOLDER:
```
data_raw/eotwash_prl2016_digitized_contract.csv
```

See `EXACT_CSV_PATH.txt` for details.

---

## Quick Start

1. **Add digitized CSV:** Place at path shown in `EXACT_CSV_PATH.txt`
2. **Run automation:** `./process_real_eotwash_curve.sh` (from repo root)
3. **Or manually:**
   ```bash
   make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
   make fifth-detectability SEED=42 NPTS=2000
   ```
4. **Read results:** `cat results/fifth_force/detectability_summary.md`

---

## Canonical Statement

**Scalar fifth force not detected; not ruled out; maximally testable at λ ≈ 0.5 mm (sub-mm to mm: 10⁻⁴ to 10⁻³ m) under current experimental constraints.**

---

## Status

- ✅ Real curve path specifications added
- ✅ Scripts updated with correct paths
- ✅ All documentation updated
- ✅ Ready for upload

---

**This is the final upload-ready package with all path specifications included.**

---

## CSV Sanity Check

Before ingesting your digitized CSV, run the sanity check:

```bash
./check_digitized_csv.sh data_raw/eotwash_prl2016_digitized_contract.csv
```

This will verify:
- ✅ Header format
- ✅ Lambda values in meters (mm-cm range: ~10^-4 to 10^-2 m)
- ✅ Alpha values dimensionless and positive
- ✅ Source ID correct
- ✅ No negative values

Or just paste the first ~10 lines here and I'll check it instantly!
