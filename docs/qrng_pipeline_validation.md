# QRNG Pipeline Validation on Synthetic Controls

**Date:** 2026-01-01  
**Repository:** MQGT-SCF  
**Commit:** `84daf2e`  
**Python:** `Python 3.12.3`  
**OS:** `Linux hds-el18e6eee4vo 4.4.0 #1 SMP Sun Jan 10 15:06:54 PST 2016 x86_64 x86_64 x86_64 GNU/Linux`  

**Command(s):**
- `python calibrate_qrng_physics.py --fair CONTROL_random_200k.csv --biased CONTROL_bias_p505_200k.csv --priors 0.5,1.0,2.0`
- `python calibrate_qrng_physics.py --mixed CONTROL_random_200k.csv,CONTROL_bias_p505_200k.csv`

---

## Purpose

This document validates the QRNG bias-detection pipeline using two synthetic control datasets:

1) A **fair** control dataset (no bias)  
2) A **known-biased** control dataset (p = 0.505)

This calibration ensures the pipeline:
- does **not** hallucinate bias in fair data, and
- does detect bias when bias is present,
- with conclusions robust to reasonable prior choices.

---

## Definitions

Let:

- \( p \) = probability of observing a "1"  
- \( \hat{p} \) = empirical estimate of \( p \)  
- \( \epsilon = p - 0.5 \)  
- \( \hat{\epsilon} = \hat{p} - 0.5 \)

We report:

- **ε̂ (epsilon_hat)**: estimated bias in probability space  
- **BF10**: Bayes factor comparing bias model (H1) vs no-bias (H0)  
  - BF10 > 1 favors bias  
  - BF10 < 1 favors no bias  
- **95% CI (ε)**: 95% credible interval for ε

---

## Control Datasets

### Fair control (expected ε ≈ 0)
- File: `CONTROL_random_200k.csv`  
- N: 200,000 bits  

### Biased control (expected ε = +0.005)
- File: `CONTROL_bias_p505_200k.csv`  
- N: 200,000 bits  

---

## Results (Primary)

| Dataset | N | p_hat | epsilon_hat (ε̂) | BF10 | 95% CI for ε | Expected |
|---|---:|---:|---:|---:|---:|---|
| Fair control | 200,000 | 0.499245 | -0.000755 | 0.00528 | [-0.002946, 0.001436] | CI includes 0, BF10 ≪ 1 |
| Biased control (p=0.505) | 200,000 | 0.50457 | +0.00457 | 17.85 | [0.002379, 0.006761] | CI > 0, BF10 ≫ 1 |

### Combined sanity behavior (expected mixture effect)

When combining both files (400,000 total bits), the fair file pulls the global evidence toward the null:

- Total N: 400,000  
- epsilon_hat: +0.0019  
- BF10: 0.0546  

This is expected for a mixed dataset: combining fair + biased data reduces global evidence for bias.

---

## Prior Robustness

Priors tested: **0.5, 1.0, 2.0**

- Fair control: BF10 remains **< 1/3** across all priors  
- Biased control: BF10 remains **> 10** across all priors  

Conclusion: qualitative results are robust to prior scale choice.

---

## Sanity Checks

- File-by-file consistency checks: **PASS**  
- Mixed evidence warning: expected (one file favors bias, one favors null)  
- Small file warning: `.gitkeep` only (harmless)  

---

## Scope and Limitations

This validation confirms the pipeline's statistical behavior on synthetic controls: it can reject bias when none is present and detect bias when present.

This document does not, by itself, establish any causal interpretation for bias in real QRNG data. Interpretation of real-world results requires careful controls, multi-source replication, and pre-registered analysis plans.

---

## Conclusion

The pipeline is calibrated:

- It rejects bias on fair control data (BF10 ≪ 1).  
- It detects bias on known-biased control data (BF10 ≫ 1).  
- Credible intervals behave correctly (contain 0 for fair; strictly > 0 for biased).  
- Conclusions are robust across reasonable prior scales.  

This validation supports using the same pipeline on real QRNG logs and reporting ε̂, BF10, and credible intervals as publication-grade outputs.

---

## Appendix: Reproduction Notes

To reproduce this validation:

1) Ensure control datasets are present:
- `CONTROL_random_200k.csv`
- `CONTROL_bias_p505_200k.csv`

2) Run:
- `python calibrate_qrng_physics.py --fair CONTROL_random_200k.csv --biased CONTROL_bias_p505_200k.csv --priors 0.5,1.0,2.0`
- `python calibrate_qrng_physics.py --mixed CONTROL_random_200k.csv,CONTROL_bias_p505_200k.csv`

3) Confirm the result table above matches within rounding error.

