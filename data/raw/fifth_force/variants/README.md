# Eöt-Wash CSV Variants

**Purpose:** Store alternate versions of the Eöt-Wash PRL 2016 digitized curve for reference and validation.

---

## Variant Files

**All variants are now present:**

1. **`eotwash_prl2016_digitized_contract_READY.csv`** ✅
   - Raw digitized data (direct extraction from plot)
   - May contain digitization noise and fluctuations
   - Used for comparison with processed versions

2. **`eotwash_prl2016_digitized_contract_sorted.csv`** ✅
   - Pre-sorted version (lambda_m strictly increasing)
   - Optimized for fast interpolation lookups
   - Same data as canonical, just pre-sorted

3. **`eotwash_prl2016_digitized_contract_monotone_conservative.csv`** ✅
   - Conservative running-minimum version (backup of canonical)
   - Same processing as canonical file

---

## Canonical File

**The canonical file is:** `../eotwash_prl2016_digitized_contract.csv`

This file uses the **monotone_conservative** version (running-minimum algorithm) to ensure conservative bounds and prevent fake-tight exclusions from digitization noise.

---

## Usage

- **Canonical analysis:** Use `../eotwash_prl2016_digitized_contract.csv` (monotone_conservative)
- **Validation:** Compare variants to verify processing correctness
- **Reference:** Keep variants for transparency and reproducibility

---

**Note:** Variants are for reference only. All canonical analysis should use the monotone_conservative version in the parent directory.
