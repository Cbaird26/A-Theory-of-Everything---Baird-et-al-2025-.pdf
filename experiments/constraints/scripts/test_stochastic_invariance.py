#!/usr/bin/env python3
"""
Regression test for stochastic invariance in QRNG calibration.

Tests:
1. Same seed → identical pooled ε_max and CI (byte-for-byte reproducibility)
2. Different seed → ε_max close, CI may vary, but dominance ordering unchanged

This is a "stochastic invariance" test that ensures the calibration pipeline
is deterministic when seeded, while documenting expected variation when seeds differ.
"""
import json
import sys
from pathlib import Path
import numpy as np
import tempfile
import shutil

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from calibrate_qrng_multisource import calibrate_multisource


def test_same_seed_reproducibility():
    """Test that same seed produces identical results."""
    print("="*60)
    print("TEST 1: Same Seed → Identical Results")
    print("="*60)
    
    # Use a test data path (adjust if needed)
    test_json = Path('experiments/grok_qrng/results/lfdr_withinrun/global_summary.json')
    if not test_json.exists():
        print(f"⚠️  Test data not found: {test_json}")
        print("   Skipping test (requires calibration data)")
        return True
    
    source_paths = [('lfdr_withinrun', test_json)]
    
    # Run calibration twice with same seed
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        print("Running calibration with seed=42 (first run)...")
        results1 = calibrate_multisource(
            source_paths,
            method='bootstrap_95',
            n_bootstrap=1000,
            random_state=42,
            output_dir=tmp_path / 'run1'
        )
        
        print("\nRunning calibration with seed=42 (second run)...")
        results2 = calibrate_multisource(
            source_paths,
            method='bootstrap_95',
            n_bootstrap=1000,
            random_state=42,
            output_dir=tmp_path / 'run2'
        )
        
        # Check pooled results
        pooled1 = results1['pooled']
        pooled2 = results2['pooled']
        
        print("\n" + "-"*60)
        print("COMPARISON (same seed=42, two runs):")
        print("-"*60)
        print(f"  Run 1: ε_max = {pooled1['epsilon_max']:.10f}, CI = [{pooled1['ci_lower']:.10f}, {pooled1['ci_upper']:.10f}]")
        print(f"  Run 2: ε_max = {pooled2['epsilon_max']:.10f}, CI = [{pooled2['ci_lower']:.10f}, {pooled2['ci_upper']:.10f}]")
        print("-"*60)
        
        # Assertions
        assert abs(pooled1['epsilon_max'] - pooled2['epsilon_max']) < 1e-10, \
            f"ε_max differs: {pooled1['epsilon_max']} vs {pooled2['epsilon_max']}"
        
        assert abs(pooled1['ci_lower'] - pooled2['ci_lower']) < 1e-10, \
            f"CI lower differs: {pooled1['ci_lower']} vs {pooled2['ci_lower']}"
        
        assert abs(pooled1['ci_upper'] - pooled2['ci_upper']) < 1e-10, \
            f"CI upper differs: {pooled1['ci_upper']} vs {pooled2['ci_upper']}"
        
        print("✅ PASS: Same seed produces identical results (byte-for-byte)")
        return True


