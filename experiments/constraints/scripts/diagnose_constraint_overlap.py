#!/usr/bin/env python3
"""
Diagnostic script to understand why a constraint didn't tighten the island.

Compares envelope alpha vs a specific constraint curve to see which is active.
If envelope_alpha(λ) < constraint_alpha(λ) everywhere, the constraint cannot tighten.
"""
import argparse
import json
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def load_exclusion_curve(csv_path: Path) -> pd.DataFrame:
    """Load exclusion curve from CSV."""
    df = pd.read_csv(csv_path)
    # Filter to excluded points only
    if 'excluded' in df.columns:
        df = df[df['excluded'] == 1].copy()
    return df.sort_values('lambda')


def get_envelope_at_lambda(envelope_df: pd.DataFrame, lambda_vals: np.ndarray) -> np.ndarray:
    """
    Get envelope alpha values at given lambda values.
    Envelope = minimum alpha (most restrictive) at each lambda.
    """
    # Group by lambda and take minimum alpha (most restrictive)
    envelope_grouped = envelope_df.groupby('lambda')['alpha'].min().reset_index()
    envelope_grouped = envelope_grouped.sort_values('lambda')
    
    # Interpolate to requested lambda values
    if len(envelope_grouped) < 2:
        return np.full_like(lambda_vals, np.nan)
    
    # Use log-space interpolation for better behavior
    log_lambda = np.log10(envelope_grouped['lambda'].values)
    log_alpha = np.log10(envelope_grouped['alpha'].values)
    
    # Interpolate
    f = interp1d(log_lambda, log_alpha, kind='linear', 
                 bounds_error=False, fill_value='extrapolate')
    
    log_lambda_req = np.log10(lambda_vals)
    log_alpha_interp = f(log_lambda_req)
    alpha_interp = 10**log_alpha_interp
    
    return alpha_interp


def get_constraint_at_lambda(constraint_df: pd.DataFrame, lambda_vals: np.ndarray) -> np.ndarray:
    """Get constraint alpha values at given lambda values via interpolation."""
    constraint_sorted = constraint_df.sort_values('lambda')
    
    if len(constraint_sorted) < 2:
        return np.full_like(lambda_vals, np.nan)
    
    # Use log-space interpolation
    log_lambda = np.log10(constraint_sorted['lambda'].values)
    log_alpha = np.log10(constraint_sorted['alpha'].values)
    
    f = interp1d(log_lambda, log_alpha, kind='linear',
                 bounds_error=False, fill_value='extrapolate')
    
    log_lambda_req = np.log10(lambda_vals)
    log_alpha_interp = f(log_lambda_req)
    alpha_interp = 10**log_alpha_interp
    
    return alpha_interp


