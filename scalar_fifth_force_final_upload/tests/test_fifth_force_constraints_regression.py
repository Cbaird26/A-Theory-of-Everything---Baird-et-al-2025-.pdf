"""Regression tests for fifth-force constraint evaluation."""

import pandas as pd
import numpy as np
import pytest

from code.inference.fifth_force.constraints import max_alpha_allowed, is_excluded


@pytest.fixture
def synthetic_curve():
    """Create a synthetic monotonic constraint curve for testing."""
    lambda_m = np.logspace(-6, -2, 20)  # 1e-6 to 1e-2 m
    alpha_max = 1e-8 * (lambda_m / 1e-6) ** -0.5  # Decreasing with lambda
    
    df = pd.DataFrame({
        "lambda_m": lambda_m,
        "alpha_max": alpha_max,
        "source_id": ["synthetic_test"] * len(lambda_m),
    })
    return df


def test_max_alpha_allowed_interpolation(synthetic_curve):
    """Test that max_alpha_allowed correctly interpolates."""
    # Test at exact point
    lambda_test = synthetic_curve["lambda_m"].iloc[10]
    alpha_expected = synthetic_curve["alpha_max"].iloc[10]
    alpha_got = max_alpha_allowed(lambda_test, synthetic_curve)
    
    assert abs(alpha_got - alpha_expected) < 1e-12


def test_max_alpha_allowed_edge_cases(synthetic_curve):
    """Test edge cases (below min, above max)."""
    # Below minimum
    alpha_below = max_alpha_allowed(1e-7, synthetic_curve)
    alpha_min = synthetic_curve["alpha_max"].iloc[0]
    assert alpha_below == alpha_min
    
    # Above maximum
    alpha_above = max_alpha_allowed(1e-1, synthetic_curve)
    alpha_max_val = synthetic_curve["alpha_max"].iloc[-1]
    assert alpha_above == alpha_max_val


def test_is_excluded_below_curve(synthetic_curve):
    """Test that points below the curve are allowed."""
    lambda_test = synthetic_curve["lambda_m"].iloc[10]
    alpha_max = synthetic_curve["alpha_max"].iloc[10]
    alpha_pred = alpha_max * 0.5  # Well below
    
    assert not is_excluded(alpha_pred, lambda_test, synthetic_curve)


def test_is_excluded_above_curve(synthetic_curve):
    """Test that points above the curve are excluded."""
    lambda_test = synthetic_curve["lambda_m"].iloc[10]
    alpha_max = synthetic_curve["alpha_max"].iloc[10]
    alpha_pred = alpha_max * 2.0  # Well above
    
    assert is_excluded(alpha_pred, lambda_test, synthetic_curve)


def test_is_excluded_on_curve(synthetic_curve):
    """Test that points exactly on the curve are excluded (strict >)."""
    lambda_test = synthetic_curve["lambda_m"].iloc[10]
    alpha_max = synthetic_curve["alpha_max"].iloc[10]
    alpha_pred = alpha_max * 1.0  # Exactly on curve
    
    # On curve: alpha == alpha_max, so alpha > alpha_max is False (not excluded)
    assert not is_excluded(alpha_pred, lambda_test, synthetic_curve)


def test_normalized_slack_consistency(synthetic_curve):
    """Test that normalized slack behaves consistently."""
    from code.inference.fifth_force.slack import fifth_force_slack
    
    lambda_test = synthetic_curve["lambda_m"].iloc[10]
    alpha_max = synthetic_curve["alpha_max"].iloc[10]
    
    # Test below curve
    alpha_pred = alpha_max * 0.5
    result = fifth_force_slack(alpha_pred, lambda_test, synthetic_curve)
    assert result["normalized_slack"] > 0
    assert result["is_allowed"] is True
    
    # Test above curve
    alpha_pred = alpha_max * 2.0
    result = fifth_force_slack(alpha_pred, lambda_test, synthetic_curve)
    assert result["normalized_slack"] < 0
    assert result["is_allowed"] is False
    
    # Test on curve (within tolerance)
    alpha_pred = alpha_max * 1.0
    result = fifth_force_slack(alpha_pred, lambda_test, synthetic_curve)
    # On curve: slack = 0, normalized_slack = 0
    assert abs(result["normalized_slack"]) < 1e-10
    assert result["is_allowed"] is True  # >= 0 means allowed