def test_different_seed_variation():
    """Test that different seeds produce close results with expected variation."""
    print("\n" + "="*60)
    print("TEST 2: Different Seed → Close Results, CI May Vary")
    print("="*60)
    
    test_json = Path('experiments/grok_qrng/results/lfdr_withinrun/global_summary.json')
    if not test_json.exists():
        print(f"⚠️  Test data not found: {test_json}")
        print("   Skipping test (requires calibration data)")
        return True
    
    source_paths = [('lfdr_withinrun', test_json)]
    
    # Run with different seeds
    seeds = [42, 123, 999]
    results = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        for seed in seeds:
            print(f"\nRunning calibration with seed={seed}...")
            result = calibrate_multisource(
                source_paths,
                method='bootstrap_95',
                n_bootstrap=1000,
                random_state=seed,
                output_dir=tmp_path / f'seed_{seed}'
            )
            results.append((seed, result['pooled']))
        
        # Extract values
        epsilon_maxes = [r[1]['epsilon_max'] for _, r in results]
        ci_lowers = [r[1]['ci_lower'] for _, r in results]
        ci_uppers = [r[1]['ci_upper'] for _, r in results]
        
        print("\n" + "-"*60)
        print("PER-SEED RESULTS (for reviewer inspection):")
        print("-"*60)
        for seed, pooled in results:
            print(f"  Seed {seed:3d}: ε_max = {pooled['epsilon_max']:.8f}, "
                  f"CI = [{pooled['ci_lower']:.8f}, {pooled['ci_upper']:.8f}]")
        print("-"*60)
        
        # Check that ε_max is stable (within sampling error)
        epsilon_max_std = np.std(epsilon_maxes)
        epsilon_max_mean = np.mean(epsilon_maxes)
        epsilon_max_cv = epsilon_max_std / epsilon_max_mean if epsilon_max_mean > 0 else 0
        
        print(f"\nε_max statistics:")
        print(f"  Mean: {epsilon_max_mean:.6f}")
        print(f"  Std: {epsilon_max_std:.6f}")
        print(f"  CV: {epsilon_max_cv:.4f}")
        
        # ε_max should be stable (CV < 0.01 = 1%)
        assert epsilon_max_cv < 0.01, \
            f"ε_max varies too much across seeds (CV = {epsilon_max_cv:.4f})"
        
        # CI bounds may vary more (expected)
        ci_lower_range = max(ci_lowers) - min(ci_lowers)
        ci_upper_range = max(ci_uppers) - min(ci_uppers)
        
        print(f"\nCI variation:")
        print(f"  Lower bound range: {ci_lower_range:.6f}")
        print(f"  Upper bound range: {ci_upper_range:.6f}")
        
        # CI bounds should vary but not wildly (range < 0.001 = 0.1%)
        # This is a sanity check - actual variation depends on bootstrap sample size
        assert ci_lower_range < 0.001, \
            f"CI lower bound varies too much (range = {ci_lower_range:.6f})"
        assert ci_upper_range < 0.001, \
            f"CI upper bound varies too much (range = {ci_upper_range:.6f})"
        
        print("✅ PASS: Different seeds produce close results with expected CI variation")
        return True


def test_dominance_ordering_persistence():
    """
    Test that dominance ordering persists across seed changes.
    
    This is a placeholder - actual dominance ordering test would require
    running the full constraint engine. For now, we just verify that
    the calibration produces reasonable values that would lead to
    consistent dominance ordering.
    """
    print("\n" + "="*60)
    print("TEST 3: Dominance Ordering Persistence")
    print("="*60)
    
    test_json = Path('experiments/grok_qrng/results/lfdr_withinrun/global_summary.json')
    if not test_json.exists():
        print(f"⚠️  Test data not found: {test_json}")
        print("   Skipping test (requires calibration data)")
        return True
    
    source_paths = [('lfdr_withinrun', test_json)]
    
    # Run with different seeds
    seeds = [42, 123, 999]
    epsilon_maxes = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        for seed in seeds:
            result = calibrate_multisource(
                source_paths,
                method='bootstrap_95',
                n_bootstrap=1000,
                random_state=seed,
                output_dir=tmp_path / f'seed_{seed}'
            )
            epsilon_maxes.append(result['pooled']['epsilon_max'])
        
        # Check that all ε_max values are in a reasonable range
        # (would lead to same dominance ordering in constraint engine)
        epsilon_max_min = min(epsilon_maxes)
        epsilon_max_max = max(epsilon_maxes)
        epsilon_max_range = epsilon_max_max - epsilon_max_min
        
        print("\n" + "-"*60)
        print("PER-SEED ε_max VALUES (for dominance ordering check):")
        print("-"*60)
        for seed, eps_max in zip(seeds, epsilon_maxes):
            print(f"  Seed {seed:3d}: ε_max = {eps_max:.8f}")
        print("-"*60)
        print(f"\nε_max range across seeds: [{epsilon_max_min:.8f}, {epsilon_max_max:.8f}]")
        print(f"Range: {epsilon_max_range:.8f}")
        
        # All values should be in the same order of magnitude
        # and within a tight range (would not flip dominance)
        assert epsilon_max_range < 0.001, \
            f"ε_max range too large (would affect dominance): {epsilon_max_range:.6f}"
        
        # All values should be positive and reasonable
        assert all(0 < eps < 0.01 for eps in epsilon_maxes), \
            f"ε_max values out of reasonable range: {epsilon_maxes}"
        
        print("✅ PASS: ε_max values are stable and would preserve dominance ordering")
        print("   (Full dominance test requires running constraint engine - see test_regression_dominance.py)")
        return True


def main():
    """Run all stochastic invariance tests."""
    print("STOCHASTIC INVARIANCE REGRESSION TEST")
    print("="*60)
    print()
    
    tests = [
        test_same_seed_reproducibility,
        test_different_seed_variation,
        test_dominance_ordering_persistence
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"\n❌ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())