def diagnose_overlap(envelope_csv: Path, constraint_csv: Path, 
                     lambda_min: float, lambda_max: float,
                     output_path: Path):
    """
    Diagnose which constraint is active in the overlap region.
    """
    # Load curves
    envelope_df = load_exclusion_curve(envelope_csv)
    constraint_df = load_exclusion_curve(constraint_csv)
    
    # Create lambda grid in overlap region
    lambda_vals = np.logspace(np.log10(lambda_min), np.log10(lambda_max), 200)
    
    # Get alpha values
    envelope_alpha = get_envelope_at_lambda(envelope_df, lambda_vals)
    constraint_alpha = get_constraint_at_lambda(constraint_df, lambda_vals)
    
    # Compare: which is more restrictive (lower alpha = tighter constraint)
    envelope_tighter = envelope_alpha < constraint_alpha
    constraint_tighter = constraint_alpha < envelope_alpha
    equal_approx = np.abs(envelope_alpha - constraint_alpha) / np.maximum(envelope_alpha, constraint_alpha) < 0.1
    
    # Statistics
    n_envelope_tighter = np.sum(envelope_tighter & ~equal_approx)
    n_constraint_tighter = np.sum(constraint_tighter & ~equal_approx)
    n_equal = np.sum(equal_approx)
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Both curves
    ax1.loglog(lambda_vals, envelope_alpha, 'b-', linewidth=2, 
              label='Envelope (existing)', alpha=0.7)
    ax1.loglog(lambda_vals, constraint_alpha, 'r--', linewidth=2,
              label='Constraint (new)', alpha=0.7)
    ax1.set_xlabel('Range λ (meters)', fontsize=12)
    ax1.set_ylabel('Yukawa strength α', fontsize=12)
    ax1.set_title('Envelope vs Constraint Comparison', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Which is tighter
    colors = np.where(envelope_tighter & ~equal_approx, 'blue',
                     np.where(constraint_tighter & ~equal_approx, 'red', 'gray'))
    ax2.scatter(lambda_vals, np.abs(envelope_alpha - constraint_alpha) / np.maximum(envelope_alpha, constraint_alpha),
               c=colors, alpha=0.6, s=10)
    ax2.set_xscale('log')
    ax2.set_xlabel('Range λ (meters)', fontsize=12)
    ax2.set_ylabel('Relative difference |α_env - α_const| / max(α)', fontsize=10)
    ax2.set_title('Which Constraint is Tighter? (Blue=Envelope, Red=Constraint, Gray=Equal)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(0.1, color='gray', linestyle=':', alpha=0.5, label='10% threshold')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved diagnostic plot: {output_path}")
    plt.close()
    
    # Print summary
    print("\n" + "="*60)
    print("DIAGNOSTIC SUMMARY")
    print("="*60)
    print(f"Lambda range: {lambda_min:.2e} to {lambda_max:.2e} m")
    print(f"  ({lambda_min*1e6:.1f} to {lambda_max*1e6:.1f} µm)")
    print()
    print(f"Envelope tighter: {n_envelope_tighter} / {len(lambda_vals)} points ({100*n_envelope_tighter/len(lambda_vals):.1f}%)")
    print(f"Constraint tighter: {n_constraint_tighter} / {len(lambda_vals)} points ({100*n_constraint_tighter/len(lambda_vals):.1f}%)")
    print(f"Approximately equal: {n_equal} / {len(lambda_vals)} points ({100*n_equal/len(lambda_vals):.1f}%)")
    print()
    
    if n_envelope_tighter > n_constraint_tighter * 2:
        print("→ CONCLUSION: Envelope dominates. Constraint cannot tighten island.")
        print("  The constraint is redundant in this region.")
    elif n_constraint_tighter > n_envelope_tighter * 2:
        print("→ CONCLUSION: Constraint dominates. Island may not be living in this region.")
        print("  The constraint is stronger, but island percentiles didn't change.")
    else:
        print("→ CONCLUSION: Mixed dominance. Need to check island location.")
        print("  Both constraints are active in different parts of the range.")
    
    # Save JSON summary
    summary = {
        'lambda_range': [float(lambda_min), float(lambda_max)],
        'n_points': len(lambda_vals),
        'envelope_tighter_count': int(n_envelope_tighter),
        'constraint_tighter_count': int(n_constraint_tighter),
        'equal_count': int(n_equal),
        'envelope_tighter_pct': float(100 * n_envelope_tighter / len(lambda_vals)),
        'constraint_tighter_pct': float(100 * n_constraint_tighter / len(lambda_vals)),
        'conclusion': 'envelope_dominates' if n_envelope_tighter > n_constraint_tighter * 2 else
                     ('constraint_dominates' if n_constraint_tighter > n_envelope_tighter * 2 else 'mixed')
    }
    
    json_path = output_path.with_suffix('.json')
    json_path.write_text(json.dumps(summary, indent=2))
    print(f"✓ Saved summary: {json_path}")


def main():
    ap = argparse.ArgumentParser(description='Diagnose why a constraint did not tighten the island')
    ap.add_argument('--envelope', type=str,
                   default='experiments/constraints/data/fifth_force_exclusion_envelope.csv',
                   help='Path to envelope CSV')
    ap.add_argument('--constraint', type=str, required=True,
                   help='Path to constraint CSV to compare')
    ap.add_argument('--lambda-min', type=float, required=True,
                   help='Minimum lambda for comparison (meters)')
    ap.add_argument('--lambda-max', type=float, required=True,
                   help='Maximum lambda for comparison (meters)')
    ap.add_argument('--out', type=str,
                   default='experiments/constraints/results/constraint_diagnostic.png',
                   help='Output plot path')
    args = ap.parse_args()
    
    envelope_path = Path(args.envelope)
    constraint_path = Path(args.constraint)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not envelope_path.exists():
        print(f"Error: Envelope file not found: {envelope_path}")
        return 1
    
    if not constraint_path.exists():
        print(f"Error: Constraint file not found: {constraint_path}")
        return 1
    
    diagnose_overlap(envelope_path, constraint_path,
                    args.lambda_min, args.lambda_max,
                    output_path)
    
    print("\nDone.")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

