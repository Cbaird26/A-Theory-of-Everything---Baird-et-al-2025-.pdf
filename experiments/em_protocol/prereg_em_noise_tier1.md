# Pre-registered Experimental Protocol: EM Noise Modulation Test (Tier 1)

## Objective

To test for protocol-linked modulation of electromagnetic (EM) signals during alternating neutral/coherence mental states, as predicted by the MQGT-SCF framework. This aims to constrain scalar field couplings to EM invariants (e.g., $F_{\mu\nu}F^{\mu\nu}$ or $F_{\mu\nu}\tilde{F}^{\mu\nu}$) that could manifest as tiny, protocol-locked changes in EM spectrum/noise floor/phase stability.

## Protocol Details

*   **Date/Time:** [To be filled at time of experiment]
*   **Hardware:** [SDR / Magnetometer / Audio interface + coil pickup]
*   **Total Duration:** 30-60 minutes
*   **Block Size:** 60 seconds per block (alternating neutral/coherence)
*   **Modulation Schedule:** Alternating blocks of "Neutral" ($s_t=0$) and "Coherence" ($s_t=1$) conditions.
    *   Each block corresponds to a fixed time interval (60 seconds).
    *   The experimenter will follow an external timer to switch conditions.
    *   Example sequence: Neutral (Block 1), Coherence (Block 2), Neutral (Block 3), Coherence (Block 4), ...
*   **Neutral Condition:** Sit calmly, no specific mental intent or focus on the EM measurement.
*   **Coherence Condition:** Engage in a standardized compassion/heart-coherence practice (e.g., focused breathing, generating feelings of appreciation/compassion), maintaining the practice for the duration of the block.
*   **Experimenter:** [Name/Initials]
*   **Stopping Rule:** Fixed total duration (30-60 minutes), no interim analysis or "peeking."

## Data Collection

### Hardware Setup

**Option A: Software Defined Radio (SDR)**
- Record continuous EM spectrum (e.g., RTL-SDR)
- Sample rate: [To be determined based on hardware]
- Frequency band: [Pre-registered band, e.g., 1-100 MHz or specific ISM band]
- Output: Time-series of spectral power in pre-defined bins

**Option B: Magnetometer**
- Record continuous magnetic field strength (phone magnetometer or dedicated sensor)
- Sample rate: [To be determined]
- Output: Time-series of magnetic field magnitude

**Option C: Audio Interface + Coil Pickup**
- Record continuous audio signal from EM pickup coil
- Sample rate: [e.g., 44.1 kHz]
- Output: Time-series of audio power/amplitude

### Environmental Controls

**Critical guardrails to minimize confounds:**
- Keep setup fixed (no movement of sensors during run)
- Log temperature if possible
- Keep phone/Wi-Fi/Bluetooth away from sensors
- Avoid power-line harmonics (50/60 Hz + harmonics) in analysis bands if possible
- Record any known environmental changes (e.g., AC turning on/off)

### Data Format

The output file will contain:
- `t`: Timestamp (seconds from start)
- `power` (or `magnitude` or `amplitude`): EM signal metric
- `s`: Modulation signal (0 for Neutral, 1 for Coherence)
- `block_id`: Block index (1, 2, 3, ...)

## Pre-registered Analysis Plan

### 1. Spectral Analysis (if using SDR)

**Pre-registered frequency bands:**
- Band 1: [e.g., 1-10 MHz] - Low-frequency band
- Band 2: [e.g., 10-50 MHz] - Mid-frequency band
- Band 3: [e.g., 50-100 MHz] - High-frequency band

**Computation:**
- Integrate spectral power in each pre-registered band over time windows (e.g., 1-second windows)
- Compute bandpower time-series: $P_i(t)$ for each band $i$

### 2. Modulation Fit

Fit a simple regression model:
\[
\text{Power}(t) = \alpha + \beta \cdot s(t) + \text{drift}(t) + \epsilon(t)
\]

Where:
- $\alpha$: Baseline power
- $\beta$: Protocol-linked modulation coefficient
- $\text{drift}(t)$: Linear or polynomial drift term (to account for environmental drift)
- $\epsilon(t)$: Residual noise

### 3. Statistical Tests

**Primary endpoint:**
- Estimate $\hat{\beta}$ and its standard error
- Test: $H_0: \beta = 0$ vs. $H_1: \beta \neq 0$
- Report: 95% confidence interval for $\beta$

**Stability checks (same as QRNG):**
- Block-size stability: Recompute $\hat{\beta}$ for different block sizes (e.g., 30s, 60s, 120s)
- Permutation test: Randomly shuffle $s(t)$ and recompute $\hat{\beta}$ to check for false positives
- Segmentation check: Split data into halves and compare $\hat{\beta}$ across segments

### 4. Interpretation Criteria

**Null result:**
- $\hat{\beta}$ close to zero with 95% CI containing zero
- No consistent sign across segments
- Permutation test shows no significant deviation

**Positive result (requires replication):**
- $\hat{\beta}$ significantly non-zero (95% CI excludes zero)
- Consistent sign across segments
- Survives permutation test
- Stable across block sizes

**Replication requirement:**
- Any significant finding requires immediate replication with an independent dataset under the same preregistered protocol

## Data Schema

The output CSV file (`em_modulated.csv`) will contain at least:
- `t`: (float) Time in seconds from start
- `power` (or `magnitude` or `amplitude`): (float) EM signal metric
- `s`: (integer) 0 for Neutral, 1 for Coherence
- `block_id`: (integer) Block index

## Deviations from Protocol

Any deviations from this protocol will be noted and discussed in the final report.

## Notes

- This is a Tier 1 "home-lab" test. Tier 2 (phase stability) and Tier 3 (atomic clocks, optical cavities) are future upgrades.
- The goal is to establish a bound on EM coupling parameters, not to claim discovery.
- Even null results are valuable: they constrain the parameter space.

