# Eöt-Wash CSV Variants - Integration Instructions

**Status:** Ready for file placement  
**Action Required:** Download files and place in this directory

---

## Files to Add

When you download the fresh files, place them here with these exact names:

1. **`eotwash_prl2016_digitized_contract_READY.csv`**
   - Source: `eotwash_prl2016_digitized_contract_READY.csv` from downloads
   - Description: Raw digitized data (direct extraction from plot)
   - May contain digitization noise and fluctuations

2. **`eotwash_prl2016_digitized_contract_sorted.csv`**
   - Source: `eotwash_prl2016_digitized_contract_sorted.csv` from downloads
   - Description: Pre-sorted version (lambda_m strictly increasing)
   - Optimized for fast interpolation lookups

3. **`eotwash_prl2016_digitized_contract_monotone_conservative.csv`**
   - Source: `eotwash_prl2016_digitized_contract_monotone_conservative.csv` from downloads
   - Description: Conservative running-minimum version (backup of canonical)
   - Same processing as canonical file

---

## Canonical File Comparison

**Before placing variants, compare the new canonical file:**

1. Download `eotwash_prl2016_digitized_contract.csv` from fresh links
2. Compare with existing: `../eotwash_prl2016_digitized_contract.csv`
3. Decision:
   - If new version is more conservative (tighter bounds) → Replace canonical
   - If identical or less conservative → Keep existing canonical
   - Always preserve old version in `variants/` for transparency

---

## CSV Format Verification

All CSV files must have these columns:
- `lambda_m` - Range in meters (float, positive, strictly increasing)
- `alpha_max` - Maximum allowed strength (dimensionless, positive)
- `source_id` - Use: `eotwash_prl2016_digitized`
- `ref` - Paper citation (optional but recommended)

---

## After Adding Files

1. Verify CSV format: Check columns and data types
2. Update `README.md` in this directory to mark files as present
3. Run data ledger: `make fifth-data-ledger` (should include all variants)
4. Verify in repository: All files should appear in git status

---

**Note:** The canonical file uses monotone_conservative processing (running-minimum algorithm) to ensure conservative bounds and prevent fake-tight exclusions from digitization noise.
