"""Test cases for ToE-native fifth-force mapping functions.

Verifies that ToE equations match expected values and Mode D produces reasonable results.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from code.inference.fifth_force.toe_mapping import (
    toe_theta_hc,
    toe_alpha_from_theta,
    toe_theta_max_from_alpha_max,
    toe_kappa_vc_max_from_theta_max,
    lambda_to_mphi_eV,
    compute_K_ToE,
    M_PL_REDUCED_GEV,
    V_HIGGS_GEV,
    M_HIGGS_GEV,
    F_N_DEFAULT,
)
from code.inference.fifth_force.yukawa import model_point_to_alpha_lambda


class TestToEThetaHC:
    """Test ToE Eq. (13) mixing angle calculation."""
    
    def test_theta_hc_basic(self):
        """Test basic θ_hc calculation with known values."""
        kappa_cH = 1e-2
        v_c_GeV = 1e-6
        m_c_GeV = 1e-3  # m_c << m_h
        
        theta = toe_theta_hc(kappa_cH, v_c_GeV, m_c_GeV)
        
        # For m_c << m_h: θ ≈ -κ_cH v v_c / m_h²
        expected = -(kappa_cH * V_HIGGS_GEV * v_c_GeV) / (M_HIGGS_GEV**2)
        
        assert abs(theta - expected) < 1e-15, f"θ_hc mismatch: {theta} vs {expected}"
    
    def test_theta_hc_small_mass_regime(self):
        """Test that m_c << m_h approximation works."""
        kappa_cH = 1e-3
        v_c_GeV = 1e-9
        m_c_GeV = 1e-4  # Very small compared to m_h
        
        theta = toe_theta_hc(kappa_cH, v_c_GeV, m_c_GeV)
        
        # Should be approximately -κ_cH v v_c / m_h²
        expected_approx = -(kappa_cH * V_HIGGS_GEV * v_c_GeV) / (M_HIGGS_GEV**2)
        
        # Should be very close (within 1% since m_c² << m_h²)
        assert abs(theta - expected_approx) / abs(expected_approx) < 0.01
    
    def test_theta_hc_vanishes_when_vc_zero(self):
        """Test that θ_hc = 0 when v_c = 0 (symmetric vacuum)."""
        kappa_cH = 1.0
        v_c_GeV = 0.0
        m_c_GeV = 1e-3
        
        theta = toe_theta_hc(kappa_cH, v_c_GeV, m_c_GeV)
        
        assert abs(theta) < 1e-15, "θ_hc should vanish when v_c = 0"
    
    def test_theta_hc_vanishes_when_kappa_zero(self):
        """Test that θ_hc = 0 when κ_cH = 0."""
        kappa_cH = 0.0
        v_c_GeV = 1e-6
        m_c_GeV = 1e-3
        
        theta = toe_theta_hc(kappa_cH, v_c_GeV, m_c_GeV)
        
        assert abs(theta) < 1e-15, "θ_hc should vanish when κ_cH = 0"


class TestToEAlphaFromTheta:
    """Test α(θ) conversion using ToE normalization."""
    
    def test_alpha_prefactor_matches_K_ToE(self):
        """Verify that K_ToE ≈ 1.76×10³¹ for f_N=0.30."""
        K_ToE = compute_K_ToE(f_n=0.30)
        expected = 1.76e31
        
        # Should match to within 5% (allows for rounding)
        assert abs(K_ToE - expected) / expected < 0.05, \
            f"K_ToE mismatch: {K_ToE:.3e} vs {expected:.3e}"
    
    def test_alpha_from_theta_small_angle(self):
        """Test α(θ) for small angles (sin θ ≈ θ)."""
        theta = 1e-10  # Very small angle
        
        alpha = toe_alpha_from_theta(theta, f_n=0.30)
        
        # For small θ: α ≈ K_ToE θ²
        K_ToE = compute_K_ToE(f_n=0.30)
        expected = K_ToE * (theta**2)
        
        assert abs(alpha - expected) / expected < 0.01, \
            f"α(θ) mismatch for small angle: {alpha:.3e} vs {expected:.3e}"
    
    def test_alpha_vanishes_when_theta_zero(self):
        """Test that α = 0 when θ = 0."""
        alpha = toe_alpha_from_theta(0.0, f_n=0.30)
        assert abs(alpha) < 1e-20, "α should vanish when θ = 0"
    
    def test_alpha_scales_with_f_n_squared(self):
        """Test that α scales as f_N²."""
        theta = 1e-10
        f_n1 = 0.25
        f_n2 = 0.30
        
        alpha1 = toe_alpha_from_theta(theta, f_n=f_n1)
        alpha2 = toe_alpha_from_theta(theta, f_n=f_n2)
        
        ratio = alpha2 / alpha1
        expected_ratio = (f_n2 / f_n1) ** 2
        
        assert abs(ratio - expected_ratio) / expected_ratio < 0.01, \
            f"α should scale as f_N²: ratio {ratio:.3f} vs expected {expected_ratio:.3f}"


class TestInverseMapping:
    """Test inverse mappings: α_max → θ_max → |κ_cH v_c|."""
    
    def test_theta_max_from_alpha_max_inverse(self):
        """Test that θ_max inversion matches forward calculation."""
        # Start with a known θ
        theta_known = 1e-12
        
        # Forward: θ → α
        alpha = toe_alpha_from_theta(theta_known, f_n=0.30)
        
        # Inverse: α → θ_max
        theta_max = toe_theta_max_from_alpha_max(alpha, f_n=0.30)
        
        # Should recover original θ (within small-angle approximation)
        assert abs(theta_max - theta_known) / abs(theta_known) < 0.01, \
            f"Inverse mismatch: {theta_max:.3e} vs {theta_known:.3e}"
    
    def test_kappa_vc_bounds_physical(self):
        """Test that |κ_cH v_c| bounds are physically reasonable."""
        # Use a typical Eöt-Wash bound
        alpha_max = 1e5  # Typical bound at short λ
        m_phi_GeV = 1e-3  # meV scale
        
        theta_max = toe_theta_max_from_alpha_max(alpha_max, f_n=0.30)
        kappa_vc_max = toe_kappa_vc_max_from_theta_max(
            theta_max=theta_max,
            m_phi_GeV=m_phi_GeV,
        )
        
        # Should be a very small number (GeV scale)
        assert kappa_vc_max > 0, "Bound should be positive"
        assert kappa_vc_max < 1e-10, \
            f"Bound should be very small: {kappa_vc_max:.3e} GeV"
    
    def test_kappa_vc_bounds_scale_correctly(self):
        """Test that bounds scale correctly with θ_max."""
        m_phi_GeV = 1e-3
        
        theta1 = 1e-12
        theta2 = 1e-11  # 10× larger
        
        kappa_vc1 = toe_kappa_vc_max_from_theta_max(theta1, m_phi_GeV)
        kappa_vc2 = toe_kappa_vc_max_from_theta_max(theta2, m_phi_GeV)
        
        # Should scale linearly with θ
        ratio = kappa_vc2 / kappa_vc1
        expected_ratio = theta2 / theta1
        
        assert abs(ratio - expected_ratio) / expected_ratio < 0.01, \
            f"Bound should scale linearly with θ: ratio {ratio:.3f} vs {expected_ratio:.3f}"


class TestModeD:
    """Test Mode D implementation in yukawa.py."""
    
    def test_mode_d_with_toe_params(self):
        """Test Mode D with explicit ToE parameters."""
        model = {
            "m_phi_GeV": 1e-3,  # meV scale
            "kappa_cH": 1e-2,
            "v_c_GeV": 1e-9,
            "m_c_GeV": 1e-3,
            "f_n": 0.30,
        }
        
        alpha_pred, lambda_m = model_point_to_alpha_lambda(
            model,
            mode="D",
        )
        
        # Should produce reasonable values
        assert alpha_pred > 0, "α_pred should be positive"
        assert lambda_m > 0, "λ should be positive"
        assert lambda_m < 1.0, "λ should be sub-meter for meV scale"
    
    def test_mode_d_with_theta_backward_compat(self):
        """Test Mode D backward compatibility with theta."""
        model = {
            "m_phi_GeV": 1e-3,
            "theta": 1e-12,  # Direct theta (backward compatibility)
        }
        
        alpha_pred, lambda_m = model_point_to_alpha_lambda(
            model,
            mode="D",
        )
        
        # Should work and produce reasonable values
        assert alpha_pred > 0, "α_pred should be positive"
        assert lambda_m > 0, "λ should be positive"
    
    def test_mode_d_vs_mode_b_comparison(self):
        """Test that Mode D and Mode B can produce similar results when parameters match."""
        # Use a small theta that both modes can handle
        theta = 1e-12
        m_phi_GeV = 1e-3
        
        # Mode D with theta
        model_d = {
            "m_phi_GeV": m_phi_GeV,
            "theta": theta,
        }
        alpha_d, lambda_d = model_point_to_alpha_lambda(model_d, mode="D")
        
        # Mode B with same theta
        model_b = {
            "m_phi_GeV": m_phi_GeV,
            "theta": theta,
        }
        alpha_b, lambda_b = model_point_to_alpha_lambda(model_b, mode="B", kappa=1.0)
        
        # Lambda should match (both use same m_phi)
        assert abs(lambda_d - lambda_b) / lambda_d < 0.01, \
            "λ should match between modes"
        
        # Alpha may differ (different normalizations), but both should be positive
        assert alpha_d > 0 and alpha_b > 0, "Both should produce positive α"
    
    def test_mode_d_requires_toe_params_or_theta(self):
        """Test that Mode D requires either ToE params or theta."""
        # Missing both
        model = {
            "m_phi_GeV": 1e-3,
        }
        
        with pytest.raises(ValueError, match="requires either"):
            model_point_to_alpha_lambda(model, mode="D")


class TestLambdaConversion:
    """Test λ ↔ m_φ conversion helpers."""
    
    def test_lambda_to_mphi_eV(self):
        """Test λ → m_φ conversion."""
        # Eöt-Wash window: λ ≈ 3×10⁻⁵ m
        lambda_m = 3e-5
        
        m_phi_eV = lambda_to_mphi_eV(lambda_m)
        
        # Should be meV scale
        assert m_phi_eV > 1e-4 and m_phi_eV < 1e-2, \
            f"m_φ should be meV scale: {m_phi_eV:.3e} eV"
    
    def test_lambda_to_mphi_inverse(self):
        """Test that λ ↔ m_φ conversion is invertible."""
        from code.inference.fifth_force.yukawa import mass_eV_to_lambda_m
        
        m_phi_eV_original = 1e-3  # meV
        
        lambda_m = mass_eV_to_lambda_m(m_phi_eV_original)
        m_phi_eV_recovered = lambda_to_mphi_eV(lambda_m)
        
        assert abs(m_phi_eV_recovered - m_phi_eV_original) / m_phi_eV_original < 0.01, \
            "Conversion should be invertible"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
