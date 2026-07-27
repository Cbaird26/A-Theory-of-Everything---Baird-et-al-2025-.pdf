# Publishing Ready ✅

**Package:** `scalar_fifth_force_upload_v3`  
**Status:** Ready for GitHub Release + Zenodo DOI

---

## What's Ready

### Publishing Materials

All materials are in `docs/publishing/`:

1. **`github_release_v1.3.0.md`** - Complete GitHub Release notes (copy-paste ready)
2. **`zenodo_metadata.md`** - Zenodo DOI metadata template
3. **`public_statement.md`** - Clean, factual public statement (no hype)
4. **`release_checklist.md`** - Pre-release verification checklist
5. **`interpretation_templates.md`** - Templates for hunt band results (persists/collapses)

### Validation Tools

- **`check_digitized_csv.sh`** - Automated CSV sanity check
- **`docs/dev/csv_validation_guide.md`** - Manual validation checklist

---

## Quick Publishing Steps

### 1. GitHub Release

1. Go to GitHub repository → Releases → Draft new release
2. Tag: `v1.3.0`
3. Title: Copy from `docs/publishing/github_release_v1.3.0.md`
4. Description: Copy full content from that file
5. Attach: `scalar_fifth_force_upload_v3.zip`
6. Publish release

### 2. Zenodo DOI

1. Connect GitHub → Zenodo (Settings → Webhooks)
2. Release will auto-create Zenodo draft
3. Fill metadata from `docs/publishing/zenodo_metadata.md`
4. Publish to mint DOI
5. Add DOI back to GitHub Release description

### 3. Public Statement (Optional)

Use content from `docs/publishing/public_statement.md`

---

## Next Science Step

**Digitize real Eöt-Wash curve:**
1. Use `docs/dev/eotwash_digitization_guide.md`
2. Save CSV at path in `EXACT_CSV_PATH.txt`
3. Run: `./check_digitized_csv.sh [path]`
4. Run: `make fifth-ingest INPUT=...`
5. Run: `make fifth-detectability SEED=42 NPTS=5000`
6. Use `docs/publishing/interpretation_templates.md` to update canonical statement

---

## Package Contents

- ✅ 49+ files (docs, code, data, results, tests)
- ✅ All publishing materials
- ✅ All validation tools
- ✅ Complete documentation suite
- ✅ Ready for upload

---

**Everything is ready. Publish when ready. Hunt when ready. 🚀**

