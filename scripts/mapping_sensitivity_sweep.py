#!/usr/bin/env python3
"""Automated mapping sensitivity sweep across alpha mapping modes (A/B/C) with S_FF scaling.

This script runs detectability analysis across all mapping modes using the SAME fixed point set,
generating a summary table and optional plot showing r_max vs S_FF for each mode.

Usage:
    python scripts/mapping_sensitivity_sweep.py --seed 42 --n-points 2000 --real-only
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from code.inference.fifth_force.detectability import (
    compute_detectability,
    sample_model_points,
)
from code.inference.fifth_force.registry import list_curves

# Import ToE mapping for Mode D
try:
    from code.inference.fifth_force.toe_mapping import toe_theta_hc
except ImportError:
    toe_theta_hc = None


def safe_git_hash() -> str:
    """Get current git commit hash, or 'UNKNOWN' if unavailable."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "UNKNOWN"
    except Exception:
        return "UNKNOWN"


def summarize_r(df: pd.DataFrame) -> Dict[str, float]:
    """Compute summary statistics from detectability DataFrame.
    
    Args:
        df: DataFrame with 'r' column from compute_detectability
        
    Returns:
        Dictionary with max_r, median_r, p99_r, p999_r, and fraction statistics
    """
    if len(df) == 0:
        return {
            "max_r": 0.0,
            "median_r": 0.0,
            "p99_r": 0.0,
            "p999_r": 0.0,
            "frac_excluded": 0.0,
            "frac_hunt": 0.0,
            "frac_safe": 0.0,
        }
    
    r_values = df["r"].values
    
    return {
        "max_r": float(np.max(r_values)),
        "median_r": float(np.median(r_values)),
        "p99_r": float(np.quantile(r_values, 0.99)),
        "p999_r": float(np.quantile(r_values, 0.999)),
        "frac_excluded": float(np.mean(r_values > 1.0)),
        "frac_hunt": float(np.mean((r_values > 0.1) & (r_values <= 1.0))),
        "frac_safe": float(np.mean(r_values <= 0.1)),
    }


def compute_scale_factors(max_r: float) -> Dict[str, float]:
    """Compute required scaling factors to reach r=0.1 and r=1.0.
    
    Args:
        max_r: Maximum detectability ratio
        
    Returns:
        Dictionary with scale_to_r_0_1 and scale_to_r_1
    """
    if max_r <= 0:
        return {
            "scale_to_r_0_1": float("inf"),
            "scale_to_r_1": float("inf"),
        }
    
    return {
        "scale_to_r_0_1": 0.1 / max_r,
        "scale_to_r_1": 1.0 / max_r,
    }


def convert_points_to_toe_params(
    points: List[Dict],
    kappa_cH_min: float = 1e-4,
    kappa_cH_max: float = 1e-1,
    v_c_min_GeV: float = 1e-9,
    v_c_max_GeV: float = 1e-3,
    seed: int = 42,
) -> List[Dict]:
    """Convert theta-based model points to ToE parameter points.
    
    For Mode D, we need kappa_cH and v_c_GeV. This function samples these
    and uses the existing m_phi to compute equivalent ToE parameters.
    
    Args:
        points: List of model point dicts with m_phi_GeV and theta
        kappa_cH_min, kappa_cH_max: Range for portal coupling (default: reasonable range)
        v_c_min_GeV, v_c_max_GeV: Range for scalar VEV in GeV (default: reasonable range)
        seed: Random seed for reproducibility
    
    Returns:
        List of model point dicts with kappa_cH, v_c_GeV, m_c_GeV
    """
    rng = np.random.RandomState(seed)
    
    toe_points = []
    for point in points:
        m_phi_GeV = point.get("m_phi_GeV")
        theta = point.get("theta")
        
        if m_phi_GeV is None or theta is None:
            continue
        
        # Sample ToE parameters
        log_kappa = rng.uniform(np.log10(kappa_cH_min), np.log10(kappa_cH_max))
        log_v_c = rng.uniform(np.log10(v_c_min_GeV), np.log10(v_c_max_GeV))
        
        kappa_cH = 10.0 ** log_kappa
        v_c_GeV = 10.0 ** log_v_c
        
        # Create ToE parameter point
        toe_point = {
            "m_phi_GeV": m_phi_GeV,
            "m_c_GeV": m_phi_GeV,  # Use m_phi as m_c
            "kappa_cH": kappa_cH,
            "v_c_GeV": v_c_GeV,
            "f_n": 0.30,  # Default nucleon form factor
        }
        toe_points.append(toe_point)
    
    return toe_points


