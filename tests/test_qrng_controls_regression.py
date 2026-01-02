"""
Regression test for QRNG control calibration.

Locks the calibration behavior:
- Fair control (k=n/2): BF10 < 1/3, CI includes 0
- Biased control (k=101000, n=200000, p=0.505): BF10 > 10, CI_low > 0

Tests across prior scales 0.5, 1.0, 2.0 to ensure robustness.
"""
import pytest
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "experiments" / "constraints" / "scripts"
sys.path.insert(0, str(scripts_dir))

from calibrate_qrng_physics import analyze_binomial


@pytest.mark.parametrize("prior_scale", [0.5, 1.0, 2.0])
def test_fair_control(prior_scale):
    """Test that fair control (k=n/2) correctly rejects bias."""
    n = 200_000
    k = n // 2  # Exactly fair: p = 0.5
    r = analyze_binomial(k, n, prior_scale)
    
    # BF10 should strongly favor null (no bias)
    assert r["bf10"] < (1.0 / 3.0), \
        f"Fair control BF10 ({r['bf10']:.6f}) should be < 1/3 for prior_scale={prior_scale}"
    
    # CI should include 0 (epsilon can be zero)
    assert r["ci_low"] <= 0.0 <= r["ci_high"], \
        f"Fair control CI [{r['ci_low']:.6f}, {r['ci_high']:.6f}] should include 0 for prior_scale={prior_scale}"


@pytest.mark.parametrize("prior_scale", [0.5, 1.0, 2.0])
def test_biased_control(prior_scale):
    """Test that biased control (p=0.505) correctly detects bias."""
    n = 200_000
    k = 101_000  # p = 0.505, epsilon = +0.005
    r = analyze_binomial(k, n, prior_scale)
    
    # BF10 should strongly favor bias
    assert r["bf10"] > 10.0, \
        f"Biased control BF10 ({r['bf10']:.6f}) should be > 10 for prior_scale={prior_scale}"
    
    # CI lower bound should be > 0 (epsilon is positive)
    assert r["ci_low"] > 0.0, \
        f"Biased control CI lower bound ({r['ci_low']:.6f}) should be > 0 for prior_scale={prior_scale}"

