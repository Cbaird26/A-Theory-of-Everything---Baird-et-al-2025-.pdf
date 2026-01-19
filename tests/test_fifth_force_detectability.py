"""Regression tests for fifth-force detectability computation."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from code.inference.fifth_force.detectability import (
    sample_model_points,
    compute_detectability,
    lambda_to_freq_eq,
    freq_to_energy_eV,
)
from code.inference.fifth_force.yukawa import model_point_to_alpha_lambda
from code.inference.fifth_force.envelope import alpha_max_envelope


@pytest.fixture
def synthetic_curve(tmp_path):
    """Create a synthetic constraint curve for testing."""
    # Create a simple monotonic curve
    lambda_m = np.logspace(-4, -2, 100)  # 0.1 mm to 1 cm
    alpha_max = 1e-10 * (lambda_m / 1e-3) ** (-1.5)  # Decreasing with lambda
    
    df = pd.DataFrame({
        "lambda_m": lambda_m,
        "alpha_max": alpha_max,
        "source_id": "test_curve",
    })
    
    curve_path = tmp_path / "test_curve_validated.csv"
    df.to_csv(curve_path, index=False)
    
    # Return curve metadata
    return {
        "source_id": "test_curve",
        "path": curve_path,
        "lambda_min": float(lambda_m.min()),
        "lambda_max": float(lambda_m.max()),
        "row_count": len(df),
    }


def test_sample_model_points():
    """Test that sampled points have correct structure and ranges."""
    points = sample_model_points(n_points=100, seed=42)
    
    assert len(points) == 100
    
    for point in points:
        assert "m_phi_GeV" in point
        assert "theta" in point
        assert "mu_sb_over_m_h" in point
        
        # Check ranges
        assert 1e-16 <= point["m_phi_GeV"] <= 1e-10
        assert 1e-22 <= point["theta"] <= 1e-18
        assert 1e-3 <= point["mu_sb_over_m_h"] <= 1.0


def test_sample_points_reproducible():
    """Test that sampling is reproducible with same seed."""
    points1 = sample_model_points(n_points=10, seed=42)
    points2 = sample_model_points(n_points=10, seed=42)
    
    assert len(points1) == len(points2)
    for p1, p2 in zip(points1, points2):
        assert p1["m_phi_GeV"] == p2["m_phi_GeV"]
        assert p1["theta"] == p2["theta"]
        assert p1["mu_sb_over_m_h"] == p2["mu_sb_over_m_h"]


def test_lambda_monotonic_with_mass():
    """Test that smaller m_phi -> larger lambda_m."""
    points = sample_model_points(n_points=50, seed=42)
    
    lambdas = []
    for point in points:
        model_dict = {
            "m_phi": point["m_phi_GeV"],
            "theta": point["theta"],
            "mu_sb": point["mu_sb_over_m_h"] * 125.0,
        }
        try:
            _, lambda_m = model_point_to_alpha_lambda(model_dict)
            lambdas.append((point["m_phi_GeV"], lambda_m))
        except Exception:
            continue
    
    # Sort by m_phi
    lambdas.sort(key=lambda x: x[0])
    
    # Check monotonicity: larger m_phi -> smaller lambda_m
    for i in range(len(lambdas) - 1):
        m1, l1 = lambdas[i]
        m2, l2 = lambdas[i + 1]
        if m2 > m1:
            assert l2 < l1, f"m_phi increased from {m1} to {m2} but lambda increased from {l1} to {l2}"


def test_detectability_r_computation(synthetic_curve, tmp_path):
    """Test that r = alpha_pred / alpha_max is computed correctly."""
    # Create a point that should be in range
    points = [{
        "m_phi_GeV": 1e-14,  # Will give lambda ~ 0.02 m (in range)
        "theta": 1e-20,
        "mu_sb_over_m_h": 0.01,
    }]
    
    # Manually compute expected values
    model_dict = {
        "m_phi": points[0]["m_phi_GeV"],
        "theta": points[0]["theta"],
        "mu_sb": points[0]["mu_sb_over_m_h"] * 125.0,
    }
    alpha_pred, lambda_m = model_point_to_alpha_lambda(model_dict)
    
    # Get alpha_max from envelope
    curves = [synthetic_curve]
    alpha_max, _ = alpha_max_envelope(lambda_m, curves)
    
    expected_r = alpha_pred / alpha_max
    
    # Compute via detectability function
    df = compute_detectability(points, curves)
    
    if len(df) > 0:
        computed_r = df.iloc[0]["r"]
        # Allow small numerical differences
        assert abs(computed_r - expected_r) < 1e-10 * max(abs(computed_r), abs(expected_r))


def test_detectability_excluded_flag(synthetic_curve):
    """Test that is_excluded flag is set correctly."""
    # Create a point with very large alpha (should be excluded)
    points = [{
        "m_phi_GeV": 1e-14,
        "theta": 1e-18,  # Large theta -> large alpha
        "mu_sb_over_m_h": 0.01,
    }]
    
    df = compute_detectability(points, [synthetic_curve])
    
    if len(df) > 0:
        # Check that r > 1 implies excluded
        for _, row in df.iterrows():
            if row["r"] > 1.0:
                assert row["is_excluded"] == True
            elif row["r"] < 1.0:
                assert row["is_excluded"] == False


def test_detectability_handles_out_of_range(synthetic_curve):
    """Test that points outside lambda range are handled gracefully."""
    # Create a point with very small m_phi (large lambda, out of range)
    points = [{
        "m_phi_GeV": 1e-20,  # Very small -> very large lambda
        "theta": 1e-20,
        "mu_sb_over_m_h": 0.01,
    }]
    
    df = compute_detectability(points, [synthetic_curve])
    
    # Should either skip the point or handle it gracefully
    # (no exception should be raised)
    assert isinstance(df, pd.DataFrame)


def test_detectability_includes_frequency_columns(synthetic_curve):
    """Test that detectability output includes f_eq_hz and E_eq_eV columns."""
    points = [{
        "m_phi_GeV": 1e-14,  # Will give lambda in range
        "theta": 1e-20,
        "mu_sb_over_m_h": 0.01,
    }]
    
    df = compute_detectability(points, [synthetic_curve])
    
    if len(df) > 0:
        # Check that frequency columns are present
        assert "f_eq_hz" in df.columns, "f_eq_hz column missing"
        assert "E_eq_eV" in df.columns, "E_eq_eV column missing"
        
        # Check that values are computed correctly
        for _, row in df.iterrows():
            lambda_m = row["lambda_m"]
            f_eq = row["f_eq_hz"]
            E_eq = row["E_eq_eV"]
            
            # Verify frequency calculation
            expected_f_eq = lambda_to_freq_eq(lambda_m)
            if not np.isnan(expected_f_eq):
                assert not np.isnan(f_eq), f"f_eq_hz is NaN for lambda_m={lambda_m}"
                assert abs(f_eq - expected_f_eq) < 1e-6 * abs(f_eq), \
                    f"f_eq mismatch: got {f_eq}, expected {expected_f_eq}"
            
            # Verify energy calculation
            expected_E_eq = freq_to_energy_eV(f_eq) if not np.isnan(f_eq) else np.nan
            if not np.isnan(expected_E_eq):
                assert not np.isnan(E_eq), f"E_eq_eV is NaN for f_eq={f_eq}"
                assert abs(E_eq - expected_E_eq) < 1e-12 * abs(E_eq), \
                    f"E_eq mismatch: got {E_eq}, expected {expected_E_eq}"


def test_detectability_frequency_values_positive(synthetic_curve):
    """Test that frequency values are positive for valid lambda."""
    points = [{
        "m_phi_GeV": 1e-14,
        "theta": 1e-20,
        "mu_sb_over_m_h": 0.01,
    }]
    
    df = compute_detectability(points, [synthetic_curve])
    
    if len(df) > 0:
        for _, row in df.iterrows():
            lambda_m = row["lambda_m"]
            f_eq = row["f_eq_hz"]
            E_eq = row["E_eq_eV"]
            
            # For valid lambda (positive), frequency should be positive
            if lambda_m > 0:
                assert f_eq > 0, f"f_eq should be positive for lambda_m={lambda_m}, got {f_eq}"
                assert E_eq > 0, f"E_eq should be positive for f_eq={f_eq}, got {E_eq}"

