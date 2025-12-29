#!/usr/bin/env python3
"""
Generate LaTeX snippet from QRNG analysis results.
Usage: python generate_latex_snippet.py --json results/global_summary.json --out qrng_results_snippet.tex
"""
import argparse
import json
from pathlib import Path


def format_number(x, precision=3, scientific=False):
    """Format number for LaTeX, handling scientific notation if needed."""
    if abs(x) < 1e-3 or abs(x) > 1e3:
        return f"{x:.{precision}e}".replace("e", r"\times 10^{") + "}"
    return f"{x:.{precision}f}"


def generate_latex_snippet(json_path: Path, out_path: Path):
    """Generate LaTeX snippet from global_summary.json."""
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    n = data["n"]
    k = data["k"]
    p_hat = data["p_hat"]
    eps_hat = data["epsilon_hat"]
    BF10 = data["BF10"]
    log_BF10 = data["log_BF10"]
    
    # Get credible intervals if available
    eps_lower = data.get("epsilon_lower_95", None)
    eps_upper = data.get("epsilon_upper_95", None)
    p_lower = data.get("p_lower_95", None)
    p_upper = data.get("p_upper_95", None)
    
    # Format numbers appropriately
    eps_str = format_number(eps_hat, precision=6)
    BF_str = format_number(BF10, precision=2)
    log_BF_str = format_number(log_BF10, precision=3)
    p_hat_str = format_number(p_hat, precision=6)
    
    # Interpret BF10
    if BF10 > 30:
        bf_interpret = "strong evidence for bias"
    elif BF10 > 10:
        bf_interpret = "substantial evidence for bias"
    elif BF10 > 3:
        bf_interpret = "moderate evidence for bias"
    elif BF10 > 1/3:
        bf_interpret = "inconclusive"
    else:
        bf_interpret = "evidence against bias"
    
    # Format credible intervals if available
    if eps_lower is not None and eps_upper is not None:
        eps_ci_str = f"$[{format_number(eps_lower, precision=6)}, {format_number(eps_upper, precision=6)}]$"
        ci_note = f" The 95\\% credible interval for $\\epsilon$ is {eps_ci_str}."
    else:
        ci_note = ""
    
    # Generate LaTeX
    snippet = f"""% Auto-generated from {json_path.name}
% Run: python generate_latex_snippet.py --json {json_path.name} --out {out_path.name}

\\paragraph{{QRNG pilot constraint.}}
We analyzed $n={n}$ QRNG bits using a Beta--Binomial Bayesian model
comparing the fair-coin null ($p=1/2$) to a symmetric Beta prior alternative.
The maximum-likelihood bias estimate was $\\hat{{\\epsilon}}=\\hat{{p}}-1/2 = {eps_str}$,
where $\\hat{{p}}={p_hat_str}$ is the observed proportion of ones.{ci_note}
The Bayes factor was $\\mathrm{{BF}}_{{10}}={BF_str}$ ($\\log \\mathrm{{BF}}_{{10}}={log_BF_str}$),
indicating {bf_interpret} relative to the fair-coin null.
These results constrain the effective ethical-bias strength $\\eta$ in the small-bias regime,
with null-consistent outcomes mapping to upper bounds on $|\\eta|$ under the operational link
$\\epsilon \\propto \\eta(\\Delta E - \\langle \\Delta E\\rangle)$.
"""
    
    out_path.write_text(snippet, encoding="utf-8")
    print(f"Generated: {out_path}")
    print(f"\nPreview:")
    print("=" * 60)
    print(snippet)
    print("=" * 60)


def main():
    ap = argparse.ArgumentParser(description="Generate LaTeX snippet from QRNG results")
    ap.add_argument("--json", type=str, default="results/global_summary.json",
                    help="Path to global_summary.json")
    ap.add_argument("--out", type=str, default="qrng_results_snippet.tex",
                    help="Output LaTeX file")
    args = ap.parse_args()
    
    json_path = Path(args.json)
    out_path = Path(args.out)
    
    if not json_path.exists():
        print(f"Error: {json_path} not found. Run analyze_qrng.py first.")
        return 1
    
    generate_latex_snippet(json_path, out_path)
    return 0


if __name__ == "__main__":
    exit(main())

