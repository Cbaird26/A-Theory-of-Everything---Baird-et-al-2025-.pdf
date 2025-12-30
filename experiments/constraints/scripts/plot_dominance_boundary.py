#!/usr/bin/env python3
"""
Plot dominance boundary showing where QRNG_tilt vs ATLAS_mu transitions occur.

Creates a 2D visualization in (m_φ, θ) or (λ, α) space showing which constraint
is tightest at each point, with emphasis on the boundary between QRNG_tilt and ATLAS_mu.
"""
import argparse
import json
from pathlib import Path
from typing import Optional, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from derive_alpha_from_portal import map_parameters_to_yukawa
from active_constraint_labeling import (
    label_constraints_for_grid,
    CONSTRAINT_LABELS
)


def create_dominance_plot(
    m_phi_min: float, m_phi_max: float, n_m_phi: int,
    theta_min: float, theta_max: float, n_theta: int,
    qrng_bounds: Optional[Dict],
    ff_bounds: Optional[Dict],
    higgs_bounds: Optional[Dict],
    envelope_data: Optional[pd.DataFrame],
    Theta_lab: float = 1.0,
    br_max: float = 0.145,
    use_normalized_slack: bool = True,
    output_path: Path = None
):
    """
    Create dominance boundary plot.
    
    Args:
        m_phi_min, m_phi_max: Scalar mass range (GeV)
        n_m_phi: Number of mass points
        theta_min, theta_max: Mixing angle range
        n_theta: Number of angle points
        qrng_bounds, ff_bounds, higgs_bounds: Constraint bounds
        envelope_data: Envelope DataFrame
        Theta_lab: Screening factor for lab experiments
        br_max: Maximum allowed BR(H→inv)
        use_normalized_slack: Use normalized slack for comparison
        output_path: Output file path
    """
    # Create parameter grids
    m_phi_range = np.logspace(np.log10(m_phi_min), np.log10(m_phi_max), n_m_phi)
    theta_range = np.logspace(np.log10(theta_min), np.log10(theta_max), n_theta)
    M_PHI_GRID, THETA_GRID = np.meshgrid(m_phi_range, theta_range)
    
    # Derive Yukawa parameters
    LAMBDA_GRID = np.zeros_like(M_PHI_GRID)
    ALPHA_GRID = np.zeros_like(M_PHI_GRID)
    
    for i in range(n_theta):
        for j in range(n_m_phi):
            m_phi = M_PHI_GRID[i, j]
            theta = THETA_GRID[i, j]
            try:
                lambda_m, alpha = map_parameters_to_yukawa(
                    m_phi, theta,
                    model='normalized',
                    Theta=1.0  # Use unscreened for derivation
                )
                LAMBDA_GRID[i, j] = lambda_m
                ALPHA_GRID[i, j] = alpha
            except Exception as e:
                LAMBDA_GRID[i, j] = np.nan
                ALPHA_GRID[i, j] = np.nan
    
    # Get constraint bounds
    alpha_max_allowed = None
    if ff_bounds:
        alpha_max_allowed = ff_bounds.get('alpha_max_allowed')
    
    epsilon_max = 0.0008
    if qrng_bounds:
        eps_upper = qrng_bounds.get('epsilon_upper_95')
        if eps_upper is not None:
            epsilon_max = abs(eps_upper)
    
    # Label constraints
    constraint_labels, slacks = label_constraints_for_grid(
        LAMBDA_GRID, ALPHA_GRID,
        m_phi_grid=M_PHI_GRID,
        envelope_data=envelope_data,
        alpha_max_allowed=alpha_max_allowed,
        epsilon_max=epsilon_max,
        Theta_lab=Theta_lab,
        br_max=br_max,
        use_normalized_slack=use_normalized_slack
    )
    
    # Create figure with two panels: (m_φ, θ) and (λ, α)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Panel 1: (m_φ, θ) space
    plot_dominance_in_fundamental_space(
        ax1, M_PHI_GRID, THETA_GRID, constraint_labels,
        "Fundamental Parameter Space\n(m_φ, θ)"
    )
    
    # Panel 2: (λ, α) space
    plot_dominance_in_yukawa_space(
        ax2, LAMBDA_GRID, ALPHA_GRID, constraint_labels,
        "Yukawa Parameter Space\n(λ, α)"
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved dominance boundary plot: {output_path}")
    plt.close()
    
    # Print summary statistics
    viable_mask = constraint_labels >= 0
    if viable_mask.sum() > 0:
        viable_labels = constraint_labels[viable_mask]
        counts = {}
        for label_idx, label_name in CONSTRAINT_LABELS.items():
            if label_idx >= 0:
                counts[label_name] = int(np.sum(viable_labels == label_idx))
        
        total = sum(counts.values())
        print("\nDominance Summary:")
        for name, count in counts.items():
            pct = 100 * count / total if total > 0 else 0
            print(f"  {name}: {pct:.1f}% ({count} points)")


def plot_dominance_in_fundamental_space(ax, m_phi_grid, theta_grid, constraint_labels, title):
    """Plot dominance in (m_φ, θ) space."""
    # Create colormap: different colors for each constraint
    # -1: Excluded (black/gray)
    # 0: ATLAS_mu (blue)
    # 1: Higgs_inv (green)
    # 2: Fifth_force (red)
    # 3: QRNG_tilt (orange)
    
    colors = ['#2c2c2c', '#1f77b4', '#2ca02c', '#d62728', '#ff7f0e']
    cmap = ListedColormap(colors)
    
    # Plot
    im = ax.pcolormesh(
        m_phi_grid, theta_grid, constraint_labels,
        cmap=cmap, vmin=-1, vmax=4, shading='auto', alpha=0.7
    )
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Scalar Mass m_φ (GeV)', fontsize=12)
    ax.set_ylabel('Mixing Angle θ', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, alpha=0.3, which='both')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors[0], label='Excluded'),
        Patch(facecolor=colors[1], label='ATLAS μ'),
        Patch(facecolor=colors[2], label='Higgs inv'),
        Patch(facecolor=colors[3], label='Fifth-force'),
        Patch(facecolor=colors[4], label='QRNG tilt'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Highlight boundary between QRNG_tilt and ATLAS_mu
    highlight_dominance_boundary(ax, m_phi_grid, theta_grid, constraint_labels, 
                                 constraint1=3, constraint2=0, color='yellow', linewidth=2)


def plot_dominance_in_yukawa_space(ax, lambda_grid, alpha_grid, constraint_labels, title):
    """Plot dominance in (λ, α) space."""
    # Same colormap as above
    colors = ['#2c2c2c', '#1f77b4', '#2ca02c', '#d62728', '#ff7f0e']
    cmap = ListedColormap(colors)
    
    # Plot
    im = ax.pcolormesh(
        lambda_grid, alpha_grid, constraint_labels,
        cmap=cmap, vmin=-1, vmax=4, shading='auto', alpha=0.7
    )
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Range λ (meters)', fontsize=12)
    ax.set_ylabel('Yukawa Strength α', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, alpha=0.3, which='both')
    
    # Highlight boundary between QRNG_tilt and ATLAS_mu
    highlight_dominance_boundary(ax, lambda_grid, alpha_grid, constraint_labels,
                                 constraint1=3, constraint2=0, color='yellow', linewidth=2)


def highlight_dominance_boundary(ax, x_grid, y_grid, constraint_labels, 
                                 constraint1, constraint2, color='yellow', linewidth=2):
    """
    Highlight the boundary between two constraints.
    
    Finds points where one constraint is tightest and neighbors have the other constraint.
    """
    shape = constraint_labels.shape
    
    # Find boundary points
    boundary_x = []
    boundary_y = []
    
    for i in range(1, shape[0] - 1):
        for j in range(1, shape[1] - 1):
            label = constraint_labels[i, j]
            
            # Check if this point has constraint1 and neighbors have constraint2 (or vice versa)
            neighbors = [
                constraint_labels[i-1, j],
                constraint_labels[i+1, j],
                constraint_labels[i, j-1],
                constraint_labels[i, j+1]
            ]
            
            if label == constraint1 and constraint2 in neighbors:
                boundary_x.append(x_grid[i, j])
                boundary_y.append(y_grid[i, j])
            elif label == constraint2 and constraint1 in neighbors:
                boundary_x.append(x_grid[i, j])
                boundary_y.append(y_grid[i, j])
    
    if len(boundary_x) > 0:
        # Plot boundary points
        ax.scatter(boundary_x, boundary_y, c=color, s=10, alpha=0.6, 
                  label=f'Boundary: {CONSTRAINT_LABELS[constraint1]} ↔ {CONSTRAINT_LABELS[constraint2]}',
                  zorder=10)
        ax.legend(loc='upper right', fontsize=10)


def load_constraint_bounds(qrng_json: Path, ff_json: Path, higgs_json: Path):
    """Load constraint bounds from JSON files."""
    qrng_bounds = None
    if qrng_json.exists():
        qrng_bounds = json.loads(qrng_json.read_text())
    
    ff_bounds = None
    if ff_json.exists():
        ff_bounds = json.loads(ff_json.read_text())
    
    higgs_bounds = None
    if higgs_json.exists():
        higgs_bounds = json.loads(higgs_json.read_text())
    
    return qrng_bounds, ff_bounds, higgs_bounds


def main():
    ap = argparse.ArgumentParser(description='Plot dominance boundary')
    ap.add_argument('--m-phi-min', type=float, default=2e-16,
                   help='Minimum scalar mass (GeV)')
    ap.add_argument('--m-phi-max', type=float, default=2e-10,
                   help='Maximum scalar mass (GeV)')
    ap.add_argument('--n-m-phi', type=int, default=100,
                   help='Number of mass points')
    ap.add_argument('--theta-min', type=float, default=1e-22,
                   help='Minimum mixing angle')
    ap.add_argument('--theta-max', type=float, default=1e-18,
                   help='Maximum mixing angle')
    ap.add_argument('--n-theta', type=int, default=100,
                   help='Number of angle points')
    ap.add_argument('--Theta-lab', type=float, default=1.0,
                   help='Screening factor for lab experiments')
    ap.add_argument('--br-max', type=float, default=0.145,
                   help='Maximum allowed BR(H→inv)')
    ap.add_argument('--qrng-json', type=str,
                   default='experiments/grok_qrng/results/lfdr_withinrun/global_summary.json',
                   help='QRNG bounds JSON')
    ap.add_argument('--ff-json', type=str,
                   default='experiments/constraints/results/fifth_force_bounds.json',
                   help='Fifth-force bounds JSON')
    ap.add_argument('--higgs-json', type=str,
                   default='experiments/constraints/results/higgs_portal_bounds.json',
                   help='Higgs portal bounds JSON')
    ap.add_argument('--envelope', type=str,
                   default='experiments/constraints/data/fifth_force_exclusion_envelope.csv',
                   help='Envelope CSV')
    ap.add_argument('--out', type=str,
                   default='experiments/constraints/results/dominance_boundary_plot.png',
                   help='Output file path')
    args = ap.parse_args()
    
    # Load constraints
    qrng_bounds, ff_bounds, higgs_bounds = load_constraint_bounds(
        Path(args.qrng_json),
        Path(args.ff_json),
        Path(args.higgs_json)
    )
    
    # Load envelope
    envelope_data = None
    if Path(args.envelope).exists():
        envelope_data = pd.read_csv(args.envelope)
    
    # Create plot
    create_dominance_plot(
        args.m_phi_min, args.m_phi_max, args.n_m_phi,
        args.theta_min, args.theta_max, args.n_theta,
        qrng_bounds, ff_bounds, higgs_bounds,
        envelope_data,
        Theta_lab=args.Theta_lab,
        br_max=args.br_max,
        use_normalized_slack=True,
        output_path=Path(args.out)
    )
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

