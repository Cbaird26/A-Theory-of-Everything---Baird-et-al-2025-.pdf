# Pre-Registration Protocol: QRNG Tilt Measurement
## Testing Scalar Field Effects in Quantum Random Number Generators

**Registration Date:** 2025-12-29  
**Registration Platform:** [OSF / AsPredicted - to be registered]  
**Registration Number:** [To be assigned]

---

## 1. Primary Hypothesis

**Primary hypothesis:** Scalar consciousness field Φ_c biases QRNG outcomes, detectable as a deviation from perfect randomness (p = 0.5).

**Directional or non-directional:** Non-directional (we test |ε| ≠ 0, not ε > 0 or ε < 0)

**Effect size threshold:** |ε| > ε_max
- **Calibrated bound (pooled point estimate):** ε_max = 0.000742
- **95% CI (bootstrap):** [0.000000, 0.001904]
- **Note:** CI lower bound of 0.000000 is a bootstrap edge case due to finite-sample effects, not a physical zero. Pooled point estimate (0.000742) is the primary calibrated value.

**Theoretical prediction:** MQGT-SCF constraint engine identifies QRNG_tilt as the primary bottleneck (83.3% baseline dominance) under calibrated bounds, making QRNG experiments the highest-leverage test of the theory.

---

## 2. Experimental Setup

### 2.1 QRNG Source
- **Primary source:** [Specify: NIST Beacon, LfD API, local hardware, etc.]
- **Backup sources:** [List alternatives if primary fails]
- **Source characteristics:**
  - Bit rate: [bits/second]
  - Output format: [binary, decimal, etc.]
  - Access method: [API, file download, hardware interface]

### 2.2 Experimental Conditions
- **Baseline condition:** Standard QRNG operation (no special setup)
- **Test condition:** [If applicable: meditator present, ethical biasing, etc.]
- **Controls:** [Blinding, randomization, etc.]

### 2.3 Data Acquisition
- **Sampling rate:** [trials per second]
- **Total duration:** [days/weeks]
- **Total sample size:** N = 1,000,000 trials (target)
- **Data storage:** [Format, location, backup]

---

## 3. Preprocessing + Windowing Rules

### 3.1 Data Cleaning
- **Outlier removal:** [Criteria, if any]
- **Missing data:** [Handling method]
- **Quality checks:** [Stationarity tests, independence tests]

### 3.2 Windowing
- **Window size:** 10,000 trials per window (or full sequence if N < 10,000)
- **Window overlap:** None (non-overlapping windows)
- **Rolling vs fixed:** Fixed windows

### 3.3 Preprocessing Pipeline
1. Load raw data
2. Apply quality checks (stationarity, independence)
3. Apply windowing (if N > 10,000)
4. Compute per-window statistics
5. Aggregate to final statistic

**Frozen code:** [Git commit hash of preprocessing script - to be filled at registration]

---

## 4. Statistical Analysis Plan

### 4.1 Primary Endpoint
- **Statistic:** |ε| = |p_hat - 0.5| (absolute QRNG bias)
- **Definition:** p_hat = (number of 1s) / (total trials)
- **Computation:** [Exact formula, code reference]

### 4.2 Secondary Endpoints
- None (single primary endpoint to avoid multiple comparisons issues)

### 4.3 Analysis Pipeline
1. Load preprocessed data
2. Compute |ε| for each window (or full sequence)
3. Aggregate to overall |ε|
4. Compare to bound: |ε| vs ε_max
5. Compute confidence intervals (bootstrap, 95% CL)

**Frozen code:** [Git commit hash of analysis script - to be filled at registration]

**Analysis script location:** `experiments/constraints/scripts/calibrate_qrng_multisource.py`

### 4.4 Multiple Comparisons
- **Correction:** None (single primary endpoint)
- **Rationale:** Single endpoint eliminates multiple comparisons concerns

### 4.5 Sensitivity Analysis
- **Report results under both bounds:**
  - Pooled point estimate: ε_max = 0.000742
  - Upper CI: ε_max = 0.001904
- **Interpretation:**
  - If |ε| < 0.000742: Theory survives (no falsification)
  - If 0.000742 < |ε| < 0.001904: Theory survives but bound tightens, viable region shrinks
  - If |ε| > 0.001904: Theory falsified or requires significant revision

---

## 5. Stopping Rule

### 5.1 Sample Size
- **Target:** N = 1,000,000 trials
- **Rationale:** Provides sufficient power to detect |ε| > 0.000742 with high confidence
- **Flexibility:** Fixed N (no adaptive stopping)

### 5.2 Duration
- **Alternative:** Run for [X] days continuous (if time-based)
- **Rationale:** [Time-based vs sample-based]

### 5.3 Early Stopping
- **Allowed:** No
- **Rationale:** Prevents optional stopping bias

---

## 6. Expected Effect Sizes + Null Interpretation

### 6.1 Expected Effect (If Theory Is Correct)
- **|ε| > ε_max (pooled: 0.000742):** Theory survives
- **Interpretation:** QRNG bias is detectable within experimental uncertainty

### 6.2 Null Result Interpretation
- **|ε| < ε_max (pooled: 0.000742):** Theory survives (no falsification)
- **|ε| > ε_max (upper CI: 0.001904):** Theory falsified (or needs revision)
- **Interpretation:** 
  - If |ε| < 0.000742: Theory survives, current bound is appropriate
  - If 0.000742 < |ε| < 0.001904: Theory survives but bound tightens, viable region shrinks
  - If |ε| > 0.001904: Theory falsified or requires significant revision

