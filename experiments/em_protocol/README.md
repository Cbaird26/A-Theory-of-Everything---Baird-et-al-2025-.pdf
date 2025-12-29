# EM Protocol Testing — Tier 1 (Home-Lab)

This directory contains the preregistration, analysis scripts, and data collection protocols for testing protocol-linked EM modulation as predicted by the MQGT-SCF framework.

## Quick Start

### 1. Preregister Your Protocol

Read `prereg_em_noise_tier1.md` and fill in:
- Hardware type (SDR / Magnetometer / Audio interface)
- Frequency bands (if using SDR)
- Duration and block size
- Date/time

### 2. Collect Data

Run your alternating protocol (60s neutral / 60s coherence) and record:
- Timestamped EM signal (power/magnitude/amplitude)
- Modulation signal `s(t)` (0 for neutral, 1 for coherence)
- Block IDs

Save as CSV with columns: `t`, `power` (or `magnitude`/`amplitude`), `s`, `block_id` (optional)

### 3. Analyze

```bash
python analyze_em.py --data data/raw/em_modulated.csv --out-dir results/em_run1
```

This will:
- Fit modulation model: `Power(t) = α + β*s(t) + drift(t) + noise`
- Run permutation test
- Test block-size stability
- Generate plots and JSON summary

### 4. Generate LaTeX Snippet

```bash
python generate_em_snippet.py --json results/em_run1/em_modulation_summary.json --out em_modulation_snippet.tex
```

## Hardware Options

### Option A: Software Defined Radio (SDR)
- **Hardware:** RTL-SDR (~$30) or similar
- **Software:** GQRX, SDR#, or Python `rtlsdr` library
- **Output:** Spectral power in pre-registered frequency bands

### Option B: Magnetometer
- **Hardware:** Phone magnetometer or dedicated sensor (e.g., HMC5883L)
- **Output:** Magnetic field magnitude time-series

### Option C: Audio Interface + Coil Pickup
- **Hardware:** Audio interface + simple coil antenna
- **Output:** Audio power/amplitude time-series

## Analysis Pipeline

The analysis script (`analyze_em.py`) performs:

1. **Modulation Fit:** Linear regression with drift terms
   - Estimates `β` (modulation coefficient)
   - 95% confidence intervals
   - t-statistic and p-value

2. **Permutation Test:** Randomly shuffle `s(t)` and recompute `β`
   - Tests for false positives
   - Returns permutation p-value

3. **Block Size Stability:** Test `β` across different block sizes
   - Checks robustness to segmentation

4. **Visualization:** Time-series plots with fitted modulation overlay

## Interpretation

**Null Result:**
- `β` close to zero with 95% CI containing zero
- Permutation test shows no significant deviation
- Stable across block sizes

**Positive Result (requires replication):**
- `β` significantly non-zero (95% CI excludes zero)
- Survives permutation test
- Consistent across block sizes
- **Must replicate before interpretation**

## Guardrails

**Environmental confounds to control:**
- Wi-Fi / Bluetooth / phones (keep away from sensors)
- Power-line harmonics (50/60 Hz)
- Temperature drift (log if possible)
- Body motion artifacts (keep setup fixed)

**Discipline:**
- Keep setup fixed
- Log temperature if possible
- Run sham sessions (randomized schedule) if possible
- Use same "block-stability" and permutation checks as QRNG

## Next Steps

- **Tier 2:** Phase stability test (crystal oscillator, frequency counter)
- **Tier 3:** Real physics lab channels (atomic clocks, optical cavities, SQUID magnetometers)

## Files

- `prereg_em_noise_tier1.md` - Preregistration document
- `analyze_em.py` - Analysis script
- `generate_em_snippet.py` - LaTeX snippet generator
- `README.md` - This file

## Example Workflow

```bash
# 1. Collect data (save as CSV)
# ... run protocol, record data ...

# 2. Analyze
python analyze_em.py --data data/raw/em_modulated.csv --out-dir results/em_run1

# 3. Generate LaTeX snippet
python generate_em_snippet.py --json results/em_run1/em_modulation_summary.json

# 4. Check results
cat results/em_run1/em_modulation_summary.json
```

## Notes

- This is a Tier 1 "home-lab" test. Even null results are valuable: they constrain the parameter space.
- The goal is to establish bounds on EM coupling parameters, not to claim discovery.
- Any significant finding requires immediate replication.

