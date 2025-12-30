# Paper 3: QRNG Protocol Outline
## Pre-registered Protocol for Testing Scalar Field Effects in Quantum Random Number Generators

**Target Journal:** Pre-registration platform (OSF, AsPredicted) + quant-ph (arXiv:quant-ph)

**Style:** Pre-registration-friendly, neutral language, single primary endpoint

---

## 1. Introduction

### Hypothesis
- **Primary hypothesis:** Scalar consciousness field Φ_c biases QRNG outcomes
- **Directional or non-directional:** Based on theory predictions (to be specified)
- **Effect size:** |ε| > ε_max
  - **Calibrated bound (pooled):** ε_max = 0.000742 (95% CI: [0.000000, 0.001904])
  - **Note:** CI lower bound of 0.000000 is a bootstrap edge case (finite samples), not physical zero. Pooled point estimate (0.000742) is ~3× tighter than previous single-source value (0.002292).

### Motivation
- QRNG_tilt is the primary constraint bottleneck (83.3% baseline dominance)
- Testing QRNG directly tests the most limiting constraint
- Pre-registration prevents p-hacking and moving goalposts

### What This Protocol Does
- Defines one primary endpoint (QRNG tilt statistic)
- Specifies data acquisition plan (sources, conditions)
- Locks analysis pipeline (frozen code hash)
- Pre-specifies stopping rule (sample size / duration)

### What This Protocol Does NOT Do
- Claim discovery (null results are equally valuable)
- Specify expected direction (unless theory predicts it)
- Allow post-hoc changes (frozen analysis plan)

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
- **Total sample size:** N = [target number, e.g., 1,000,000]
- **Data storage:** [Format, location, backup]

---

## 3. Preprocessing + Windowing Rules

### 3.1 Data Cleaning
- **Outlier removal:** [Criteria, if any]
- **Missing data:** [Handling method]
- **Quality checks:** [Stationarity tests, independence tests]

### 3.2 Windowing
- **Window size:** [e.g., 10,000 trials per window]
- **Window overlap:** [None, 50%, etc.]
- **Rolling vs fixed:** [Specify]

### 3.3 Preprocessing Pipeline
1. Load raw data
2. Apply quality checks
3. Apply windowing
4. Compute per-window statistics
5. Aggregate to final statistic

**Frozen code:** [Git commit hash of preprocessing script]

---

## 4. Statistical Analysis Plan

### 4.1 Primary Endpoint
- **Statistic:** |ε| = |p_hat - 0.5| (absolute QRNG bias)
- **Definition:** p_hat = (number of 1s) / (total trials)
- **Computation:** [Exact formula, code reference]

### 4.2 Secondary Endpoints
- [List if any, but keep minimal]

### 4.3 Analysis Pipeline
1. Load preprocessed data
2. Compute |ε| for each window
3. Aggregate to overall |ε|
4. Compare to bound: |ε| vs ε_max
5. Compute confidence intervals (bootstrap, 95% CL)

**Frozen code:** [Git commit hash of analysis script]

### 4.4 Multiple Comparisons
- **Correction:** [Bonferroni, FDR, or explicitly no correction]
- **Rationale:** [Why this choice]

---

## 5. Stopping Rule

### 5.1 Sample Size
- **Target:** N = 1,000,000 trials (or similar)
- **Rationale:** Power analysis (if available)
- **Flexibility:** [Fixed N, or adaptive with pre-specified rule]

### 5.2 Duration
- **Alternative:** Run for [X] days continuous
- **Rationale:** [Time-based vs sample-based]

### 5.3 Early Stopping
- **Allowed:** [Yes/No]
- **If yes:** Pre-specified criteria (e.g., p < 0.001 with interim analysis)

---

## 6. Expected Effect Sizes + Null Interpretation

### 6.1 Expected Effect (If Theory Is Correct)
- **|ε| > ε_max (pooled: 0.000742):** Theory survives
- **Interpretation:** QRNG bias is detectable within experimental uncertainty

### 6.2 Null Result Interpretation
- **|ε| < ε_max (pooled: 0.000742):** Theory survives (no falsification)
- **|ε| > ε_max (upper CI: 0.001888):** Theory falsified (or needs revision)
- **Interpretation:** 
  - If |ε| < 0.000742: Theory survives, current bound is appropriate
  - If 0.000742 < |ε| < 0.001888: Theory survives but bound tightens, viable region shrinks
  - If |ε| > 0.001888: Theory falsified or requires significant revision

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
- **If |ε| > ε_max (upper CI):** Theory falsified
- **If |ε| < ε_max (lower CI):** Theory survives, but bound tightens
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
- **Preprocessing script:** [Git commit hash]
- **Analysis script:** [Git commit hash]
- **Repository:** [GitHub link]

### 9.2 Data Availability
- **Raw data:** [Where stored, how accessed]
- **Preprocessed data:** [Where stored, how accessed]
- **Results:** [Where stored, how accessed]

### 9.3 Reproducibility Hashes
- **Data hash:** SHA256 of raw data file
- **Script hash:** SHA256 of analysis script
- **Environment:** [Python version, package versions]

---

## 10. Timeline

### 10.1 Pre-registration
- **Date:** [When protocol registered]
- **Platform:** [OSF, AsPredicted, etc.]
- **Registration number:** [If applicable]

### 10.2 Data Collection
- **Start date:** [When data collection begins]
- **End date:** [When data collection ends]
- **Duration:** [Total time]

### 10.3 Analysis
- **Start date:** [When analysis begins]
- **End date:** [When analysis ends]
- **Duration:** [Total time]

### 10.4 Publication
- **Target date:** [When results will be shared]
- **Venue:** [Where results will be published]

---

## 11. Appendices

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

---

## References

- QRNG Calibration Protocol: [Link to QRNG_CALIBRATION_PROTOCOL.md]
- Constraint Engine Paper: [Link to Paper 2]
- Core Theory Paper: [Link to Paper 1]

