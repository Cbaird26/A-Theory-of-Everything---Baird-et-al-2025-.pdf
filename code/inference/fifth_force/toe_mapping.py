"""ToE-native fifth-force mapping functions using explicit ToE equations.

This module implements the exact bridge from ToE parameters to Yukawa fifth-force
strength using the ToE paper's equations (Eq. 13 for Higgs mixing, etc.).

Key equations:
- ToE Eq. (13): θ_hc ≃ κ_cH v v_c / (m_c² - m_h²)
- Yukawa strength: α = 2 f_N² (M_Pl/v)² sin²θ
- Inverse: θ_max = √(α_max / K_ToE) where K_ToE = 2 f_N² (M_Pl/v)²
"""

import numpy as np
from typing import Optional

# ToE-defined constants (matching ToE paper conventions)
# Reduced Planck mass: M_Pl² = (8πG)⁻¹
M_PL_REDUCED_GEV = 2.435e18  # GeV
V_HIGGS_GEV = 246.0  # GeV (Higgs vev)
M_HIGGS_GEV = 125.0  # GeV (Higgs mass)
F_N_DEFAULT = 0.30  # Nucleon scalar form factor (default, can be swept)

# CODATA 2018: ħc = 1.973269804e-16 GeV·m
HBAR_C_GEV_M = 1.973269804e-16

# CODATA 2018: ħc = 1.973269804e-7 eV·m (for eV-based calculations)
HBAR_C_EV_M = 1.973269804e-7


def toe_theta_hc(
    kappa_cH: float,
    v_c_GeV: float,
    m_c_GeV: float,
    v_GeV: float = V_HIGGS_GEV,
    m_h_GeV: float = M_HIGGS_GEV,
) -> float:
    """Compute Higgs-scalar mixing angle using ToE Eq. (13).
    
    Implements: θ_hc ≃ κ_cH v v_c / (m_c² - m_h²)
    
    For m_c << m_h (typical in Eöt-Wash window): θ_hc ≈ -κ_cH v v_c / m_h²
    
    Args:
        kappa_cH: Portal coupling constant (dimensionless)
        v_c_GeV: Scalar VEV in GeV
        m_c_GeV: Scalar mass in GeV
        v_GeV: Higgs vev in GeV (default: 246.0)
        m_h_GeV: Higgs mass in GeV (default: 125.0)
    
    Returns:
        Mixing angle θ_hc in radians
    
    Reference:
        ToE paper Eq. (13)
    """
    denominator = m_c_GeV**2 - m_h_GeV**2
    if abs(denominator) < 1e-10:
        # Avoid division by zero (degenerate case)
        raise ValueError(f"Degenerate case: m_c² ≈ m_h² (m_c={m_c_GeV:.3e} GeV)")
    
    theta_hc = (kappa_cH * v_GeV * v_c_GeV) / denominator
    return theta_hc


def toe_alpha_from_theta(
    theta: float,
    f_n: float = F_N_DEFAULT,
    mpl_reduced_GeV: float = M_PL_REDUCED_GEV,
    v_GeV: float = V_HIGGS_GEV,
) -> float:
    """Compute Yukawa strength from mixing angle using ToE normalization.
    
    Implements: α = 2 f_N² (M_Pl/v)² sin²θ
    
    Numerically, for f_N=0.30: K_ToE ≈ 1.76×10³¹
    
    Args:
        theta: Mixing angle in radians
        f_n: Nucleon scalar form factor (default: 0.30)
        mpl_reduced_GeV: Reduced Planck mass in GeV (default: 2.435e18)
        v_GeV: Higgs vev in GeV (default: 246.0)
    
    Returns:
        Yukawa strength α (dimensionless)
    
    Note:
        Uses ToE's reduced Planck mass convention: M_Pl² = (8πG)⁻¹
    """
    sin_theta = np.sin(theta)
    # K_ToE = 2 f_N² (M_Pl/v)²
    K_ToE = 2.0 * (f_n**2) * ((mpl_reduced_GeV / v_GeV) ** 2)
    alpha = K_ToE * (sin_theta**2)
    return alpha


