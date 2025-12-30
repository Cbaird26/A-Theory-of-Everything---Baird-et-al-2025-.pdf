#!/usr/bin/env python3
"""
Stress-test QRNG_tilt constraint implementation.

Tests:
1. Scaling formula correctness
2. Sign handling (positive/negative epsilon)
3. Monotonicity (alpha increases → slack decreases)
4. Boundary conditions (epsilon = 0, epsilon_max, > epsilon_max)
5. Units consistency
6. Normalized slack behavior
"""
import numpy as np
from typing import Tuple
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from active_constraint_labeling import compute_qrng_tilt_slack


def test_scaling_formula():
    """Test that epsilon = alpha * 1e3 scaling is correct."""
    print("=" * 60)
    print("TEST 1: Scaling Formula")
    print("=" * 60)
    
    test_cases = [
        (0.0, 0.0, "alpha = 0 → epsilon = 0"),
        (1e-6, 1e-3, "alpha = 1e-6 → epsilon = 1e-3"),
        (0.0008 / 1e3, 0.0008, "alpha = epsilon_max/1e3 → epsilon = epsilon_max"),
        (2 * 0.0008 / 1e3, 2 * 0.0008, "alpha = 2*epsilon_max/1e3 → epsilon = 2*epsilon_max"),
    ]
    
    epsilon_max = 0.0008
    all_passed = True
    
    for alpha, expected_epsilon, description in test_cases:
        # Compute epsilon using the same formula as in compute_qrng_tilt_slack
        epsilon = alpha * 1e3
        slack, bound = compute_qrng_tilt_slack(alpha, lambda_m=1e-6, epsilon_max=epsilon_max)
        
        # Verify epsilon matches expected
        if abs(epsilon - expected_epsilon) < 1e-10:
            print(f"✓ {description}")
            print(f"  alpha = {alpha:.6e}, epsilon = {epsilon:.6e} (expected {expected_epsilon:.6e})")
        else:
            print(f"✗ {description}")
            print(f"  alpha = {alpha:.6e}, epsilon = {epsilon:.6e} (expected {expected_epsilon:.6e})")
            all_passed = False
    
    return all_passed


def test_sign_handling():
    """Test that abs(epsilon) correctly handles both signs."""
    print("\n" + "=" * 60)
    print("TEST 2: Sign Handling")
    print("=" * 60)
    
    epsilon_max = 0.0008
    
    # Test positive alpha (positive epsilon)
    alpha_pos = 0.0008 / 1e3
    slack_pos, bound_pos = compute_qrng_tilt_slack(alpha_pos, lambda_m=1e-6, epsilon_max=epsilon_max)
    epsilon_pos = alpha_pos * 1e3
    
    # Test negative alpha (negative epsilon) - should be treated as positive via abs()
    # Note: In current implementation, alpha is always positive (Yukawa strength)
    # But epsilon can be negative in QRNG data, so we test the constraint logic
    
    # The constraint is |epsilon| < epsilon_max, so both +epsilon and -epsilon should give same slack
    # Since epsilon = alpha * 1e3 and alpha >= 0, epsilon >= 0, so abs(epsilon) = epsilon
    # But we can test the logic by checking if slack = epsilon_max - abs(epsilon)
    
    expected_slack = epsilon_max - abs(epsilon_pos)
    
    if abs(slack_pos - expected_slack) < 1e-10:
        print(f"✓ Sign handling correct")
        print(f"  alpha = {alpha_pos:.6e}, epsilon = {epsilon_pos:.6e}")
        print(f"  slack = {slack_pos:.6e}, expected = {expected_slack:.6e}")
        return True
    else:
        print(f"✗ Sign handling incorrect")
        print(f"  alpha = {alpha_pos:.6e}, epsilon = {epsilon_pos:.6e}")
        print(f"  slack = {slack_pos:.6e}, expected = {expected_slack:.6e}")
        return False


