# mm-cm Range Fifth-Force Constraints

This directory contains constraint curves covering the millimeter to centimeter range (approximately 1 mm to 10 cm), extending beyond the sub-millimeter range covered by Eöt-Wash PRL 2016.

## Expected Files

### Kapner et al. (2007) - PRL
- **Source:** Kapner et al., "Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale", Physical Review Letters 98, 021101 (2007)
- **arXiv:** hep-ph/0611184
- **Coverage:** 55 μm to 9.53 mm
- **Figure:** Figure 6 (composite exclusion plot)
- **Expected filename:** `kapner_prl2007_digitized_contract.csv`
- **Status:** ⏳ To be digitized

### Lee et al. (2020) - Eöt-Wash Update
- **Source:** Lee et al., "Test of the Gravitational Inverse-Square Law at Millimeter Ranges", Physical Review Letters 124, 101101 (2020)
- **arXiv:** 2002.11761
- **Coverage:** 52 μm to 3.0 mm
- **Figure:** Figure 5 (bottom panel, 95% CL upper limits on |α|)
- **Expected filename:** `lee_arxiv2020_digitized_contract.csv`
- **Status:** ⏳ To be digitized

## Digitization Guide

See `docs/dev/mm_cm_constraints_digitization_guide.md` for step-by-step instructions on:
- Using WebPlotDigitizer to extract data from figures
- Format requirements for CSV files
- Processing workflow (raw → sorted → monotone conservative)

## CSV Format

All constraint CSVs must follow the contract schema:
```csv
lambda_m,alpha_max,source_id
1.0e-3,1.0e-4,kapner_prl2007_digitized
...
```

- `lambda_m`: Interaction range in meters
- `alpha_max`: Maximum allowed Yukawa coupling strength (dimensionless)
- `source_id`: Unique identifier matching the importer's expected source_id

## Integration

After digitizing and placing CSV files here, run:
```bash
make fifth-ingest-kapner   # For Kapner 2007
make fifth-ingest-lee      # For Lee 2020
```

This will validate, create provenance, and move processed files to `data/processed/`.
