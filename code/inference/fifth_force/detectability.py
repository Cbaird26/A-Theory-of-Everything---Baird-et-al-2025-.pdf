#!/usr/bin/env python3
"""Compute detectability map: r = alpha_pred / alpha_max for model points."""

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import pandas as pd

try:
    from .yukawa import model_point_to_alpha_lambda
    from .envelope import alpha_max_envelope, list_curves
    from .constraints import is_excluded
except ImportError:
    # Handle case when run as script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
    from code.inference.fifth_force.yukawa import model_point_to_alpha_lambda
    from code.inference.fifth_force.envelope import alpha_max_envelope, list_curves
    from code.inference.fifth_force.constraints import is_excluded


def sample_model_points(
    n_points: int = 1000,
    m_phi_min: float = 1e-16,
    m_phi_max: float = 1e-10,
    theta_min: float = 1e-22,
    theta_max: float = 1e-18,
    mu_sb_min: float = 1e-3,
    mu_sb_max: float = 1.0,
    seed: int = 42,
) -> List[Dict[str, float]]:
    """Sample model points uniformly in log space.
    
    Args:
        n_points: Number of points to sample
        m_phi_min, m_phi_max: Scalar mass range (GeV)
        theta_min, theta_max: Mixing angle range
        mu_sb_min, mu_sb_max: Scale-breaking mass range (as ratio mu_sb/m_h)
        seed: Random seed for reproducibility
    
    Returns:
        List of model point dictionaries
    """
    rng = np.random.RandomState(seed)
    
    points = []
    for i in range(n_points):
        # Log-uniform sampling
        log_m_phi = rng.uniform(np.log10(m_phi_min), np.log10(m_phi_max))
        log_theta = rng.uniform(np.log10(theta_min), np.log10(theta_max))
        log_mu_sb = rng.uniform(np.log10(mu_sb_min), np.log10(mu_sb_max))
        
        points.append({
            "m_phi_GeV": 10.0 ** log_m_phi,
            "theta": 10.0 ** log_theta,
            "mu_sb_over_m_h": 10.0 ** log_mu_sb,
        })
    
    return points


def compute_detectability(
    model_points: List[Dict[str, float]],
    curves: List[Dict] = None,
) -> pd.DataFrame:
    """Compute detectability ratio r = alpha_pred / alpha_max for each point.
    
    Args:
        model_points: List of model point dictionaries
        curves: List of curve metadata (default: auto-discover)
    
    Returns:
        DataFrame with columns: m_phi_GeV, theta, mu_sb_over_m_h, 
        alpha_pred, lambda_m, alpha_max, r, is_excluded, tightest_source_id
    """
    if curves is None:
        curves = list_curves()
    
    if not curves:
        raise ValueError("No constraint curves available")
    
    results = []
    
    for point in model_points:
        try:
            # Convert to format expected by model_point_to_alpha_lambda
            model_dict = {
                "m_phi": point["m_phi_GeV"],
                "theta": point["theta"],
                "mu_sb": point["mu_sb_over_m_h"] * 125.0,  # Convert ratio to GeV
            }
            
            # Compute (alpha_pred, lambda_m)
            alpha_pred, lambda_m = model_point_to_alpha_lambda(model_dict)
            
            # Get envelope alpha_max
            try:
                alpha_max, tightest_source_id = alpha_max_envelope(lambda_m, curves)
            except ValueError:
                # Out of range - skip
                continue
            
            # Compute detectability ratio
            r = alpha_pred / alpha_max if alpha_max > 0 else np.inf
            
            # Check if excluded
            # Load the tightest curve to check exclusion
            tightest_curve_path = None
            for curve_info in curves:
                if curve_info["source_id"] == tightest_source_id:
                    tightest_curve_path = curve_info["path"]
                    break
            
            if tightest_curve_path:
                from .constraints import load_constraint_curve
                tightest_curve = load_constraint_curve(tightest_curve_path)
                excluded = is_excluded(alpha_pred, lambda_m, tightest_curve)
            else:
                excluded = alpha_pred > alpha_max
            
            results.append({
                "m_phi_GeV": point["m_phi_GeV"],
                "theta": point["theta"],
                "mu_sb_over_m_h": point["mu_sb_over_m_h"],
                "alpha_pred": alpha_pred,
                "lambda_m": lambda_m,
                "alpha_max": alpha_max,
                "r": r,
                "is_excluded": excluded,
                "tightest_source_id": tightest_source_id,
            })
        except Exception as e:
            # Skip points that fail
            continue
    
    return pd.DataFrame(results)


