#!/usr/bin/env python3
"""
Active constraint labeling: identify which constraint is tightest for each viable point.

For each point in parameter space, compute slack (distance to violation) for each constraint,
then label the point with the constraint that has the smallest slack (is tightest).
"""
import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


# Constraint labels
CONSTRAINT_LABELS = {
    0: 'ATLAS_mu',
    1: 'Higgs_inv',
    2: 'Fifth_force',
    3: 'QRNG_tilt',
    -1: 'Excluded'
}


def compute_atlas_mu_slack(alpha: float, lambda_m: float) -> Tuple[float, float]:
    """
    Compute slack to ATLAS μ constraint.
    
    ATLAS μ = 1.023 ± 0.056 (from ATLAS-CONF-2025-006)
    Portal coupling affects signal strength deviation.
    
    Simplified: μ deviation ∝ α (for small mixing)
    Slack = distance to 2σ limit (μ < 1.135 or μ > 0.911)
    
    Args:
        alpha: Yukawa strength
        lambda_m: Range (m)
    
    Returns:
        (slack, bound) where:
          slack: Slack (positive if viable, negative if excluded)
          bound: 2σ uncertainty (0.112) for normalization
    """
    # Simplified: μ deviation scales with α
    # More complete would map α → portal coupling → μ
    mu_deviation = alpha * 1e6  # Rough scaling
    mu_upper = 1.023 + 2 * 0.056  # 2σ upper limit
    mu_lower = 1.023 - 2 * 0.056  # 2σ lower limit
    bound = 2 * 0.056  # 2σ uncertainty for normalization
    
    # Slack is distance to nearest violation
    if mu_deviation > 0:
        slack = mu_upper - (1.0 + mu_deviation)
    else:
        slack = (1.0 + mu_deviation) - mu_lower
    
    return slack, bound


def compute_higgs_inv_slack(alpha: float, lambda_m: float, m_phi: float, 
                            br_max: float = 0.145) -> Tuple[float, float]:
    """
    Compute slack to Higgs invisible width constraint.
    
    BR(H→inv) < 0.145 @ 95% CL (conservative) or ~0.107 (tight mode)
    Portal coupling affects invisible branching ratio.
    
    Simplified: BR(H→inv) ∝ α (for small mixing)
    Slack = br_max - BR(H→inv)
    
    Args:
        alpha: Yukawa strength
        lambda_m: Range (m)
        m_phi: Scalar mass (GeV) - needed for phase space
        br_max: Maximum allowed BR (default 0.145 conservative, 0.107 tight)
    
    Returns:
        (slack, bound) where:
          slack: Slack (positive if viable, negative if excluded)
          bound: Maximum allowed BR (for normalization)
    """
    # Simplified: BR scales with α
    # More complete: BR = Γ(H→φφ) / Γ_H_total
    # For m_φ < m_H/2, phase space is open
    if m_phi < 62.5:  # m_H/2
        br_inv = alpha * 0.1  # Rough scaling
    else:
        br_inv = 0.0  # Phase space closed
    
    slack = br_max - br_inv
    return slack, br_max


def compute_fifth_force_slack(alpha: float, lambda_m: float,
                              envelope_data: Optional[pd.DataFrame] = None,
                              alpha_max_allowed: Optional[float] = None,
                              Theta_lab: float = 1.0) -> Tuple[float, float]:
    """
    Compute slack to fifth-force envelope constraint.
    
    Uses existing envelope or alpha_max_allowed.
    Applies screening factor Θ_lab to alpha (for macroscopic experiments).
    Slack = alpha_max_allowed - alpha_eff where alpha_eff = Theta_lab^2 * alpha
    
    Args:
        alpha: Yukawa strength (unscreened)
        lambda_m: Range (m)
        envelope_data: Optional envelope DataFrame
        alpha_max_allowed: Optional maximum allowed alpha
        Theta_lab: Screening factor for lab experiments (default 1.0 = unscreened)
    
    Returns:
        (slack, bound) where:
          slack: Slack (positive if viable, negative if excluded)
          bound: Maximum allowed alpha (for normalization)
    """
    # Apply screening: alpha_eff = Theta_lab^2 * alpha
    alpha_eff = (Theta_lab ** 2) * alpha
    
    if alpha_max_allowed is not None:
        alpha_max = alpha_max_allowed
    elif envelope_data is not None:
        # Interpolate envelope at this lambda
        excluded = envelope_data[envelope_data['excluded'] == 1]
        if len(excluded) > 0:
            excluded_sorted = excluded.sort_values('lambda')
            # Find minimum alpha at this lambda (most restrictive)
            # Simple: use global minimum for now
            alpha_max = excluded_sorted['alpha'].min()
        else:
            alpha_max = 1e-3  # Default
    else:
        alpha_max = 1e-6  # Default from bounds JSON
    
    slack = alpha_max - alpha_eff
    return slack, alpha_max


