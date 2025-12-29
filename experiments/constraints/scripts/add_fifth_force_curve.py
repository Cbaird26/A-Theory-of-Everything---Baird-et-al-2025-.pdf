#!/usr/bin/env python3
"""
Add additional fifth-force exclusion curves to the constraint envelope.

This script helps digitize and integrate new exclusion curves (e.g., Sushkov 2011,
Decca 2005) into the constraint envelope.

Usage:
  # Create placeholder CSV from published data
  python add_fifth_force_curve.py --create-template --source "Sushkov2011" --out data/sushkov2011_exclusion.csv

  # After digitizing, merge with existing bounds
  python add_fifth_force_curve.py --merge --existing data/fifth_force_exclusion.csv --new data/sushkov2011_exclusion.csv --out data/fifth_force_exclusion_envelope.csv
"""
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def create_template_csv(source: str, output_path: Path, lambda_range: Optional[List[float]] = None):
    """
    Create a template CSV for digitizing an exclusion curve.
    
    Args:
        source: Source name (e.g., "Sushkov2011", "Decca2005")
        output_path: Where to save the template
        lambda_range: Optional range of lambda values to include (in meters)
    """
    if lambda_range is None:
        # Default: cover the range where this constraint is strongest
        if "Sushkov" in source or "sushkov" in source.lower():
            # Sushkov 2011: 0.4-4 µm range
            lambda_range = np.logspace(-7, -5, 100)  # 0.1 to 10 µm
        elif "Decca" in source or "decca" in source.lower():
            # Decca 2005: sub-µm range
            lambda_range = np.logspace(-8, -6, 100)  # 10 nm to 1 µm
        else:
            # Generic: 1 nm to 1 m
            lambda_range = np.logspace(-9, 0, 200)
    
    # Create placeholder alpha values (will be replaced by digitization)
    alpha_placeholder = np.full_like(lambda_range, 1e-6)  # Placeholder
    
    df = pd.DataFrame({
        'lambda': lambda_range,
        'alpha': alpha_placeholder,
        'excluded': 0,  # 0 = allowed, 1 = excluded
        'source': source
    })
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✓ Created template: {output_path}")
    print(f"  Source: {source}")
    print(f"  Lambda range: {lambda_range.min():.2e} to {lambda_range.max():.2e} m")
    print(f"\nNext steps:")
    print(f"  1. Digitize the exclusion curve from the paper")
    print(f"  2. Replace 'alpha' column with digitized values")
    print(f"  3. Set 'excluded=1' for points above the curve")
    print(f"  4. Run --merge to combine with existing bounds")


def load_exclusion_curves(csv_paths: List[Path]) -> pd.DataFrame:
    """Load and combine multiple exclusion curve CSVs."""
    dfs = []
    for path in csv_paths:
        if not path.exists():
            print(f"Warning: {path} not found, skipping")
            continue
        df = pd.read_csv(path)
        dfs.append(df)
    
    if not dfs:
        raise ValueError("No valid exclusion curve files found")
    
    combined = pd.concat(dfs, ignore_index=True)
    return combined


def compute_envelope(df: pd.DataFrame, lambda_resolution: int = 1000) -> pd.DataFrame:
    """
    Compute the envelope (most restrictive bound) across multiple exclusion curves.
    
    For each lambda value, take the minimum alpha that is excluded.
    """
    # Create fine lambda grid
    lambda_min = df['lambda'].min()
    lambda_max = df['lambda'].max()
    lambda_grid = np.logspace(np.log10(lambda_min), np.log10(lambda_max), lambda_resolution)
    
    # For each lambda, find the minimum excluded alpha
    envelope_alpha = []
    for lam in lambda_grid:
        # Find all points near this lambda
        mask = (df['lambda'] >= lam * 0.9) & (df['lambda'] <= lam * 1.1)
        if not mask.any():
            continue
        
        # Among excluded points, find minimum alpha
        excluded_mask = mask & (df['excluded'] == 1)
        if excluded_mask.any():
            min_alpha = df.loc[excluded_mask, 'alpha'].min()
            envelope_alpha.append((lam, min_alpha))
    
    if not envelope_alpha:
        print("Warning: No excluded points found in envelope computation")
        return df
    
    envelope_df = pd.DataFrame(envelope_alpha, columns=['lambda', 'alpha'])
    envelope_df['excluded'] = 1
    envelope_df['source'] = 'envelope'
    
    return envelope_df


