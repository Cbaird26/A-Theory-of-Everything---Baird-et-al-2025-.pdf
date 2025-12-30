#!/usr/bin/env python3
"""
Robustness check: vary constraint bounds by ±10% and test if dominance ranking remains stable.

Tests whether the QRNG_tilt bottleneck is robust to small changes in experimental bounds.
"""
import argparse
import json
from pathlib import Path
from typing import Optional, Dict, List

import numpy as np
import pandas as pd
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from check_overlap_derived_alpha import compute_viable_region_derived_alpha, load_constraint_bounds
from active_constraint_labeling import CONSTRAINT_LABELS


def run_robustness_check(
    m_phi_min: float, m_phi_max: float, n_m_phi: int,
    theta_min: float, theta_max: float, n_theta: int,
    qrng_bounds: Optional[Dict],
    ff_bounds: Optional[Dict],
    higgs_bounds: Optional[Dict],
    envelope_data: Optional[pd.DataFrame],
    Theta_lab: float = 1.0,
    br_max: float = 0.145,
    use_normalized_slack: bool = True,
    variation: float = 0.1  # ±10%
) -> Dict:
    """
    Run robustness check by varying bounds.
    
    Returns:
        Dictionary with results for each bound variation
    """
    results = {}
    
    # Baseline run
    print("Running baseline (no variation)...")
    baseline = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, n_m_phi,
        theta_min, theta_max, n_theta,
        qrng_bounds, ff_bounds, higgs_bounds,
        envelope_data,
        model='normalized',
        Theta_lab=Theta_lab,
        br_max=br_max,
        use_normalized_slack=use_normalized_slack
    )
    results['baseline'] = extract_dominance_summary(baseline)
    
    # Variation 1: QRNG epsilon_max +10%
    print(f"\nRunning QRNG epsilon_max +{variation*100:.0f}%...")
    qrng_bounds_plus = qrng_bounds.copy() if qrng_bounds else {}
    if 'epsilon_upper_95' in qrng_bounds_plus:
        qrng_bounds_plus['epsilon_upper_95'] = qrng_bounds_plus['epsilon_upper_95'] * (1 + variation)
    elif qrng_bounds is None:
        # Create default
        qrng_bounds_plus = {'epsilon_upper_95': 0.0008 * (1 + variation)}
    
    result_plus = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, n_m_phi,
        theta_min, theta_max, n_theta,
        qrng_bounds_plus, ff_bounds, higgs_bounds,
        envelope_data,
        model='normalized',
        Theta_lab=Theta_lab,
        br_max=br_max,
        use_normalized_slack=use_normalized_slack
    )
    results['qrng_plus_10pct'] = extract_dominance_summary(result_plus)
    
    # Variation 2: QRNG epsilon_max -10%
    print(f"\nRunning QRNG epsilon_max -{variation*100:.0f}%...")
    qrng_bounds_minus = qrng_bounds.copy() if qrng_bounds else {}
    if 'epsilon_upper_95' in qrng_bounds_minus:
        qrng_bounds_minus['epsilon_upper_95'] = qrng_bounds_minus['epsilon_upper_95'] * (1 - variation)
    elif qrng_bounds is None:
        qrng_bounds_minus = {'epsilon_upper_95': 0.0008 * (1 - variation)}
    
    result_minus = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, n_m_phi,
        theta_min, theta_max, n_theta,
        qrng_bounds_minus, ff_bounds, higgs_bounds,
        envelope_data,
        model='normalized',
        Theta_lab=Theta_lab,
        br_max=br_max,
        use_normalized_slack=use_normalized_slack
    )
    results['qrng_minus_10pct'] = extract_dominance_summary(result_minus)
    
    # Variation 3: ATLAS μ uncertainty +10%
    print(f"\nRunning ATLAS μ uncertainty +{variation*100:.0f}%...")
    # ATLAS μ constraint is hardcoded in compute_atlas_mu_slack
    # We can't easily vary it without modifying the function
    # For now, skip this variation (would require refactoring)
    results['atlas_plus_10pct'] = {'note': 'ATLAS μ constraint hardcoded, skipping variation'}
    
    # Variation 4: ATLAS μ uncertainty -10%
    results['atlas_minus_10pct'] = {'note': 'ATLAS μ constraint hardcoded, skipping variation'}
    
    # Variation 5: Higgs BR +10%
    print(f"\nRunning Higgs BR +{variation*100:.0f}%...")
    br_max_plus = br_max * (1 + variation)
    result_br_plus = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, n_m_phi,
        theta_min, theta_max, n_theta,
        qrng_bounds, ff_bounds, higgs_bounds,
        envelope_data,
        model='normalized',
        Theta_lab=Theta_lab,
        br_max=br_max_plus,
        use_normalized_slack=use_normalized_slack
    )
    results['higgs_plus_10pct'] = extract_dominance_summary(result_br_plus)
    
    # Variation 6: Higgs BR -10%
    print(f"\nRunning Higgs BR -{variation*100:.0f}%...")
    br_max_minus = br_max * (1 - variation)
    result_br_minus = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, n_m_phi,
        theta_min, theta_max, n_theta,
        qrng_bounds, ff_bounds, higgs_bounds,
        envelope_data,
        model='normalized',
        Theta_lab=Theta_lab,
        br_max=br_max_minus,
        use_normalized_slack=use_normalized_slack
    )
    results['higgs_minus_10pct'] = extract_dominance_summary(result_br_minus)
    
    # Variation 7: Fifth-force alpha_max +10%
    print(f"\nRunning Fifth-force alpha_max +{variation*100:.0f}%...")
    ff_bounds_plus = ff_bounds.copy() if ff_bounds else {}
    if 'alpha_max_allowed' in ff_bounds_plus:
        ff_bounds_plus['alpha_max_allowed'] = ff_bounds_plus['alpha_max_allowed'] * (1 + variation)
    elif ff_bounds is None:
        ff_bounds_plus = {'alpha_max_allowed': 1e-6 * (1 + variation)}
    
    result_ff_plus = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, n_m_phi,
        theta_min, theta_max, n_theta,
        qrng_bounds, ff_bounds_plus, higgs_bounds,
        envelope_data,
        model='normalized',
        Theta_lab=Theta_lab,
        br_max=br_max,
        use_normalized_slack=use_normalized_slack
    )
    results['fifth_force_plus_10pct'] = extract_dominance_summary(result_ff_plus)
    
    # Variation 8: Fifth-force alpha_max -10%
    print(f"\nRunning Fifth-force alpha_max -{variation*100:.0f}%...")
    ff_bounds_minus = ff_bounds.copy() if ff_bounds else {}
    if 'alpha_max_allowed' in ff_bounds_minus:
        ff_bounds_minus['alpha_max_allowed'] = ff_bounds_minus['alpha_max_allowed'] * (1 - variation)
    elif ff_bounds is None:
        ff_bounds_minus = {'alpha_max_allowed': 1e-6 * (1 - variation)}
    
    result_ff_minus = compute_viable_region_derived_alpha(
        m_phi_min, m_phi_max, n_m_phi,
        theta_min, theta_max, n_theta,
        qrng_bounds, ff_bounds_minus, higgs_bounds,
        envelope_data,
        model='normalized',
        Theta_lab=Theta_lab,
        br_max=br_max,
        use_normalized_slack=use_normalized_slack
    )
    results['fifth_force_minus_10pct'] = extract_dominance_summary(result_ff_minus)
    
    return results


