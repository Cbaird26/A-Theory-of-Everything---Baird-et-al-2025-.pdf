# Frequency Atlas Update Instructions

**Date:** 2026-01-19  
**Purpose:** Instructions for updating frequency atlas files when new versions are downloaded

---

## Files to Compare

When you download fresh `frequency_atlas.py` and `frequency_atlas.md` files:

1. **Compare `frequency_atlas.py`:**
   - Existing: `scripts/frequency_atlas.py`
   - New: Downloaded `frequency_atlas.py`
   - Action: Compare functionality, update if new version has improvements

2. **Compare `frequency_atlas.md`:**
   - Existing: `docs/frequency_atlas.md`
   - New: Downloaded `frequency_atlas.md`
   - Action: Compare content, update if new version has improvements or corrections

---

## Update Process

### Step 1: Compare Files

```bash
# Compare Python script
diff scripts/frequency_atlas.py frequency_atlas.py

# Compare markdown documentation
diff docs/frequency_atlas.md frequency_atlas.md
```

### Step 2: Review Differences

**Look for:**
- New conversion functions
- Updated constants (CODATA values)
- New constraint channel mappings
- Documentation improvements
- Bug fixes

### Step 3: Update If Needed

**If new version has improvements:**

```bash
# Backup existing files
cp scripts/frequency_atlas.py scripts/frequency_atlas.py.backup
cp docs/frequency_atlas.md docs/frequency_atlas.md.backup

# Replace with new versions
cp frequency_atlas.py scripts/frequency_atlas.py
cp frequency_atlas.md docs/frequency_atlas.md

# Verify syntax
python -m py_compile scripts/frequency_atlas.py
```

### Step 4: Test Integration

```bash
# Test that frequency atlas still works
python -c "from scripts.frequency_atlas import length_to_freq_yukawa; print(length_to_freq_yukawa(1e-4))"

# Verify documentation renders correctly
# (check docs/frequency_atlas.md in browser or markdown viewer)
```

### Step 5: Update References

If files were updated, verify:
- `docs/frequency_atlas.md` is referenced correctly in other docs
- `scripts/frequency_atlas.py` is imported correctly in code
- No broken links or import errors

---

## Current Status

**Existing files:**
- `scripts/frequency_atlas.py` - Conversion functions for physical scales to frequencies (✅ Updated with improved version)
- `scripts/frequency_figure.py` - Visualization generator for frequency atlas (✅ New)
- `docs/frequency_atlas.md` - Frequency ladder documentation (preserved with detailed explanations)

**Status:** 
- ✅ Python script updated with improved structure (backward compatible)
- ✅ Figure generation script integrated
- ✅ Detailed markdown documentation preserved

---

## Related Documentation

- Frequency atlas: [`docs/frequency_atlas.md`](frequency_atlas.md)
- Mapping sensitivity: [`docs/MAPPING_SENSITIVITY.md`](MAPPING_SENSITIVITY.md)
- Claims/limits: [`docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`](CLAIMS_LIMITS_AND_FALSIFIERS.md)

---

**Update frequency atlas files only if new versions provide improvements or corrections.**
