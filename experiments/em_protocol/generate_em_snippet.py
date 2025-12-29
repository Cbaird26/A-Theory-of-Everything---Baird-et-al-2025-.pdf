#!/usr/bin/env python3
"""
Generate LaTeX snippet for EM modulation test results.
Similar to generate_modulation_snippet.py for QRNG.
"""
import argparse
import json
from pathlib import Path


def format_number(num, precision=3, sci_threshold=1e-3):
    """Format number for LaTeX."""
    if abs(num) < sci_threshold and num != 0:
        return f"{num:.{precision}e}"
    return f"{num:.{precision}f}"


def main():
    ap = argparse.ArgumentParser(description="Generate LaTeX snippet for EM modulation test results")
    ap.add_argument("--json", type=str, default="results/em_modulation_summary.json",
                    help="Path to em_modulation_summary.json")
    ap.add_argument("--out", type=str, default="em_modulation_snippet.tex",
                    help="Output LaTeX file name")
    args = ap.parse_args()

    json_path = Path(args.json)
    out_path = Path(args.out)

    if not json_path.exists():
        print(f"Error: {json_path} not found. Run analyze_em.py first.")
        return 1

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    n = data.get("n", 0)
    beta = data.get("beta", None)
    beta_std = data.get("beta_std", None)
    beta_lower = data.get("beta_lower_95", None)
    beta_upper = data.get("beta_upper_95", None)
    p_value = data.get("p_value", None)
    perm_p_value = data.get("permutation_p_value", None)

    if beta is None or beta_std is None:
        print("Warning: Modulation fit data not found in JSON. Skipping snippet generation.")
        return 0

    beta_str = format_number(beta, precision=3)
    beta_std_str = format_number(beta_std, precision=3)
    
    # Format CI
    if beta_lower is not None and beta_upper is not None:
        ci_str = f"$\\beta \\in [{format_number(beta_lower, precision=3)}, {format_number(beta_upper, precision=3)}]$"
    else:
        ci_str = f"$\\beta = {beta_str} \\pm {beta_std_str}$"

    # Interpret result
    if p_value is not None and p_value < 0.05:
        result_interpretation = "significant"
    elif perm_p_value is not None and perm_p_value < 0.05:
        result_interpretation = "significant (permutation test)"
    else:
        result_interpretation = "null (consistent with noise)"

    snippet = f"""% Auto-generated EM modulation test snippet
% Source: {json_path.name}

\\paragraph{{EM modulation test.}}
We performed a preregistered alternating-protocol EM noise test using $n={n}$ data points
from [hardware: SDR/magnetometer/audio interface].
Fitting a modulation model $P(t)=\\alpha+\\beta s(t)+\\text{{drift}}(t)+\\epsilon(t)$
where $s(t)\\in\\{{0,1\\}}$ labels neutral vs coherence blocks yielded
$\\hat{{\\beta}}={beta_str}$ with standard error $\\sigma_\\beta={beta_std_str}$,
yielding 95\\% confidence interval {ci_str}.
The modulation coefficient is {result_interpretation} at the sensitivity of this dataset.
"""

    if perm_p_value is not None:
        snippet += f"Permutation test (1000 shuffles) yielded $p={perm_p_value:.6f}$.\n"

    snippet += """
Thus, within the sensitivity of this dataset and this operational model, we find
[no evidence / evidence] for protocol-linked modulation of EM signals.
"""

    out_path.write_text(snippet, encoding="utf-8")
    print(f"Generated: {out_path}")
    print("\nPreview:\n============================================================")
    print(snippet)
    print("============================================================")
    return 0


if __name__ == "__main__":
    exit(main())