def merge_curves(existing_path: Path, new_paths: List[Path], output_path: Path, create_envelope: bool = True):
    """
    Merge multiple exclusion curves into a single envelope.
    """
    all_paths = [existing_path] + new_paths
    combined = load_exclusion_curves(all_paths)
    
    if create_envelope:
        envelope = compute_envelope(combined)
        
        # Combine original curves + envelope
        final = pd.concat([combined, envelope], ignore_index=True)
    else:
        final = combined
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(output_path, index=False)
    
    print(f"✓ Merged exclusion curves: {output_path}")
    print(f"  Sources: {final['source'].unique().tolist()}")
    print(f"  Total points: {len(final)}")
    
    # Plot comparison
    plot_comparison(final, output_path.with_suffix('.png'))


def plot_comparison(df: pd.DataFrame, output_path: Path):
    """Plot all exclusion curves and the envelope."""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot each source separately
    sources = df['source'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(sources)))
    
    for source, color in zip(sources, colors):
        source_df = df[df['source'] == source]
        excluded = source_df[source_df['excluded'] == 1]
        
        if len(excluded) > 0:
            ax.plot(excluded['lambda'], excluded['alpha'], 'o-', 
                   label=source, color=color, alpha=0.7, markersize=2)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Range λ (meters)', fontsize=12)
    ax.set_ylabel('Yukawa strength α', fontsize=12)
    ax.set_title('Fifth-Force Exclusion Curves (Envelope)', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved plot: {output_path}")
    plt.close()


def main():
    ap = argparse.ArgumentParser(description='Add and merge fifth-force exclusion curves')
    ap.add_argument('--create-template', action='store_true',
                   help='Create a template CSV for digitization')
    ap.add_argument('--source', type=str, default='Unknown',
                   help='Source name (e.g., Sushkov2011, Decca2005)')
    ap.add_argument('--merge', action='store_true',
                   help='Merge multiple exclusion curves into envelope')
    ap.add_argument('--base', type=str,
                   default='experiments/constraints/data/fifth_force_exclusion.csv',
                   help='Base exclusion curve CSV')
    ap.add_argument('--add', type=str, nargs='+',
                   help='Additional exclusion curve CSV(s) to merge')
    ap.add_argument('--existing', type=str,
                   help='[Deprecated] Use --base instead')
    ap.add_argument('--new', type=str, nargs='+',
                   help='[Deprecated] Use --add instead')
    ap.add_argument('--out', type=str, required=True,
                   help='Output CSV path')
    ap.add_argument('--plot', type=str,
                   help='Output path for comparison plot (optional)')
    args = ap.parse_args()
    
    if args.create_template:
        output_path = Path(args.out)
        create_template_csv(args.source, output_path)
        return 0
    
    if args.merge:
        # Support both old and new argument names
        base_path = Path(args.base if args.base else (args.existing or 'experiments/constraints/data/fifth_force_exclusion.csv'))
        add_paths = [Path(p) for p in (args.add or args.new or [])]
        
        if not add_paths:
            print("Error: --add (or --new) required when using --merge")
            return 1
        
        output_path = Path(args.out)
        plot_path = Path(args.plot) if args.plot else None
        
        merge_curves(base_path, add_paths, output_path, create_envelope=True)
        
        if plot_path:
            # Load and plot the merged result
            merged_df = pd.read_csv(output_path)
            plot_comparison(merged_df, plot_path)
        
        return 0
    
    print("Error: Must specify --create-template or --merge")
    return 1


if __name__ == '__main__':
    exit(main())

