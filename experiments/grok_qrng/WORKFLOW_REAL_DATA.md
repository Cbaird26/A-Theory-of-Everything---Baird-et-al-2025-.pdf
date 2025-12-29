# Workflow for Real QRNG Data

## Important: Don't Combine Different Experimental Regimes

The "GLOBAL" result should represent **one dataset/condition**, not everything in the folder. Otherwise a large null session can drown a smaller biased session.

## Recommended Workflow

### 1. Organize Data by Run/Condition

Create separate folders for each dataset:

```
data/raw/
  grok_run_01/
    your_qrng_files.csv
  grok_run_02/
    your_qrng_files.csv
  twitter_2024_11/
    your_qrng_files.csv
```

### 2. Run Analysis Per Dataset

```bash
# Activate environment
source .venv/bin/activate

# Analyze each run separately
python analyze_qrng.py --data-dir data/raw/grok_run_01 --out-dir results/grok_run_01 --prior 1.0
python analyze_qrng.py --data-dir data/raw/grok_run_02 --out-dir results/grok_run_02 --prior 1.0
```

### 3. Run Sanity Checks Per Dataset

```bash
python sanity_checks.py \
  --summary results/grok_run_01/summary.csv \
  --global-json results/grok_run_01/global_summary.json

python sanity_checks.py \
  --summary results/grok_run_02/summary.csv \
  --global-json results/grok_run_02/global_summary.json
```

### 4. Generate LaTeX Snippets Per Dataset

```bash
python generate_latex_snippet.py \
  --json results/grok_run_01/global_summary.json \
  --out results/grok_run_01/qrng_results_snippet.tex

python generate_latex_snippet.py \
  --json results/grok_run_02/global_summary.json \
  --out results/grok_run_02/qrng_results_snippet.tex
```

### 5. Include in Paper

In `papers/toe_closed_core/main.tex`:

```latex
\section{Pilot constraints from QRNG logs}

\subsection{Grok Run 01}
\input{../../experiments/grok_qrng/results/grok_run_01/qrng_results_snippet.tex}

\subsection{Grok Run 02}
\input{../../experiments/grok_qrng/results/grok_run_02/qrng_results_snippet.tex}
```

Or copy snippets into `papers/toe_closed_core/` to keep the paper self-contained.

## Interpretation Guide

After running on real data, check:

1. **Null but informative** (BF10 < 1/3, epsilon_hat near 0)
   - → Publish as strong upper bound on η
   - → Still valuable: constrains the theory

2. **Bias-like but artifact-suspect** (BF10 > 3, but sanity checks flag issues)
   - → Run forensic checks (file-by-file, temporal patterns)
   - → Investigate parsing artifacts

3. **Bias-like and robust** (BF10 > 10, passes all sanity checks)
   - → Write up as decisive constraint
   - → Propose replication experiment

## Quick Reference

```bash
# One-liner for a single run
RUN_NAME="grok_run_01"
python analyze_qrng.py --data-dir data/raw/$RUN_NAME --out-dir results/$RUN_NAME --prior 1.0 && \
python sanity_checks.py --summary results/$RUN_NAME/summary.csv --global-json results/$RUN_NAME/global_summary.json && \
python generate_latex_snippet.py --json results/$RUN_NAME/global_summary.json --out results/$RUN_NAME/qrng_results_snippet.tex && \
echo "✓ Results ready: results/$RUN_NAME/"
```

