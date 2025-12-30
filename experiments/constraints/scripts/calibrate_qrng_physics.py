#!/usr/bin/env python3
"""
Calibrate QRNG_tilt constraint physics.

Reviews the mapping from (α, λ, η, ...) → predicted bias ε,
and verifies epsilon_max from experimental data.
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import numpy as np


def load_qrng_data(qrng_json_path: Path) -> Optional[Dict]:
    """Load QRNG experimental data."""
    if not qrng_json_path.exists():
        return None
    
    data = json.loads(qrng_json_path.read_text())
    return data


def compute_epsilon_max_from_data(qrng_data: Dict) -> float:
    """
    Compute epsilon_max from experimental data.
    
    epsilon_max = max(|epsilon_lower_95|, |epsilon_upper_95|)
    """
    eps_lower = qrng_data.get('epsilon_lower_95', 0.0)
    eps_upper = qrng_data.get('epsilon_upper_95', 0.0)
    
    epsilon_max = max(abs(eps_lower), abs(eps_upper))
    return epsilon_max


def review_qrng_physics_mapping():
    """
    Review the physics mapping: (α, λ, η, ...) → ε
    
    Current implementation:
    - epsilon = alpha * 1e3 (simplified)
    
    Physical relationship (from MQGT-SCF):
    - ε ∝ η(ΔE - ⟨ΔE⟩) where η is ethical bias parameter
    - For small mixing: η ∝ α
    - So: ε ∝ α * (energy scale factor)
    
    The 1e3 scaling factor is a placeholder that needs physical justification.
    """
    print("=" * 80)
    print("QRNG TILT PHYSICS MAPPING REVIEW")
    print("=" * 80)
    print()
    
    print("Current Implementation:")
    print("  epsilon = alpha * 1e3")
    print()
    
    print("Physical Relationship (MQGT-SCF):")
    print("  ε = η * (ΔE - ⟨ΔE⟩)")
    print("  where:")
    print("    ε = QRNG tilt/bias (dimensionless)")
    print("    η = ethical bias parameter (dimensionless)")
    print("    ΔE = energy difference between outcomes")
    print("    ⟨ΔE⟩ = average energy difference")
    print()
    
    print("For small mixing (Higgs portal):")
    print("  η ∝ α (Yukawa strength)")
    print("  So: ε ∝ α * (energy scale factor)")
    print()
    
    print("Current Scaling Factor (1e3):")
    print("  - This is a PLACEHOLDER")
    print("  - Needs physical justification")
    print("  - Should relate to:")
    print("    * Energy scale of QRNG process")
    print("    * Coupling strength to quantum system")
    print("    * Experimental conditions (temperature, etc.)")
    print()
    
    print("Recommendations:")
    print("  1. Derive proper scaling from MQGT-SCF Lagrangian")
    print("  2. Calibrate against experimental data if available")
    print("  3. Document assumptions and uncertainties")
    print()


def calibrate_epsilon_max(qrng_json_path: Path, current_default: float = 0.0008):
    """
    Calibrate epsilon_max from experimental data.
    """
    print("=" * 80)
    print("EPSILON_MAX CALIBRATION")
    print("=" * 80)
    print()
    
    qrng_data = load_qrng_data(qrng_json_path)
    
    if qrng_data is None:
        print(f"❌ QRNG data not found: {qrng_json_path}")
        print(f"   Using default: epsilon_max = {current_default}")
        return current_default
    
    # Extract data
    n = qrng_data.get('n', 0)
    k = qrng_data.get('k', 0)
    p_hat = qrng_data.get('p_hat', 0.5)
    epsilon_hat = qrng_data.get('epsilon_hat', 0.0)
    eps_lower = qrng_data.get('epsilon_lower_95', 0.0)
    eps_upper = qrng_data.get('epsilon_upper_95', 0.0)
    
    print(f"Experimental Data:")
    print(f"  n (trials): {n:,}")
    print(f"  k (successes): {k:,}")
    print(f"  p_hat: {p_hat:.6f}")
    print(f"  epsilon_hat: {epsilon_hat:.6f}")
    print(f"  epsilon_lower_95: {eps_lower:.6f}")
    print(f"  epsilon_upper_95: {eps_upper:.6f}")
    print()
    
    # Compute epsilon_max
    epsilon_max = compute_epsilon_max_from_data(qrng_data)
    
    print(f"Computed epsilon_max:")
    print(f"  epsilon_max = max(|{eps_lower:.6f}|, |{eps_upper:.6f}|)")
    print(f"  epsilon_max = {epsilon_max:.6f}")
    print()
    
    print(f"Comparison with current default:")
    print(f"  Current default: {current_default:.6f}")
    print(f"  Data-derived:    {epsilon_max:.6f}")
    delta = abs(epsilon_max - current_default)
    ratio = epsilon_max / current_default if current_default > 0 else float('inf')
    print(f"  Difference:       {delta:.6f}")
    print(f"  Ratio:           {ratio:.2f}x")
    print()
    
    if abs(epsilon_max - current_default) > 0.0001:
        print("⚠️  WARNING: Current default differs from experimental data!")
        print(f"   Recommend updating default to: {epsilon_max:.6f}")
    else:
        print("✓ Current default matches experimental data")
    
    return epsilon_max


def document_experimental_conditions(qrng_data: Optional[Dict]):
    """Document experimental conditions for QRNG constraint."""
    print("=" * 80)
    print("EXPERIMENTAL CONDITIONS")
    print("=" * 80)
    print()
    
    if qrng_data is None:
        print("No experimental data available.")
        return
    
    n = qrng_data.get('n', 0)
    
    print("QRNG Experimental Setup:")
    print(f"  Sample size: {n:,} trials")
    print("  Type: Quantum Random Number Generator (QRNG)")
    print("  Measurement: Binary outcomes (0/1)")
    print()
    
    print("Physical Conditions:")
    print("  - Room temperature (assumed)")
    print("  - Quantum coherence required")
    print("  - Ethical bias parameter η couples to energy differences")
    print()
    
    print("Constraint Interpretation:")
    print("  |ε| < epsilon_max means:")
    print("  - QRNG outcomes are unbiased within experimental uncertainty")
    print("  - No detectable ethical bias in quantum measurement")
    print("  - Scalar field effects (if present) are below detection threshold")
    print()


def main():
    ap = argparse.ArgumentParser(description='Calibrate QRNG_tilt physics constraint')
    ap.add_argument('--qrng-json', type=str,
                   default='experiments/grok_qrng/results/lfdr_withinrun/global_summary.json',
                   help='QRNG bounds JSON')
    ap.add_argument('--current-default', type=float, default=0.0008,
                   help='Current default epsilon_max value')
    args = ap.parse_args()
    
    qrng_path = Path(args.qrng_json)
    qrng_data = load_qrng_data(qrng_path)
    
    # Review physics mapping
    review_qrng_physics_mapping()
    
    # Calibrate epsilon_max
    epsilon_max = calibrate_epsilon_max(qrng_path, args.current_default)
    
    # Document experimental conditions
    document_experimental_conditions(qrng_data)
    
    # Summary
    print("=" * 80)
    print("CALIBRATION SUMMARY")
    print("=" * 80)
    print()
    print(f"Recommended epsilon_max: {epsilon_max:.6f}")
    print()
    print("Next Steps:")
    print("  1. Update default epsilon_max in active_constraint_labeling.py")
    print("  2. Document physical justification for scaling factor (1e3)")
    print("  3. Consider making epsilon_max data-driven (load from JSON)")
    print()
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

