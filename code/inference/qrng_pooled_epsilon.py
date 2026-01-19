#!/usr/bin/env python3
"""
Pooled Epsilon Max Computation

Computes a conservative pooled epsilon_max from multiple independent QRNG sources.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import the analysis function from calibrate_qrng_physics
# Use absolute import path relative to project root
import sys
from pathlib import Path

# Add experiments/constraints/scripts to path
# Try multiple possible project root locations
_current_file = Path(__file__).resolve()
_possible_roots = [
    _current_file.parent.parent.parent.parent,  # code/inference/qrng_pooled_epsilon.py -> root
    Path.cwd(),  # Current working directory
]

_scripts_dir = None
for root in _possible_roots:
    candidate = root / "experiments" / "constraints" / "scripts" / "calibrate_qrng_physics.py"
    if candidate.exists():
        _scripts_dir = root / "experiments" / "constraints" / "scripts"
        break

if _scripts_dir is None:
    # Fallback: try relative to current working directory
    _scripts_dir = Path("experiments/constraints/scripts")
    if not (_scripts_dir / "calibrate_qrng_physics.py").exists():
        raise ImportError("Could not find calibrate_qrng_physics.py. Please run from project root.")

if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from calibrate_qrng_physics import analyze_binomial


def compute_pooled_epsilon_max(
    processed_dir: Path,
    results_dir: Path,
    prior_scale: float = 1.0,
    ci_mass: float = 0.95,
    pooling_method: str = "conservative_max",
    compute_both_modes: bool = False,
) -> Dict[str, Any]:
    """
    Compute pooled epsilon_max from multiple validated QRNG sources.
    
    Args:
        processed_dir: Directory containing validated CSV files per source
        results_dir: Directory for output files
        prior_scale: Beta prior scale for analysis (default 1.0)
        ci_mass: Credible interval mass (default 0.95)
        pooling_method: "conservative_max" (default) or "weighted" (documented but not default)
    
    Returns:
        Dictionary with pooled epsilon_max, per-source results, and metadata
    """
    processed_dir = Path(processed_dir)
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all validated CSV files
    validated_files = sorted((processed_dir / "qrng_sources").glob("*_validated.csv"))
    if not validated_files:
        raise ValueError(f"No validated CSV files found in {processed_dir / 'qrng_sources'}")
    
    per_source_results: List[Dict[str, Any]] = []
    
    for validated_file in validated_files:
        # Count bits: k = number of 1s, n = total bits
        k = 0
        n = 0
        source_id = None
        
        with validated_file.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bit = int(row["bit"])
                n += 1
                if bit == 1:
                    k += 1
                if source_id is None:
                    source_id = row.get("source_id", validated_file.stem)
        
        if n == 0:
            continue  # Skip empty files
        
        # Analyze this source
        analysis = analyze_binomial(k, n, prior_scale=prior_scale, ci_mass=ci_mass)
        
        # Compute CI radius for conservative pooling
        ci_radius = max(abs(analysis["ci_low"]), abs(analysis["ci_high"]))
        epsilon_bound = abs(analysis["epsilon_hat"]) + ci_radius
        
        per_source_results.append({
            "source_id": source_id,
            "validated_csv": str(validated_file),
            "n": analysis["n"],
            "k": analysis["k"],
            "p_hat": analysis["p_hat"],
            "epsilon_hat": analysis["epsilon_hat"],
            "bf10": analysis["bf10"],
            "ci_low": analysis["ci_low"],
            "ci_high": analysis["ci_high"],
            "ci_radius": ci_radius,
            "epsilon_bound": epsilon_bound,
        })
    
    if not per_source_results:
        raise ValueError("No valid sources found for pooling")
    
    # Compute pooled epsilon_max
    if pooling_method == "conservative_max":
        # Default: max over sources of |epsilon_hat| + CI_radius
        epsilon_max_pooled = max(r["epsilon_bound"] for r in per_source_results)
        method_description = "max over sources of |epsilon_hat| + CI_radius"
    elif pooling_method == "weighted":
        # Weighted pooling: inverse-variance weighted average
        # Weight by 1 / variance, where variance ≈ (CI_width / 2)^2
        total_weight = 0.0
        weighted_sum = 0.0
        for r in per_source_results:
            # Approximate variance from CI width
            ci_width = r["ci_high"] - r["ci_low"]
            variance = (ci_width / (2 * 1.96)) ** 2  # 1.96 for 95% CI
            if variance > 0:
                weight = 1.0 / variance
                total_weight += weight
                weighted_sum += weight * abs(r["epsilon_hat"])
        
        if total_weight > 0:
            weighted_epsilon = weighted_sum / total_weight
            # Add a conservative margin (max CI_radius across sources)
            max_ci_radius = max(r["ci_radius"] for r in per_source_results)
            epsilon_max_pooled = weighted_epsilon + max_ci_radius
            method_description = "inverse-variance weighted average + max CI_radius"
        else:
            # Fallback to conservative if no valid weights
            epsilon_max_pooled = max(r["epsilon_bound"] for r in per_source_results)
            method_description = "weighted pooling (fallback to conservative_max)"
    else:
        raise ValueError(f"Unknown pooling method: {pooling_method}")
    
    # Compute both modes if requested (for sensitivity analysis)
    epsilon_max_weighted = None
    if compute_both_modes and pooling_method == "conservative_max":
        # Also compute weighted mode for comparison
        total_weight = 0.0
        weighted_sum = 0.0
        for r in per_source_results:
            ci_width = r["ci_high"] - r["ci_low"]
            variance = (ci_width / (2 * 1.96)) ** 2
            if variance > 0:
                weight = 1.0 / variance
                total_weight += weight
                weighted_sum += weight * abs(r["epsilon_hat"])
        if total_weight > 0:
            weighted_epsilon = weighted_sum / total_weight
            max_ci_radius = max(r["ci_radius"] for r in per_source_results)
            epsilon_max_weighted = weighted_epsilon + max_ci_radius
    
    result = {
        "epsilon_max": float(epsilon_max_pooled),
        "method": pooling_method,
        "method_description": method_description,
        "prior_scale": prior_scale,
        "ci_mass": ci_mass,
        "sources": per_source_results,
        "num_sources": len(per_source_results),
    }
    
    if epsilon_max_weighted is not None:
        result["epsilon_max_weighted"] = float(epsilon_max_weighted)
        result["sensitivity_note"] = "Both conservative_max and weighted modes computed for comparison"
    
    # Write JSON output
    json_path = results_dir / "multisource_epsilon_max.json"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    
    # Write markdown summary
    md_path = results_dir / "multisource_epsilon_summary.md"
    md_lines = [
        "# Multi-Source QRNG Epsilon Max Summary",
        "",
        f"**Pooled epsilon_max (Mode A - Conservative)**: `{epsilon_max_pooled:.6f}`",
        f"**Method**: {method_description}",
    ]
    
    if epsilon_max_weighted is not None:
        md_lines.extend([
            f"**Pooled epsilon_max (Mode B - Weighted)**: `{epsilon_max_weighted:.6f}`",
            "",
            "**Sensitivity Analysis**: Both pooling modes computed for comparison.",
            "- Mode A (Conservative): max over sources of |epsilon_hat| + CI_radius (default, credibility-first)",
            "- Mode B (Weighted): inverse-variance weighted average + max CI_radius (sensitivity check)",
        ])
    
    md_lines.extend([
        "",
        f"**Prior scale**: {prior_scale}",
        f"**CI mass**: {ci_mass}",
        f"**Number of sources**: {len(per_source_results)}",
        "",
        "## Per-Source Results",
        "",
        "| Source ID | N | epsilon_hat | BF10 | 95% CI for ε | epsilon_bound |",
        "|-----------|------|-------------|------|--------------|---------------|",
    ])
    
    for r in per_source_results:
        md_lines.append(
            f"| {r['source_id']} | {int(r['n'])} | {r['epsilon_hat']:.6f} | "
            f"{r['bf10']:.3f} | [{r['ci_low']:.6f}, {r['ci_high']:.6f}] | "
            f"{r['epsilon_bound']:.6f} |"
        )
    
    md_lines.extend([
        "",
        "## Provenance",
        "",
        f"- Combined manifest: `results/qrng/multisource_manifest.json`",
        f"- Pooled epsilon_max JSON: `results/qrng/multisource_epsilon_max.json`",
        "",
        "## Notes",
        "",
        "- epsilon_bound = |epsilon_hat| + CI_radius (where CI_radius = max(|CI_low|, |CI_high|))",
        "- Mode A (Conservative): Can only loosen or stay same as more sources are added (worst-case bound)",
        "- Mode B (Weighted): Can tighten with more independent data (statistical meta-analysis)",
        "- Conservative mode is default for scientific rigor; weighted mode provided for sensitivity analysis",
    ])
    
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    
    return result


if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser(description="Compute pooled epsilon_max from multiple QRNG sources")
    ap.add_argument(
        "--processed-dir",
        type=str,
        default="data/processed",
        help="Directory containing validated CSV files",
    )
    ap.add_argument(
        "--results-dir",
        type=str,
        default="results/qrng",
        help="Directory for output files",
    )
    ap.add_argument(
        "--prior-scale",
        type=float,
        default=1.0,
        help="Beta prior scale (default: 1.0)",
    )
    ap.add_argument(
        "--ci-mass",
        type=float,
        default=0.95,
        help="Credible interval mass (default: 0.95)",
    )
    ap.add_argument(
        "--pooling-method",
        type=str,
        default="conservative_max",
        choices=["conservative_max", "weighted"],
        help="Pooling method (default: conservative_max)",
    )
    ap.add_argument(
        "--compute-both-modes",
        action="store_true",
        help="Compute both conservative and weighted modes for sensitivity analysis",
    )
    args = ap.parse_args()
    
    result = compute_pooled_epsilon_max(
        processed_dir=Path(args.processed_dir),
        results_dir=Path(args.results_dir),
        prior_scale=args.prior_scale,
        ci_mass=args.ci_mass,
        pooling_method=args.pooling_method,
        compute_both_modes=args.compute_both_modes,
    )
    
    print(f"Pooled epsilon_max: {result['epsilon_max']:.6f}")
    print(f"Method: {result['method_description']}")
    if 'epsilon_max_weighted' in result:
        print(f"Pooled epsilon_max (weighted): {result['epsilon_max_weighted']:.6f}")
    print(f"Sources: {result['num_sources']}")
    print(f"Summary: {args.results_dir}/multisource_epsilon_summary.md")