### 6.3 Effect Size Ranges
- **Small:** |ε| ~ 0.0001 (barely detectable)
- **Medium:** |ε| ~ 0.001 (clearly detectable)
- **Large:** |ε| > 0.01 (strong signal)

---

## 7. Blinding + Randomization

### 7.1 Blinding
- **Experimenter blinding:** [Yes/No, how]
- **Analysis blinding:** [Yes/No, how]
- **Rationale:** [Prevent bias]

### 7.2 Randomization
- **Trial order:** [Randomized?]
- **Condition order:** [If applicable: A-B-A, etc.]
- **Rationale:** [Control for time-dependent effects]

---

## 8. What Would Change Our Mind?

### 8.1 Falsification Criteria
- **If |ε| > ε_max (upper CI: 0.001904):** Theory falsified
- **If |ε| < ε_max (pooled: 0.000742):** Theory survives, but bound tightens if |ε| > pooled
- **If |ε| ≈ ε_max:** Inconclusive, need more data

### 8.2 Revision Criteria
- **If preprocessing fails:** Revise preprocessing (document changes)
- **If source fails:** Switch to backup source (document switch)
- **If analysis bug found:** Fix and re-run (document fix)

### 8.3 Commitment to Publish
- **Null results:** Will publish regardless of outcome
- **Publication venue:** [OSF, arXiv, journal, etc.]
- **Timeline:** [When results will be shared]

---

## 9. Reproducibility

### 9.1 Frozen Code
- **Preprocessing script:** [Git commit hash - to be filled at registration]
- **Analysis script:** [Git commit hash - to be filled at registration]
- **Repository:** [GitHub link]

### 9.2 Data Availability
- **Raw data:** [Where stored, how accessed]
- **Preprocessed data:** [Where stored, how accessed]
- **Results:** [Where stored, how accessed]

### 9.3 Reproducibility Hashes
- **Data hash:** SHA256 of raw data file (to be computed)
- **Script hash:** SHA256 of analysis script (to be computed)
- **Environment:** [Python version, package versions]

### 9.4 Calibration Provenance
- **Calibration source:** Multi-source QRNG calibration (`QRNG_CALIBRATION.json`)
- **Calibration script:** `experiments/constraints/scripts/calibrate_qrng_multisource.py`
- **Calibration hash:** [To be filled]
- **Calibration date:** 2025-12-29

---

## 10. Sensitivity to Calibration Uncertainty

### 10.1 Why This Matters
The constraint engine analysis shows that the baseline bottleneck **flips** depending on ε_max:
- **Pooled (ε_max = 0.000742):** QRNG_tilt 83.3% (dominant), ATLAS_mu 16.7%
- **Upper CI (ε_max = 0.001904):** Fifth_force 83.3% (dominant), ATLAS_mu 16.7%, QRNG_tilt 0%

This demonstrates that **experimental calibration of ε_max is the highest-leverage empirical uncertainty** for the theory.

### 10.2 Pre-Registration Commitment
We commit to:
1. Report results under both bounds (pooled + upper CI)
2. Not cherry-pick the bound that makes the theory look best
3. Explicitly state which bound was used for each analysis
4. Update calibration if new data becomes available

---

## 11. Timeline

### 11.1 Pre-registration
- **Date:** 2025-12-29
- **Platform:** [OSF, AsPredicted, etc.]
- **Registration number:** [If applicable]

### 11.2 Data Collection
- **Start date:** [When data collection begins]
- **End date:** [When data collection ends]
- **Duration:** [Total time]

### 11.3 Analysis
- **Start date:** [When analysis begins]
- **End date:** [When analysis ends]
- **Duration:** [Total time]

### 11.4 Publication
- **Target date:** [When results will be shared]
- **Venue:** [Where results will be published]

---

## 12. Appendices

### A. Power Analysis
- **Effect size assumptions:** [What effect sizes are detectable]
- **Sample size calculation:** [How N was chosen]
- **Power curves:** [If available]

### B. Preprocessing Details
- **Full preprocessing code:** [Complete script]
- **Quality check criteria:** [Detailed criteria]
- **Window size sensitivity:** [How window size affects results]

### C. Analysis Details
- **Full analysis code:** [Complete script]
- **Bootstrap procedure:** [Detailed method]
- **Confidence interval computation:** [Detailed method]

### D. Calibration Details
- **Calibration protocol:** See `QRNG_CALIBRATION_PROTOCOL.md`
- **Calibration results:** See `QRNG_CALIBRATION.json`
- **Calibration plot:** See `QRNG_CALIBRATION.png`

---

## References

- QRNG Calibration Protocol: `experiments/constraints/results/QRNG_CALIBRATION_PROTOCOL.md`
- Constraint Engine Paper: Paper 2 (PAPER_2_CONSTRAINT_ENGINE_OUTLINE.md)
- Core Theory Paper: Paper 1 (PAPER_1_CORE_THEORY_OUTLINE.md)
- High-Resolution Phase Diagram: `experiments/constraints/results/HIGH_RES_PHASE_DIAGRAM_SUMMARY.md`

