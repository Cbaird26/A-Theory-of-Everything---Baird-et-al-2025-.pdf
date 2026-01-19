# Pre-Release Checklist

**Before creating GitHub Release v1.3.0**

---

## Code & Data

- [ ] All code committed and pushed
- [ ] All results files generated with fixed seeds
- [ ] Package zip file created: `scalar_fifth_force_upload_v3.zip`
- [ ] Package contains all necessary files (49 files)
- [ ] No sensitive data or credentials in package

## Documentation

- [ ] Canonical summaries updated and reviewed
- [ ] All cross-references working
- [ ] File index complete
- [ ] README files updated

## Validation

- [ ] Tests pass: `make fifth-validate`
- [ ] QRNG multisource tests pass
- [ ] Fifth-force tests pass
- [ ] Detectability tests pass

## Reproducibility

- [ ] Can reproduce results with:
  ```bash
  make fifth-detectability SEED=42 NPTS=2000
  ```
- [ ] Results match expected outputs
- [ ] Provenance manifests generated

## Release Materials

- [ ] GitHub Release notes drafted (`docs/publishing/github_release_v1.3.0.md`)
- [ ] Zenodo metadata prepared (`docs/publishing/zenodo_metadata.md`)
- [ ] Public statement drafted (`docs/publishing/public_statement.md`)

## Final Checks

- [ ] No "TODO" or "FIXME" in canonical documents
- [ ] All citations complete
- [ ] License specified
- [ ] Contact information included (if applicable)

---

## Release Steps

1. **Create GitHub Release:**
   - Tag: `v1.3.0`
   - Title: "v1.3.0 — Constraint Lab: QRNG Multisource + Scalar Fifth-Force Detectability"
   - Description: Copy from `docs/publishing/github_release_v1.3.0.md`
   - Attach: `scalar_fifth_force_upload_v3.zip`

2. **Mint Zenodo DOI:**
   - Connect GitHub → Zenodo (if not already)
   - Release will auto-create Zenodo draft
   - Fill metadata from `docs/publishing/zenodo_metadata.md`
   - Publish to mint DOI

3. **Update Release with DOI:**
   - Add Zenodo DOI to GitHub Release description
   - Update citation information

---

**This checklist ensures a clean, professional release.**

