#!/usr/bin/env python3
"""
Sweep μ_sb (scale-breaking) parameter and generate phase diagram showing dominance transitions.

This is the "one figure to rule them all" - shows where QRNG_tilt → ATLAS_mu transitions occur,
and where Higgs_inv / Fifth_force become active as μ_sb suppression changes.

Plot: x = log10(mu_sb/m_h), y = log10(theta), color = dominant constraint
"""
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from collections import Counter
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from derive_alpha_from_portal import map_parameters_to_yukawa
from check_overlap_derived_alpha import load_constraint_bounds, compute_viable_region_derived_alpha
from active_constraint_labeling import CONSTRAINT_LABELS


def print_dominance_diagnostic(
    mu_sb_ratio: float,
    percentages: Dict[str, float],
    norm_slacks: Dict[str, np.ndarray],
    n_viable: int
):
    """
    Print compact dominance diagnostic block for a given μ_sb value.
    
    Format:
    μ_sb/m_h = 1e-2
    dominant fractions: QRNG_tilt 78%, ATLAS_mu 12%, Higgs_inv 8%, Fifth_force 2%
    median normalized slack (top3): QRNG_tilt 0.91, ATLAS_mu 0.94, Higgs_inv 0.97
    """
    # Sort constraints by percentage
    sorted_constraints = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    
    # Format fractions
    frac_str = ", ".join([f"{name} {pct:.1f}%" for name, pct in sorted_constraints[:4]])
    
    # Compute median normalized slack for top-3
    top3_names = [name for name, _ in sorted_constraints[:3]]
    median_slacks = []
    for name in top3_names:
        if name in norm_slacks and isinstance(norm_slacks[name], np.ndarray):
            arr = norm_slacks[name]
            if arr.size > 0:
                median_slack = float(np.median(arr))
                median_slacks.append(f"{name} {median_slack:.3f}")
    
    median_str = ", ".join(median_slacks) if median_slacks else "N/A"
    
    # Print diagnostic block
    print(f"  μ_sb/m_h = {mu_sb_ratio:.1e}  n={n_viable:,}")
    print(f"  dominant fractions: {frac_str}")
    if median_str != "N/A":
        print(f"  median normalized slack (top3): {median_str}")


