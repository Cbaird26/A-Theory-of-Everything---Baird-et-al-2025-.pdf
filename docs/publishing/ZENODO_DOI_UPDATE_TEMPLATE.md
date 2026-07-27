# Zenodo DOI Update Template

**Purpose:** Template for updating CITATION.cff after minting Zenodo DOI

---

## After Minting Zenodo DOI

When you receive the Zenodo DOI (format: `10.5281/zenodo.XXXXXXX`), update `CITATION.cff` as follows:

### Current CITATION.cff (Before DOI)

```yaml
cff-version: 1.2.0
title: "Merged Quantum Gauge and Scalar Consciousness Framework (MQGT-SCF)"
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Baird"
    given-names: "Christopher M."
    orcid: "https://orcid.org/0000-0000-0000-0000"
version: "1.4.0"
date-released: "2026-01-20"
repository-code: "https://github.com/Cbaird26/MQGT-SCF"
license: "CC-BY-4.0"
license-url: "https://creativecommons.org/licenses/by/4.0/"
```

### Updated CITATION.cff (After DOI)

Add the `doi` field:

```yaml
cff-version: 1.2.0
title: "Merged Quantum Gauge and Scalar Consciousness Framework (MQGT-SCF)"
message: "If you use this software, please cite it as below."
authors:
  - family-names: "Baird"
    given-names: "Christopher M."
    orcid: "https://orcid.org/0000-0000-0000-0000"
version: "1.4.0"
date-released: "2026-01-20"
doi: "10.5281/zenodo.XXXXXXX"
repository-code: "https://github.com/Cbaird26/MQGT-SCF"
license: "CC-BY-4.0"
license-url: "https://creativecommons.org/licenses/by/4.0/"
```

**Replace `XXXXXXX` with actual Zenodo record number.**

---

## Update Steps

1. **Get DOI from Zenodo:**
   - Go to published Zenodo record
   - Copy DOI (format: `10.5281/zenodo.XXXXXXX`)

2. **Edit CITATION.cff:**
   - Add `doi: "10.5281/zenodo.XXXXXXX"` field
   - Place after `date-released` and before `repository-code`

3. **Commit and push:**
   ```bash
   git add CITATION.cff
   git commit -m "Update CITATION.cff with Zenodo DOI for v1.4.0"
   git push
   ```

4. **Verify:**
   - Check GitHub "Cite this repository" button (may take time to update)
   - Verify DOI link resolves correctly

---

## Field Descriptions

- **doi:** The Digital Object Identifier for this version (from Zenodo)
- **version:** Semantic version number (e.g., "1.4.0")
- **date-released:** Release date in YYYY-MM-DD format

---

**Note:** The `doi` field is optional in CITATION.cff but recommended for versioned releases with Zenodo archives.
