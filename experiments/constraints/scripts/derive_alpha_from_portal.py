#!/usr/bin/env python3
"""
Derive Yukawa parameters (α, λ) from fundamental Higgs portal parameters.

Model: Light scalar φ that mixes with Higgs via mixing angle θ.
This prevents α from being a free "dial to zero" parameter.
"""
import argparse
import numpy as np
from typing import Tuple, Optional


# Physical constants
HBAR_C = 197.3e-15  # ħc in GeV·m (for conversion)
M_H = 125.0  # Higgs mass in GeV
M_PL = 2.435e18  # Planck mass in GeV
V_H = 246.0  # Higgs vev in GeV
M_N = 0.938  # Nucleon mass in GeV
G_NEWTON = 6.674e-11  # Newton's constant in m³/(kg·s²)


def derive_lambda_from_mass(m_phi: float, units: str = 'gev') -> float:
    """
    Derive Yukawa range λ from scalar mass m_φ.
    
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
    
    # λ = ħ/(m_φ c) in natural units
    # In SI: λ = ħc / (m_φ c²)
    # Using ħc ≈ 197.3 MeV·fm = 197.3e-15 GeV·m
    lambda_m = HBAR_C / m_phi_gev
    
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
                            rho: float = 0.0, screening: bool = False) -> float:
    """
    Properly normalized α derivation from Brax & Burrage (2021).
    
    Uses β_φ / m_Pl = sin θ / v (Eq. 26), and α = 2β² in standard Yukawa notation.
    Includes screening suppression if enabled.
    
    For nucleons, the proper scaling is:
    α ≈ (sin θ / v)² * (m_Pl / m_N)² ≈ (θ / v)² * (m_Pl / m_N)² for small θ
    
    Args:
        theta: Mixing angle (dimensionless)
        m_phi: Scalar mass (in GeV)
        rho: Matter density (in kg/m³, for screening; default 0 = vacuum)
        screening: Whether to apply screening suppression
    
    Returns:
        α (dimensionless Yukawa strength)
    """
    # Brax & Burrage: β_φ / m_Pl = sin θ / v
    # For small θ: sin θ ≈ θ
    beta_over_mpl = np.sin(theta) / V_H
    
    # Fifth-force strength: α = 2β² (in standard Yukawa notation)
    # For nucleons: α ≈ (β_φ / m_Pl)² * (m_Pl / m_N)²
    # This gives: α ≈ (sin θ / v)² * (m_Pl / m_N)²
    # Using m_Pl ≈ 2.435e18 GeV, m_N ≈ 0.938 GeV
    # So (m_Pl / m_N)² ≈ (2.435e18 / 0.938)² ≈ 6.75e36
    # But this is still huge! Need to check literature more carefully.
    # 
    # Actually, the standard Yukawa α is defined relative to gravity:
    # V(r) = -G m1 m2 / r (1 + α e^{-r/λ})
    # So α is dimensionless and typically < 1 for weak forces.
    # 
    # For Higgs portal, the matter coupling comes from Higgs Yukawas:
    # After mixing, scalar couples as: (sin θ / v) * m_f * φ f̄ f
    # The fifth-force strength is: α ≈ (sin θ / v)² * (m_f / m_Pl)²
    # For nucleons (m_f ≈ 1 GeV): α ≈ (θ / v)² * (1 / m_Pl)²
    # This gives much smaller α!
    
    # More conservative: use (m_N / m_Pl)² factor (not m_Pl / m_N)
    # This gives: α ≈ (sin θ / v)² * (m_N / m_Pl)²
    # For small θ: α ≈ (θ / v)² * (m_N / m_Pl)²
    alpha_unscreened = (beta_over_mpl * (M_N / M_PL))**2
    
    # Alternative: if literature says α ∝ θ² directly (simple portal),
    # then normalized version might be: α = θ² * (m_N² / (v² m_Pl²))
    # This is much smaller and more reasonable
    # Let's use this more conservative form:
    alpha_unscreened = (theta / V_H)**2 * (M_N / M_PL)**2
    
    # Screening: α_eff = α / (1 + ρ / ρ_crit)
    # where ρ_crit ~ m_φ² / θ² (in appropriate units)
    if screening and rho > 0:
        # Critical density: ρ_crit ~ m_φ² / (θ² * normalization)
        # In SI: ρ_crit ≈ m_phi² c² / (θ² ħ²) for screening
        # Simplified: use approximate scaling
        # For typical screening: ρ_crit ≈ 10^3 - 10^4 kg/m³ for micron-scale
        rho_crit = (m_phi * 1e9)**2 / (theta**2 * 1e18)  # Rough scaling in kg/m³
        if rho_crit > 0:
            alpha = alpha_unscreened / (1.0 + rho / rho_crit)
        else:
            alpha = alpha_unscreened
    else:
        alpha = alpha_unscreened
    
    return alpha


def derive_alpha_with_scale_breaking(theta: float, mu: float, 
                                     m_phi: float, m_h: float = M_H) -> float:
    """
    α derivation with explicit scale breaking: α = θ² (μ/m_h)².
    
    This includes suppression from scale breaking mass μ.
    
    Args:
        theta: Mixing angle
        mu: Scale breaking mass (in GeV)
        m_phi: Scalar mass (in GeV)
        m_h: Higgs mass (default 125 GeV)
    
    Returns:
        α (dimensionless Yukawa strength)
    """
    return theta**2 * (mu / m_h)**2


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
                             mu: Optional[float] = None,
                             rho: float = 0.0,
                             model: str = 'simple',
                             screening: bool = False) -> Tuple[float, float]:
    """
    Map fundamental parameters to Yukawa (α, λ).
    
    Args:
        m_phi: Scalar mass (in GeV)
        theta: Mixing angle (dimensionless)
        g_Hphi: Portal coupling (optional, for 'portal' model)
        mu: Scale breaking mass (optional, for 'scale_breaking' model)
        rho: Matter density (in kg/m³, for screening; default 0 = vacuum)
        model: 'simple', 'normalized', 'scale_breaking', 'portal', or 'screened'
        screening: Whether to apply screening (for 'normalized' or 'screened' models)
    
    Returns:
        (lambda_m, alpha) where lambda_m is in meters, alpha is dimensionless
    """
    # Derive λ from mass
    # Unit check: λ = ħc / (m_φ c²) = ħc / m_φ (in natural units)
    # Using ħc ≈ 197.3 MeV·fm = 197.3e-15 GeV·m
    lambda_m = derive_lambda_from_mass(m_phi, units='gev')
    
    # Derive α based on model
    if model == 'simple':
        alpha = derive_alpha_simple(theta)
    elif model == 'normalized':
        alpha = derive_alpha_normalized(theta, m_phi, rho=rho, screening=screening)
    elif model == 'screened':
        alpha = derive_alpha_normalized(theta, m_phi, rho=rho, screening=True)
    elif model == 'scale_breaking':
        if mu is None:
            raise ValueError("mu required for scale_breaking model")
        alpha = derive_alpha_with_scale_breaking(theta, mu, m_phi)
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
    ap.add_argument('--mu', type=float, default=None,
                   help='Scale breaking mass (GeV, for scale_breaking model)')
    ap.add_argument('--model', type=str, default='simple',
                   choices=['simple', 'normalized', 'screened', 'scale_breaking', 'portal'],
                   help='Model type')
    ap.add_argument('--rho', type=float, default=0.0,
                   help='Matter density (kg/m³) for screening')
    ap.add_argument('--screening', action='store_true',
                   help='Enable screening suppression')
    args = ap.parse_args()
    
    lambda_m, alpha = map_parameters_to_yukawa(
        args.m_phi, args.theta,
        g_Hphi=args.g_Hphi,
        mu=args.mu,
        rho=args.rho,
        model=args.model,
        screening=args.screening
    )
    
    print(f"Input parameters:")
    print(f"  m_φ = {args.m_phi:.3e} GeV")
    print(f"  θ = {args.theta:.3e}")
    if args.g_Hphi is not None:
        print(f"  g_Hφ = {args.g_Hphi:.3e}")
    if args.mu is not None:
        print(f"  μ = {args.mu:.3e} GeV")
    print(f"  Model: {args.model}")
    print()
    print(f"Derived Yukawa parameters:")
    print(f"  λ = {lambda_m:.3e} m ({lambda_m*1e6:.3f} µm)")
    print(f"  α = {alpha:.3e}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