def sweep_mu_phase_diagram(
    m_phi_min: float, m_phi_max: float, n_m_phi: int,
    theta_min: float, theta_max: float, n_theta: int,
    mu_sb_min_ratio: float = 1e-4,  # mu_sb/m_h minimum
    mu_sb_max_ratio: float = 1.0,    # mu_sb/m_h maximum (1.0 = no suppression)
    n_mu_sb: int = 20,
    qrng_bounds: Optional[Dict] = None,
    ff_bounds: Optional[Dict] = None,
    higgs_bounds: Optional[Dict] = None,
    envelope_data: Optional[pd.DataFrame] = None,
    Theta_lab: float = 1.0,
    br_max: float = 0.145,
    epsilon_max: Optional[float] = None,  # Override QRNG epsilon_max
    output_dir: Path = None
) -> Dict:
    """
    Sweep μ_sb parameter and compute dominance at each point.
    
    Args:
        m_phi_min, m_phi_max: Scalar mass range (GeV)
        n_m_phi: Number of mass points
        theta_min, theta_max: Mixing angle range
        n_theta: Number of angle points
        mu_sb_min_ratio: Minimum mu_sb/m_h ratio (e.g., 1e-4)
        mu_sb_max_ratio: Maximum mu_sb/m_h ratio (1.0 = no suppression)
        n_mu_sb: Number of mu_sb points
        qrng_bounds, ff_bounds, higgs_bounds: Constraint bounds
        envelope_data: Envelope DataFrame
        Theta_lab: Screening factor for lab experiments
        br_max: Maximum allowed BR(H→inv)
        output_dir: Output directory
    
    Returns:
        Dictionary with sweep results
    """
    M_H = 125.0  # Higgs mass in GeV
    
    # Create mu_sb grid (in units of m_h)
    mu_sb_ratios = np.logspace(
        np.log10(mu_sb_min_ratio),
        np.log10(mu_sb_max_ratio),
        n_mu_sb
    )
    mu_sb_values = mu_sb_ratios * M_H  # Convert to GeV
    
    # Create m_phi and theta grids
    m_phi_range = np.logspace(np.log10(m_phi_min), np.log10(m_phi_max), n_m_phi)
    theta_range = np.logspace(np.log10(theta_min), np.log10(theta_max), n_theta)
    
    # Storage for results
    results = []
    
    print(f"Sweeping {n_mu_sb} μ_sb values × {n_m_phi} m_φ × {n_theta} θ = {n_mu_sb * n_m_phi * n_theta:,} points")
    print(f"μ_sb range: {mu_sb_min_ratio:.2e} to {mu_sb_max_ratio:.2e} × m_h")
    print()
    
    # Sweep mu_sb
    for i, mu_sb in enumerate(mu_sb_values):
        mu_sb_ratio = mu_sb / M_H
        print(f"[{i+1}/{n_mu_sb}] μ_sb/m_h = {mu_sb_ratio:.4e} (μ_sb = {mu_sb:.3e} GeV)")
        
        # Override qrng_bounds epsilon_max if provided
        qrng_bounds_override = dict(qrng_bounds) if qrng_bounds else {}
        if epsilon_max is not None:
            qrng_bounds_override['epsilon_upper_95'] = epsilon_max
            qrng_bounds_override['epsilon_max'] = epsilon_max
        
        # For each mu_sb, run parameter scan
        summary = compute_viable_region_derived_alpha(
            m_phi_min, m_phi_max, n_m_phi,
            theta_min, theta_max, n_theta,
            qrng_bounds_override, ff_bounds, higgs_bounds,
            envelope_data,
            model='normalized',
            Theta_lab=Theta_lab,
            br_max=br_max,
            use_normalized_slack=True,
            mu_sb=mu_sb,
            output_dir=None  # Don't save individual outputs
        )
        
        if summary.get('viable_region_exists', True):
            n_viable = summary.get('n_viable_points', 0)
            constraint_dom = summary.get('constraint_dominance', {})
            if isinstance(constraint_dom, dict) and 'percentages' in constraint_dom:
                percentages = constraint_dom['percentages']
            else:
                percentages = summary.get('constraint_percentages', {})
            
            # Extract normalized slacks if available (for diagnostic block)
            norm_slacks = summary.get('normalized_slacks', {})
            
            # Print dominance diagnostic block
            print_dominance_diagnostic(mu_sb_ratio, percentages, norm_slacks, n_viable)
            
            results.append({
                'mu_sb': float(mu_sb),
                'mu_sb_ratio': float(mu_sb_ratio),
                'log10_mu_sb_ratio': float(np.log10(mu_sb_ratio)),
                'n_viable': n_viable,
                'constraint_dominance': percentages
            })
        else:
            results.append({
                'mu_sb': float(mu_sb),
                'mu_sb_ratio': float(mu_sb_ratio),
                'log10_mu_sb_ratio': float(np.log10(mu_sb_ratio)),
                'n_viable': 0,
                'constraint_dominance': {}
            })
    
    # Create phase diagram plot
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        plot_mu_phase_diagram(results, m_phi_range, theta_range, output_dir, epsilon_max=epsilon_max)
    
    # Save results with metadata
    import datetime
    sweep_results = {
        'metadata': {
            'timestamp': datetime.datetime.now().isoformat(),
            'epsilon_max': float(epsilon_max) if epsilon_max is not None else 'auto',
            'calibration_source': 'QRNG_CALIBRATION.json' if epsilon_max is None else 'manual_override',
            'script_hash': None  # Could add file hash here
        },
        'sweep_parameters': {
            'mu_sb_range': {
                'min_ratio': float(mu_sb_min_ratio),
                'max_ratio': float(mu_sb_max_ratio),
                'n_points': n_mu_sb,
                'values': [float(mu_sb / M_H) for mu_sb in mu_sb_values]
            },
            'm_phi_range': {
                'min': float(m_phi_min),
                'max': float(m_phi_max),
                'n_points': n_m_phi
            },
            'theta_range': {
                'min': float(theta_min),
                'max': float(theta_max),
                'n_points': n_theta
            }
        },
        'results': results
    }
    
    if output_dir:
        json_path = output_dir / 'MU_PHASE_DIAGRAM.json'
        json_path.write_text(json.dumps(sweep_results, indent=2))
        print(f"✓ Saved results: {json_path}")
    
    return sweep_results


