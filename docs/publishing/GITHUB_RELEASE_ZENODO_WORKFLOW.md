# GitHub Release + Zenodo DOI Workflow

**Date:** 2026-01-19  
**Repository:** MQGT-SCF  
**Status:** **Canonical (Release Workflow)** ⭐

---

## Purpose

This document provides step-by-step instructions for creating GitHub Releases and minting permanent Zenodo DOIs for MQGT-SCF artifacts. This workflow ensures all releases are permanently archived and citable.

---

## Prerequisites

1. **GitHub repository:** `Cbaird26/MQGT-SCF` must exist and be accessible
2. **Zenodo account:** Create account at https://zenodo.org if needed
3. **GitHub token:** For automated workflows (optional, for CI/CD)

---

## Step-by-Step Workflow

### Step 1: Prepare Release Artifacts

Before creating a release, prepare all artifacts:

```bash
# Run release preparation script
make prepare-release

# Or manually:
# 1. Generate data ledgers
make fifth-data-ledger
make fifth-sha256-ledger

# 2. Run tests to ensure everything works
make test

# 3. Verify reproducibility
make reproduce

# 4. Create release bundle (if script doesn't exist)
zip -r mqgt_scf_release_v1.4.0.zip \
  code/ data/ docs/ scripts/ tests/ \
  Makefile README.md LICENSE CITATION.cff pyproject.toml \
  -x "*.pyc" "__pycache__/*" "*.git/*"
```

**Checklist:**
- [ ] All code committed and pushed
- [ ] All tests pass (`make test`)
- [ ] Results reproducible (`make reproduce`)
- [ ] Data ledgers generated
- [ ] SHA256 hashes computed
- [ ] Release bundle created
- [ ] `.zenodo.json` is up-to-date

---

### Step 2: Enable Zenodo GitHub Integration

**One-time setup:**

1. **Log in to Zenodo:**
   - Go to https://zenodo.org
   - Sign in with GitHub (recommended) or create account

2. **Connect GitHub repository:**
   - Go to: https://zenodo.org/account/settings/github/
   - Find `Cbaird26/MQGT-SCF` in the list
   - Toggle the switch to **ON** (enable Zenodo archiving)
   - Select release type: **"Release"** (not pre-release)

3. **Verify connection:**
   - Zenodo will show "Connected" status
   - Future GitHub Releases will automatically create Zenodo drafts

**Note:** If `.zenodo.json` exists in the repo root, Zenodo will use it for metadata. Otherwise, Zenodo will auto-generate metadata from repository files.

---

### Step 3: Create GitHub Release

**On GitHub:**

1. **Navigate to Releases:**
   - Go to: https://github.com/Cbaird26/MQGT-SCF/releases
   - Click "Draft a new release"