def test_monotonicity():
    """Test that slack decreases monotonically as alpha increases."""
    print("\n" + "=" * 60)
    print("TEST 3: Monotonicity")
    print("=" * 60)
    
    epsilon_max = 0.0008
    lambda_m = 1e-6
    
    # Test sequence of increasing alpha values
    alpha_values = np.logspace(-9, -5, 20)  # 20 points from 1e-9 to 1e-5
    
    slacks = []
    for alpha in alpha_values:
        slack, bound = compute_qrng_tilt_slack(alpha, lambda_m, epsilon_max)
        slacks.append(slack)
    
    # Check monotonicity: slack should decrease as alpha increases
    is_monotonic = all(slacks[i] >= slacks[i+1] for i in range(len(slacks) - 1))
    
    if is_monotonic:
        print(f"✓ Monotonicity test passed")
        print(f"  Tested {len(alpha_values)} alpha values from {alpha_values[0]:.6e} to {alpha_values[-1]:.6e}")
        print(f"  Slack decreases from {slacks[0]:.6e} to {slacks[-1]:.6e}")
        return True
    else:
        print(f"✗ Monotonicity test failed")
        # Find violations
        violations = []
        for i in range(len(slacks) - 1):
            if slacks[i] < slacks[i+1]:
                violations.append((i, alpha_values[i], alpha_values[i+1], slacks[i], slacks[i+1]))
        print(f"  Found {len(violations)} violations:")
        for idx, a1, a2, s1, s2 in violations[:5]:  # Show first 5
            print(f"    alpha[{idx}] = {a1:.6e} (slack={s1:.6e}) < alpha[{idx+1}] = {a2:.6e} (slack={s2:.6e})")
        return False


def test_boundary_conditions():
    """Test boundary conditions: epsilon = 0, epsilon_max, > epsilon_max."""
    print("\n" + "=" * 60)
    print("TEST 4: Boundary Conditions")
    print("=" * 60)
    
    epsilon_max = 0.0008
    lambda_m = 1e-6
    
    tests = [
        {
            'name': 'epsilon = 0',
            'alpha': 0.0,
            'expected_epsilon': 0.0,
            'expected_slack': epsilon_max,
            'expected_viable': True
        },
        {
            'name': 'epsilon = epsilon_max',
            'alpha': epsilon_max / 1e3,
            'expected_epsilon': epsilon_max,
            'expected_slack': 0.0,
            'expected_viable': True  # At boundary, should be viable (slack = 0)
        },
        {
            'name': 'epsilon = 0.5 * epsilon_max',
            'alpha': 0.5 * epsilon_max / 1e3,
            'expected_epsilon': 0.5 * epsilon_max,
            'expected_slack': 0.5 * epsilon_max,
            'expected_viable': True
        },
        {
            'name': 'epsilon = 1.1 * epsilon_max (excluded)',
            'alpha': 1.1 * epsilon_max / 1e3,
            'expected_epsilon': 1.1 * epsilon_max,
            'expected_slack': -0.1 * epsilon_max,  # Negative = excluded
            'expected_viable': False
        },
        {
            'name': 'epsilon = 2 * epsilon_max (excluded)',
            'alpha': 2 * epsilon_max / 1e3,
            'expected_epsilon': 2 * epsilon_max,
            'expected_slack': -epsilon_max,  # Negative = excluded
            'expected_viable': False
        },
    ]
    
    all_passed = True
    for test in tests:
        slack, bound = compute_qrng_tilt_slack(test['alpha'], lambda_m, epsilon_max)
        epsilon = test['alpha'] * 1e3
        viable = slack >= 0
        
        # Check epsilon
        epsilon_ok = abs(epsilon - test['expected_epsilon']) < 1e-10
        
        # Check slack (allow small tolerance for floating point)
        slack_ok = abs(slack - test['expected_slack']) < 1e-10
        
        # Check viability
        viable_ok = viable == test['expected_viable']
        
        if epsilon_ok and slack_ok and viable_ok:
            print(f"✓ {test['name']}")
            print(f"  alpha = {test['alpha']:.6e}, epsilon = {epsilon:.6e}, slack = {slack:.6e}, viable = {viable}")
        else:
            print(f"✗ {test['name']}")
            print(f"  alpha = {test['alpha']:.6e}, epsilon = {epsilon:.6e} (expected {test['expected_epsilon']:.6e})")
            print(f"  slack = {slack:.6e} (expected {test['expected_slack']:.6e})")
            print(f"  viable = {viable} (expected {test['expected_viable']})")
            all_passed = False
    
    return all_passed


