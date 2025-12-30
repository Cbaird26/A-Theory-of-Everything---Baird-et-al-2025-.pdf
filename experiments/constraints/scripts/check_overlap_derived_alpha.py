#!/usr/bin/env python3
"""
Check overlap region using derived α from fundamental parameters.

Instead of scanning (λ, α) directly, scans (m_φ, θ) and derives α and λ.
This prevents "dial α to zero" escape.
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
from pathlib import Path
# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from derive_alpha_from_portal import map_parameters_to_yukawa
from active_constraint_labeling import (
    label_constraints_for_grid,
    plot_constraint_heatmap,
    plot_constraint_histogram,
    CONSTRAINT_LABELS
)


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


def compute_viable_region_derived_alpha(
    m_phi_min: float, m_phi_max: float, n_m_phi: int,
    theta_min: float, theta_max: float, n_theta: int,
    qrng_bounds: Optional[Dict],
    ff_bounds: Optional[Dict],
    higgs_bounds: Optional[Dict],
    envelope_data: Optional[pd.DataFrame],
    model: str = 'simple',
    rho: float = 0.0,
    screening: bool = False,
    Theta: float = 1.0,  # Legacy: global screening (deprecated, use Theta_lab)
    Theta_lab: float = 1.0,  # Screening for lab experiments (fifth-force only)
    br_max: float = 0.145,  # Maximum allowed BR(H→inv): 0.145 conservative, 0.107 tight
    use_normalized_slack: bool = True,  # Use normalized slack for dominance comparison
    mu_sb: Optional[float] = None,  # Scale breaking mass (GeV, optional). If provided, applies (μ_sb/m_h)^4 suppression. Note: distinct from ATLAS signal strength μ.
    output_dir: Optional[Path] = None
) -> Dict:
    """
    Compute viable region scanning fundamental parameters (m_φ, θ).
    
    Args:
        m_phi_min, m_phi_max: Scalar mass range (GeV)
        n_m_phi: Number of mass points
        theta_min, theta_max: Mixing angle range
        n_theta: Number of angle points
        qrng_bounds, ff_bounds, higgs_bounds: Constraint bounds
        envelope_data: Envelope DataFrame
        model: 'simple', 'scale_breaking', or 'portal'
        output_dir: Output directory
    
    Returns:
        Summary dict with island coordinates and constraint labels
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
                    rho=rho,
                    model=model,
                    screening=screening,
                    Theta=Theta,
                    mu_sb=mu_sb
                )
                LAMBDA_GRID[i, j] = lambda_m
                ALPHA_GRID[i, j] = alpha
            except Exception as e:
                # Handle edge cases (e.g., very small theta causing issues)
                LAMBDA_GRID[i, j] = np.nan
                ALPHA_GRID[i, j] = np.nan
    
    # Get constraint bounds
    alpha_max_allowed = None
    if ff_bounds:
        alpha_max_allowed = ff_bounds.get('alpha_max_allowed')
    
    # Try to load calibrated epsilon_max from multi-source calibration
    epsilon_max = 0.002292  # Default (previous data-derived value)
    calibration_path = Path('experiments/constraints/results/QRNG_CALIBRATION.json')
    if calibration_path.exists():
        try:
            import json
            with open(calibration_path, 'r') as f:
                calibration = json.load(f)
            pooled = calibration.get('pooled', {})
            if 'epsilon_max' in pooled:
                epsilon_max = pooled['epsilon_max']
                print(f"Using calibrated ε_max from multi-source calibration: {epsilon_max:.6f}")
        except Exception as e:
            print(f"Warning: Could not load calibrated epsilon_max: {e}")
            print(f"  Falling back to default or qrng_bounds value")
    
    # Override with qrng_bounds if provided (for backward compatibility)
    if qrng_bounds:
        eps_upper = qrng_bounds.get('epsilon_upper_95')
        if eps_upper is not None:
            epsilon_max = abs(eps_upper)
            print(f"Using ε_max from qrng_bounds: {epsilon_max:.6f}")
    
    # Label constraints
    # Use Theta_lab for differential screening (fifth-force only, collider unscreened)
    # Use normalized slack for fair comparison across constraints
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
    
    # Create viable mask
    viable_mask = constraint_labels >= 0
    
    # Summarize island
    if viable_mask.sum() == 0:
        print("❌ No viable region found with derived α!")
        return {'viable_region_exists': False}
    
    # Extract viable points
    viable_lambda = LAMBDA_GRID[viable_mask]
    viable_alpha = ALPHA_GRID[viable_mask]
    viable_m_phi = M_PHI_GRID[viable_mask]
    viable_theta = THETA_GRID[viable_mask]
    viable_labels = constraint_labels[viable_mask]
    
    # Compute statistics
    island_summary = {
        'n_viable_points': int(viable_mask.sum()),
        'lambda_m': {
            'min': float(np.min(viable_lambda)),
            'max': float(np.max(viable_lambda)),
            'p05': float(np.percentile(viable_lambda, 5)),
            'p50': float(np.percentile(viable_lambda, 50)),
            'p95': float(np.percentile(viable_lambda, 95)),
        },
        'alpha': {
            'min': float(np.min(viable_alpha)),
            'max': float(np.max(viable_alpha)),
            'p05': float(np.percentile(viable_alpha, 5)),
            'p50': float(np.percentile(viable_alpha, 50)),
            'p95': float(np.percentile(viable_alpha, 95)),
        },
        'm_phi': {
            'min': float(np.min(viable_m_phi)),
            'max': float(np.max(viable_m_phi)),
            'p05': float(np.percentile(viable_m_phi, 5)),
            'p50': float(np.percentile(viable_m_phi, 50)),
            'p95': float(np.percentile(viable_m_phi, 95)),
        },
        'theta': {
            'min': float(np.min(viable_theta)),
            'max': float(np.max(viable_theta)),
            'p05': float(np.percentile(viable_theta, 5)),
            'p50': float(np.percentile(viable_theta, 50)),
            'p95': float(np.percentile(viable_theta, 95)),
        },
    }
    
    # Constraint dominance
    constraint_counts = {}
    for label_idx, label_name in CONSTRAINT_LABELS.items():
        if label_idx >= 0:
            count = int(np.sum(viable_labels == label_idx))
            constraint_counts[label_name] = count
    
    total_viable = sum(constraint_counts.values())
    constraint_percentages = {
        name: 100 * count / total_viable if total_viable > 0 else 0
        for name, count in constraint_counts.items()
    }
    
    island_summary['constraint_dominance'] = {
        'counts': constraint_counts,
        'percentages': constraint_percentages
    }
    
    # Save outputs
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save island summary
        island_json = output_dir / 'overlap_pass3_derived_alpha.json'
        island_json.write_text(json.dumps(island_summary, indent=2))
        print(f"✓ Saved island summary: {island_json}")
        
        # Plot constraint heatmap (in (m_φ, θ) space)
        fig, ax = plt.subplots(figsize=(12, 10))
        im = ax.pcolormesh(M_PHI_GRID, THETA_GRID, constraint_labels,
                          cmap=plt.cm.get_cmap('tab10', 5), vmin=-1, vmax=4, shading='auto')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Scalar Mass m_φ (GeV)', fontsize=12)
        ax.set_ylabel('Mixing Angle θ', fontsize=12)
        ax.set_title('Active Constraint Map (Fundamental Parameters)\n(Color indicates tightest constraint)', fontsize=14)
        cbar = plt.colorbar(im, ax=ax, ticks=[-1, 0, 1, 2, 3])
        cbar.set_ticklabels(['Excluded', 'ATLAS μ', 'Higgs inv', 'Fifth-force', 'QRNG tilt'])
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        heatmap_path = output_dir / 'active_constraint_heatmap_derived.png'
        plt.savefig(heatmap_path, dpi=200, bbox_inches='tight')
        print(f"✓ Saved heatmap: {heatmap_path}")
        plt.close()
        
        # Plot histogram
        hist_path = output_dir / 'constraint_dominance_histogram.png'
        plot_constraint_histogram(constraint_labels, hist_path)
    
    # Print summary
    print("\n" + "="*60)
    print("ISLAND SUMMARY (Derived α)")
    print("="*60)
    print(f"Viable points: {island_summary['n_viable_points']:,}")
    print()
    print("Lambda (range) bounds:")
    print(f"  p05: {island_summary['lambda_m']['p05']:.3e} m ({island_summary['lambda_m']['p05']*1e6:.3f} µm)")
    print(f"  p50: {island_summary['lambda_m']['p50']:.3e} m ({island_summary['lambda_m']['p50']*1e3:.3f} mm)")
    print(f"  p95: {island_summary['lambda_m']['p95']:.3e} m ({island_summary['lambda_m']['p95']*1e2:.3f} cm)")
    print()
    print("Alpha (strength) bounds:")
    print(f"  p05: {island_summary['alpha']['p05']:.3e}")
    print(f"  p50: {island_summary['alpha']['p50']:.3e}")
    print(f"  p95: {island_summary['alpha']['p95']:.3e}")
    print()
    print("Fundamental parameters:")
    print(f"  m_φ: {island_summary['m_phi']['p05']:.3e} - {island_summary['m_phi']['p95']:.3e} GeV")
    print(f"  θ: {island_summary['theta']['p05']:.3e} - {island_summary['theta']['p95']:.3e}")
    print()
    print("Constraint dominance:")
    for name, pct in constraint_percentages.items():
        print(f"  {name}: {pct:.1f}%")
    
    return island_summary


