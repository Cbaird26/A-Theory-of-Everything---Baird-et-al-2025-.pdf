#!/usr/bin/env python3
"""
Fifth-force (Yukawa) constraint mapping for MQGT-SCF mediator.

Maps mediator parameters (m_M, g_M) → Yukawa (λ, α) where:
  λ = 1/m_M (range)
  α ∝ g_M^2 (strength, up to matter-coupling assumptions)

Reads exclusion curves from data files and produces allowed/excluded regions.
"""
import argparse
import json
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def load_exclusion_data(csv_path: Path) -> pd.DataFrame:
    """
    Load exclusion curve data.
    Expected CSV format: lambda (range in meters), alpha (strength), excluded (bool or 1/0)
    """
    if not csv_path.exists():
        # Create a placeholder with typical Eötvös/EP test bounds
        # These are conservative estimates - replace with real digitized data
        print(f"Warning: {csv_path} not found. Creating placeholder data.")
        lambda_vals = np.logspace(-6, 0, 100)  # 1 micron to 1 meter
        alpha_vals = np.logspace(-12, -3, 100)  # Typical EP test sensitivity
        # Simple exclusion: alpha > 10^-6 for lambda > 10^-4
        excluded = (alpha_vals > 1e-6) & (lambda_vals > 1e-4)
        df = pd.DataFrame({
            'lambda': lambda_vals,
            'alpha': alpha_vals,
            'excluded': excluded.astype(int)
        })
        df.to_csv(csv_path, index=False)
        print(f"Created placeholder: {csv_path}")
    
    df = pd.read_csv(csv_path)
    return df

def mediator_to_yukawa(m_M: float, g_M: float, matter_coupling: float = 1.0) -> Tuple[float, float]:
    """
    Convert mediator parameters to Yukawa parameters.
    
    Args:
        m_M: Mediator mass (in natural units, or specify units)
        g_M: Mediator coupling strength
        matter_coupling: Effective matter coupling (default 1.0, adjust for specific models)
    
    Returns:
        (lambda, alpha) where:
          lambda = 1/m_M (range in meters if m_M in 1/m)
          alpha = (g_M^2 * matter_coupling^2) / (4*pi) (strength)
    """
    lambda_range = 1.0 / m_M  # Range parameter
    alpha_strength = (g_M**2 * matter_coupling**2) / (4 * np.pi)
    return lambda_range, alpha_strength

def plot_constraints(df: pd.DataFrame, output_path: Path, 
                     mediator_params: Optional[Tuple[float, float]] = None):
    """
    Plot exclusion region and optionally overlay mediator parameter point.
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot exclusion curve
    excluded = df[df['excluded'] == 1]
    if len(excluded) > 0:
        ax.fill_between(excluded['lambda'], excluded['alpha'], 
                       excluded['alpha'].max() * 10,
                       alpha=0.3, color='red', label='Excluded (EP tests)')
    
    # Plot allowed region boundary
    allowed = df[df['excluded'] == 0]
    if len(allowed) > 0:
        ax.plot(allowed['lambda'], allowed['alpha'], 
               'b-', linewidth=2, label='Current bound')
    
    # Overlay mediator point if provided
    if mediator_params:
        m_M, g_M = mediator_params
        lambda_val, alpha_val = mediator_to_yukawa(m_M, g_M)
        ax.plot(lambda_val, alpha_val, 'go', markersize=10, 
               label=f'Mediator: m_M={m_M:.2e}, g_M={g_M:.2e}')
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Range λ (meters)', fontsize=12)
    ax.set_ylabel('Yukawa strength α', fontsize=12)
    ax.set_title('Fifth-Force (Yukawa) Constraints\nMediator → Yukawa Mapping', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim(df['lambda'].min(), df['lambda'].max())
    ax.set_ylim(df['alpha'].min(), df['alpha'].max())
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()
    
    # Save bounds as JSON
    bounds_json = {
        'lambda_min': float(df['lambda'].min()),
        'lambda_max': float(df['lambda'].max()),
        'alpha_max_allowed': float(df[df['excluded'] == 0]['alpha'].max() if len(df[df['excluded'] == 0]) > 0 else df['alpha'].max()),
        'exclusion_points': len(excluded)
    }
    json_path = output_path.with_suffix('.json')
    json_path.write_text(json.dumps(bounds_json, indent=2))
    print(f"✓ Saved bounds: {json_path}")

def main():
    ap = argparse.ArgumentParser(description='Map mediator parameters to Yukawa constraints')
    ap.add_argument('--in', dest='input_csv', type=str,
                   default='experiments/constraints/data/fifth_force_exclusion.csv',
                   help='Input CSV with exclusion curve data')
    ap.add_argument('--out', dest='output_png', type=str,
                   default='experiments/constraints/results/fifth_force_bounds.png',
                   help='Output PNG path')
    ap.add_argument('--m-mediator', type=float, default=None,
                   help='Mediator mass (optional, for overlay)')
    ap.add_argument('--g-mediator', type=float, default=None,
                   help='Mediator coupling (optional, for overlay)')
    args = ap.parse_args()
    
    input_path = Path(args.input_csv)
    output_path = Path(args.output_png)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = load_exclusion_data(input_path)
    
    mediator_params = None
    if args.m_mediator is not None and args.g_mediator is not None:
        mediator_params = (args.m_mediator, args.g_mediator)
    
    plot_constraints(df, output_path, mediator_params)
    print("Done.")

if __name__ == '__main__':
    main()

