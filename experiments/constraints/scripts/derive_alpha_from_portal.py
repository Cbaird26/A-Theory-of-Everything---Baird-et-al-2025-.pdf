#!/usr/bin/env python3
"""
Derive Yukawa parameters (α, λ) from fundamental Higgs portal parameters.

Model: Light scalar φ that mixes with Higgs via mixing angle θ.
This prevents α from being a free "dial to zero" parameter.
"""
import argparse
import numpy as np
from typing import Tuple, Optional


# Physical constants (CODATA 2018)
HBAR_C_GeV_m = 1.973269804e-16  # ħc in GeV·m (CODATA 2018)
M_H = 125.0  # Higgs mass in GeV
# Reduced Planck mass: m_Pl^2 = 1/(8π G_N) (Brax & Burrage use reduced Planck mass)
# m_Pl_reduced = m_Pl_nonreduced / sqrt(8π) ≈ 2.43×10^18 GeV
M_PL = 2.435e18  # Reduced Planck mass in GeV (corrected from 1.22e19)
V_H = 246.0  # Higgs vev in GeV
M_N = 0.938  # Nucleon mass in GeV
G_NEWTON = 6.674e-11  # Newton's constant in m³/(kg·s²)


def derive_lambda_from_mass(m_phi: float, units: str = 'gev') -> float:
    """
    Derive Yukawa range λ from scalar mass m_φ using CODATA ħc.
    
    λ = ħc / (m_φ c²) in natural units
    
    Args:
        m_phi: Scalar mass (in GeV if units='gev', or eV/keV/MeV)
        units: 'gev', 'ev', 'kev', 'mev'
    
    Returns:
        λ in meters
    """
    # Convert to GeV
    if units == 'ev':
        m_phi_gev = m_phi * 1e-9
    elif units == 'kev':
        m_phi_gev = m_phi * 1e-6
    elif units == 'mev':
        m_phi_gev = m_phi * 1e-3
    elif units == 'gev':
        m_phi_gev = m_phi
    else:
        raise ValueError(f"Unknown units: {units}")
    
    # λ = ħc / m_φ (CODATA value)
    lambda_m = HBAR_C_GeV_m / m_phi_gev
    
    return lambda_m


def derive_alpha_simple(theta: float) -> float:
    """
    Simple α derivation: α = θ² for universal mass-proportional coupling.
    
    This is the minimal model where mixing angle directly sets fifth-force strength.
    NOTE: This is a toy mapping. Use derive_alpha_normalized for proper physics.
    
    Args:
        theta: Mixing angle (dimensionless, typically < 0.1)
    
    Returns:
        α (dimensionless Yukawa strength)
    """
    return theta**2


def derive_alpha_normalized(theta: float, m_phi: float, 
                            rho: float = 0.0, screening: bool = False,
                            Theta: float = 1.0, mu_sb: Optional[float] = None) -> float:
    """
    Properly normalized α derivation from Brax & Burrage (2021).
    
    Uses β_φ / m_Pl = sin θ / v (Eq. 26), and α = 2β² in standard Yukawa notation.
    Screening applied multiplicatively: α_eff = α_unscreened * Θ² (Eq. 97-98).
    
    Scale-breaking suppression (Burrage et al. 2018):
    When μ_sb is provided, applies additional suppression: α_eff = α_unscreened * (μ_sb/m_h)^4
    This models explicit scale breaking that suppresses tree-level fifth forces.
    
    Note: μ_sb (scale-breaking mass) is distinct from ATLAS signal strength μ.
    
    Args:
        theta: Mixing angle (dimensionless)
        m_phi: Scalar mass (in GeV)
        rho: Matter density (in kg/m³, for screening; default 0 = vacuum)
        screening: Whether to apply screening suppression
        Theta: Screening factor (0 < Θ ≤ 1), applied as α_eff = Θ² * α_unscreened
        mu_sb: Scale breaking mass (in GeV, optional). If provided, applies (μ_sb/m_h)^4 suppression.
    
    Returns:
        α (dimensionless Yukawa strength)
    """
    # Brax & Burrage Eq. 26: β_φ / m_Pl = sin θ / v
    # So: β_φ = (m_Pl / v) sin θ
    beta_phi = (M_PL / V_H) * np.sin(theta)
    
    # Standard Yukawa: α = 2 β² (Eq. 21 → Eq. 68 in linear regime)
    alpha_unscreened = 2.0 * beta_phi**2
    
    # Scale-breaking suppression (Burrage et al. 2018)
    # For μ_sb << m_h, tree-level fifth forces are suppressed as (μ_sb/m_h)^4
    if mu_sb is not None:
        scale_breaking_suppression = (mu_sb / M_H)**4
        alpha_unscreened = alpha_unscreened * scale_breaking_suppression
    
    # Screening: α_eff = Θ² * α_unscreened (Brax & Burrage Eq. 97-98)
    # Θ is the screening factor (0 < Θ ≤ 1), computed from paper's expressions
    # For now, allow user-set Theta; can compute from paper's formulas later
    if screening:
        alpha = (Theta**2) * alpha_unscreened
    else:
        alpha = alpha_unscreened
    
    return alpha


def derive_alpha_with_scale_breaking(theta: float, mu_sb: float, 
                                     m_phi: float, m_h: float = M_H) -> float:
    """
    α derivation with explicit scale breaking: α = θ² (μ_sb/m_h)².
    
    This includes suppression from scale breaking mass μ_sb.
    Note: μ_sb (scale-breaking mass) is distinct from ATLAS signal strength μ.
    
    Args:
        theta: Mixing angle
        mu_sb: Scale breaking mass (in GeV)
        m_phi: Scalar mass (in GeV)
        m_h: Higgs mass (default 125 GeV)
    
    Returns:
        α (dimensionless Yukawa strength)
    """
    return theta**2 * (mu_sb / m_h)**2


