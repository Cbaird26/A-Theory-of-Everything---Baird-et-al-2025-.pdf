# Next Experiments: Modulation Testing

## Current Status

✅ **Baseline constraint established:**
- Real QRNG (LfD/ID Quantique): 200k bits
- Result: Null (BF10 = 0.00386, epsilon_hat = -0.000895)
- Constraint: |epsilon| < 0.003086 (95% CI)
- **Publishable as experimental bound on η**

## Next Steps: Testing the Modulation Hypothesis

The baseline constrains constant bias. To test the operational link:
**ε ∝ η(ΔE - ⟨ΔE⟩)**

we need experiments with **registered modulation signals**.

---

## Experiment 1: AB Test (Two Independent Runs)

**Protocol:**
- Run A (neutral): 200k bits, no special intent, baseline condition
- Run B (coherence): 200k bits, during compassion/heart-coherence practice

**Steps:**
```bash
# Create folders
mkdir -p data/raw/lfdr_A_neutral data/raw/lfdr_B_coherence

# Fetch Run A (neutral condition)
./fetch_lfdr_qrng_bits.py --n-bits 200000 --out data/raw/lfdr_A_neutral/lfdr_bits.txt

# [Perform coherence practice for ~3 minutes]

# Fetch Run B (coherence condition)
./fetch_lfdr_qrng_bits.py --n-bits 200000 --out data/raw/lfdr_B_coherence/lfdr_bits.txt

# Analyze each
./quick_run.sh lfdr_A_neutral
./quick_run.sh lfdr_B_coherence

# Compare results
cat results/lfdr_A_neutral/global_summary.json
cat results/lfdr_B_coherence/global_summary.json
```

**Publishable outcomes:**
- Both null → constrains modulation too
- One shifts → testable lead (requires replication)

---

## Experiment 2: Within-Run Modulation (Strongest Test)

**Protocol:**
- Single 400k-bit pull from LfD
- Split into blocks (e.g., 100 blocks of 4k bits)
- Assign modulation signal: s=0 (neutral) vs s=+1 (coherence)
- Alternating: 1 minute neutral, 1 minute coherence, repeat

**Steps:**
```bash
# Create modulated dataset
./fetch_lfdr_modulated.py \
  --n-bits 400000 \
  --block-size 4000 \
  --protocol alternating \
  --out data/raw/lfdr_modulated/lfdr_modulated.csv

# Analyze (pipeline auto-detects 's' column and fits modulation)
./quick_run.sh lfdr_modulated

# Check modulation fit in summary.csv
cat results/lfdr_modulated/summary.csv | grep mod_
```

**What to look for:**
- `mod_beta` coefficient: if significantly non-zero, suggests modulation
- `mod_loglik`: compare to null model
- Cumulative epsilon plot: should show correlation with s signal

**Why this is strongest:**
- Reduces "different day, different context" confounds
- Single continuous dataset
- Explicit modulation signal allows direct test of ε ∝ η(ΔE - ⟨ΔE⟩)

---

## Paper Language (Current Result)

You can already write:

> "We report a baseline constraint using hardware QRNG (ID Quantique source via LfD API). We analyzed n=200,000 bits using a Beta-Binomial Bayesian model comparing the fair-coin null (p=1/2) to a symmetric Beta prior alternative. The maximum-likelihood bias estimate was ε̂ = -8.95×10⁻⁴, with 95% credible interval [-3.086×10⁻³, 1.296×10⁻³]. The Bayes factor was BF₁₀ = 3.86×10⁻³, indicating strong evidence against bias relative to the fair-coin null. These results constrain the effective ethical-bias strength η in the small-bias regime, with null-consistent outcomes mapping to upper bounds on |η| under the operational link ε ∝ η(ΔE - ⟨ΔE⟩)."

---

## Status

- ✅ Baseline constraint: **Complete and publishable**
- ⏳ AB test: Ready to run (requires two separate pulls)
- ⏳ Within-run modulation: Script ready, requires single pull + protocol

The framework is now **testable and constrained**. Next experiments probe the modulation hypothesis directly.

