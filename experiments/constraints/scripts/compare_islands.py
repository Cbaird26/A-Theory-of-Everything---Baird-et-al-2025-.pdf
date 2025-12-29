#!/usr/bin/env python3
"""
Compare island coordinates before and after adding constraints.

Usage:
  python compare_islands.py --before overlap_pass1.json --after overlap_pass2.json
"""
import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_island_coords(json_path: Path):
    """Load island coordinates from JSON."""
    with json_path.open('r') as f:
        data = json.load(f)
    
    island = data.get('island_coordinates', {})
    if not island:
        return None
    
    return {
        'lambda': island.get('lambda_m', {}),
        'alpha': island.get('alpha', {}),
        'n_points': island.get('n_viable_points', 0)
    }


def compare_islands(before_path: Path, after_path: Path, output_path: Path = None):
    """Compare two island coordinate sets."""
    before = load_island_coords(before_path)
    after = load_island_coords(after_path)
    
    if before is None or after is None:
        print("Error: Could not load island coordinates from one or both files")
        return
    
    print("=" * 60)
    print("ISLAND COMPARISON: Before vs After")
    print("=" * 60)
    print()
    
    # Lambda comparison
    print("Lambda (range) bounds:")
    print(f"  Before: p05={before['lambda']['p05']:.6e}, p50={before['lambda']['p50']:.6e}, p95={before['lambda']['p95']:.6e} m")
    print(f"  After:  p05={after['lambda']['p05']:.6e}, p50={after['lambda']['p50']:.6e}, p95={after['lambda']['p95']:.6e} m")
    
    lambda_p95_change = (after['lambda']['p95'] - before['lambda']['p95']) / before['lambda']['p95'] * 100
    lambda_p05_change = (after['lambda']['p05'] - before['lambda']['p05']) / before['lambda']['p05'] * 100
    
    print(f"  Change: p05={lambda_p05_change:+.1f}%, p95={lambda_p95_change:+.1f}%")
    print()
    
    # Alpha comparison
    print("Alpha (strength) bounds:")
    print(f"  Before: p05={before['alpha']['p05']:.6e}, p50={before['alpha']['p50']:.6e}, p95={before['alpha']['p95']:.6e}")
    print(f"  After:  p05={after['alpha']['p05']:.6e}, p50={after['alpha']['p50']:.6e}, p95={after['alpha']['p95']:.6e}")
    
    alpha_p95_change = (after['alpha']['p95'] - before['alpha']['p95']) / before['alpha']['p95'] * 100
    alpha_p05_change = (after['alpha']['p05'] - before['alpha']['p05']) / before['alpha']['p05'] * 100
    
    print(f"  Change: p05={alpha_p05_change:+.1f}%, p95={alpha_p95_change:+.1f}%")
    print()
    
    # Viable points comparison
    print("Viable points:")
    print(f"  Before: {before['n_points']:,}")
    print(f"  After:  {after['n_points']:,}")
    points_change = (after['n_points'] - before['n_points']) / before['n_points'] * 100
    print(f"  Change: {points_change:+.1f}%")
    print()
    
    # Interpretation
    print("=" * 60)
    print("INTERPRETATION:")
    print("=" * 60)
    
    if lambda_p95_change < -5:
        print("✅ Lambda p95 tightened (island shrunk at high-λ end)")
    elif lambda_p95_change > 5:
        print("⚠️  Lambda p95 expanded (unexpected - check constraints)")
    else:
        print("→ Lambda p95 stable")
    
    if lambda_p05_change > 5:
        print("✅ Lambda p05 increased (island shrunk at low-λ end - Sushkov likely bit!)")
    elif lambda_p05_change < -5:
        print("⚠️  Lambda p05 decreased (unexpected - check digitization)")
    else:
        print("→ Lambda p05 stable")
    
    if alpha_p95_change < -5:
        print("✅ Alpha p95 tightened (island shrunk at high-α end)")
    elif alpha_p95_change > 5:
        print("⚠️  Alpha p95 expanded (unexpected)")
    else:
        print("→ Alpha p95 stable")
    
    # Save comparison plot
    if output_path:
        plot_comparison(before, after, output_path)


def plot_comparison(before, after, output_path: Path):
    """Create comparison plot."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Lambda comparison
    ax1 = axes[0]
    params = ['p05', 'p50', 'p95']
    before_vals = [before['lambda'][p] for p in params]
    after_vals = [after['lambda'][p] for p in params]
    
    x = np.arange(len(params))
    width = 0.35
    
    ax1.bar(x - width/2, before_vals, width, label='Before', alpha=0.7)
    ax1.bar(x + width/2, after_vals, width, label='After', alpha=0.7)
    ax1.set_yscale('log')
    ax1.set_ylabel('Lambda (meters)', fontsize=12)
    ax1.set_xlabel('Percentile', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(params)
    ax1.set_title('Lambda (Range) Bounds Comparison', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Alpha comparison
    ax2 = axes[1]
    before_vals = [before['alpha'][p] for p in params]
    after_vals = [after['alpha'][p] for p in params]
    
    ax2.bar(x - width/2, before_vals, width, label='Before', alpha=0.7)
    ax2.bar(x + width/2, after_vals, width, label='After', alpha=0.7)
    ax2.set_yscale('log')
    ax2.set_ylabel('Alpha (Yukawa strength)', fontsize=12)
    ax2.set_xlabel('Percentile', fontsize=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(params)
    ax2.set_title('Alpha (Strength) Bounds Comparison', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"\n✓ Saved comparison plot: {output_path}")
    plt.close()


def main():
    ap = argparse.ArgumentParser(description='Compare island coordinates before and after')
    ap.add_argument('--before', type=str, required=True,
                   help='JSON file with "before" island coordinates')
    ap.add_argument('--after', type=str, required=True,
                   help='JSON file with "after" island coordinates')
    ap.add_argument('--plot', type=str,
                   help='Output path for comparison plot (optional)')
    args = ap.parse_args()
    
    before_path = Path(args.before)
    after_path = Path(args.after)
    plot_path = Path(args.plot) if args.plot else None
    
    if not before_path.exists():
        print(f"Error: {before_path} not found")
        return 1
    
    if not after_path.exists():
        print(f"Error: {after_path} not found")
        return 1
    
    compare_islands(before_path, after_path, plot_path)
    return 0


if __name__ == '__main__':
    exit(main())

