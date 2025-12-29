# QRNG Analysis Pipeline

## Quick Start

1. **Install dependencies** (one-time):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -U pip
   pip install -r requirements.txt
   ```

2. **Drop your QRNG data files** into `data/raw/`:
   - CSV files (columns: `bit`, `b`, `outcome`, etc.)
   - JSON/JSONL files (objects with `bit`/`b`/`outcome` keys)
   - Plain text files with 0/1 bitstrings
   - Optional: include `t`/`time` for timestamps, `s`/`mod`/`signal` for modulation

3. **Run the analysis**:
   ```bash
   python analyze_qrng.py --data-dir data/raw --out-dir results --prior 1.0
   ```

## Output Files

- `results/summary.csv` - Per-file bias statistics and Bayes factors
- `results/global_summary.json` - Global aggregated results
- `results/*_cumulative_epsilon.png` - Per-file cumulative bias plots
- `results/GLOBAL_cumulative_epsilon.png` - Global cumulative bias plot

## Results Interpretation

- **BF10** (Bayes Factor): Evidence for bias vs fair coin null
  - BF10 > 1: Evidence for bias
  - BF10 < 1: Evidence for fair coin
  - BF10 ≈ 1: Inconclusive

- **epsilon_hat**: Estimated bias (p_hat - 0.5)
  - Positive: bias toward 1
  - Negative: bias toward 0
  - Near zero: fair coin

## Generate LaTeX Snippet Automatically

After running the analysis, generate a LaTeX snippet:

```bash
python generate_latex_snippet.py --json results/global_summary.json --out qrng_results_snippet.tex
```

This creates a ready-to-paste LaTeX paragraph with all numbers filled in.

Then in `main.tex`, add:
```latex
\section{Pilot constraints from QRNG logs}
\input{qrng_results_snippet.tex}
```

## Run Sanity Checks

Before trusting results, run sanity checks:

```bash
python sanity_checks.py --summary results/summary.csv --global results/global_summary.json
```

This checks:
1. File-by-file consistency (is bias driven by one file?)
2. Temporal drift patterns
3. Format artifacts
4. Global summary interpretation

## LaTeX Template for Results (Manual)

If you prefer to write manually, use this template:

```latex
\paragraph{QRNG pilot constraint.}
We analyzed $n$ QRNG bits aggregated across $m$ log files using a Beta--Binomial Bayesian model
comparing the fair-coin null ($p=1/2$) to a symmetric Beta prior alternative.
The maximum-likelihood bias estimate was $\hat{\epsilon}=\hat{p}-1/2 = \langle \hat{p}\rangle - 1/2$,
and the Bayes factor was $\mathrm{BF}_{10}=\exp(\log \mathrm{BF}_{10})$ in favor of bias.
These results constrain the effective ethical-bias strength $\eta$ in the small-bias regime,
with null-consistent outcomes mapping to upper bounds on $|\eta|$ under the operational link
$\epsilon \propto \eta(\Delta E - \langle \Delta E\rangle)$.
```

Replace the placeholders with actual values from `global_summary.json`.