def plot_mu_phase_diagram(results: List[Dict], m_phi_range: np.ndarray, 
                         theta_range: np.ndarray, output_dir: Path, epsilon_max: Optional[float] = None):
    """
    Create phase diagram plot: x = log10(mu_sb/m_h), y = log10(theta), color = dominant constraint.
    
    For each mu_sb value, we have aggregate dominance percentages. To create a 2D plot,
    we need to either:
    1. Show aggregate dominance as a function of mu_sb (1D plot)
    2. Run a finer grid for a few mu_sb values and show 2D slices
    3. Interpolate/extrapolate from aggregate results
    
    For now, create a 1D plot showing how dominance changes with mu_sb, and a summary table.
    """
    # Extract data
    mu_sb_ratios = [r['mu_sb_ratio'] for r in results]
    log10_mu_sb_ratios = [r['log10_mu_sb_ratio'] for r in results]
    n_viable = [r['n_viable'] for r in results]
    
    # Extract dominance percentages
    qrng_pct = []
    atlas_pct = []
    higgs_pct = []
    ff_pct = []
    
    for r in results:
        dom = r.get('constraint_dominance', {})
        qrng_pct.append(dom.get('QRNG_tilt', 0.0))
        atlas_pct.append(dom.get('ATLAS_mu', 0.0))
        higgs_pct.append(dom.get('Higgs_inv', 0.0))
        ff_pct.append(dom.get('Fifth_force', 0.0))
    
    # Create figure with two panels
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Panel 1: Dominance percentages vs mu_sb
    ax1.plot(log10_mu_sb_ratios, qrng_pct, 'o-', label='QRNG_tilt', color='#ff7f0e', linewidth=2, markersize=6)
    ax1.plot(log10_mu_sb_ratios, atlas_pct, 's-', label='ATLAS_mu', color='#1f77b4', linewidth=2, markersize=6)
    ax1.plot(log10_mu_sb_ratios, higgs_pct, '^-', label='Higgs_inv', color='#2ca02c', linewidth=2, markersize=6)
    ax1.plot(log10_mu_sb_ratios, ff_pct, 'v-', label='Fifth_force', color='#d62728', linewidth=2, markersize=6)
    
    ax1.set_xlabel('log₁₀(μ_sb / m_h)', fontsize=12)
    ax1.set_ylabel('Dominance Percentage (%)', fontsize=12)
    ax1.set_title('Constraint Dominance vs Scale-Breaking Suppression', fontsize=14)
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([-2, 102])
    
    # Panel 2: Viable points vs mu_sb
    ax2.plot(log10_mu_sb_ratios, n_viable, 'o-', color='black', linewidth=2, markersize=6)
    ax2.set_xlabel('log₁₀(μ_sb / m_h)', fontsize=12)
    ax2.set_ylabel('Number of Viable Points', fontsize=12)
    ax2.set_title('Viable Parameter Space vs Scale-Breaking Suppression', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    plt.tight_layout()
    plot_path = output_dir / 'MU_PHASE_DIAGRAM.png'
    plt.savefig(plot_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved phase diagram: {plot_path}")
    plt.close()
    
    # Create interpretation document
    create_phase_diagram_interpretation(results, output_dir, epsilon_max=epsilon_max)


def create_phase_diagram_interpretation(results: List[Dict], output_dir: Path, epsilon_max: Optional[float] = None):
    """Create markdown interpretation of phase diagram results."""
    import datetime
    md_content = f"""# μ_sb Phase Diagram Interpretation

## Date
{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Calibration Metadata
- **ε_max used:** {epsilon_max if epsilon_max is not None else 'auto (from QRNG_CALIBRATION.json)'}
- **Calibration source:** {'Manual override' if epsilon_max is not None else 'Multi-source calibration (QRNG_CALIBRATION.json)'}
- **Note:** If ε_max = 0.000742, this is the pooled point estimate from multi-source QRNG calibration (95% CI: [0.000000, 0.001904]). The CI lower bound of 0.000000 is a bootstrap edge case due to finite-sample effects, not a physical zero.

## Overview
Phase diagram showing how constraint dominance changes as scale-breaking suppression (μ_sb) varies.
This is the "one figure to rule them all" - shows where bottlenecks switch and which constraints become active.

## Key Findings

### Dominance Transitions

"""
    
    # Find transition points
    prev_dominant = None
    transitions = []
    
    for i, r in enumerate(results):
        dom = r.get('constraint_dominance', {})
        if dom:
            # Find dominant constraint
            dominant = max(dom.items(), key=lambda x: x[1])[0] if dom else None
            
            if prev_dominant is not None and dominant != prev_dominant:
                transitions.append({
                    'mu_sb_ratio': r['mu_sb_ratio'],
                    'log10_mu_sb_ratio': r['log10_mu_sb_ratio'],
                    'from': prev_dominant,
                    'to': dominant
                })
            prev_dominant = dominant
    
    if transitions:
        md_content += "**Dominance Transitions:**\n\n"
        for t in transitions:
            md_content += f"- At μ_sb/m_h = {t['mu_sb_ratio']:.4e} (log₁₀ = {t['log10_mu_sb_ratio']:.2f}): "
            md_content += f"{t['from']} → {t['to']}\n"
        md_content += "\n"
    
    # Summary table
    md_content += "### Summary Table\n\n"
    md_content += "| μ_sb/m_h | log₁₀(μ_sb/m_h) | Viable Points | QRNG_tilt (%) | ATLAS_mu (%) | Higgs_inv (%) | Fifth_force (%) |\n"
    md_content += "|----------|-----------------|---------------|---------------|--------------|----------------|-----------------|\n"
    
    for r in results[::max(1, len(results)//10)]:  # Sample every 10th point
        dom = r.get('constraint_dominance', {})
        md_content += f"| {r['mu_sb_ratio']:.4e} | {r['log10_mu_sb_ratio']:.2f} | {r['n_viable']:,} | "
        md_content += f"{dom.get('QRNG_tilt', 0.0):.1f} | {dom.get('ATLAS_mu', 0.0):.1f} | "
        md_content += f"{dom.get('Higgs_inv', 0.0):.1f} | {dom.get('Fifth_force', 0.0):.1f} |\n"
    
    md_content += f"""

## Interpretation

### Baseline (μ_sb/m_h = 1.0, no suppression)
- QRNG_tilt: ~86.7% (dominant bottleneck)
- ATLAS_mu: ~13.3% (secondary)
- Higgs_inv: ~0%
- Fifth_force: ~0%

### Strong Suppression (μ_sb/m_h << 1)
- As μ_sb decreases, α_eff = α_unscreened * (μ_sb/m_h)^4 becomes very small
- This should relieve QRNG_tilt constraint
- But other constraints (Higgs_inv, Fifth_force) may become active

### Key Questions Answered
1. **Where does QRNG_tilt → ATLAS_mu transition occur?**
   - See transitions table above

2. **Where do Higgs_inv / Fifth_force become active?**
   - See summary table above

3. **Is viable region "narrow knife-edge" or "broad basin"?**
   - Check viable points vs μ_sb plot

4. **What μ_sb range gives most viable space?**
   - See viable points column in summary table

## Next Steps
- Use this phase diagram to decide which experiment to pre-register
- If QRNG_tilt remains dominant across μ_sb range → focus on QRNG calibration
- If collider constraints become judge → focus on LHC Run 3 data
"""
    
    md_path = output_dir / 'MU_PHASE_DIAGRAM.md'
    md_path.write_text(md_content)
    print(f"✓ Saved interpretation: {md_path}")


def main():
    ap = argparse.ArgumentParser(description='Sweep μ_sb and generate phase diagram')
    ap.add_argument('--m-phi-min', type=float, default=2e-16,
                   help='Minimum scalar mass (GeV)')
    ap.add_argument('--m-phi-max', type=float, default=2e-10,
                   help='Maximum scalar mass (GeV)')
    ap.add_argument('--n-m-phi', type=int, default=50,
                   help='Number of mass points')
    ap.add_argument('--theta-min', type=float, default=1e-22,
                   help='Minimum mixing angle')
    ap.add_argument('--theta-max', type=float, default=1e-18,
                   help='Maximum mixing angle')
    ap.add_argument('--n-theta', type=int, default=50,
                   help='Number of angle points')
    ap.add_argument('--mu-sb-min-ratio', type=float, default=1e-4,
                   help='Minimum μ_sb/m_h ratio (default 1e-4)')
    ap.add_argument('--mu-sb-max-ratio', type=float, default=1.0,
                   help='Maximum μ_sb/m_h ratio (default 1.0 = no suppression)')
    ap.add_argument('--n-mu-sb', type=int, default=20,
                   help='Number of μ_sb points')
    ap.add_argument('--Theta-lab', type=float, default=1.0,
                   help='Screening factor for lab experiments')
    ap.add_argument('--br-max', type=float, default=0.145,
                   help='Maximum allowed BR(H→inv)')
    ap.add_argument('--epsilon-max', type=float, default=None,
                   help='Override QRNG epsilon_max (calibrated value). If not provided, loads from QRNG_CALIBRATION.json or qrng_bounds.')
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
    ap.add_argument('--lambda-regime', type=str, default=None,
                   choices=['sub-nm', 'micron-to-meter'],
                   help='λ regime: automatically sets m_phi range')
    ap.add_argument('--out-dir', type=str,
                   default='experiments/constraints/results',
                   help='Output directory')
    args = ap.parse_args()
    
    # Adjust m_phi range based on lambda-regime if specified
    if args.lambda_regime == 'micron-to-meter':
        args.m_phi_min = 2e-16
        args.m_phi_max = 2e-10
        print(f"Using micron-to-meter regime: m_φ = {args.m_phi_min:.3e} to {args.m_phi_max:.3e} GeV")
    elif args.lambda_regime == 'sub-nm':
        args.m_phi_min = 2e-6
        args.m_phi_max = 0.5
        print(f"Using sub-nm regime: m_φ = {args.m_phi_min:.3e} to {args.m_phi_max:.3e} GeV")
    
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
    
    # Run sweep
    results = sweep_mu_phase_diagram(
        args.m_phi_min, args.m_phi_max, args.n_m_phi,
        args.theta_min, args.theta_max, args.n_theta,
        mu_sb_min_ratio=args.mu_sb_min_ratio,
        mu_sb_max_ratio=args.mu_sb_max_ratio,
        n_mu_sb=args.n_mu_sb,
        qrng_bounds=qrng_bounds,
        ff_bounds=ff_bounds,
        higgs_bounds=higgs_bounds,
        envelope_data=envelope_data,
        Theta_lab=args.Theta_lab,
        br_max=args.br_max,
        epsilon_max=args.epsilon_max,
        output_dir=Path(args.out_dir)
    )
    
    print("\n" + "="*60)
    print("μ_sb PHASE DIAGRAM COMPLETE")
    print("="*60)
    print(f"Results saved to: {Path(args.out_dir)}")
    print(f"  - MU_PHASE_DIAGRAM.json (raw data)")
    print(f"  - MU_PHASE_DIAGRAM.png (plot)")
    print(f"  - MU_PHASE_DIAGRAM.md (interpretation)")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