def compute_qrng_tilt_slack(alpha: float, lambda_m: float,
                            epsilon_max: float = 0.002292) -> Tuple[float, float]:
    """
    Compute slack to QRNG tilt constraint.
    
    |ε| < 0.002292 (from lfdr_withinrun results, 95% CL)
    Updated from 0.0008 to match experimental data (calibrate_qrng_physics.py)
    Tilt relates to ethical bias: ε ∝ η(ΔE - ⟨ΔE⟩)
    For small mixing: η ∝ α
    
    Simplified: ε ∝ α
    Slack = epsilon_max - |ε|
    
    Args:
        alpha: Yukawa strength
        lambda_m: Range (m)
        epsilon_max: Maximum allowed tilt (default 0.0008)
    
    Returns:
        (slack, bound) where:
          slack: Slack (positive if viable, negative if excluded)
          bound: Maximum allowed epsilon (for normalization)
    """
    # Simplified: ε scales with α
    epsilon = alpha * 1e3  # Rough scaling
    slack = epsilon_max - abs(epsilon)
    return slack, epsilon_max


def label_constraints_for_grid(lambda_grid: np.ndarray, alpha_grid: np.ndarray,
                               m_phi_grid: Optional[np.ndarray] = None,
                               envelope_data: Optional[pd.DataFrame] = None,
                               alpha_max_allowed: Optional[float] = None,
                               epsilon_max: float = 0.002292,
                               Theta_lab: float = 1.0,
                               br_max: float = 0.145,
                               use_normalized_slack: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Label each point in grid with tightest constraint.
    
    Uses normalized slack for comparison: normalized_slack = slack / bound
    This allows fair comparison across constraints with different scales.
    
    Args:
        lambda_grid: Lambda values (m)
        alpha_grid: Alpha values (unscreened)
        m_phi_grid: Optional scalar mass grid (GeV) for Higgs constraint
        envelope_data: Optional envelope DataFrame
        alpha_max_allowed: Optional maximum allowed alpha
        epsilon_max: Maximum allowed QRNG tilt
        Theta_lab: Screening factor for lab experiments (applied only to fifth-force)
        br_max: Maximum allowed BR(H→inv) (default 0.145 conservative, 0.107 tight)
        use_normalized_slack: If True, compare normalized slack instead of raw slack
    
    Returns:
        (constraint_labels, slacks) where:
          constraint_labels: array of constraint indices (-1=excluded, 0-3=constraint types)
          slacks: array of (n_points, n_constraints) slack values (raw or normalized based on flag)
    """
    shape = lambda_grid.shape
    n_constraints = 4
    
    # Initialize
    slacks_raw = np.zeros((shape[0], shape[1], n_constraints))
    slacks_normalized = np.zeros((shape[0], shape[1], n_constraints))
    bounds = np.zeros((shape[0], shape[1], n_constraints))
    constraint_labels = np.full(shape, -1, dtype=int)
    
    # Compute slacks for each constraint
    for i in range(shape[0]):
        for j in range(shape[1]):
            lam = lambda_grid[i, j]
            alp = alpha_grid[i, j]
            
            # Derive m_phi from lambda if not provided
            if m_phi_grid is not None:
                m_phi = m_phi_grid[i, j]
            else:
                # λ = ħc / (m_φ c²), so m_φ = ħc / (λ c²)
                # Using ħc ≈ 197.3e-15 GeV·m
                m_phi = 197.3e-15 / lam  # GeV
            
            # Compute slacks (now return (slack, bound) tuples)
            # Collider constraints: unscreened (Θ_collider = 1, collisions are microscopic/high-energy)
            slack_atlas, bound_atlas = compute_atlas_mu_slack(alp, lam)
            slack_higgs, bound_higgs = compute_higgs_inv_slack(alp, lam, m_phi, br_max=br_max)
            # Fifth-force: screened (Θ_lab << 1 for macroscopic experiments)
            slack_ff, bound_ff = compute_fifth_force_slack(alp, lam, envelope_data, alpha_max_allowed, Theta_lab=Theta_lab)
            slack_qrng, bound_qrng = compute_qrng_tilt_slack(alp, lam, epsilon_max)
            
            # Store raw slacks and bounds
            slacks_raw[i, j, 0] = slack_atlas
            slacks_raw[i, j, 1] = slack_higgs
            slacks_raw[i, j, 2] = slack_ff
            slacks_raw[i, j, 3] = slack_qrng
            
            bounds[i, j, 0] = bound_atlas
            bounds[i, j, 1] = bound_higgs
            bounds[i, j, 2] = bound_ff
            bounds[i, j, 3] = bound_qrng
            
            # Compute normalized slack: (bound - value) / bound = slack / bound
            # For constraints where slack = bound - value, normalized_slack = slack / bound
            slacks_normalized[i, j, 0] = slack_atlas / bound_atlas if bound_atlas > 0 else slack_atlas
            slacks_normalized[i, j, 1] = slack_higgs / bound_higgs if bound_higgs > 0 else slack_higgs
            slacks_normalized[i, j, 2] = slack_ff / bound_ff if bound_ff > 0 else slack_ff
            slacks_normalized[i, j, 3] = slack_qrng / bound_qrng if bound_qrng > 0 else slack_qrng
            
            # Use normalized or raw slack for comparison
            slacks_to_compare = slacks_normalized if use_normalized_slack else slacks_raw
            
            # Check if viable (all slacks > 0)
            if np.all(slacks_to_compare[i, j, :] > 0):
                # Find tightest constraint (smallest normalized slack)
                tightest = np.argmin(slacks_to_compare[i, j, :])
                constraint_labels[i, j] = tightest
            else:
                constraint_labels[i, j] = -1  # Excluded
    
    # Return the slacks that were used for comparison
    slacks = slacks_normalized if use_normalized_slack else slacks_raw
    return constraint_labels, slacks


def plot_constraint_heatmap(lambda_grid: np.ndarray, alpha_grid: np.ndarray,
                           constraint_labels: np.ndarray,
                           output_path: Path):
    """Plot heatmap showing which constraint is tightest."""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create colormap
    cmap = plt.cm.get_cmap('tab10', 5)
    
    # Plot
    im = ax.pcolormesh(lambda_grid, alpha_grid, constraint_labels,
                      cmap=cmap, vmin=-1, vmax=4, shading='auto')
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Range λ (meters)', fontsize=12)
    ax.set_ylabel('Yukawa strength α', fontsize=12)
    ax.set_title('Active Constraint Map\n(Color indicates tightest constraint)', fontsize=14)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax, ticks=[-1, 0, 1, 2, 3])
    cbar.set_ticklabels(['Excluded', 'ATLAS μ', 'Higgs inv', 'Fifth-force', 'QRNG tilt'])
    cbar.set_label('Tightest Constraint', fontsize=11)
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved heatmap: {output_path}")
    plt.close()


def plot_constraint_histogram(constraint_labels: np.ndarray, output_path: Path):
    """Plot histogram showing constraint dominance."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Count points by constraint
    viable_mask = constraint_labels >= 0
    viable_labels = constraint_labels[viable_mask]
    
    counts = {}
    for label_idx, label_name in CONSTRAINT_LABELS.items():
        if label_idx >= 0:
            counts[label_name] = int(np.sum(viable_labels == label_idx))
    
    # Plot
    labels = list(counts.keys())
    values = list(counts.values())
    colors = plt.cm.tab10(range(len(labels)))
    
    bars = ax.bar(labels, values, color=colors, alpha=0.7, edgecolor='black')
    ax.set_ylabel('Number of Viable Points', fontsize=12)
    ax.set_xlabel('Tightest Constraint', fontsize=12)
    ax.set_title('Constraint Dominance\n(Which constraint limits the most points?)', fontsize=14)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add percentage labels
    total = sum(values)
    for bar, val in zip(bars, values):
        height = bar.get_height()
        pct = 100 * val / total if total > 0 else 0
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val}\n({pct:.1f}%)',
               ha='center', va='bottom', fontsize=10)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved histogram: {output_path}")
    plt.close()
    
    return counts


