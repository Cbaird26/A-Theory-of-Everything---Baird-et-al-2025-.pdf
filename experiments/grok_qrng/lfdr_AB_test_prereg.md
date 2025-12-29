# Preregistration: AB Test (Neutral vs Coherence)

**Date:** [Fill in when running]  
**Protocol ID:** lfdr_AB_001

## Source
- **QRNG Provider:** LfD (Laboratory for Digitalisation)
- **Hardware:** ID Quantique QRNG (PCIe)
- **API:** https://lfdr.de/qrng_api/qrng

## Sample Size
- **Run A (Neutral):** 200,000 bits
- **Run B (Coherence):** 200,000 bits
- **Total:** 400,000 bits

## Protocol
- **Run A (Neutral):**
  - Condition: Baseline, no special intent
  - Duration: ~3 minutes (time to fetch 200k bits)
  - Posture: Standard seated position
  - Intent: Neutral observation

- **Run B (Coherence):**
  - Condition: Compassion/heart-coherence practice
  - Duration: ~3 minutes (time to fetch 200k bits)
  - Posture: Same as Run A
  - Intent: Standardized coherence practice (pre-registered method)

## Primary Endpoint
- **Comparison:** Difference in `epsilon_hat` between Run A and Run B
- **Null hypothesis:** `epsilon_A = epsilon_B` (no difference between conditions)

## Secondary Endpoints
- Individual Bayes factors for each run
- Combined analysis (if appropriate)

## Stopping Rule
- **Fixed N:** 200k bits per run (no peeking, no early stopping)
- **Analysis:** Run once after both runs complete

## Analysis Plan
1. Analyze Run A independently: `./quick_run.sh lfdr_A_neutral`
2. Analyze Run B independently: `./quick_run.sh lfdr_B_coherence`
3. Compare `epsilon_hat` values and credible intervals
4. Check for overlap in 95% CIs

## Expected Outcomes
- **Both null:** Constrains modulation too (publishable as stronger bound)
- **One shifts:** Testable lead (requires replication with same protocol)

