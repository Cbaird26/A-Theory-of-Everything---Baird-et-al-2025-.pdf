# GitHub Release Description Template

**Version:** v1.4.0  
**Date:** 2026-01-19  
**Template for:** GitHub Release descriptions

---

## Template

Copy this template and customize for each release:

```markdown
## MQGT-SCF vX.Y.Z

**MQGT-SCF** publishes a reproducible "constraint lab" for pressure-testing a parameterized operational hypothesis against public experimental constraints across multiple channels.

### What This Release Includes

- Reproducible scripts and deterministic runs (seeded scans where applicable)
- Versioned outputs (tables/figures) sufficient to reproduce results from a clean clone
- Canonical datasets with provenance tracking (SHA256 hashes)
- Complete documentation suite

### Scope / Non-Claims

This release does not claim confirmation of new physics; it provides an auditable instrument intended to be inspected, replicated, and falsified.

### Reproduce

```bash
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF
make install
make test
make reproduce
```

See [`docs/REVIEWER_QUICKSTART.md`](docs/REVIEWER_QUICKSTART.md) for detailed instructions.

### Zenodo DOI

This release is archived on Zenodo with DOI: [10.5281/zenodo.XXXXXXX](https://zenodo.org/record/XXXXXXX)

**Cite this release:**
```
Baird, C. M. (2026). MQGT-SCF: Reproducible constraint lab for operational tests (Version X.Y.Z) [Software]. 
Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
```

### Changes in This Release

#### New Features
- [Feature 1]
- [Feature 2]

#### Data Updates
- [New dataset or update]

#### Documentation
- [Documentation improvements]

#### Bug Fixes
- [Bug fix 1]
- [Bug fix 2]

### Key Results (If Applicable)

[Brief summary of key analysis results, if this release includes new analysis]

### Important Notes

- All results generated with fixed seeds for reproducibility
- Real-only mode available for canonical analysis (excludes synthetic curves)
- Mapping sensitivity modes (A/B/C) documented and testable
- See [`docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`](docs/CLAIMS_LIMITS_AND_FALSIFIERS.md) for scientific contract

### Links

- **Repository:** https://github.com/Cbaird26/MQGT-SCF
- **Documentation:** [`docs/REVIEWER_QUICKSTART.md`](docs/REVIEWER_QUICKSTART.md)
- **Scientific Contract:** [`docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`](docs/CLAIMS_LIMITS_AND_FALSIFIERS.md)
- **Zenodo Archive:** https://zenodo.org/record/XXXXXXX
```

---

## Customization Guidelines

### For Major Releases (X.0.0)

- Emphasize new analysis capabilities
- Highlight new constraint channels
- Note any breaking changes
- Include migration guide if needed

### For Minor Releases (X.Y.0)

- Focus on new datasets or features
- Highlight documentation improvements
- Note new Makefile targets
- Emphasize backward compatibility

### For Patch Releases (X.Y.Z)

- Focus on bug fixes
- Note critical corrections
- Emphasize stability improvements
- Keep description concise

---

## Tone Guidelines

**Do:**
- Use factual, operational language
- Emphasize reproducibility and auditability
- Link to documentation
- Include reproduction instructions
- State non-claims explicitly

**Don't:**
- Overclaim results
- Use marketing language
- Make unsubstantiated claims
- Skip reproduction instructions
- Forget to include DOI

---

## Examples

### Example 1: Major Release (New Analysis)

```markdown
## MQGT-SCF v2.0.0

**Major Release:** Fifth-force detectability analysis with real-only envelope mode and coverage reporting.

### What This Release Includes

- Real-only envelope mode (excludes synthetic curves)
- Coverage reporting for experimental data ranges
- Mapping sensitivity modes (A/B/C) with documented assumptions
- Eöt-Wash PRL 2016 digitized constraint (canonical: monotone_conservative)
- Complete frequency atlas integration

### Key Results

- Hunt band identified: λ ~ 0.3-1.3 mm (f_eq ~ 5×10¹⁰–1.6×10¹² Hz)
- Fifth-force dominance: < 3% even at ×10 mapping scaling
- Coverage: [X]% of sampled points within real experimental ranges

[Rest of template...]
```

### Example 2: Minor Release (Documentation)

```markdown
## MQGT-SCF v1.4.0

**Documentation Release:** World-grade documentation suite and GitHub Release workflow.

### What This Release Includes

- Scientific contract document (`docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`)
- Reviewer quickstart guide (`docs/REVIEWER_QUICKSTART.md`)
- GitHub Release + Zenodo DOI workflow documentation
- Release preparation scripts
- Updated licensing (MIT for code, CC-BY-4.0 for docs)

### Changes in This Release

#### Documentation
- Added scientific contract separating claims from assumptions
- Added 10-minute reviewer quickstart guide
- Added GitHub Release workflow documentation
- Created release template for future releases

#### Infrastructure
- Created `.zenodo.json` for automatic Zenodo metadata
- Added release preparation script
- Updated Makefile with release targets

[Rest of template...]
```

---

**Use this template to ensure consistent, professional release descriptions.**
