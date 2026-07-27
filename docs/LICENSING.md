# Licensing Information for MQGT-SCF

This repository uses a multi-license approach, with different licenses for different content types. This is a standard practice in academic software repositories.

## License Assignment

### Code Files (MIT License)

The following files and directories are licensed under the MIT License:

- All Python files (`.py`) in `code/`, `scripts/`, `tests/`
- Shell scripts (`.sh`)
- Makefile
- Configuration files (`.toml`, `.yml`, `.yaml`)
- Test data files used for validation

**License text:** See [`LICENSES/MIT`](../LICENSES/MIT)

**Summary:** Free to use, modify, and distribute with attribution to copyright notice.

### Documentation and Papers (CC-BY-4.0)

The following files are licensed under the Creative Commons Attribution 4.0 International License (CC-BY-4.0):

- All Markdown files (`.md`) in `docs/`
- LaTeX files (`.tex`)
- PDF documents
- Papers in `papers/` directory
- README.md

**License text:** See [`LICENSES/CC-BY-4.0`](../LICENSES/CC-BY-4.0)

**Summary:** Free to share and adapt with attribution.

### Data Files (CC-BY-4.0)

The following data files are licensed under CC-BY-4.0:

- CSV files in `data/raw/` and `data/processed/`
- JSON data files
- Other data files used for constraint analysis

**Rationale:** Data files require attribution to maintain provenance and credit original sources.

## Quick Reference

| Content Type | License | File Extensions |
|--------------|---------|----------------|
| Code | MIT | `.py`, `.sh`, Makefile, `.toml`, `.yml` |
| Documentation | CC-BY-4.0 | `.md`, `.tex`, `.pdf` |
| Data | CC-BY-4.0 | `.csv`, `.json`, other data formats |

## How to Cite

### For Code Usage (MIT License)

```python
# MIT License applies - include copyright notice:
# Copyright (c) 2025 Cbaird26
```

### For Documentation/Paper Usage (CC-BY-4.0)

Please cite as:

```
Baird, C. M. (2025). Merged Quantum Gauge and Scalar Consciousness Framework (MQGT-SCF) [Software/Data]. 
GitHub. https://github.com/Cbaird26/MQGT-SCF
```

Or use the CITATION.cff file:

```bash
# If using cffconvert
cffconvert --outputformat bibtex CITATION.cff
```

## Attribution Requirements

**MIT License (Code):**
- Include copyright notice in source files you modify
- Include license text in distributions

**CC-BY-4.0 (Docs/Data):**
- Credit the original author(s)
- Link to the license
- Indicate if changes were made
- Do not suggest endorsement by the licensor

## Questions

If you have questions about licensing, please:
- Open an issue on GitHub
- Review the full license texts in `LICENSES/`
- Contact the authors directly

## License Compatibility

This multi-license approach is:
- Compatible with academic publication requirements
- Allows code reuse under permissive MIT terms
- Ensures documentation attribution via CC-BY-4.0
- Follows standard practices in research software repositories
