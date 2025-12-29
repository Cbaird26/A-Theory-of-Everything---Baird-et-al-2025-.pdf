# Quick Reference: CSV Format for Real Data

## Exact Format Required

```csv
lambda,alpha,excluded
1e-06,1e-12,0
2e-06,1.5e-12,0
5e-06,2e-12,1
...
```

## Validation Checklist

When you digitize a real curve, ensure:

- [ ] **Columns:** Exactly `lambda,alpha,excluded` (lowercase, no spaces)
- [ ] **Lambda units:** Meters (not cm, not mm)
- [ ] **Alpha:** Dimensionless (Yukawa strength parameter)
- [ ] **Excluded:** 0 (allowed) or 1 (excluded), integer
- [ ] **Lambda monotonic:** Values increase (or at least don't decrease)
- [ ] **Log spacing:** Roughly log-spaced recommended (not required, but helps plots)
- [ ] **Range:** Typically 1e-6 to 1e0 meters for short-range tests

## Example: First 3 Rows (Current Placeholder)

```csv
lambda,alpha,excluded
1e-06,1.2328467394420685e-12,0
1.1497569953977357e-06,1.5199110829529332e-12,0
1.3219411484660288e-06,1.873817422860387e-12,0
```

**When you digitize real data, replace these with actual (λ, α) points from the published exclusion curve.**

## Units Reminder

- **λ (lambda):** Range parameter in **meters**
  - 1 mm = 0.001 m = 1e-3 m
  - 1 μm = 0.000001 m = 1e-6 m
- **α (alpha):** Dimensionless Yukawa strength
  - Typically 1e-12 to 1e-3 for EP tests

## After Digitization

1. Replace `fifth_force_exclusion.csv` with your digitized file
2. Regenerate: `python scripts/fifth_force_yukawa.py`
3. Verify the plot matches the published exclusion curve
4. Update citation in paper to match the exact source you digitized