def main():
    ap = argparse.ArgumentParser(description='Check overlap with derived α from fundamental parameters')
    ap.add_argument('--m-phi-min', type=float, default=1e-6,
                   help='Minimum scalar mass (GeV)')
    ap.add_argument('--m-phi-max', type=float, default=1.0,
                   help='Maximum scalar mass (GeV)')
    ap.add_argument('--n-m-phi', type=int, default=200,
                   help='Number of mass points')
    ap.add_argument('--theta-min', type=float, default=1e-6,
                   help='Minimum mixing angle')
    ap.add_argument('--theta-max', type=float, default=0.1,
                   help='Maximum mixing angle')
    ap.add_argument('--n-theta', type=int, default=200,
                   help='Number of angle points')
    ap.add_argument('--model', type=str, default='simple',
                   choices=['simple', 'normalized', 'screened', 'scale_breaking', 'portal'],
                   help='Model type')
    ap.add_argument('--rho', type=float, default=0.0,
                   help='Matter density (kg/m³) for screening')
    ap.add_argument('--screening', action='store_true',
                   help='Enable screening suppression')
    ap.add_argument('--Theta', type=float, default=1.0,
                   help='Legacy: Global screening factor (deprecated, use --Theta-lab)')
    ap.add_argument('--Theta-lab', type=float, default=1.0,
                   help='Screening factor for lab experiments (fifth-force only, 0 < Θ ≤ 1, default 1.0 = unscreened). Collider constraints remain unscreened.')
    ap.add_argument('--br-max', type=float, default=0.145,
                   help='Maximum allowed BR(H→inv): 0.145 (conservative) or 0.107 (tight mode)')
    ap.add_argument('--mu-sb', type=float, default=None,
                   dest='mu_sb',
                   help='Scale breaking mass μ_sb (GeV, optional). If provided, applies (μ_sb/m_h)^4 suppression to α (Burrage et al. 2018). Note: distinct from ATLAS signal strength μ.')
    ap.add_argument('--use-normalized-slack', action='store_true', default=True,
                   help='Use normalized slack for dominance comparison (default: True)')
    ap.add_argument('--no-normalized-slack', dest='use_normalized_slack', action='store_false',
                   help='Use raw slack instead of normalized slack')
    ap.add_argument('--lambda-regime', type=str, default='sub-nm',
                   choices=['sub-nm', 'micron-to-meter'],
                   help='λ regime: sub-nm (m_φ in MeV-GeV) or micron-to-meter (m_φ ultralight)')
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
    ap.add_argument('--out-dir', type=str,
                   default='experiments/constraints/results',
                   help='Output directory')
    args = ap.parse_args()
    
    # Adjust m_φ scan range based on λ regime if defaults are used
    m_phi_min = args.m_phi_min
    m_phi_max = args.m_phi_max
    if args.lambda_regime == 'micron-to-meter':
        # For λ ~ μm to meters, need ultralight m_φ
        # λ = 1 μm → m_φ ≈ 2×10^-10 GeV ≈ 0.2 eV
        # λ = 1 m → m_φ ≈ 2×10^-16 GeV ≈ 2×10^-7 eV
        if args.m_phi_min == 1e-6:  # Using default
            m_phi_min = 2e-16
        if args.m_phi_max == 1.0:  # Using default
            m_phi_max = 2e-10
        print(f"Using micron-to-meter regime: m_φ = {m_phi_min:.3e} to {m_phi_max:.3e} GeV")
    # else: sub-nm regime uses defaults (m_φ in MeV-GeV range)
    
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
    
    # Compute viable region
    # Use Theta_lab for differential screening (fifth-force only)
    # If --Theta is provided (legacy), use it as Theta_lab
    Theta_lab = args.Theta_lab if hasattr(args, 'Theta_lab') else args.Theta
    
    summary = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, args.n_m_phi,
        args.theta_min, args.theta_max, args.n_theta,
        qrng_bounds, ff_bounds, higgs_bounds,
        envelope_data,
        model=args.model,
        rho=args.rho,
        screening=args.screening,
        Theta=args.Theta,  # Legacy
        Theta_lab=Theta_lab,  # Differential screening
        br_max=args.br_max,
        use_normalized_slack=args.use_normalized_slack,
        mu_sb=args.mu_sb,  # Scale breaking mass (distinct from ATLAS signal strength μ)
        output_dir=Path(args.out_dir)
    )
    
    print("\nDone.")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

