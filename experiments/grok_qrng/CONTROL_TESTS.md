# Control Test Files

This directory contains control test files to validate the QRNG analysis pipeline.

## Test Files

1. **CONTROL_random_200k.csv** - Known-fair coin (p=0.5)
   - Expected: BF10 ≈ 1, epsilon_hat ≈ 0
   - Validates that the pipeline doesn't create false positives

2. **CONTROL_bias_p505_200k.csv** - Known-biased coin (p=0.505)
   - Expected: BF10 > 1 (substantial), epsilon_hat ≈ +0.005
   - Validates that the pipeline can detect real bias

## Running Control Tests

```bash
# Run analysis on control files
python analyze_qrng.py --data-dir data/raw --out-dir results --prior 1.0

# Run sanity checks
python sanity_checks.py --summary results/summary.csv --global results/global_summary.json

# Check results
cat results/global_summary.json
```

## Expected Results

### CONTROL_random_200k.csv
- `BF10`: Should be near 1 (0.5 to 2.0 is typical for fair coin)
- `epsilon_hat`: Should be very close to 0 (within ~0.001)
- Cumulative epsilon plot: Should wobble around 0 with no persistent drift

### CONTROL_bias_p505_200k.csv
- `BF10`: Should be clearly > 1 (often 10-100+ for this bias level)
- `epsilon_hat`: Should be around +0.005
- Cumulative epsilon plot: Should show persistent positive drift

## If Control Tests Fail

If the known-fair file shows strong bias (BF10 >> 1), check:
1. Random number generator seed (should be different each run)
2. Parser logic (verify bits are being read correctly)
3. Statistical calculations (Beta-Binomial marginal likelihood)

If the known-biased file doesn't show bias (BF10 ≈ 1), check:
1. Sample size (200k should be sufficient for p=0.505)
2. Prior strength (try --prior 0.5 or --prior 2.0)
3. Statistical calculations

## After Control Tests Pass

Once both control files behave as expected, the pipeline is validated and ready for real QRNG data.

