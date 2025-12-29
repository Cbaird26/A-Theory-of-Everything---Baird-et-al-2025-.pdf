#!/usr/bin/env python3
"""
Combine constraints from all channels into a single global constraints figure.

Reads:
  - QRNG bounds (from analyze_qrng.py output)
  - Fifth-force bounds (from fifth_force_yukawa.py)
  - Higgs portal bounds (from higgs_portal_bounds.py)

Outputs:
  - Combined figure showing all constraint channels
  - JSON summary of global allowed/excluded regions
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

def load_qrng_bounds(qrng_json_path: Path) -> Optional[Dict]:
    """Load QRNG constraint summary."""
    if not qrng_json_path.exists():
        print(f"Warning: {qrng_json_path} not found. Skipping QRNG bounds.")
        return None
    
    data = json.loads(qrng_json_path.read_text())
    return {
        'epsilon_upper_95': data.get('epsilon_upper_95', None),
        'epsilon_lower_95': data.get('epsilon_lower_95', None),
        'BF10': data.get('BF10', None),
        'n': data.get('n', None)
    }

def load_fifth_force_bounds(ff_json_path: Path) -> Optional[Dict]:
    """Load fifth-force constraint bounds."""
    if not ff_json_path.exists():
        print(f"Warning: {ff_json_path} not found. Skipping fifth-force bounds.")
        return None
    
    return json.loads(ff_json_path.read_text())

def load_higgs_bounds(higgs_json_path: Path) -> Optional[Dict]:
    """Load Higgs portal constraint bounds."""
    if not higgs_json_path.exists():
        print(f"Warning: {higgs_json_path} not found. Skipping Higgs portal bounds.")
        return None
    
    return json.loads(higgs_json_path.read_text())

def create_global_figure(qrng_bounds: Optional[Dict],
                         ff_bounds: Optional[Dict],
                         higgs_bounds: Optional[Dict],
                         output_path: Path):
    """
    Create combined global constraints figure.
    """
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Panel 1: QRNG constraints (epsilon bounds)
    ax1 = fig.add_subplot(gs[0, 0])
    if qrng_bounds:
        eps_upper = qrng_bounds.get('epsilon_upper_95')
        eps_lower = qrng_bounds.get('epsilon_lower_95')
        if eps_upper is not None and eps_lower is not None:
            ax1.barh(0, eps_upper - eps_lower, left=eps_lower, height=0.5,
                    color='blue', alpha=0.5, label='95% CI')
            ax1.axvline(0, color='black', linestyle='--', linewidth=1)
            ax1.set_xlabel('ε (bias parameter)', fontsize=11)
            ax1.set_ylabel('QRNG constraint', fontsize=11)
            ax1.set_title('QRNG Baseline + Modulation\n(n={})'.format(qrng_bounds.get('n', 'N/A')), fontsize=12)
            ax1.set_ylim(-0.5, 0.5)
            ax1.set_xlim(eps_lower - 0.001, eps_upper + 0.001)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
    else:
        ax1.text(0.5, 0.5, 'QRNG bounds\nnot available', 
                ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('QRNG Constraints', fontsize=12)
    
    # Panel 2: Fifth-force (Yukawa) constraints
    ax2 = fig.add_subplot(gs[0, 1])
    if ff_bounds:
        # Placeholder visualization - would show exclusion region
        ax2.text(0.5, 0.5, f"Fifth-Force Bounds\nλ range: {ff_bounds.get('lambda_min', 'N/A'):.2e} - {ff_bounds.get('lambda_max', 'N/A'):.2e} m\nα_max: {ff_bounds.get('alpha_max_allowed', 'N/A'):.2e}",
                ha='center', va='center', transform=ax2.transAxes, fontsize=10)
        ax2.set_title('Fifth-Force (Yukawa) Constraints', fontsize=12)
    else:
        ax2.text(0.5, 0.5, 'Fifth-force bounds\nnot available',
                ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('Fifth-Force Constraints', fontsize=12)
    
    # Panel 3: Higgs portal constraints
    ax3 = fig.add_subplot(gs[1, 0])
    if higgs_bounds:
        mass_range = higgs_bounds.get('mass_range_gev', [1, 1000])
        coupling_range = higgs_bounds.get('coupling_range', [1e-6, 1e-2])
        ax3.text(0.5, 0.5, f"Higgs Portal Bounds\nm_Φ: {mass_range[0]:.1f} - {mass_range[1]:.1f} GeV\n"
                           f"g_ΦH: {coupling_range[0]:.2e} - {coupling_range[1]:.2e}",
                ha='center', va='center', transform=ax3.transAxes, fontsize=10)
        ax3.set_title('Higgs Portal Constraints', fontsize=12)
    else:
        ax3.text(0.5, 0.5, 'Higgs portal bounds\nnot available',
                ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Higgs Portal Constraints', fontsize=12)
    
    # Panel 4: Summary table
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    summary_text = "Global Constraints Summary\n\n"
    summary_text += "Channel\t\tStatus\n"
    summary_text += "-" * 40 + "\n"
    
    if qrng_bounds:
        summary_text += f"QRNG\t\t|ε| < {abs(qrng_bounds.get('epsilon_upper_95', 0)):.4f}\n"
    else:
        summary_text += "QRNG\t\tNot available\n"
    
    if ff_bounds:
        summary_text += f"Fifth-force\tExcluded above α={ff_bounds.get('alpha_max_allowed', 'N/A')}\n"
    else:
        summary_text += "Fifth-force\tNot available\n"
    
    if higgs_bounds:
        summary_text += f"Higgs portal\tBounds on (m_Φ, g_ΦH)\n"
    else:
        summary_text += "Higgs portal\tNot available\n"
    
    ax4.text(0.1, 0.5, summary_text, fontsize=10, family='monospace',
            verticalalignment='center', transform=ax4.transAxes)
    ax4.set_title('Summary', fontsize=12)
    
    plt.suptitle('MQGT-SCF Global Constraints Across Channels', fontsize=16, y=0.98)
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()
    
    # Save combined JSON
    global_summary = {
        'qrng': qrng_bounds,
        'fifth_force': ff_bounds,
        'higgs_portal': higgs_bounds
    }
    json_path = output_path.with_suffix('.json')
    json_path.write_text(json.dumps(global_summary, indent=2))
    print(f"✓ Saved summary: {json_path}")

def main():
    ap = argparse.ArgumentParser(description='Combine all constraint channels into global figure')
    ap.add_argument('--qrng-json', type=str,
                   default='experiments/grok_qrng/results/lfdr_withinrun/global_summary.json',
                   help='QRNG bounds JSON')
    ap.add_argument('--ff-json', type=str,
                   default='experiments/constraints/results/fifth_force_bounds.json',
                   help='Fifth-force bounds JSON')
    ap.add_argument('--higgs-json', type=str,
                   default='experiments/constraints/results/higgs_portal_bounds.json',
                   help='Higgs portal bounds JSON')
    ap.add_argument('--out', type=str,
                   default='experiments/constraints/results/global_constraints.png',
                   help='Output PNG path')
    args = ap.parse_args()
    
    qrng_path = Path(args.qrng_json)
    ff_path = Path(args.ff_json)
    higgs_path = Path(args.higgs_json)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    qrng_bounds = load_qrng_bounds(qrng_path)
    ff_bounds = load_fifth_force_bounds(ff_path)
    higgs_bounds = load_higgs_bounds(higgs_path)
    
    create_global_figure(qrng_bounds, ff_bounds, higgs_bounds, output_path)
    print("Done.")

if __name__ == '__main__':
    main()

