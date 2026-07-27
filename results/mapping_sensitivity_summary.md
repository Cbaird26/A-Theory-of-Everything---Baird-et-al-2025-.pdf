# Mapping Sensitivity Sweep Summary

**Seed:** 42
**N Points:** 100
**Real-Only Mode:** Enabled
**Git Commit:** a8c1419cd15e70fd2e6cac7794ee8776d4512756

## Results

| Mode | S_FF | Max r | Median r | p99 r | p99.9 r | Frac r>1 | Frac 0.1<r≤1 | Frac r≤0.1 | Scale to r=0.1 | Scale to r=1 |
|------|------|-------|----------|-------|---------|----------|---------------|-------------|----------------|--------------|
| A | 1.0e+00 | 4.012e-11 | 3.399e-31 | 4.278e-12 | 3.654e-11 | 0.000e+00 | 0.000e+00 | 1.000e+00 | 2.492e+09 | 2.492e+10 |
| B | 1.0e+00 | 8.025e-11 | 6.799e-31 | 8.557e-12 | 7.308e-11 | 0.000e+00 | 0.000e+00 | 1.000e+00 | 1.246e+09 | 1.246e+10 |
| C | 1.0e-01 | 4.012e-12 | 3.399e-32 | 4.278e-13 | 3.654e-12 | 0.000e+00 | 0.000e+00 | 1.000e+00 | 2.492e+10 | 2.492e+11 |
| C | 1.0e+00 | 4.012e-11 | 3.399e-31 | 4.278e-12 | 3.654e-11 | 0.000e+00 | 0.000e+00 | 1.000e+00 | 2.492e+09 | 2.492e+10 |
| C | 1.0e+01 | 4.012e-10 | 3.399e-30 | 4.278e-11 | 3.654e-10 | 0.000e+00 | 0.000e+00 | 1.000e+00 | 2.492e+08 | 2.492e+09 |
| C | 1.0e+02 | 4.012e-09 | 3.399e-29 | 4.278e-10 | 3.654e-09 | 0.000e+00 | 0.000e+00 | 1.000e+00 | 2.492e+07 | 2.492e+08 |
| C | 1.0e+03 | 4.012e-08 | 3.399e-28 | 4.278e-09 | 3.654e-08 | 0.000e+00 | 0.000e+00 | 1.000e+00 | 2.492e+06 | 2.492e+07 |
| C | 1.0e+04 | 4.012e-07 | 3.399e-27 | 4.278e-08 | 3.654e-07 | 0.000e+00 | 0.000e+00 | 1.000e+00 | 2.492e+05 | 2.492e+06 |

## Interpretation

- **Max r:** Maximum detectability ratio across all sampled points
- **Scale to r=0.1:** Multiplicative factor needed on α_pred to reach r=0.1 (near-detectable)
- **Scale to r=1:** Multiplicative factor needed on α_pred to reach r=1 (exclusion boundary)
- **Fraction r>1:** Fraction of points excluded (r > 1)
- **Fraction 0.1<r≤1:** Fraction in hunt band (near-detectable)
- **Fraction r≤0.1:** Fraction safely below detectability threshold

**Conclusion:** If max_r << 1 across all modes and S_FF values, the 'undetectable' conclusion is robust to mapping uncertainty.