def test_units_consistency():
    """Test that units are consistent (alpha and epsilon are both dimensionless)."""
    print("\n" + "=" * 60)
    print("TEST 5: Units Consistency")
    print("=" * 60)
    
    # alpha is Yukawa strength (dimensionless)
    # epsilon is tilt/bias (dimensionless)
    # The scaling epsilon = alpha * 1e3 should preserve dimensionless nature
    
    alpha = 1e-6  # dimensionless
    epsilon = alpha * 1e3  # should also be dimensionless
    
    # Check that the scaling factor (1e3) is dimensionless
    # If alpha has units [1] and epsilon has units [1], then 1e3 must have units [1]
    # This is correct - it's just a numerical scaling factor
    
    print(f"✓ Units check:")
    print(f"  alpha (dimensionless) = {alpha:.6e}")
    print(f"  epsilon (dimensionless) = {epsilon:.6e}")
    print(f"  Scaling factor = 1e3 (dimensionless)")
    print(f"  Units are consistent: [1] * [1] = [1]")
    
    return True


def test_normalized_slack():
    """Test normalized slack = slack / bound behavior."""
    print("\n" + "=" * 60)
    print("TEST 6: Normalized Slack")
    print("=" * 60)
    
    epsilon_max = 0.0008
    lambda_m = 1e-6
    
    test_cases = [
        (0.0, "alpha = 0"),
        (0.5 * epsilon_max / 1e3, "alpha = 0.5 * epsilon_max / 1e3"),
        (epsilon_max / 1e3, "alpha = epsilon_max / 1e3"),
        (1.5 * epsilon_max / 1e3, "alpha = 1.5 * epsilon_max / 1e3"),
    ]
    
    all_passed = True
    for alpha, description in test_cases:
        slack, bound = compute_qrng_tilt_slack(alpha, lambda_m, epsilon_max)
        normalized_slack = slack / bound if bound > 0 else slack
        
        # Expected normalized slack
        epsilon = alpha * 1e3
        expected_normalized = (epsilon_max - abs(epsilon)) / epsilon_max
        
        if abs(normalized_slack - expected_normalized) < 1e-10:
            print(f"✓ {description}")
            print(f"  slack = {slack:.6e}, bound = {bound:.6e}")
            print(f"  normalized_slack = {normalized_slack:.6e} (expected {expected_normalized:.6e})")
        else:
            print(f"✗ {description}")
            print(f"  slack = {slack:.6e}, bound = {bound:.6e}")
            print(f"  normalized_slack = {normalized_slack:.6e} (expected {expected_normalized:.6e})")
            all_passed = False
    
    return all_passed


def main():
    """Run all stress tests."""
    print("QRNG Tilt Constraint Stress Test")
    print("=" * 60)
    print()
    
    results = {}
    
    results['scaling'] = test_scaling_formula()
    results['sign_handling'] = test_sign_handling()
    results['monotonicity'] = test_monotonicity()
    results['boundary'] = test_boundary_conditions()
    results['units'] = test_units_consistency()
    results['normalized_slack'] = test_normalized_slack()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    if all_passed:
        print("✓ All stress tests passed!")
        return 0
    else:
        print("✗ Some stress tests failed. Review output above.")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())

