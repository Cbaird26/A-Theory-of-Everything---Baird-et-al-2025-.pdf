# Preregistration: Within-Run Modulation Test

**Date:** [Fill in when running]  
**Protocol ID:** lfdr_withinrun_001

## Source
- **QRNG Provider:** LfD (Laboratory for Digitalisation)
- **Hardware:** ID Quantique QRNG (PCIe)
- **API:** https://lfdr.de/qrng_api/qrng

## Sample Size
- **Total bits:** 400,000
- **Block size:** 4,000 bits per block
- **Number of blocks:** 100

## Protocol
- **Schedule:** Alternating blocks
  - Block 0, 2, 4, ... (even): Neutral condition (s=0)
  - Block 1, 3, 5, ... (odd): Coherence condition (s=+1)
- **Timing:** Clock-driven
  - 60 seconds neutral
  - 60 seconds coherence
  - Repeat (follow external timer, no "vibe" adjustments)

## Primary Endpoint
- **Modulation coefficient:** `mod_beta` from logistic regression fit
- **Direction:** Sign of `mod_beta` (positive = coherence increases p, negative = decreases p)
- **Null hypothesis:** `mod_beta = 0` (no modulation)

## Secondary Endpoints
- Stability across block size choices (sensitivity analysis: 2k vs 4k bits per block)
- Bayes factor for modulated model vs constant-bias model

## Stopping Rule
- **Fixed N:** 400,000 bits (no peeking, no early stopping)
- **Analysis:** Run once after all data collected

## Analysis Plan
1. Fit logistic modulation model: `p_t = sigmoid(alpha + beta * s_t)`
2. Extract `mod_beta` and its sign
3. Compare to null (beta=0)
4. Generate LaTeX snippet with results

## Expected Outcomes
- **Null:** `mod_beta ≈ 0` → Stronger bound on modulation (and η)
- **Signal:** `mod_beta` significantly non-zero → Testable lead (requires replication)

