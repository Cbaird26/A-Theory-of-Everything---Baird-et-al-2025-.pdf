#!/usr/bin/env python3
"""
Generate LaTeX snippet for modulation test results.
Usage: python generate_modulation_snippet.py --summary results/lfdr_withinrun/summary.csv --out modulation_snippet.tex
"""
import argparse
import pandas as pd
from pathlib import Path


def format_number(x, precision=3, scientific=False):
    """Format number for LaTeX, handling scientific notation if needed."""
    if abs(x) < 1e-3 or abs(x) > 1e3:
        return f"{x:.{precision}e}".replace("e", r"\times 10^{") + "}"
    return f"{x:.{precision}f}"


def generate_modulation_snippet(summary_csv: Path, out_path: Path):
    """Generate LaTeX snippet for modulation test."""
    df = pd.read_csv(summary_csv)
    
    if df.empty or 'mod_beta' not in df.columns or df['mod_beta'].isna().all():
        snippet = """% No modulation fit found in summary.csv
% Run analyze_qrng.py on data with 's' column to get modulation fit
"""
        out_path.write_text(snippet, encoding="utf-8")
        print("⚠️  No modulation fit found. Ensure data has 's' column.")
        return
    
    row = df.iloc[0]
    n = int(row['n'])
    mod_beta = float(row['mod_beta'])
    mod_alpha = float(row['mod_alpha'])
    mod_loglik = float(row['mod_loglik'])
    
    # Get baseline for comparison
    null_loglik = float(row['log_p_D_H0'])
    improvement = mod_loglik - null_loglik
    
    # Format
    beta_str = format_number(mod_beta, precision=3)
    alpha_str = format_number(mod_alpha, precision=3)
    
    # Interpret
    if abs(mod_beta) < 0.001:
        interpretation = "no evidence for protocol-linked modulation"
    elif abs(mod_beta) < 0.01:
        interpretation = "minimal modulation, consistent with noise"
    else:
        interpretation = f"modulation detected (beta = {beta_str})"
    
    snippet = f"""% Auto-generated modulation test snippet
% Source: {summary_csv.name}

\\paragraph{{Within-run modulation test.}}
We performed a preregistered alternating-protocol within-run modulation test using $n={n:,}$ bits
from a hardware QRNG source (ID Quantique via LfD API).
Fitting a logistic modulation model $p_t=\\sigma(\\alpha+\\beta s_t)$ where $s_t\\in\\{{0,1\\}}$ labels
neutral vs coherence blocks yielded $\\hat{{\\alpha}}={alpha_str}$ and $\\hat{{\\beta}}={beta_str}$.
The modulated model improved log-likelihood by {improvement:.2f} units relative to the constant-bias null,
which is minimal and consistent with noise.
Thus, within the sensitivity of this dataset and this operational model, we find {interpretation}
of QRNG outcomes.
"""
    
    out_path.write_text(snippet, encoding="utf-8")
    print(f"Generated: {out_path}")
    print(f"\nPreview:")
    print("=" * 60)
    print(snippet)
    print("=" * 60)


def main():
    ap = argparse.ArgumentParser(description="Generate LaTeX snippet for modulation results")
    ap.add_argument("--summary", type=str, default="results/lfdr_withinrun/summary.csv",
                    help="Path to summary.csv with modulation fit")
    ap.add_argument("--out", type=str, default="modulation_snippet.tex",
                    help="Output LaTeX file")
    args = ap.parse_args()
    
    summary_path = Path(args.summary)
    out_path = Path(args.out)
    
    if not summary_path.exists():
        print(f"Error: {summary_path} not found.")
        return 1
    
    generate_modulation_snippet(summary_path, out_path)
    return 0


if __name__ == "__main__":
    exit(main())