def extract_dominance_summary(summary: Dict) -> Dict:
    """Extract dominance percentages from summary."""
    if not summary.get('viable_region_exists', True):  # Default to True if key missing
        return {
            'viable_points': 0,
            'constraint_dominance': {}
        }
    
    n_viable = summary.get('n_viable_points', 0)
    
    # Handle nested structure: constraint_dominance['percentages']
    constraint_dom = summary.get('constraint_dominance', {})
    if isinstance(constraint_dom, dict) and 'percentages' in constraint_dom:
        constraint_percentages = constraint_dom['percentages']
    else:
        # Fallback: try direct access
        constraint_percentages = summary.get('constraint_percentages', {})
    
    return {
        'viable_points': n_viable,
        'constraint_dominance': constraint_percentages
    }


def print_robustness_summary(results: Dict):
    """Print formatted summary of robustness check."""
    print("\n" + "=" * 80)
    print("ROBUSTNESS CHECK SUMMARY")
    print("=" * 80)
    
    baseline = results['baseline']
    baseline_dom = baseline['constraint_dominance']
    
    print(f"\nBaseline:")
    print(f"  Viable points: {baseline['viable_points']:,}")
    print(f"  Dominance:")
    for name, pct in baseline_dom.items():
        print(f"    {name}: {pct:.1f}%")
    
    print("\n" + "-" * 80)
    print("Variations (±10%):")
    print("-" * 80)
    
    # Compare each variation to baseline
    variations = [
        ('QRNG ε_max', 'qrng_plus_10pct', 'qrng_minus_10pct'),
        ('Higgs BR', 'higgs_plus_10pct', 'higgs_minus_10pct'),
        ('Fifth-force α_max', 'fifth_force_plus_10pct', 'fifth_force_minus_10pct'),
    ]
    
    for var_name, plus_key, minus_key in variations:
        print(f"\n{var_name}:")
        
        if plus_key in results and 'note' not in results[plus_key]:
            plus = results[plus_key]
            print(f"  +10%: {plus['viable_points']:,} points")
            for name, pct in plus['constraint_dominance'].items():
                baseline_pct = baseline_dom.get(name, 0)
                delta = pct - baseline_pct
                print(f"    {name}: {pct:.1f}% (Δ{delta:+.1f}%)")
        
        if minus_key in results and 'note' not in results[minus_key]:
            minus = results[minus_key]
            print(f"  -10%: {minus['viable_points']:,} points")
            for name, pct in minus['constraint_dominance'].items():
                baseline_pct = baseline_dom.get(name, 0)
                delta = pct - baseline_pct
                print(f"    {name}: {pct:.1f}% (Δ{delta:+.1f}%)")
    
    # Assess robustness
    print("\n" + "-" * 80)
    print("Robustness Assessment:")
    print("-" * 80)
    
    # Check if QRNG_tilt remains dominant across variations
    qrng_robust = True
    for key, result in results.items():
        if key == 'baseline' or 'note' in result:
            continue
        dom = result.get('constraint_dominance', {})
        qrng_pct = dom.get('QRNG_tilt', 0)
        if qrng_pct < 50:  # If QRNG drops below 50%, it's no longer dominant
            qrng_robust = False
            break
    
    if qrng_robust:
        print("✓ QRNG_tilt bottleneck is ROBUST: remains dominant across ±10% variations")
    else:
        print("✗ QRNG_tilt bottleneck is FRAGILE: dominance shifts with ±10% variations")
    
    # Check if ranking changes
    baseline_ranking = sorted(baseline_dom.items(), key=lambda x: x[1], reverse=True)
    ranking_stable = True
    if len(baseline_ranking) > 0:
        baseline_top = baseline_ranking[0][0]
        for key, result in results.items():
            if key == 'baseline' or 'note' in result:
                continue
            dom = result.get('constraint_dominance', {})
            ranking = sorted(dom.items(), key=lambda x: x[1], reverse=True)
            if len(ranking) > 0 and ranking[0][0] != baseline_top:  # Top constraint changed
                ranking_stable = False
                break
    else:
        ranking_stable = False  # No baseline ranking to compare
    
    if ranking_stable:
        print("✓ Constraint ranking is STABLE: top constraint unchanged across variations")
    else:
        print("✗ Constraint ranking is UNSTABLE: top constraint changes with variations")


def main():
    ap = argparse.ArgumentParser(description='Robustness check: vary bounds ±10%')
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
    ap.add_argument('--Theta-lab', type=float, default=1.0,
                   help='Screening factor for lab experiments')
    ap.add_argument('--br-max', type=float, default=0.145,
                   help='Maximum allowed BR(H→inv)')
    ap.add_argument('--variation', type=float, default=0.1,
                   help='Bound variation fraction (default 0.1 = +/-10%%)')
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
    ap.add_argument('--out-json', type=str,
                   default='experiments/constraints/results/robustness_check_results.json',
                   help='Output JSON file')
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
    
    # Run robustness check
    results = run_robustness_check(
        args.m_phi_min, args.m_phi_max, args.n_m_phi,
        args.theta_min, args.theta_max, args.n_theta,
        qrng_bounds, ff_bounds, higgs_bounds,
        envelope_data,
        Theta_lab=args.Theta_lab,
        br_max=args.br_max,
        use_normalized_slack=True,
        variation=args.variation
    )
    
    # Print summary
    print_robustness_summary(results)
    
    # Save results
    output_path = Path(args.out_json)
    output_path.write_text(json.dumps(results, indent=2))
    print(f"\n✓ Saved results: {output_path}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