2. **Create Release:**
   - **Tag version:** `v1.4.0` (or appropriate version)
   - **Release title:** `v1.4.0 — Constraint Lab: [Brief Description]`
   - **Description:** Copy from `docs/publishing/RELEASE_TEMPLATE.md` and customize
   - **Target:** `main` branch (or appropriate branch)
   - **Pre-release:** Unchecked (unless it's a pre-release)

3. **Attach Release Assets:**
   - Click "Attach binaries"
   - Upload: `mqgt_scf_release_v1.4.0.zip` (or your release bundle)
   - Optionally attach: Individual data files, documentation PDFs, etc.

4. **Publish Release:**
   - Click "Publish release"
   - GitHub will create the release and tag

**Release Description Template:**

```markdown
## MQGT-SCF v1.4.0

**MQGT-SCF** publishes a reproducible "constraint lab" for pressure-testing a parameterized operational hypothesis against public experimental constraints across multiple channels.

### What This Release Includes

- Reproducible scripts and deterministic runs (seeded scans where applicable)
- Versioned outputs (tables/figures) sufficient to reproduce results from a clean clone
- Canonical datasets with provenance tracking
- Complete documentation suite

### Scope / Non-Claims

This release does not claim confirmation of new physics; it provides an auditable instrument intended to be inspected, replicated, and falsified.

### Reproduce

```bash
make install && make test && make reproduce
```

See [`docs/REVIEWER_QUICKSTART.md`](docs/REVIEWER_QUICKSTART.md) for detailed instructions.

### Zenodo DOI

[Will be added after Step 4]

### Changes in This Release

- [List key changes]
- [New features]
- [Bug fixes]
- [Documentation updates]
```

---

### Step 4: Mint Zenodo DOI

**After GitHub Release is published:**

1. **Check Zenodo:**
   - Go to: https://zenodo.org/account/settings/github/
   - Find `Cbaird26/MQGT-SCF`
   - Click on the new draft (should appear within minutes)

2. **Review Zenodo Metadata:**
   - Zenodo will auto-populate from `.zenodo.json` or repository files
   - Verify:
     - Title is correct
     - Description is appropriate
     - License is CC-BY-4.0
     - Creators are listed correctly
     - Keywords are relevant

3. **Edit Metadata (if needed):**
   - Update description if auto-generated version is incomplete
   - Add additional keywords if needed
   - Verify related identifiers point to GitHub repo

4. **Publish to Mint DOI:**
   - Click "Publish" button
   - Zenodo will assign a DOI (e.g., `10.5281/zenodo.1234567`)
   - **Copy the DOI** - you'll need it for Step 5

**Important:** Once published, the Zenodo record is permanent. You can create new versions, but the DOI is fixed.

---

### Step 5: Update GitHub Release with DOI

**Back on GitHub:**

1. **Edit Release:**
   - Go to: https://github.com/Cbaird26/MQGT-SCF/releases
   - Click "Edit" on the release you just created

2. **Add DOI to Description:**
   - Add section at top or bottom:
   ```markdown
   ### Zenodo DOI
   
   This release is archived on Zenodo with DOI: [10.5281/zenodo.XXXXXXX](https://zenodo.org/record/XXXXXXX)
   
   **Cite this release:**
   ```
   Baird, C. M. (2026). MQGT-SCF: Reproducible constraint lab for operational tests (Version 1.4.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
   ```

3. **Save Changes:**
   - Click "Update release"

---

### Step 6: Update CITATION.cff

**Update citation file with new DOI:**

1. **Edit `CITATION.cff`:**
   - Update `version:` to match release version
   - Update `date-released:` to release date
   - Add `doi:` field with Zenodo DOI:
   ```yaml
   doi: "10.5281/zenodo.XXXXXXX"
   ```

2. **Commit and push:**
   ```bash
   git add CITATION.cff
   git commit -m "Update CITATION.cff with Zenodo DOI for v1.4.0"
   git push
   ```

**Note:** GitHub's "Cite this repository" button will automatically use the DOI from `CITATION.cff`.

---

### Step 7: Update README (Optional)

**Add DOI badge or link:**

Add to `README.md`:

```markdown
## Citation

This work is archived on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

**Latest Release:** v1.4.0 (DOI: 10.5281/zenodo.XXXXXXX)

See [`CITATION.cff`](CITATION.cff) for machine-readable citation format.
```

---

## Troubleshooting

### Issue: Zenodo draft doesn't appear after GitHub Release

**Solutions:**
- Wait 5-10 minutes (Zenodo sync can be delayed)
- Check Zenodo GitHub integration is enabled
- Verify `.zenodo.json` exists and is valid JSON
- Check Zenodo account notifications for errors

### Issue: Zenodo metadata is incorrect

**Solutions:**
- Edit `.zenodo.json` in repo and push changes
- Manually edit Zenodo draft before publishing
- Note: `.zenodo.json` takes precedence over auto-generated metadata

### Issue: DOI doesn't appear in GitHub citation button

**Solutions:**
- Ensure `CITATION.cff` includes `doi:` field
- Verify DOI format is correct: `10.5281/zenodo.XXXXXXX`
- Wait for GitHub to refresh (can take hours)
- Check `CITATION.cff` syntax is valid YAML

### Issue: Release bundle is too large

**Solutions:**
- Zenodo has 50GB limit per record
- Exclude large files: `*.zip`, `*.pdf` (if already in repo)
- Use Git LFS for large files
- Split into multiple releases if necessary

---

## Best Practices

### Release Frequency

- **Major releases:** Significant new features or analysis results
- **Minor releases:** New datasets, documentation updates, bug fixes
- **Patch releases:** Critical bug fixes only

### Version Numbering

- Follow semantic versioning: `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes or major new analysis
- `MINOR`: New features, datasets, or analyses
- `PATCH`: Bug fixes, documentation updates

### Release Descriptions

- Use template from `docs/publishing/RELEASE_TEMPLATE.md`
- Keep descriptions factual and non-overclaiming
- Include reproduction instructions
- Link to relevant documentation

### Artifact Contents

**Always include:**
- Code (all Python scripts)
- Data (canonical datasets)
- Documentation (markdown files)
- Scripts (Makefile, shell scripts)
- Metadata (CITATION.cff, .zenodo.json)

**Optional:**
- Pre-computed results (for quick verification)
- Figures/plots (if not generated by scripts)
- PDFs (if not auto-generated)

---

## Automated Workflow (Future Enhancement)

**For CI/CD integration:**

Create `.github/workflows/release.yml`:

```yaml
name: Release Preparation

on:
  release:
    types: [created]

jobs:
  prepare-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate ledgers
        run: |
          make fifth-data-ledger
          make fifth-sha256-ledger
      - name: Create release bundle
        run: |
          zip -r release_bundle.zip code/ data/ docs/ scripts/ tests/ Makefile README.md LICENSE CITATION.cff
      - name: Upload release bundle
        uses: actions/upload-artifact@v3
        with:
          name: release-bundle
          path: release_bundle.zip
```

---

## Quick Reference

**GitHub Release URL:**
```
https://github.com/Cbaird26/MQGT-SCF/releases/tag/v1.4.0
```

**Zenodo Record URL:**
```
https://zenodo.org/record/XXXXXXX
```

**DOI Format:**
```
10.5281/zenodo.XXXXXXX
```

**Citation Format:**
```
Baird, C. M. (2026). MQGT-SCF: Reproducible constraint lab (Version 1.4.0) [Software]. 
Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
```

---

## Related Documentation

- Release template: [`docs/publishing/RELEASE_TEMPLATE.md`](RELEASE_TEMPLATE.md)
- Release checklist: [`docs/publishing/release_checklist.md`](release_checklist.md)
- Citation instructions: [`docs/publishing/CITATION_UPDATE_INSTRUCTIONS.md`](CITATION_UPDATE_INSTRUCTIONS.md)
- Data ground truth: [`docs/DATA_GROUND_TRUTH.md`](../DATA_GROUND_TRUTH.md)

---

**This workflow ensures all releases are permanently archived, citable, and reproducible.**
