#!/usr/bin/env python3
"""
Regression test for constraint dominance (baseline-scoped).

Ensures that normalized slack comparison produces the expected dominance split
for BASELINE parameters:
- epsilon_max = 0.002292 (data-derived)
- mu_sb = None (no scale-breaking)
- Theta_lab = 1.0 (unscreened)
- br_max = 0.145 (conservative)

Expected baseline dominance:
- QRNG_tilt: ~86.7%
- ATLAS_mu: ~13.3%
- Fifth_force: ~0%
- Higgs_inv: ~0%

This prevents the scale-trap (raw slack bias) from creeping back in.
NOTE: This test locks in baseline behavior. Legitimate physics updates (like
changing epsilon_max from new data) should update the baseline parameters.
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent))

from check_overlap_derived_alpha import compute_viable_region_derived_alpha, load_constraint_bounds
import pandas as pd


def test_dominance_regression(
    m_phi_min: float = 2e-16,
    m_phi_max: float = 2e-10,
    n_m_phi: int = 50,
    theta_min: float = 1e-22,
    theta_max: float = 1e-18,
    n_theta: int = 50,
    tolerance: float = 2.0,  # ±2% tolerance
    # Baseline parameters (explicit)
    epsilon_max: float = 0.002292,  # Data-derived from QRNG experiments
    mu_sb: Optional[float] = None,  # No scale-breaking
    Theta_lab: float = 1.0,  # Unscreened
    br_max: float = 0.145  # Conservative collider bound
) -> bool:
    """
    Run regression test and check dominance percentages.
    
    Returns:
        True if test passes, False otherwise
    """
    # Load constraints
    qrng_bounds, ff_bounds, higgs_bounds = load_constraint_bounds(
        Path('experiments/grok_qrng/results/lfdr_withinrun/global_summary.json'),
        Path('experiments/constraints/results/fifth_force_bounds.json'),
        Path('experiments/constraints/results/higgs_portal_bounds.json')
    )
    
    # Load envelope
    envelope_data = None
    envelope_path = Path('experiments/constraints/data/fifth_force_exclusion_envelope.csv')
    if envelope_path.exists():
        envelope_data = pd.read_csv(envelope_path)
    
    # Run with baseline parameters (explicit)
    # Override qrng_bounds epsilon_max if needed
    if qrng_bounds:
        # Use baseline epsilon_max
        qrng_bounds['epsilon_upper_95'] = epsilon_max
    
    summary = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, n_m_phi,
        theta_min, theta_max, n_theta,
        qrng_bounds, ff_bounds, higgs_bounds,
        envelope_data,
        model='normalized',
        Theta_lab=Theta_lab,  # Baseline: unscreened
        br_max=br_max,  # Baseline: conservative
        use_normalized_slack=True,  # Explicitly use normalized slack
        mu_sb=mu_sb,  # Baseline: no scale-breaking
        output_dir=None  # Don't save outputs for test
    )
    
    # Check if viable region exists
    n_viable = summary.get('n_viable_points', 0)
    if n_viable == 0:
        print("❌ No viable region found!")
        return False
    
    # Extract dominance percentages
    constraint_dom = summary.get('constraint_dominance', {})
    if isinstance(constraint_dom, dict) and 'percentages' in constraint_dom:
        percentages = constraint_dom['percentages']
    else:
        # Fallback: try direct access
        percentages = summary.get('constraint_percentages', {})
    
    # Expected values (from validation results)
    expected = {
        'QRNG_tilt': 86.7,
        'ATLAS_mu': 13.3,
        'Fifth_force': 0.0,
        'Higgs_inv': 0.0
    }
    
    # Check each constraint
    all_passed = True
    print("\n" + "=" * 60)
    print("REGRESSION TEST: Constraint Dominance")
    print("=" * 60)
    print(f"Tolerance: ±{tolerance}%")
    print()
    
    for constraint_name, expected_pct in expected.items():
        actual_pct = percentages.get(constraint_name, 0.0)
        delta = abs(actual_pct - expected_pct)
        
        if delta <= tolerance:
            status = "✓ PASS"
        else:
            status = "✗ FAIL"
            all_passed = False
        
        print(f"{status}: {constraint_name}")
        print(f"  Expected: {expected_pct:.1f}%")
        print(f"  Actual:   {actual_pct:.1f}%")
        print(f"  Delta:    {delta:.1f}%")
        print()
    
    # Summary
    print("=" * 60)
    if all_passed:
        print("✓ All dominance percentages within tolerance")
        print("✓ Normalized slack comparison is working correctly")
    else:
        print("✗ Some dominance percentages outside tolerance")
        print("✗ Possible regression: check if normalized slack is being used")
    print("=" * 60)
    
    return all_passed


def main():
    ap = argparse.ArgumentParser(description='Regression test for constraint dominance')
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
    ap.add_argument('--tolerance', type=float, default=2.0,
                   help='Tolerance for dominance percentages (default 2.0%%)')
    args = ap.parse_args()
    
    passed = test_dominance_regression(
        args.m_phi_min, args.m_phi_max, args.n_m_phi,
        args.theta_min, args.theta_max, args.n_theta,
        tolerance=args.tolerance
    )
    
    return 0 if passed else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())

