#!/usr/bin/env python3
"""
Higgs portal constraint mapping for MQGT-SCF scalar fields.

Maps Higgs-portal couplings (g_PhiH, g_EH) and scalar masses (m_Phi, m_E)
to collider/invisible-width bounds.

Conservative approach: accepts externally provided limit numbers/curves.
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import matplotlib.pyplot as plt

def load_higgs_limits(config_path: Path) -> Dict:
    """
    Load Higgs portal limits from JSON config.
    
    Expected format:
    {
      "invisible_width_limit": 0.1,  # MeV (example)
      "signal_strength_deviation": 0.05,  # fractional
      "mass_range": [1, 1000],  # GeV
      "coupling_range": [1e-6, 1e-2]
    }
    """
    if not config_path.exists():
        # Create placeholder with conservative LHC bounds
        print(f"Warning: {config_path} not found. Creating placeholder limits.")
        placeholder = {
            "invisible_width_limit": 0.1,  # MeV (conservative)
            "signal_strength_deviation": 0.05,
            "mass_range_gev": [1.0, 1000.0],
            "coupling_range": [1e-6, 1e-2],
            "note": "Placeholder limits - replace with real LHC/HL-LHC bounds"
        }
        config_path.write_text(json.dumps(placeholder, indent=2))
        print(f"Created placeholder: {config_path}")
    
    return json.loads(config_path.read_text())

def compute_excluded_region(limits: Dict, m_phi_range: np.ndarray, 
                           g_phiH_range: np.ndarray) -> np.ndarray:
    """
    Compute excluded region in (m_Phi, g_PhiH) space.
    
    Simple model: exclusion if invisible width exceeds limit OR
    signal strength deviation exceeds limit.
    """
    M_H = 125.0  # Higgs mass (GeV)
    Gamma_H_SM = 4.1  # SM Higgs width (MeV)
    
    excluded = np.zeros((len(m_phi_range), len(g_phiH_range)), dtype=bool)
    
    for i, m_phi in enumerate(m_phi_range):
        for j, g_phiH in enumerate(g_phiH_range):
            # Simple invisible width estimate (tree-level, simplified)
            if m_phi < M_H / 2:
                # Higgs can decay to Phi pairs
                # Rough estimate: Gamma_inv ~ g_phiH^2 * M_H^3 / (8*pi*m_phi^2)
                # (This is a placeholder - real calculation needs full model)
                gamma_inv_est = (g_phiH**2 * M_H**3) / (8 * np.pi * m_phi**2) * 1e-3  # Convert to MeV
                if gamma_inv_est > limits.get('invisible_width_limit', 0.1):
                    excluded[i, j] = True
            
            # Signal strength deviation (simplified)
            # Rough estimate: deviation ~ g_phiH^2 * (some function of m_phi)
            deviation_est = g_phiH**2 * (M_H / m_phi)**2 * 1e-3
            if deviation_est > limits.get('signal_strength_deviation', 0.05):
                excluded[i, j] = True
    
    return excluded

def plot_higgs_bounds(limits: Dict, output_path: Path):
    """
    Plot allowed/excluded region in (m_Phi, g_PhiH) space.
    """
    m_phi_min, m_phi_max = limits.get('mass_range_gev', [1.0, 1000.0])
    g_min, g_max = limits.get('coupling_range', [1e-6, 1e-2])
    
    m_phi_vals = np.logspace(np.log10(m_phi_min), np.log10(m_phi_max), 100)
    g_phiH_vals = np.logspace(np.log10(g_min), np.log10(g_max), 100)
    
    M_phi, G_phiH = np.meshgrid(m_phi_vals, g_phiH_vals)
    
    excluded = compute_excluded_region(limits, m_phi_vals, g_phiH_vals)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot excluded region
    ax.contourf(M_phi, G_phiH, excluded.T, levels=[0.5, 1.5], 
               colors=['red'], alpha=0.3, label='Excluded (LHC bounds)')
    
    # Plot boundary
    # Find boundary curve (simplified)
    boundary_m = []
    boundary_g = []
    for i, m in enumerate(m_phi_vals):
        for j, g in enumerate(g_phiH_vals):
            if excluded[i, j] and (i == 0 or not excluded[i-1, j]):
                boundary_m.append(m)
                boundary_g.append(g)
                break
    
    if boundary_m:
        ax.plot(boundary_m, boundary_g, 'r-', linewidth=2, label='Current bound')
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Scalar mass m_Φ (GeV)', fontsize=12)
    ax.set_ylabel('Higgs-portal coupling g_ΦH', fontsize=12)
    ax.set_title('Higgs Portal Constraints\nCollider/Invisible-Width Bounds', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()
    
    # Save bounds summary
    bounds_json = {
        'mass_range_gev': [float(m_phi_min), float(m_phi_max)],
        'coupling_range': [float(g_min), float(g_max)],
        'invisible_width_limit_mev': limits.get('invisible_width_limit', 0.1),
        'signal_strength_deviation': limits.get('signal_strength_deviation', 0.05)
    }
    json_path = output_path.with_suffix('.json')
    json_path.write_text(json.dumps(bounds_json, indent=2))
    print(f"✓ Saved bounds: {json_path}")

def main():
    ap = argparse.ArgumentParser(description='Map Higgs portal parameters to collider bounds')
    ap.add_argument('--config', type=str,
                   default='experiments/constraints/data/higgs_limits.json',
                   help='Input JSON config with limits')
    ap.add_argument('--out', type=str,
                   default='experiments/constraints/results/higgs_portal_bounds.png',
                   help='Output PNG path')
    args = ap.parse_args()
    
    config_path = Path(args.config)
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    limits = load_higgs_limits(config_path)
    plot_higgs_bounds(limits, output_path)
    print("Done.")

if __name__ == '__main__':
    main()

