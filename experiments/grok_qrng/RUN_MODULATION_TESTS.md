# Run Modulation Tests

## Quick Reference Commands

### AB Test (Two Independent Pulls)

```bash
cd experiments/grok_qrng

# Run A: Neutral condition
./fetch_lfdr_qrng_bits.py --n-bits 200000 --out data/raw/lfdr_A_neutral/bits.txt
./quick_run.sh lfdr_A_neutral

# [Perform coherence practice for ~3 minutes]

# Run B: Coherence condition  
./fetch_lfdr_qrng_bits.py --n-bits 200000 --out data/raw/lfdr_B_coherence/bits.txt
./quick_run.sh lfdr_B_coherence

# Compare results
cat results/lfdr_A_neutral/global_summary.json
cat results/lfdr_B_coherence/global_summary.json
```

### Within-Run Modulation (Single Pull with Embedded Signal)

```bash
cd experiments/grok_qrng

# Create modulated dataset (clock-driven: 60s neutral, 60s coherence, repeat)
./fetch_lfdr_modulated.py \
  --n-bits 400000 \
  --block-size 4000 \
  --protocol alternating \
  --out data/raw/lfdr_withinrun/modulated.csv

# Analyze (pipeline auto-detects 's' column and fits modulation)
./quick_run.sh lfdr_withinrun

# Check results
cat results/lfdr_withinrun/global_summary.json
head -n 12 results/lfdr_withinrun/summary.csv
```

## What Counts as "Signal"

For within-run modulation, check:

1. **Primary:** `mod_beta` coefficient in `summary.csv`
   - Sign: positive = coherence increases p, negative = decreases p
   - Magnitude: non-zero suggests modulation

2. **Stability:** Run with different block sizes (2k vs 4k bits)
   - If `mod_beta` is consistent across block sizes → more robust

3. **Visual:** Check cumulative epsilon plot
   - Should show correlation with s signal if modulation exists

## Interpretation Guide

After running, paste:
- `results/lfdr_withinrun/global_summary.json`
- First ~12 lines of `results/lfdr_withinrun/summary.csv`

Classification:
- **Null** → Publish as stronger bound on modulation (and η)
- **Bias-like but artifact-suspect** → Run block stability + permutation check
- **Bias-like and robust** → Replicate immediately (same prereg, same N)

## Clock-Driven Protocol (Important)

For within-run modulation:
- Use external timer (phone/computer)
- 60 seconds neutral → switch to coherence
- 60 seconds coherence → switch to neutral
- Repeat
- **No "vibe" adjustments** - follow the timer like a robot
- Block assignment is automatic; your job is just to follow the timer

