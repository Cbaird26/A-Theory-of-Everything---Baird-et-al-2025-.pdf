# GitHub Release Instructions for v1.4.0

**Purpose:** Step-by-step instructions for creating GitHub Release v1.4.0 with Zenodo DOI integration

---

## Prerequisites

- [ ] Release bundle created: `mqgt_scf_release_v1.4.0.zip`
- [ ] SHA256 hash file: `mqgt_scf_release_v1.4.0.zip.sha256`
- [ ] All files committed and pushed to GitHub
- [ ] Zenodo GitHub integration enabled (see Step 1)

---

## Step 1: Enable Zenodo Integration (One-Time Setup)

**If not already done:**

1. Go to: https://zenodo.org/account/settings/github/
2. Find `Cbaird26/MQGT-SCF` in the repository list
3. Toggle switch to **ON**
4. Select release type: **"Release"**

**Result:** Zenodo will auto-create draft records for each GitHub Release.

---

## Step 2: Create GitHub Release

### 2.1 Navigate to Releases

1. Go to: https://github.com/Cbaird26/MQGT-SCF/releases/new
2. Or: Repository → Releases → "Draft a new release"

### 2.2 Fill Release Information

**Tag:**
- Click "Choose a tag" → Type: `v1.4.0`
- Select "Create new tag: v1.4.0 on publish"
- Target: `main` branch (or appropriate branch)

**Title:**
```
v1.4.0 — Constraint Lab: File Integration and Permanent Artifact Storage
```

**Description:**
Copy and paste from the template below, then customize as needed:

```markdown
## v1.4.0 — Constraint Lab: File Integration and Permanent Artifact Storage

**Release Date:** 2026-01-20

### What's Included

This release integrates fresh downloads and establishes permanent artifact storage:

- **Eöt-Wash CSV Variants:** All digitized curve variants (READY, sorted, monotone_conservative)
- **Digitization Visuals:** Process documentation images (raw vs monotone, WebPlotDigitizer guide)
- **Frequency Atlas:** Updated conversion utilities and documentation
- **Zenodo Integration:** `.zenodo.json` metadata for automatic DOI minting
- **Release Infrastructure:** Automated release preparation and verification

### Scope / Non-Claims

This release does not claim confirmation of new physics. It provides an auditable instrument intended to be inspected, replicated, and falsified. The constraint lab framework tests a parameterized hypothesis against public experimental constraints across multiple channels.

### Reproduction Instructions

To reproduce results from this release:

```bash
# Clone repository
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF

# Checkout this release
git checkout v1.4.0

# Install dependencies
make install

# Run tests
make test

# Reproduce results
make reproduce
```

See [`docs/REVIEWER_QUICKSTART.md`](docs/REVIEWER_QUICKSTART.md) for detailed instructions.

### Zenodo DOI

**Note:** DOI will be added after Zenodo record is published. See Step 3 below.

This release will be archived on Zenodo with a permanent DOI. Check back here for the DOI link after completing the Zenodo publishing step.

### Changes in This Release

- Integrated Eöt-Wash CSV variants into `data/raw/fifth_force/variants/`
- Added digitization visuals to `docs/dev/digitization_visuals/`
- Created `.zenodo.json` for automatic Zenodo metadata
- Enhanced release preparation automation
- Updated documentation with file integration details

### Key Results

- All Eöt-Wash digitized curve variants available for reference
- Visual documentation of digitization process
- Permanent artifact storage via GitHub Release + Zenodo DOI
- Improved reproducibility and auditability

### Important Notes

- **License:** Code under MIT, documentation/data under CC-BY-4.0 (see `LICENSES/`)
- **Data Provenance:** All datasets include SHA256 hashes and provenance tracking
- **Reproducibility:** All results generated with fixed seeds (seed=42) for determinism

### Links

- **Repository:** https://github.com/Cbaird26/MQGT-SCF
- **Documentation:** See `docs/` directory for detailed guides
- **Zenodo DOI:** [To be added after publishing]

---

**For questions or issues, please open an issue on GitHub.**
```

### 2.3 Attach Release Bundle

1. Scroll to "Attach binaries"
2. Click "select your files" or drag and drop
3. Upload: `mqgt_scf_release_v1.4.0.zip`
4. (Optional) Upload: `mqgt_scf_release_v1.4.0.zip.sha256`

### 2.4 Publish Release

1. Review all information
2. Ensure "Set as the latest release" is checked (if this is the latest)
3. Click **"Publish release"**

**Result:** Release published with stable download URL.

---

## Step 3: Mint Zenodo DOI (Next Steps)

After publishing the GitHub Release:

1. **Wait 2-5 minutes** for Zenodo to create draft
2. **Go to:** https://zenodo.org/account/settings/github/
3. **Find the draft** for v1.4.0
4. **Review metadata** (auto-populated from `.zenodo.json`)
5. **Publish** to mint DOI
6. **Copy DOI:** Format will be `10.5281/zenodo.XXXXXXX`

Then:
- Update GitHub Release description with DOI (Step 4)
- Update `CITATION.cff` with DOI (Step 5)

---

## Step 4: Update GitHub Release with DOI

1. Go back to GitHub Release: https://github.com/Cbaird26/MQGT-SCF/releases/tag/v1.4.0
2. Click **"Edit release"**
3. In description, find the "Zenodo DOI" section
4. Replace placeholder with:
   ```markdown
   ### Zenodo DOI
   
   This release is archived on Zenodo: [10.5281/zenodo.XXXXXXX](https://zenodo.org/record/XXXXXXX)
   ```
   (Replace `XXXXXXX` with actual Zenodo record number)
5. Click **"Update release"**

---

## Step 5: Update CITATION.cff

1. Edit `CITATION.cff` in repository
2. Update fields:
   ```yaml
   version: "1.4.0"
   date-released: "2026-01-20"
   doi: "10.5281/zenodo.XXXXXXX"
   ```
3. Commit and push:
   ```bash
   git add CITATION.cff
   git commit -m "Update CITATION.cff with Zenodo DOI for v1.4.0"
   git push
   ```

---

## Verification Checklist

After completing all steps:

- [ ] GitHub Release exists and is accessible
- [ ] Release bundle downloads correctly
- [ ] Zenodo record exists and is accessible
- [ ] DOI resolves correctly
- [ ] DOI appears in GitHub Release description
- [ ] `CITATION.cff` includes DOI
- [ ] GitHub "Cite this repository" button shows DOI

---

## Troubleshooting

**Release bundle too large:**
- Zenodo limit is 50GB
- If bundle exceeds limit, exclude large generated files
- Consider using Git LFS for large files

**Zenodo draft doesn't appear:**
- Wait 5-10 minutes (sync delay)
- Verify Zenodo GitHub integration is enabled
- Check that `.zenodo.json` exists in repository root
- Verify GitHub Release was created (not just a tag)

**DOI doesn't appear in citation button:**
- Wait for GitHub to refresh (can take hours)
- Verify `CITATION.cff` syntax is valid YAML
- Check DOI format: `10.5281/zenodo.XXXXXXX`

---

**Last Updated:** 2026-01-20
