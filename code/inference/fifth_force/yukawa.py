"""Map model parameters to Yukawa fifth-force parameters (alpha, lambda)."""

import sys
from pathlib import Path
import importlib.util

# Import ToE-native mapping functions
try:
    from .toe_mapping import (
        toe_theta_hc,
        toe_alpha_from_theta,
        lambda_to_mphi_GeV,
    )
except ImportError:
    # Fallback if toe_mapping not available
    toe_theta_hc = None
    toe_alpha_from_theta = None
    lambda_to_mphi_GeV = None

# Try to import derive_alpha functions from experiments/constraints/scripts
_derive_module = None
_scripts_path = Path(__file__).parent.parent.parent.parent / "experiments" / "constraints" / "scripts"
_derive_path = _scripts_path / "derive_alpha_from_portal.py"

if _derive_path.exists():
    spec = importlib.util.spec_from_file_location("derive_alpha_from_portal", _derive_path)
    if spec and spec.loader:
        _derive_module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(_derive_module)
            derive_alpha_normalized = _derive_module.derive_alpha_normalized
            derive_lambda_from_mass = _derive_module.derive_lambda_from_mass
        except Exception:
            _derive_module = None

if _derive_module is None:
    # Fallback if module not available
    def derive_alpha_normalized(*args, **kwargs):
        raise NotImplementedError("derive_alpha_from_portal module not available - ensure experiments/constraints/scripts/derive_alpha_from_portal.py exists")
    
    def derive_lambda_from_mass(m_phi, **kwargs):
        raise NotImplementedError("derive_alpha_from_portal module not available")


# CODATA 2018: ħc = 1.973269804e-16 GeV·m
HBAR_C_GEV_M = 1.973269804e-16


def mass_eV_to_lambda_m(m_eV: float) -> float:
    """Convert scalar mediator mass to Compton wavelength.

    Args:
        m_eV: Mass in eV

    Returns:
        Compton wavelength in meters: λ = ħc / (m c²)
    """
    if m_eV <= 0:
        raise ValueError(f"Mass must be positive, got {m_eV}")
    
    # Convert eV to GeV
    m_GeV = m_eV * 1e-9
    
    # λ = ħc / m
    lambda_m = HBAR_C_GEV_M / m_GeV
    return lambda_m