def run_sweep(
    seed: int,
    n_points: int,
    real_only: bool = True,
    s_ff_values: List[float] = None,
    output_dir: Path = None,
    m_phi_min: float = 1e-16,
    m_phi_max: float = 1e-10,
    theta_min: float = 1e-22,
    theta_max: float = 1e-18,
    mu_sb_min: float = 1e-3,
    mu_sb_max: float = 1.0,
    include_mode_d: bool = True,
) -> Dict:
    """Run mapping sensitivity sweep across modes A, B, C, and optionally D.
    
    Args:
        seed: Random seed for reproducibility
        n_points: Number of model points to sample
        real_only: If True, exclude synthetic curves
        s_ff_values: List of S_FF values to sweep for mode C (default: [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0])
        output_dir: Directory for output files
        m_phi_min, m_phi_max: Scalar mass range (GeV)
        theta_min, theta_max: Mixing angle range
        mu_sb_min, mu_sb_max: Scale-breaking mass range
        
    Returns:
        Dictionary with sweep results and metadata
    """
    if output_dir is None:
        output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if s_ff_values is None:
        s_ff_values = [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]
    
    commit_hash = safe_git_hash()
    
    # Get curves for targeted sampling
    curves = list_curves(real_only=real_only)
    
    # Generate FIXED point set ONCE (this is critical for mapping-only comparison)
    print(f"Generating fixed point set (seed={seed}, n_points={n_points})...")
    
    # Build lambda ranges for targeted sampling if real_only
    target_lambda_ranges = None
    if real_only and curves:
        target_lambda_ranges = [(c["lambda_min"], c["lambda_max"]) for c in curves]
    
    # Sample fixed point set
    fixed_points = sample_model_points(
        n_points=n_points,
        m_phi_min=m_phi_min,
        m_phi_max=m_phi_max,
        theta_min=theta_min,
        theta_max=theta_max,
        mu_sb_min=mu_sb_min,
        mu_sb_max=mu_sb_max,
        seed=seed,
        target_lambda_ranges=target_lambda_ranges,
    )
    
    print(f"  Generated {len(fixed_points)} model points")
    print("")
    
    # Store results
    results = []
    
    # Mode A: Legacy placeholder (alpha_pred = alpha_eff^2)
    print("Running Mode A (Legacy placeholder)...")
    df_a = compute_detectability(
        model_points=fixed_points,
        curves=curves,
        real_only=real_only,
        alpha_mode="A",
        kappa=1.0,
        s_ff=1.0,
        s_lambda=1.0,
    )
    stats_a = summarize_r(df_a)
    scale_a = compute_scale_factors(stats_a["max_r"])
    results.append({
        "mode": "A",
        "s_ff": 1.0,
        "kappa": 1.0,
        **stats_a,
        **scale_a,
    })
    print(f"  Max r: {stats_a['max_r']:.3e}, Scale to r=0.1: {scale_a['scale_to_r_0_1']:.3e}, Scale to r=1: {scale_a['scale_to_r_1']:.3e}")
    print("")
    
    # Mode B: Portal-derived proxy (alpha_pred = 2(kappa * alpha_eff)^2)
    print("Running Mode B (Portal-derived proxy)...")
    df_b = compute_detectability(
        model_points=fixed_points,
        curves=curves,
        real_only=real_only,
        alpha_mode="B",
        kappa=1.0,
        s_ff=1.0,
        s_lambda=1.0,
    )
    stats_b = summarize_r(df_b)
    scale_b = compute_scale_factors(stats_b["max_r"])
    results.append({
        "mode": "B",
        "s_ff": 1.0,
        "kappa": 1.0,
        **stats_b,
        **scale_b,
    })
    print(f"  Max r: {stats_b['max_r']:.3e}, Scale to r=0.1: {scale_b['scale_to_r_0_1']:.3e}, Scale to r=1: {scale_b['scale_to_r_1']:.3e}")
    print("")
    
    # Mode C: Agnostic scaling (alpha_pred = s_ff * alpha_eff^2)
    print(f"Running Mode C (Agnostic scaling) with S_FF values: {s_ff_values}...")
    for s_ff in s_ff_values:
        print(f"  S_FF = {s_ff:.1e}...")
        df_c = compute_detectability(
            model_points=fixed_points,
            curves=curves,
            real_only=real_only,
            alpha_mode="C",
            kappa=1.0,
            s_ff=s_ff,
            s_lambda=1.0,
        )
        stats_c = summarize_r(df_c)
        scale_c = compute_scale_factors(stats_c["max_r"])
        results.append({
            "mode": "C",
            "s_ff": s_ff,
            "kappa": 1.0,
            **stats_c,
            **scale_c,
        })
        print(f"    Max r: {stats_c['max_r']:.3e}, Scale to r=0.1: {scale_c['scale_to_r_0_1']:.3e}, Scale to r=1: {scale_c['scale_to_r_1']:.3e}")
    print("")
    
    # Mode D: ToE-Native (if enabled and module available)
    if include_mode_d and toe_theta_hc is not None:
        print("Running Mode D (ToE-Native Higgs-Mixing Bridge)...")
        # Convert fixed points to ToE parameters
        toe_points = convert_points_to_toe_params(
            fixed_points,
            seed=seed + 1000,  # Different seed for ToE parameter sampling
        )
        print(f"  Converted {len(toe_points)} points to ToE parameters")
        
        df_d = compute_detectability(
            model_points=toe_points,
            curves=curves,
            real_only=real_only,
            alpha_mode="D",
            kappa=1.0,  # Not used in Mode D
            s_ff=1.0,   # Not used in Mode D
            s_lambda=1.0,
        )
        stats_d = summarize_r(df_d)
        scale_d = compute_scale_factors(stats_d["max_r"])
        results.append({
            "mode": "D",
            "s_ff": 1.0,  # Not applicable
            "kappa": 1.0,  # Not applicable
            **stats_d,
            **scale_d,
        })
        print(f"  Max r: {stats_d['max_r']:.3e}, Scale to r=0.1: {scale_d['scale_to_r_0_1']:.3e}, Scale to r=1: {scale_d['scale_to_r_1']:.3e}")
        print("")
    elif include_mode_d:
        print("⚠️  Mode D requested but toe_mapping module not available. Skipping.")
        print("")
    
    # Compile summary
    summary = {
        "seed": seed,
        "n_points": n_points,
        "real_only": real_only,
        "commit_hash": commit_hash,
        "results": results,
    }
    
    # Write JSON output
    json_path = output_dir / "mapping_sensitivity_summary.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"✅ JSON summary: {json_path}")
    
    # Write Markdown table
    md_path = output_dir / "mapping_sensitivity_summary.md"
    with open(md_path, "w") as f:
        f.write("# Mapping Sensitivity Sweep Summary\n\n")
        f.write(f"**Seed:** {seed}\n")
        f.write(f"**N Points:** {n_points}\n")
        f.write(f"**Real-Only Mode:** {'Enabled' if real_only else 'Disabled'}\n")
        f.write(f"**Git Commit:** {commit_hash}\n\n")
        f.write("## Results\n\n")
        f.write("| Mode | S_FF | Max r | Median r | p99 r | p99.9 r | ")
        f.write("Frac r>1 | Frac 0.1<r≤1 | Frac r≤0.1 | Scale to r=0.1 | Scale to r=1 |\n")
        f.write("|------|------|-------|----------|-------|---------|")
        f.write("----------|---------------|-------------|----------------|--------------|\n")
        
        for r in results:
            f.write(
                f"| {r['mode']} | {r['s_ff']:.1e} | {r['max_r']:.3e} | "
                f"{r['median_r']:.3e} | {r['p99_r']:.3e} | {r['p999_r']:.3e} | "
                f"{r['frac_excluded']:.3e} | {r['frac_hunt']:.3e} | {r['frac_safe']:.3e} | "
                f"{r['scale_to_r_0_1']:.3e} | {r['scale_to_r_1']:.3e} |\n"
            )
        
        f.write("\n## Interpretation\n\n")
        f.write("- **Max r:** Maximum detectability ratio across all sampled points\n")
        f.write("- **Scale to r=0.1:** Multiplicative factor needed on α_pred to reach r=0.1 (near-detectable)\n")
        f.write("- **Scale to r=1:** Multiplicative factor needed on α_pred to reach r=1 (exclusion boundary)\n")
        f.write("- **Fraction r>1:** Fraction of points excluded (r > 1)\n")
        f.write("- **Fraction 0.1<r≤1:** Fraction in hunt band (near-detectable)\n")
        f.write("- **Fraction r≤0.1:** Fraction safely below detectability threshold\n\n")
        f.write("**Conclusion:** If max_r << 1 across all modes and S_FF values, ")
        f.write("the 'undetectable' conclusion is robust to mapping uncertainty.\n")
    
    print(f"✅ Markdown summary: {md_path}")
    
    # Generate plot if matplotlib is available
    try:
        import matplotlib.pyplot as plt
        
        # Filter to mode C (which sweeps S_FF) and optionally include mode B as reference
        mode_c_data = [r for r in results if r["mode"] == "C"]
        mode_b_data = [r for r in results if r["mode"] == "B"]
        
        if mode_c_data:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot mode C (sweeps S_FF)
            # Sort by s_ff to ensure proper line plotting
            mode_c_sorted = sorted(mode_c_data, key=lambda x: x["s_ff"])
            s_ff_c = [r["s_ff"] for r in mode_c_sorted]
            r_max_c = [r["max_r"] for r in mode_c_sorted]
            ax.loglog(s_ff_c, r_max_c, 's-', label='Mode C (Agnostic scaling)', linewidth=2, markersize=8)
            
            # Optionally add mode B as a reference point (it doesn't use S_FF, but shows r_max at kappa=1.0)
            if mode_b_data:
                # Place mode B at s_ff=1.0 for reference (though mode B doesn't actually use S_FF)
                r_max_b = mode_b_data[0]["max_r"]
                ax.plot([1.0], [r_max_b], 'o', label='Mode B (Portal-derived, κ=1.0, ref.)', 
                        markersize=10, markeredgewidth=2, markeredgecolor='C0', markerfacecolor='white')
            
            ax.set_xlabel('S_FF (scaling factor for Mode C)', fontsize=12)
            ax.set_ylabel('r_max (maximum detectability ratio)', fontsize=12)
            ax.set_title('Mapping Sensitivity: r_max vs S_FF (Mode C sweep)', fontsize=14)
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            
            plot_path = output_dir / "mapping_sensitivity_plot.png"
            plt.tight_layout()
            plt.savefig(plot_path, dpi=150, bbox_inches='tight')
            plt.close()
            print(f"✅ Plot: {plot_path}")
    except ImportError:
        print("   (Skipping plot generation - matplotlib not available)")
    except Exception as e:
        print(f"   (Skipping plot generation - error: {e})")
    
    return summary