def write_summary(
    df: pd.DataFrame,
    output_path: Path,
    curves: List[Dict] = None,
) -> None:
    """Write detectability summary markdown.
    
    Args:
        df: DataFrame with detectability results
        output_path: Path to write summary
        curves: List of curve metadata (for reporting)
    """
    if len(df) == 0:
        output_path.write_text("# Detectability Summary\n\nNo points computed.\n")
        return
    
    # Get curve info
    if curves is None:
        curves = list_curves()
    
    curve_info = "Envelope (tightest bound across all curves)"
    if curves:
        curve_ids = [c["source_id"] for c in curves]
        curve_info = f"Envelope across: {', '.join(curve_ids)}"
    
    # Compute statistics
    total = len(df)
    r_gt_1 = (df["r"] > 1.0).sum()
    r_gt_01 = (df["r"] > 0.1).sum()
    r_gt_001 = (df["r"] > 0.01).sum()
    r_gt_0001 = (df["r"] > 0.001).sum()
    
    # Top points by r
    top_points = df.nlargest(25, "r")
    
    # Find lambda band where r is largest
    if len(df) > 0:
        max_r_idx = df["r"].idxmax()
        max_r_lambda = df.loc[max_r_idx, "lambda_m"]
        max_r_value = df.loc[max_r_idx, "r"]
        
        # Find band around max
        lambda_band_min = df["lambda_m"].quantile(0.1)
        lambda_band_max = df["lambda_m"].quantile(0.9)
        band_avg_r = df[(df["lambda_m"] >= lambda_band_min) & 
                        (df["lambda_m"] <= lambda_band_max)]["r"].mean()
    else:
        max_r_lambda = None
        max_r_value = None
        lambda_band_min = None
        lambda_band_max = None
        band_avg_r = None
    
    # Write markdown
    lines = [
        "# Fifth-Force Detectability Summary",
        "",
        "## Purpose",
        "",
        "This report quantifies where the scalar would be detectable if it exists by computing",
        "r = alpha_pred / alpha_max_envelope(lambda_m) for sampled model points.",
        "",
        "## Curve Used",
        "",
        f"{curve_info}",
        "",
        "**Note:** Synthetic curves are for plumbing validation only; canonical detectability conclusions require real envelope curves with full provenance.",
        "",
        "## Statistics",
        "",
        f"Total points computed: {total}",
        "",
        "| Threshold | Count | Fraction |",
        "|-----------|-------|----------|",
        f"| r > 1.0   | {r_gt_1:5d} | {r_gt_1/total*100:.1f}% |",
        f"| r > 0.1  | {r_gt_01:5d} | {r_gt_01/total*100:.1f}% |",
        f"| r > 0.01 | {r_gt_001:5d} | {r_gt_001/total*100:.1f}% |",
        f"| r > 0.001| {r_gt_0001:5d} | {r_gt_0001/total*100:.1f}% |",
        "",
        "## Top 25 Points by Detectability Ratio (r)",
        "",
        "These are the points closest to detection threshold:",
        "",
    ]
    
    # Add table header
    lines.extend([
        "| m_phi_GeV | theta | mu_sb/m_h | alpha_pred | lambda_m (m) | alpha_max | r | excluded | source |",
        "|-----------|-------|-----------|------------|--------------|-----------|---|----------|--------|",
    ])
    
    # Add top points
    for _, row in top_points.iterrows():
        lines.append(
            f"| {row['m_phi_GeV']:.3e} | {row['theta']:.3e} | {row['mu_sb_over_m_h']:.3e} | "
            f"{row['alpha_pred']:.3e} | {row['lambda_m']:.3e} | {row['alpha_max']:.3e} | "
            f"{row['r']:.3e} | {row['is_excluded']} | {row['tightest_source_id']} |"
        )
    
    lines.extend([
        "",
        "## Where to Look",
        "",
    ])
    
    if max_r_lambda is not None:
        lines.extend([
            f"The highest detectability ratio is r = {max_r_value:.3e} at λ = {max_r_lambda:.3e} m.",
            "",
            f"Across the central 80% of the λ range ({lambda_band_min:.3e} to {lambda_band_max:.3e} m),",
            f"the average detectability ratio is r = {band_avg_r:.3e}.",
            "",
            "**Interpretation:**",
            "- r ≪ 1: scalar is well below current experimental sensitivity",
            "- r ≈ 0.1–1: scalar is in the detectable range; near-future experiments could see it",
            "- r > 1: scalar is excluded by current constraints",
        ])
    else:
        lines.append("No points computed.")
    
    output_path.write_text("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(
        description="Compute fifth-force detectability map"
    )
    ap.add_argument(
        "--n-points",
        type=int,
        default=1000,
        help="Number of model points to sample (default: 1000)",
    )
    ap.add_argument(
        "--m-phi-min",
        type=float,
        default=1e-16,
        help="Minimum m_phi in GeV (default: 1e-16)",
    )
    ap.add_argument(
        "--m-phi-max",
        type=float,
        default=1e-10,
        help="Maximum m_phi in GeV (default: 1e-10)",
    )
    ap.add_argument(
        "--theta-min",
        type=float,
        default=1e-22,
        help="Minimum theta (default: 1e-22)",
    )
    ap.add_argument(
        "--theta-max",
        type=float,
        default=1e-18,
        help="Maximum theta (default: 1e-18)",
    )
    ap.add_argument(
        "--mu-sb-min",
        type=float,
        default=1e-3,
        help="Minimum mu_sb/m_h ratio (default: 1e-3)",
    )
    ap.add_argument(
        "--mu-sb-max",
        type=float,
        default=1.0,
        help="Maximum mu_sb/m_h ratio (default: 1.0)",
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=Path("results/fifth_force/detectability_summary.md"),
        help="Output path for summary (default: results/fifth_force/detectability_summary.md)",
    )
    
    args = ap.parse_args()
    
    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    # Sample points
    print(f"Sampling {args.n_points} model points...")
    points = sample_model_points(
        n_points=args.n_points,
        m_phi_min=args.m_phi_min,
        m_phi_max=args.m_phi_max,
        theta_min=args.theta_min,
        theta_max=args.theta_max,
        mu_sb_min=args.mu_sb_min,
        mu_sb_max=args.mu_sb_max,
        seed=args.seed,
    )
    
    # Compute detectability
    print("Computing detectability ratios...")
    df = compute_detectability(points)
    
    print(f"Computed detectability for {len(df)} points")
    
    # Write summary
    print(f"Writing summary to {args.output}...")
    write_summary(df, args.output)
    
    print("Done.")


if __name__ == "__main__":
    main()