def derive_alpha_portal(theta: float, g_Hphi: float, m_phi: float,
                        m_h: float = M_H, v: float = 246.0) -> float:
    """
    More complete α derivation including portal coupling.
    
    For Higgs portal models, the effective coupling to matter is:
    α ∝ θ² (m_f² / v²) for fermions, or more generally:
    α = θ² * (g_Hphi² / (4π)) * (m_phi² / M²) for some scale M.
    
    Simplified version: α = θ² * (g_Hphi / g_weak)²
    
    Args:
        theta: Mixing angle
        g_Hphi: Higgs portal coupling (dimensionless)
        m_phi: Scalar mass (in GeV)
        m_h: Higgs mass (default 125 GeV)
        v: Higgs vev (default 246 GeV)
    
    Returns:
        α (dimensionless Yukawa strength)
    """
    # Simple approximation: α = θ² * g_Hphi²
    # More complete would include mass ratios
    return theta**2 * g_Hphi**2


def map_parameters_to_yukawa(m_phi: float, theta: float,
                             g_Hphi: Optional[float] = None,
                             mu_sb: Optional[float] = None,
                             rho: float = 0.0,
                             model: str = 'simple',
                             screening: bool = False,
                             Theta: float = 1.0) -> Tuple[float, float]:
    """
    Map fundamental parameters to Yukawa (α, λ).
    
    Args:
        m_phi: Scalar mass (in GeV)
        theta: Mixing angle (dimensionless)
        g_Hphi: Portal coupling (optional, for 'portal' model)
        mu_sb: Scale breaking mass (optional, for 'scale_breaking' model). Note: distinct from ATLAS signal strength μ.
        rho: Matter density (in kg/m³, for screening; default 0 = vacuum)
        model: 'simple', 'normalized', 'scale_breaking', 'portal', or 'screened'
        screening: Whether to apply screening (for 'normalized' or 'screened' models)
        Theta: Screening factor (0 < Θ ≤ 1), applied as α_eff = Θ² * α_unscreened
    
    Returns:
        (lambda_m, alpha) where lambda_m is in meters, alpha is dimensionless
    """
    # Derive λ from mass using CODATA ħc
    lambda_m = derive_lambda_from_mass(m_phi, units='gev')
    
    # Derive α based on model
    if model == 'simple':
        alpha = derive_alpha_simple(theta)
    elif model == 'normalized':
        alpha = derive_alpha_normalized(theta, m_phi, rho=rho, screening=screening, Theta=Theta, mu_sb=mu_sb)
    elif model == 'screened':
        alpha = derive_alpha_normalized(theta, m_phi, rho=rho, screening=True, Theta=Theta, mu_sb=mu_sb)
    elif model == 'scale_breaking':
        if mu_sb is None:
            raise ValueError("mu_sb required for scale_breaking model")
        alpha = derive_alpha_with_scale_breaking(theta, mu_sb, m_phi)
    elif model == 'portal':
        if g_Hphi is None:
            g_Hphi = 1.0  # Default coupling
        alpha = derive_alpha_portal(theta, g_Hphi, m_phi)
    else:
        raise ValueError(f"Unknown model: {model}")
    
    return lambda_m, alpha


def main():
    ap = argparse.ArgumentParser(description='Derive Yukawa parameters from Higgs portal')
    ap.add_argument('--m-phi', type=float, required=True,
                   help='Scalar mass (GeV)')
    ap.add_argument('--theta', type=float, required=True,
                   help='Mixing angle (dimensionless)')
    ap.add_argument('--g-Hphi', type=float, default=None,
                   help='Portal coupling (for portal model)')
    ap.add_argument('--mu-sb', type=float, default=None,
                   dest='mu_sb',
                   help='Scale breaking mass μ_sb (GeV, for scale_breaking model). Note: distinct from ATLAS signal strength μ.')
    ap.add_argument('--model', type=str, default='simple',
                   choices=['simple', 'normalized', 'screened', 'scale_breaking', 'portal'],
                   help='Model type')
    ap.add_argument('--rho', type=float, default=0.0,
                   help='Matter density (kg/m³) for screening')
    ap.add_argument('--screening', action='store_true',
                   help='Enable screening suppression')
    ap.add_argument('--Theta', type=float, default=1.0,
                   help='Screening factor Θ (0 < Θ ≤ 1, default 1.0 = unscreened)')
    args = ap.parse_args()
    
    lambda_m, alpha = map_parameters_to_yukawa(
        args.m_phi, args.theta,
        g_Hphi=args.g_Hphi,
        mu_sb=args.mu_sb,
        rho=args.rho,
        model=args.model,
        screening=args.screening,
        Theta=args.Theta
    )
    
    print(f"Input parameters:")
    print(f"  m_φ = {args.m_phi:.3e} GeV")
    print(f"  θ = {args.theta:.3e}")
    if args.g_Hphi is not None:
        print(f"  g_Hφ = {args.g_Hphi:.3e}")
    if args.mu_sb is not None:
        print(f"  μ_sb = {args.mu_sb:.3e} GeV")
    print(f"  Model: {args.model}")
    print()
    print(f"Derived Yukawa parameters:")
    print(f"  λ = {lambda_m:.3e} m ({lambda_m*1e6:.3f} µm)")
    print(f"  α = {alpha:.3e}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