def main():
    ap = argparse.ArgumentParser(
        description="Run mapping sensitivity sweep across alpha mapping modes"
    )
    ap.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    ap.add_argument("--n-points", type=int, default=2000, help="Number of model points (default: 2000)")
    ap.add_argument("--real-only", action="store_true", default=True, help="Use real-only mode (default: True)")
    ap.add_argument("--no-real-only", dest="real_only", action="store_false", help="Disable real-only mode")
    ap.add_argument("--s-ff-values", type=str, default="0.1,1.0,10.0,100.0,1000.0,10000.0",
                    help="Comma-separated S_FF values for mode C (default: 0.1,1.0,10.0,100.0,1000.0,10000.0)")
    ap.add_argument("--output-dir", type=str, default="results", help="Output directory (default: results)")
    
    # Parameter ranges (optional overrides)
    ap.add_argument("--m-phi-min", type=float, default=1e-16, help="Min scalar mass (GeV)")
    ap.add_argument("--m-phi-max", type=float, default=1e-10, help="Max scalar mass (GeV)")
    ap.add_argument("--theta-min", type=float, default=1e-22, help="Min mixing angle")
    ap.add_argument("--theta-max", type=float, default=1e-18, help="Max mixing angle")
    ap.add_argument("--mu-sb-min", type=float, default=1e-3, help="Min mu_sb/m_h ratio")
    ap.add_argument("--mu-sb-max", type=float, default=1.0, help="Max mu_sb/m_h ratio")
    
    args = ap.parse_args()
    
    # Parse S_FF values
    s_ff_values = [float(x.strip()) for x in args.s_ff_values.split(",")]
    
    output_dir = Path(args.output_dir)
    
    print("=" * 60)
    print("Mapping Sensitivity Sweep")
    print("=" * 60)
    print(f"Seed: {args.seed}")
    print(f"N Points: {args.n_points}")
    print(f"Real-Only: {args.real_only}")
    print(f"S_FF Values: {s_ff_values}")
    print("=" * 60)
    print("")
    
    summary = run_sweep(
        seed=args.seed,
        n_points=args.n_points,
        real_only=args.real_only,
        s_ff_values=s_ff_values,
        output_dir=output_dir,
        m_phi_min=args.m_phi_min,
        m_phi_max=args.m_phi_max,
        theta_min=args.theta_min,
        theta_max=args.theta_max,
        mu_sb_min=args.mu_sb_min,
        mu_sb_max=args.mu_sb_max,
        include_mode_d=True,  # Include Mode D by default
    )
    
    print("")
    print("=" * 60)
    print("Sweep Complete")
    print("=" * 60)
    print(f"Summary: {output_dir / 'mapping_sensitivity_summary.md'}")


if __name__ == "__main__":
    main()
