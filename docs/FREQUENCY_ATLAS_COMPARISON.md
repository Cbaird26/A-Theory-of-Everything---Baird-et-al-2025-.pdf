# Frequency Atlas Comparison Guide

**Purpose:** Instructions for comparing downloaded frequency atlas files with existing versions

---

## Files to Compare

**Downloaded Files (from fresh links):**
- `frequency_atlas.py` - Python script
- `frequency_atlas.md` - Markdown documentation

**Existing Files (in repository):**
- `scripts/frequency_atlas.py` - Current Python script (already updated with improvements)
- `docs/frequency_atlas.md` - Current markdown documentation (detailed version)

---

## Comparison Process

### Step 1: Python Script Comparison

**Command:**
```bash
diff scripts/frequency_atlas.py frequency_atlas.py
```

**What to look for:**
- New functions or features
- Improved code structure
- Bug fixes
- Better documentation strings
- New conversion functions

**Note:** The existing `scripts/frequency_atlas.py` already includes:
- Backward compatibility (original function names preserved)
- Modern Python features (dataclasses, type hints)
- Markdown/CSV output generation
- Figure generation script integration

**Decision:**
- If downloaded version has improvements not in existing → Update
- If identical or existing is better → Keep existing
- Always preserve backward compatibility

### Step 2: Markdown Documentation Comparison

**Command:**
```bash
diff docs/frequency_atlas.md frequency_atlas.md
```

**What to look for:**
- New content or explanations
- Corrections to existing content
- Additional frequency ladder entries
- Better formatting or structure

**Note:** The existing `docs/frequency_atlas.md` includes:
- Detailed explanations of each frequency range
- Conversion formulas with context
- MQGT-SCF channel mappings
- Comprehensive documentation

**Decision:**
- If downloaded version has new content → Merge into existing
- If downloaded is just a table → Keep existing detailed version
- If downloaded has corrections → Apply corrections to existing

### Step 3: Update Decision

**If updating Python script:**
1. Backup existing: `cp scripts/frequency_atlas.py scripts/frequency_atlas.py.backup`
2. Compare carefully to preserve backward compatibility
3. Merge improvements while keeping existing function names
4. Test: `python -m py_compile scripts/frequency_atlas.py`
5. Verify imports still work: `python -c "from scripts.frequency_atlas import length_to_freq_yukawa"`

**If updating markdown:**
1. Backup existing: `cp docs/frequency_atlas.md docs/frequency_atlas.md.backup`
2. Merge new content into existing detailed version
3. Preserve detailed explanations
4. Add any new frequency ladder entries
5. Verify markdown renders correctly

**If keeping existing:**
- No action needed
- Document decision in this file

---

## Current Status

**Existing Python Script:**
- ✅ Already updated with improved version (2026-01-19)
- ✅ Includes backward compatibility
- ✅ Has modern Python features
- ✅ Includes figure generation integration

**Existing Markdown:**
- ✅ Detailed documentation with explanations
- ✅ Comprehensive frequency ladder
- ✅ MQGT-SCF channel mappings
- ✅ Conversion formulas with context

**Recommendation:** Compare downloaded files, but existing versions are likely already up-to-date or better. Only update if downloaded versions have significant improvements.

---

## After Comparison

1. Document decision in this file
2. If updated: Test thoroughly
3. If kept: Note why in this file
4. Update `docs/FREQUENCY_ATLAS_UPDATE.md` with results

---

**Last Updated:** 2026-01-20
