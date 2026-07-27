# Quick Start: Creating Your First GitHub Release + Zenodo DOI

**Time:** ~15 minutes  
**Purpose:** Get your first release archived and citable

---

## Prerequisites

- [ ] GitHub repository exists: `Cbaird26/MQGT-SCF`
- [ ] Zenodo account created: https://zenodo.org
- [ ] All code committed and pushed to GitHub
- [ ] `.zenodo.json` exists in repo root (already created)

---

## 5-Minute Setup (One-Time)

### 1. Enable Zenodo GitHub Integration (2 minutes)

1. Go to: https://zenodo.org/account/settings/github/
2. Find `Cbaird26/MQGT-SCF` in the list
3. Toggle switch to **ON**
4. Select release type: **"Release"**

**Done!** Zenodo will now auto-create drafts for each GitHub Release.

---

## 10-Minute Release Process

### Step 1: Prepare Release (3 minutes)

```bash
# Generate ledgers and create release bundle
make prepare-release VERSION=v1.4.0
```

**Output:**
- `mqgt_scf_release_v1.4.0.zip` - Release bundle
- `mqgt_scf_release_v1.4.0.zip.sha256` - Hash file

### Step 2: Create GitHub Release (3 minutes)

1. Go to: https://github.com/Cbaird26/MQGT-SCF/releases/new
2. **Tag:** `v1.4.0`
3. **Title:** `v1.4.0 — Constraint Lab: [Brief Description]`
4. **Description:** Copy from `docs/publishing/RELEASE_TEMPLATE.md` and customize
5. **Attach:** Upload `mqgt_scf_release_v1.4.0.zip`
6. **Publish release**

### Step 3: Mint Zenodo DOI (2 minutes)

1. Wait 2-5 minutes for Zenodo to create draft
2. Go to: https://zenodo.org/account/settings/github/
3. Click on the new draft
4. Review metadata (auto-populated from `.zenodo.json`)
5. Click **"Publish"** to mint DOI

**Copy the DOI:** `10.5281/zenodo.XXXXXXX`

### Step 4: Update GitHub Release with DOI (1 minute)

1. Go back to GitHub Release
2. Click **"Edit release"**
3. Add DOI section to description:
   ```markdown
   ### Zenodo DOI
   
   This release is archived on Zenodo: [10.5281/zenodo.XXXXXXX](https://zenodo.org/record/XXXXXXX)
   ```
4. **Update release**

### Step 5: Update CITATION.cff (1 minute)

1. Edit `CITATION.cff`:
   ```yaml
   version: "1.4.0"
   date-released: "2026-01-19"
   doi: "10.5281/zenodo.XXXXXXX"
   ```

2. Commit and push:
   ```bash
   git add CITATION.cff
   git commit -m "Update CITATION.cff with Zenodo DOI for v1.4.0"
   git push
   ```

---

## Verification

**Check these:**

- [ ] GitHub Release exists: https://github.com/Cbaird26/MQGT-SCF/releases/tag/v1.4.0
- [ ] Zenodo record exists: https://zenodo.org/record/XXXXXXX
- [ ] DOI appears in GitHub Release description
- [ ] `CITATION.cff` includes DOI
- [ ] GitHub "Cite this repository" button shows DOI

---

## Troubleshooting

**Zenodo draft doesn't appear:**
- Wait 5-10 minutes (sync delay)
- Check Zenodo integration is enabled
- Verify `.zenodo.json` exists

**DOI doesn't appear in citation button:**
- Wait for GitHub to refresh (can take hours)
- Verify `CITATION.cff` syntax is valid YAML
- Check DOI format: `10.5281/zenodo.XXXXXXX`

---

## Next Release

For future releases, just repeat Steps 1-5 with new version number. Zenodo will automatically create a new draft for each GitHub Release.

---

## Full Documentation

For detailed instructions, see:
- [`docs/publishing/GITHUB_RELEASE_ZENODO_WORKFLOW.md`](GITHUB_RELEASE_ZENODO_WORKFLOW.md) - Complete workflow
- [`docs/publishing/RELEASE_TEMPLATE.md`](RELEASE_TEMPLATE.md) - Release description template
- [`docs/publishing/CITATION_UPDATE_INSTRUCTIONS.md`](CITATION_UPDATE_INSTRUCTIONS.md) - Citation maintenance

---

**That's it! Your release is now permanently archived and citable.**
