# Digitization Visuals - File Placement Checklist

**Status:** Ready for file placement  
**Action Required:** Download PNG files and place in this directory

---

## Quick Placement Instructions

1. **Download the files** from the fresh links provided
2. **Rename them** as specified below
3. **Place them** in this directory: `docs/dev/digitization_visuals/`
4. **Verify** they display correctly
5. **Update** `README.md` to mark files as present

---

## Files to Add

### File 1: Raw vs Monotone Comparison

**Download:** `eotwash_digitized_compare.png`  
**Rename to:** `eotwash_raw_vs_monotone.png`  
**Place in:** `docs/dev/digitization_visuals/eotwash_raw_vs_monotone.png`

**Verification:**
- File should show blue line (raw) and orange line (monotone)
- Log-log plot with alpha_max vs lambda_m
- File size should be reasonable (< 5MB)

### File 2: WebPlotDigitizer Guide

**Download:** `eotwash_digitization_where_to_click_orange.png`  
**Rename to:** `eotwash_webplotdigitizer_guide.png`  
**Place in:** `docs/dev/digitization_visuals/eotwash_webplotdigitizer_guide.png`

**Verification:**
- File should show WebPlotDigitizer interface
- Orange overlays indicating which curve to digitize
- File size should be reasonable (< 5MB)

---

## After Placement

1. **Update README.md:**
   - Change status from "⏳ (To be added)" to "✅ (Present)"
   - Remove "Action Required" notes

2. **Verify Image Links:**
   - Check `docs/dev/eotwash_digitization_guide.md` - images should display
   - Check `docs/DATA_GROUND_TRUTH.md` - image references should work
   - Check `docs/REAL_VS_SYNTHETIC_GUARDRAILS.md` - links should resolve

3. **Test Display:**
   - Open markdown files in a markdown viewer
   - Verify images render correctly
   - Check that file paths are relative and correct

---

## Troubleshooting

**If images don't display:**
- Verify file names match exactly (case-sensitive)
- Check file paths are relative to markdown file location
- Ensure files are committed to git (not just staged)
- Verify file formats are PNG (not corrupted)

**If file sizes are too large:**
- Consider compressing images if > 5MB
- Use PNG optimization tools if needed
- Verify images are not unnecessarily high resolution

---

**Once files are placed, mark this checklist complete and update README.md.**