def main():
    ap = argparse.ArgumentParser(description='Label viable points with tightest constraint')
    ap.add_argument('--lambda-grid', type=str, required=True,
                   help='Path to lambda grid (CSV or JSON)')
    ap.add_argument('--alpha-grid', type=str, required=True,
                   help='Path to alpha grid (CSV or JSON)')
    ap.add_argument('--envelope', type=str,
                   default='experiments/constraints/data/fifth_force_exclusion_envelope.csv',
                   help='Path to envelope CSV')
    ap.add_argument('--alpha-max', type=float, default=None,
                   help='Maximum allowed alpha (overrides envelope)')
    ap.add_argument('--epsilon-max', type=float, default=0.0008,
                   help='Maximum allowed QRNG tilt')
    ap.add_argument('--out-dir', type=str,
                   default='experiments/constraints/results',
                   help='Output directory')
    args = ap.parse_args()
    
    # Load grids (simplified - would need actual grid loading)
    # For now, create from overlap results
    # In practice, this would load from check_overlap_region output
    
    # Load envelope
    envelope_path = Path(args.envelope)
    envelope_data = None
    if envelope_path.exists():
        envelope_data = pd.read_csv(envelope_path)
    
    # Create example grid (in practice, load from overlap analysis)
    lambda_range = np.logspace(-6, -1, 100)
    alpha_range = np.logspace(-12, -6, 100)
    lambda_grid, alpha_grid = np.meshgrid(lambda_range, alpha_range)
    
    # Label constraints
    constraint_labels, slacks = label_constraints_for_grid(
        lambda_grid, alpha_grid,
        envelope_data=envelope_data,
        alpha_max_allowed=args.alpha_max,
        epsilon_max=args.epsilon_max
    )
    
    # Output directory
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Plot heatmap
    heatmap_path = out_dir / 'active_constraint_heatmap.png'
    plot_constraint_heatmap(lambda_grid, alpha_grid, constraint_labels, heatmap_path)
    
    # Plot histogram
    hist_path = out_dir / 'constraint_dominance_histogram.png'
    counts = plot_constraint_histogram(constraint_labels, hist_path)
    
    # Save summary
    summary = {
        'total_points': int(constraint_labels.size),
        'viable_points': int(np.sum(constraint_labels >= 0)),
        'excluded_points': int(np.sum(constraint_labels == -1)),
        'constraint_counts': counts,
        'constraint_percentages': {
            name: 100 * count / sum(counts.values()) if sum(counts.values()) > 0 else 0
            for name, count in counts.items()
        }
    }
    
    summary_path = out_dir / 'active_constraint_summary.json'
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"✓ Saved summary: {summary_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("ACTIVE CONSTRAINT SUMMARY")
    print("="*60)
    print(f"Total points: {summary['total_points']:,}")
    print(f"Viable points: {summary['viable_points']:,}")
    print(f"Excluded points: {summary['excluded_points']:,}")
    print()
    print("Constraint dominance:")
    for name, pct in summary['constraint_percentages'].items():
        print(f"  {name}: {pct:.1f}%")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