def model_point_to_alpha_lambda(
    model: dict,
    mode: str = "A",
    kappa: float = 1.0,
    s_ff: float = 1.0,
    s_lambda: float = 1.0,
) -> tuple[float, float]:
    """Map a model point to (alpha_pred, lambda_m) for fifth-force evaluation.

    Args:
        model: Dictionary with keys:
            - For modes A/B/C:
                - m_phi (or m_phi_eV): scalar mass in GeV (or eV)
                - theta: mixing angle
                - mu_sb (optional): scale-breaking mass in GeV
                - Theta_lab (optional): screening factor
            - For mode D (ToE-native):
                - kappa_cH: portal coupling constant (dimensionless)
                - v_c_GeV: scalar VEV in GeV
                - m_c_GeV (or m_phi/m_phi_eV): scalar mass in GeV (or eV)
                - OR theta: mixing angle (for backward compatibility)
                - f_n (optional): nucleon scalar form factor (default: 0.30)
        mode: Mapping mode - "A" (placeholder), "B" (portal-proxy), "C" (agnostic scaling), "D" (ToE-native)
        kappa: Portal coupling factor for mode B (default: 1.0)
        s_ff: Scaling factor for alpha in mode C (default: 1.0)
        s_lambda: Scaling factor for lambda in mode C (default: 1.0)

    Returns:
        (alpha_pred, lambda_m) where:
            alpha_pred: predicted fifth-force strength (dimensionless)
            lambda_m: range in meters (scaled by s_lambda in mode C)
    
    Mapping Modes:
        - Mode A: α_pred = α_eff² (legacy placeholder)
        - Mode B: α_pred = 2(κ α_eff)² (portal-derived proxy)
        - Mode C: α_pred = s_ff α_eff², λ → s_lambda λ (agnostic scaling)
        - Mode D: ToE-native bridge using κ_cH, v_c → θ_hc (Eq. 13) → α (ToE normalization)
    """
    # Extract m_phi (handle both GeV and eV)
    m_phi = model.get("m_phi") or model.get("m_phi_GeV")
    m_phi_eV = model.get("m_phi_eV")
    
    if m_phi_eV is not None:
        m_phi = m_phi_eV * 1e-9  # Convert eV to GeV
    
    if m_phi is None or m_phi <= 0:
        raise ValueError(f"Invalid m_phi: {model.get('m_phi')}")
    
    # Compute lambda_m
    if m_phi_eV is not None:
        lambda_m = mass_eV_to_lambda_m(m_phi_eV)
    else:
        # Convert GeV to eV for lambda calculation
        m_phi_eV = m_phi * 1e9
        lambda_m = mass_eV_to_lambda_m(m_phi_eV)
    
    # Handle Mode D separately (ToE-native, doesn't use derive_alpha_normalized)
    if mode == "D":
        # Mode D: ToE-Native Higgs-Mixing Bridge
        # Uses explicit ToE equations: κ_cH, v_c → θ_hc (Eq. 13) → α
        if toe_theta_hc is None or toe_alpha_from_theta is None:
            raise NotImplementedError(
                "Mode D requires toe_mapping module. Ensure code/inference/fifth_force/toe_mapping.py exists"
            )
        
        # Extract ToE parameters
        kappa_cH = model.get("kappa_cH")
        v_c_GeV = model.get("v_c_GeV")
        m_c_GeV = model.get("m_c_GeV")
        f_n = model.get("f_n", 0.30)  # Default nucleon form factor
        
        # Support backward compatibility: if theta is provided directly, use it
        theta_provided = model.get("theta")
        
        if theta_provided is not None and (kappa_cH is None or v_c_GeV is None):
            # Backward compatibility: use provided theta directly
            theta_hc = theta_provided
        elif kappa_cH is not None and v_c_GeV is not None:
            # ToE-native: compute theta from portal parameters
            if m_c_GeV is None:
                # Try to derive m_c from m_phi
                if m_phi_eV is not None:
                    m_c_GeV = m_phi_eV * 1e-9
                elif m_phi is not None:
                    m_c_GeV = m_phi
                else:
                    raise ValueError(
                        "Mode D requires m_c_GeV (or m_phi/m_phi_eV) when using kappa_cH, v_c"
                    )
            
            # Compute θ_hc using ToE Eq. (13)
            theta_hc = toe_theta_hc(
                kappa_cH=kappa_cH,
                v_c_GeV=v_c_GeV,
                m_c_GeV=m_c_GeV,
            )
        else:
            raise ValueError(
                "Mode D requires either (kappa_cH, v_c_GeV, m_c_GeV) or theta in model dict"
            )
        
        # Compute α_pred using ToE normalization
        alpha_pred = toe_alpha_from_theta(theta=theta_hc, f_n=f_n)
        
        # Lambda is already computed from m_phi above
        # No additional scaling for Mode D (it's the "exact" mapping)
        return alpha_pred, lambda_m
    
    # For modes A/B/C, extract theta and use existing pipeline
    theta = model.get("theta")
    if theta is None:
        raise ValueError("theta required in model point for modes A/B/C")
    
    # Compute alpha using existing pipeline function
    mu_sb = model.get("mu_sb")
    Theta_lab = model.get("Theta_lab", 1.0)
    model_type = model.get("model", "normalized")
    
    # Call derive_alpha_normalized with appropriate parameters
    try:
        alpha_eff = derive_alpha_normalized(
            theta=theta,
            m_phi=m_phi,
            mu_sb=mu_sb,
            screening=Theta_lab != 1.0,
            Theta=Theta_lab,
        )
        
        # Apply mapping mode
        if mode == "A":
            # Mode A: Legacy placeholder
            # α_pred = α_eff² (temporary surrogate, kept for backward compatibility)
            alpha_pred = alpha_eff ** 2
        elif mode == "B":
            # Mode B: Portal-derived proxy
            # α_pred = 2(κ α_eff)² (based on Higgs portal literature approximations)
            # Assumption: Portal coupling factor κ provides reasonable approximation
            # Limitation: Not derived from first principles
            alpha_pred = 2.0 * (kappa * alpha_eff) ** 2
        elif mode == "C":
            # Mode C: Agnostic scaling
            # α_pred = s_ff α_eff², λ → s_lambda λ
            # Explicit scaling knobs for sensitivity analysis
            # Limitation: No physical justification for specific scaling values
            alpha_pred = s_ff * (alpha_eff ** 2)
            lambda_m = s_lambda * lambda_m
        elif mode == "D":
            # Mode D: ToE-Native Higgs-Mixing Bridge
            # Uses explicit ToE equations: κ_cH, v_c → θ_hc (Eq. 13) → α
            # This is the exact mapping from ToE parameters to Yukawa strength
            if toe_theta_hc is None or toe_alpha_from_theta is None:
                raise NotImplementedError(
                    "Mode D requires toe_mapping module. Ensure code/inference/fifth_force/toe_mapping.py exists"
                )
            
            # Extract ToE parameters
            kappa_cH = model.get("kappa_cH")
            v_c_GeV = model.get("v_c_GeV")
            m_c_GeV = model.get("m_c_GeV")
            f_n = model.get("f_n", 0.30)  # Default nucleon form factor
            
            # Support backward compatibility: if theta is provided directly, use it
            theta_provided = model.get("theta")
            
            if theta_provided is not None and (kappa_cH is None or v_c_GeV is None):
                # Backward compatibility: use provided theta directly
                theta_hc = theta_provided
            elif kappa_cH is not None and v_c_GeV is not None:
                # ToE-native: compute theta from portal parameters
                if m_c_GeV is None:
                    # Try to derive m_c from m_phi
                    if m_phi_eV is not None:
                        m_c_GeV = m_phi_eV * 1e-9
                    elif m_phi is not None:
                        m_c_GeV = m_phi
                    else:
                        raise ValueError(
                            "Mode D requires m_c_GeV (or m_phi/m_phi_eV) when using kappa_cH, v_c"
                        )
                
                # Compute θ_hc using ToE Eq. (13)
                theta_hc = toe_theta_hc(
                    kappa_cH=kappa_cH,
                    v_c_GeV=v_c_GeV,
                    m_c_GeV=m_c_GeV,
                )
            else:
                raise ValueError(
                    "Mode D requires either (kappa_cH, v_c_GeV, m_c_GeV) or theta in model dict"
                )
            
            # Compute α_pred using ToE normalization
            alpha_pred = toe_alpha_from_theta(theta=theta_hc, f_n=f_n)
            
            # Lambda is already computed from m_phi above
            # No additional scaling for Mode D (it's the "exact" mapping)
        else:
            raise ValueError(f"Invalid mapping mode: {mode}. Must be 'A', 'B', 'C', or 'D'")
        
        # Ensure positive
        if alpha_pred <= 0:
            alpha_pred = abs(alpha_eff) ** 2
        
    except Exception as e:
        # Fallback if derivation fails
        raise ValueError(f"Failed to compute alpha: {e}") from e
    
    return alpha_pred, lambda_m