def toe_theta_max_from_alpha_max(
    alpha_max: float,
    f_n: float = F_N_DEFAULT,
    mpl_reduced_GeV: float = M_PL_REDUCED_GEV,
    v_GeV: float = V_HIGGS_GEV,
) -> float:
    """Invert α(θ) to get maximum mixing angle from experimental bound.
    
    Implements: θ_max = √(α_max / K_ToE)
    
    This converts Eöt-Wash α_max(λ) bounds to mixing-angle bounds.
    
    Args:
        alpha_max: Maximum allowed Yukawa strength (from experimental bound)
        f_n: Nucleon scalar form factor (default: 0.30)
        mpl_reduced_GeV: Reduced Planck mass in GeV (default: 2.435e18)
        v_GeV: Higgs vev in GeV (default: 246.0)
    
    Returns:
        Maximum mixing angle θ_max in radians
    
    Note:
        Uses small-angle approximation: sin θ ≈ θ for tiny angles
    """
    if alpha_max < 0:
        # Clamp negative values (digitization noise)
        alpha_max = 0.0
    
    # K_ToE = 2 f_N² (M_Pl/v)²
    K_ToE = 2.0 * (f_n**2) * ((mpl_reduced_GeV / v_GeV) ** 2)
    
    if K_ToE <= 0:
        return float("nan")
    
    # θ_max = √(α_max / K_ToE)
    # For small angles, sin θ ≈ θ, so this is valid
    theta_max = np.sqrt(alpha_max / K_ToE)
    return theta_max


def toe_kappa_vc_max_from_theta_max(
    theta_max: float,
    m_phi_GeV: float,
    v_GeV: float = V_HIGGS_GEV,
    m_h_GeV: float = M_HIGGS_GEV,
) -> float:
    """Compute bound on portal parameter combination |κ_cH v_c| from mixing bound.
    
    Inverts ToE Eq. (13) to get: |κ_cH v_c| ≤ θ_max · (m_h²/v)
    
    For m_c << m_h (typical in Eöt-Wash window):
    |κ_cH v_c| ≤ θ_max · (m_h²/v) ≈ θ_max · 63.5 GeV
    
    Args:
        theta_max: Maximum mixing angle in radians
        m_phi_GeV: Scalar mediator mass in GeV
        v_GeV: Higgs vev in GeV (default: 246.0)
        m_h_GeV: Higgs mass in GeV (default: 125.0)
    
    Returns:
        Maximum allowed |κ_cH v_c| in GeV
    
    Reference:
        ToE paper Eq. (13) inverted
    """
    # For m_c << m_h, denominator ≈ -m_h², so:
    # |κ_cH v_c| ≤ |θ_max| · |m_c² - m_h²| / v
    # For m_c << m_h: |κ_cH v_c| ≤ θ_max · m_h² / v
    
    if m_phi_GeV < m_h_GeV * 0.1:  # m_c << m_h regime
        kappa_vc_max = abs(theta_max) * (m_h_GeV**2) / v_GeV
    else:
        # General case (though less common in Eöt-Wash window)
        denominator = abs(m_phi_GeV**2 - m_h_GeV**2)
        kappa_vc_max = abs(theta_max) * denominator / v_GeV
    
    return kappa_vc_max


def lambda_to_mphi_eV(lambda_m: float) -> float:
    """Convert Yukawa range to scalar mediator mass.
    
    Inverse of mass_eV_to_lambda_m: m_φ = ħc / λ
    
    Args:
        lambda_m: Yukawa range in meters
    
    Returns:
        Scalar mediator mass in eV
    """
    if lambda_m <= 0:
        raise ValueError(f"Lambda must be positive, got {lambda_m}")
    
    # m_φ (eV) = ħc (eV·m) / λ (m)
    m_phi_eV = HBAR_C_EV_M / lambda_m
    return m_phi_eV


def lambda_to_mphi_GeV(lambda_m: float) -> float:
    """Convert Yukawa range to scalar mediator mass in GeV.
    
    Args:
        lambda_m: Yukawa range in meters
    
    Returns:
        Scalar mediator mass in GeV
    """
    m_phi_eV = lambda_to_mphi_eV(lambda_m)
    m_phi_GeV = m_phi_eV * 1e-9
    return m_phi_GeV


def compute_K_ToE(
    f_n: float = F_N_DEFAULT,
    mpl_reduced_GeV: float = M_PL_REDUCED_GEV,
    v_GeV: float = V_HIGGS_GEV,
) -> float:
    """Compute the ToE prefactor K_ToE = 2 f_N² (M_Pl/v)².
    
    This is the constant that relates mixing angle to Yukawa strength:
    α = K_ToE sin²θ
    
    Args:
        f_n: Nucleon scalar form factor (default: 0.30)
        mpl_reduced_GeV: Reduced Planck mass in GeV (default: 2.435e18)
        v_GeV: Higgs vev in GeV (default: 246.0)
    
    Returns:
        K_ToE prefactor (dimensionless)
    
    Example:
        For f_N=0.30: K_ToE ≈ 1.76×10³¹
    """
    K_ToE = 2.0 * (f_n**2) * ((mpl_reduced_GeV / v_GeV) ** 2)
    return K_ToE
