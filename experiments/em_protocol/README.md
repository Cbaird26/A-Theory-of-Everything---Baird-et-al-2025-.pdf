# EM Protocol Testing — Tier 1 (Home-Lab)

This directory contains the preregistration, analysis scripts, and data collection protocols for testing protocol-linked EM modulation as predicted by the MQGT-SCF framework.

## 🚀 Quick Start: Phone Magnetometer Test (30 minutes)

**Goal:** Record magnetometer data, convert to analysis format, run analysis.

### Step 1: Record Magnetometer Data

**Setup:**
- Phone in **airplane mode**
- Place on stable surface (don't touch it)
- Keep away from chargers, speakers, laptops, big metal objects
- Use any sensor logger app that exports CSV with:
  - `mx, my, mz` (magnetic field components, usually in µT)
  - `t` or `time` or `timestamp` (optional, can use `--sample-hz` instead)

**Protocol:**
- Record for **30 minutes**
- **60s neutral / 60s coherence** alternating (use external timer)
- Export CSV to your computer

**Recommended apps:**
- **iOS:** SensorLog, Physics Toolbox Suite
- **Android:** Sensor Logger, Physics Toolbox Suite

### Step 2: Convert Raw CSV → Analysis Format

```bash
# If CSV has timestamps:
python prep_magnetometer_csv.py --in /path/to/raw_mag.csv --out data/raw/em_modulated.csv --block-sec 60 --start 0

# If CSV has no timestamps (provide sample rate):
python prep_magnetometer_csv.py --in /path/to/raw_mag.csv --out data/raw/em_modulated.csv --sample-hz 10 --block-sec 60 --start 0
```

This will:
- Extract `mx, my, mz` columns (handles various naming conventions)
- Compute magnetic field magnitude: `|B| = sqrt(mx² + my² + mz²)`
- Bin into 1-second windows
- Compute "power" as within-second standard deviation of `|B|`
- Add protocol label `s(t)` (0=neutral, 1=coherence) based on alternating blocks

### Step 3: Analyze

```bash
python analyze_em.py --data data/raw/em_modulated.csv --out-dir results/em_run1
```

This will:
- Fit modulation model: `Power(t) = α + β*s(t) + drift(t) + noise`
- Run permutation test (1000 shuffles)
- Test block-size stability
- Generate plots and JSON summary

### Step 4: Generate LaTeX Snippet

```bash
python generate_em_snippet.py --json results/em_run1/em_modulation_summary.json --out em_modulation_snippet.tex
```

---

## Full Workflow (All Hardware Options)

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
- `prep_magnetometer_csv.py` - Convert raw magnetometer CSV → analysis format
- `analyze_em.py` - Analysis script
- `generate_em_snippet.py` - LaTeX snippet generator
- `README.md` - This file

## Example Workflow (Magnetometer)

```bash
# 1. Record magnetometer data (30 min, alternating protocol)
# ... use sensor app, export CSV ...

# 2. Convert to analysis format
python prep_magnetometer_csv.py --in raw_magnetometer.csv --out data/raw/em_modulated.csv --block-sec 60 --start 0

# 3. Analyze
python analyze_em.py --data data/raw/em_modulated.csv --out-dir results/em_run1

# 4. Generate LaTeX snippet
python generate_em_snippet.py --json results/em_run1/em_modulation_summary.json

# 5. Check results
cat results/em_run1/em_modulation_summary.json
ls results/em_run1/em_modulation_plot.png
```

## Notes

- This is a Tier 1 "home-lab" test. Even null results are valuable: they constrain the parameter space.
- The goal is to establish bounds on EM coupling parameters, not to claim discovery.
- Any significant finding requires immediate replication.

