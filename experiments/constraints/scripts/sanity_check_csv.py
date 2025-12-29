#!/usr/bin/env python3
"""
Quick sanity check for digitized fifth-force CSV before running full pipeline.

Checks:
  - Format (columns, types)
  - Units (lambda in meters, reasonable range)
  - Monotonicity (lambda should generally increase)
  - Excluded flag (should be 1 for boundary points)
"""
import argparse
from pathlib import Path

import pandas as pd
import numpy as np

def sanity_check(csv_path: Path):
    """Run sanity checks on CSV."""
    print(f"Checking: {csv_path}\n")
    
    # Load
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Failed to read CSV: {e}")
        return False
    
    # Check columns
    required_cols = ['lambda', 'alpha', 'excluded']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"❌ Missing columns: {missing}")
        return False
    print(f"✅ Columns: {list(df.columns)}")
    
    # Check types
    if not pd.api.types.is_numeric_dtype(df['lambda']):
        print(f"❌ lambda column is not numeric")
        return False
    if not pd.api.types.is_numeric_dtype(df['alpha']):
        print(f"❌ alpha column is not numeric")
        return False
    if not pd.api.types.is_numeric_dtype(df['excluded']):
        print(f"❌ excluded column is not numeric")
        return False
    print(f"✅ All columns are numeric")
    
    # Check units (lambda should be in meters, reasonable range)
    lambda_min = df['lambda'].min()
    lambda_max = df['lambda'].max()
    if lambda_min < 1e-9 or lambda_max > 1e2:
        print(f"⚠️  Lambda range seems unusual: {lambda_min:.2e} to {lambda_max:.2e} m")
        print(f"   (Expected: ~1e-6 to ~1e0 m for EP tests)")
    else:
        print(f"✅ Lambda range: {lambda_min:.2e} to {lambda_max:.2e} m (reasonable)")
    
    # Check alpha (dimensionless, reasonable range)
    alpha_min = df['alpha'].min()
    alpha_max = df['alpha'].max()
    if alpha_min < 1e-15 or alpha_max > 1e-1:
        print(f"⚠️  Alpha range seems unusual: {alpha_min:.2e} to {alpha_max:.2e}")
        print(f"   (Expected: ~1e-12 to ~1e-3 for EP tests)")
    else:
        print(f"✅ Alpha range: {alpha_min:.2e} to {alpha_max:.2e} (reasonable)")
    
    # Check excluded flag
    excluded_count = df['excluded'].sum()
    total = len(df)
    if excluded_count == 0:
        print(f"⚠️  No excluded=1 points (all boundary points should be excluded=1)")
    elif excluded_count == total:
        print(f"✅ All {total} points marked as excluded=1 (boundary curve)")
    else:
        print(f"⚠️  Mixed excluded flags: {excluded_count}/{total} are excluded=1")
        print(f"   (Recommendation: all boundary points should be excluded=1)")
    
    # Check monotonicity (lambda should generally increase)
    lambda_diff = np.diff(df['lambda'].values)
    decreasing = np.sum(lambda_diff < 0)
    if decreasing > len(df) * 0.1:  # More than 10% decreasing
        print(f"⚠️  Lambda has {decreasing} decreasing steps (may indicate calibration issue)")
    else:
        print(f"✅ Lambda is generally monotonic ({decreasing} decreasing steps)")
    
    # Check for duplicates
    duplicates = df.duplicated(subset=['lambda', 'alpha']).sum()
    if duplicates > 0:
        print(f"⚠️  {duplicates} duplicate (lambda, alpha) pairs")
    else:
        print(f"✅ No duplicate points")
    
    # Show first 5 rows
    print(f"\n📋 First 5 rows:")
    print(df.head(5).to_string(index=False))
    
    # Summary
    print(f"\n{'='*60}")
    if excluded_count == total and decreasing < len(df) * 0.1:
        print("✅ CSV looks good! Ready to regenerate figures.")
    else:
        print("⚠️  CSV has some warnings. Review before proceeding.")
    print(f"{'='*60}\n")
    
    return True

def main():
    ap = argparse.ArgumentParser(description='Sanity check digitized CSV')
    ap.add_argument('csv', type=str, nargs='?',
                   default='experiments/constraints/data/fifth_force_exclusion.csv',
                   help='CSV file to check')
    args = ap.parse_args()
    
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        return 1
    
    sanity_check(csv_path)
    return 0

if __name__ == '__main__':
    exit(main())

