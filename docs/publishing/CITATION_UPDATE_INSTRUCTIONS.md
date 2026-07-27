# CITATION.cff Update Instructions

**Date:** 2026-01-19  
**Repository:** MQGT-SCF  
**Purpose:** Maintain `CITATION.cff` with current Zenodo DOI after each release

---

## When to Update

Update `CITATION.cff` **after** each GitHub Release that creates a new Zenodo DOI:

1. Create GitHub Release
2. Zenodo mints new DOI
3. **Update `CITATION.cff`** with new DOI
4. Commit and push changes

---

## Update Process

### Step 1: Get Zenodo DOI

After publishing Zenodo record, copy the DOI:
- Format: `10.5281/zenodo.XXXXXXX`
- Found in: Zenodo record page or GitHub Release description

### Step 2: Edit CITATION.cff

Update these fields:

```yaml
version: "1.4.0"  # Update to match release version
date-released: "2026-01-19"  # Update to release date
doi: "10.5281/zenodo.XXXXXXX"  # Add or update DOI
```

**Full example:**

```yaml
cff-version: 1.2.0
title: "Merged Quantum Gauge and Scalar Consciousness Framework (MQGT-SCF)"
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Baird"
    given-names: "Christopher M."
    orcid: "https://orcid.org/0000-0000-0000-0000"
version: "1.4.0"
date-released: "2026-01-19"
doi: "10.5281/zenodo.XXXXXXX"
repository-code: "https://github.com/Cbaird26/MQGT-SCF"
license: "CC-BY-4.0"
license-url: "https://creativecommons.org/licenses/by/4.0/"
keywords:
  - "quantum physics"
  - "effective field theory"
  - "consciousness"
  - "ethics"
  - "constraint analysis"
  - "fifth force"
  - "quantum random number generator"
abstract: "An effective field theory extension of the Standard Model and General Relativity incorporating scalar fields for consciousness and ethical weighting, with operational constraints tested across multiple experimental channels (QRNG, fifth-force, Higgs portals, cosmology)."
```

### Step 3: Commit and Push

```bash
git add CITATION.cff
git commit -m "Update CITATION.cff with Zenodo DOI for v1.4.0"
git push
```

---

## Field Descriptions

### Required Fields

- **`version`:** Semantic version (e.g., "1.4.0")
- **`date-released`:** ISO 8601 date (YYYY-MM-DD)
- **`doi`:** Zenodo DOI (format: "10.5281/zenodo.XXXXXXX")

### Optional but Recommended

- **`repository-code`:** GitHub repository URL
- **`license`:** License identifier (CC-BY-4.0)
- **`license-url`:** License URL
- **`keywords`:** List of relevant keywords
- **`abstract`:** Brief description

---

## Verification

After updating, verify:

1. **GitHub Citation Button:**
   - Go to repository main page
   - Click "Cite this repository"
   - Verify DOI appears correctly

2. **YAML Syntax:**
   ```bash
   # Check syntax (if cffconvert installed)
   cffconvert --validate CITATION.cff
   ```

3. **Manual Check:**
   - Open `CITATION.cff` in text editor
   - Verify indentation (2 spaces, not tabs)
   - Verify all quotes are consistent
   - Verify DOI format is correct

---

## Common Issues

### Issue: GitHub citation button doesn't show DOI

**Solution:**
- Ensure `doi:` field exists in `CITATION.cff`
- Wait for GitHub to refresh (can take hours)
- Verify YAML syntax is valid

### Issue: DOI format error

**Solution:**
- Use format: `10.5281/zenodo.XXXXXXX` (no URL prefix)
- Ensure quotes around DOI value
- Verify no extra spaces

### Issue: Version mismatch

**Solution:**
- Keep `version:` in `CITATION.cff` matching GitHub Release tag
- Update both when creating new release

---

## Best Practices

1. **Update immediately after Zenodo publish:** Don't wait - update `CITATION.cff` right after getting DOI
2. **Keep versions synchronized:** `CITATION.cff` version should match GitHub Release tag
3. **Include in release checklist:** Add "Update CITATION.cff" to release workflow
4. **Verify after update:** Check GitHub citation button works

---

## Related Documentation

- GitHub Release workflow: [`docs/publishing/GITHUB_RELEASE_ZENODO_WORKFLOW.md`](GITHUB_RELEASE_ZENODO_WORKFLOW.md)
- Release template: [`docs/publishing/RELEASE_TEMPLATE.md`](RELEASE_TEMPLATE.md)
- CITATION.cff spec: https://citation-file-format.github.io/

---

**Keeping `CITATION.cff` updated ensures proper citation attribution for all releases.**
