#!/usr/bin/env python3
"""
Sanity check for digitized exclusion curves.

Validates:
- λ values in expected range (meters)
- α magnitudes plausible and monotone-ish
- No axis flip
- Proper excluded/allowed labeling
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr


def validate_curve(csv_path: Path, expected_lambda_range: tuple = (1e-7, 1e-5), source_name: str = "Unknown"):
    """
    Validate a digitized exclusion curve CSV.
    
    Args:
        csv_path: Path to CSV file
        expected_lambda_range: (min, max) in meters
        source_name: Name of source (for error messages)
    
    Returns:
        (is_valid, issues_list)
    """
    issues = []
    
    if not csv_path.exists():
        return False, [f"File not found: {csv_path}"]
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return False, [f"Failed to read CSV: {e}"]
    
    # Check required columns
    required_cols = ['lambda', 'alpha']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        issues.append(f"Missing columns: {missing}")
        return False, issues
    
    # Check lambda range
    lambda_vals = pd.to_numeric(df['lambda'], errors='coerce')
    lambda_min = lambda_vals.min()
    lambda_max = lambda_vals.max()
    
    expected_min, expected_max = expected_lambda_range
    
    if lambda_min < expected_min * 0.1 or lambda_max > expected_max * 10:
        issues.append(f"Lambda range {lambda_min:.2e} to {lambda_max:.2e} m seems outside expected range {expected_min:.2e} to {expected_max:.2e} m")
    
    # Check alpha magnitudes (should be positive, reasonable scale)
    alpha_vals = pd.to_numeric(df['alpha'], errors='coerce')
    alpha_min = alpha_vals.min()
    alpha_max = alpha_vals.max()
    
    if alpha_min < 0:
        issues.append(f"Negative alpha values found (min: {alpha_min:.2e})")
    
    # For exclusion curves, alpha can be very large at small lambda (10^9-10^12 is normal)
    # Only flag if absurdly large (likely unit error)
    if alpha_max > 1e18:
        issues.append(f"Alpha values seem absurdly large (max: {alpha_max:.2e}, possible unit error)")
    
    if alpha_max < 1e-15:
        issues.append(f"Alpha values seem too small (max: {alpha_max:.2e}, might be axis flip)")
    
    # Check monotonicity (exclusion curves should DECREASE with lambda)
    # Sort by lambda
    df_sorted = df.sort_values('lambda')
    lambda_sorted = pd.to_numeric(df_sorted['lambda'], errors='coerce')
    alpha_sorted = pd.to_numeric(df_sorted['alpha'], errors='coerce')
    
    # Remove NaN values for correlation check
    valid_mask = lambda_sorted.notna() & alpha_sorted.notna()
    if valid_mask.sum() < 3:
        issues.append("Not enough valid data points for trend analysis")
    else:
        log_lambda = np.log10(lambda_sorted[valid_mask].values)
        log_alpha = np.log10(alpha_sorted[valid_mask].values)
        
        # Use Spearman correlation to check for decreasing trend
        rho, p_value = spearmanr(log_lambda, log_alpha)
        
        # For exclusion curves, expect negative correlation (alpha decreases as lambda increases)
        if rho > -0.3:
            issues.append(f"Curve not strongly decreasing (Spearman rho={rho:.2f}). Expected negative correlation for exclusion curves. Check digitization/axes.")
        else:
            print(f"✓ Decreasing exclusion curve behavior OK (Spearman rho={rho:.2f})")
        
        # Also check simple decreasing fraction
        decreasing_fraction = (np.diff(alpha_sorted[valid_mask].values) < 0).mean()
        if decreasing_fraction < 0.5:
            issues.append(f"Alpha doesn't appear monotone-decreasing with lambda (only {decreasing_fraction:.1%} of steps are decreasing). Possible axis flip?")
    
    # Check excluded column if present
    if 'excluded' in df.columns:
        excluded_vals = df['excluded'].unique()
        if not all(v in [0, 1] for v in excluded_vals):
            issues.append(f"'excluded' column should contain only 0 or 1, found: {excluded_vals}")
    else:
        issues.append("Warning: 'excluded' column not found. Will assume all points are boundary points.")
    
    # Summary statistics
    print(f"\n=== Validation Report: {source_name} ===")
    print(f"File: {csv_path}")
    print(f"Rows: {len(df)}")
    print(f"Lambda range: {lambda_min:.2e} to {lambda_max:.2e} m")
    print(f"Alpha range: {alpha_min:.2e} to {alpha_max:.2e}")
    if 'excluded' in df.columns:
        n_excluded = (df['excluded'] == 1).sum()
        print(f"Excluded points: {n_excluded} / {len(df)}")
    
    if issues:
        print(f"\n⚠️  Issues found ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
        return False, issues
    else:
        print("\n✅ Validation passed!")
        return True, []


def plot_curve(csv_path: Path, output_path: Path = None):
    """Quick plot of the curve for visual sanity check."""
    df = pd.read_csv(csv_path)
    
    lambda_vals = pd.to_numeric(df['lambda'], errors='coerce')
    alpha_vals = pd.to_numeric(df['alpha'], errors='coerce')
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    if 'excluded' in df.columns:
        excluded = df['excluded'] == 1
        ax.scatter(lambda_vals[excluded], alpha_vals[excluded], 
                  c='red', alpha=0.5, label='Excluded', s=10)
        ax.scatter(lambda_vals[~excluded], alpha_vals[~excluded], 
                  c='blue', alpha=0.5, label='Allowed', s=10)
    else:
        ax.plot(lambda_vals, alpha_vals, 'o-', alpha=0.7, markersize=3)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Range λ (meters)', fontsize=12)
    ax.set_ylabel('Yukawa strength α', fontsize=12)
    ax.set_title(f'Digitized Curve: {csv_path.name}', fontsize=14)
    ax.grid(True, alpha=0.3)
    if 'excluded' in df.columns:
        ax.legend()
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        print(f"✓ Saved plot: {output_path}")
    else:
        plt.savefig(csv_path.with_suffix('.png'), dpi=200, bbox_inches='tight')
        print(f"✓ Saved plot: {csv_path.with_suffix('.png')}")
    
    plt.close()


def main():
    ap = argparse.ArgumentParser(description='Validate digitized exclusion curve')
    ap.add_argument('--csv', type=str, required=True,
                   help='Path to digitized CSV file')
    ap.add_argument('--source', type=str, default='Unknown',
                   help='Source name (e.g., Sushkov2011)')
    ap.add_argument('--lambda-min', type=float, default=1e-7,
                   help='Expected minimum lambda (meters)')
    ap.add_argument('--lambda-max', type=float, default=1e-5,
                   help='Expected maximum lambda (meters)')
    ap.add_argument('--plot', action='store_true',
                   help='Generate validation plot')
    args = ap.parse_args()
    
    csv_path = Path(args.csv)
    is_valid, issues = validate_curve(
        csv_path,
        expected_lambda_range=(args.lambda_min, args.lambda_max),
        source_name=args.source
    )
    
    if args.plot:
        plot_curve(csv_path)
    
    if not is_valid:
        print("\n❌ Validation failed. Please fix issues before proceeding.")
        return 1
    
    print("\n✅ Curve is ready for merging!")
    return 0


if __name__ == '__main__':
    sys.exit(main())

