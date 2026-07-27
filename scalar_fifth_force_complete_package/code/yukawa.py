"""Map model parameters to Yukawa fifth-force parameters (alpha, lambda)."""

import sys
from pathlib import Path
import importlib.util

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


def model_point_to_alpha_lambda(model: dict) -> tuple[float, float]:
    """Map a model point to (alpha_pred, lambda_m) for fifth-force evaluation.

    Args:
        model: Dictionary with keys:
            - m_phi (or m_phi_eV): scalar mass in GeV (or eV)
            - theta: mixing angle
            - mu_sb (optional): scale-breaking mass in GeV
            - Theta_lab (optional): screening factor
            - model (optional): model variant string

    Returns:
        (alpha_pred, lambda_m) where:
            alpha_pred: predicted fifth-force strength (dimensionless)
            lambda_m: range in meters
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
    
    # Extract theta
    theta = model.get("theta")
    if theta is None:
        raise ValueError("theta required in model point")
    
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
        
        # TODO: Temporary mapping - alpha_pred = alpha_eff**2
        # This should be refined based on physics justification
        # For now, use squared to ensure positive alpha_pred
        alpha_pred = alpha_eff ** 2
        
        # Ensure positive
        if alpha_pred <= 0:
            alpha_pred = abs(alpha_eff) ** 2
        
    except Exception as e:
        # Fallback if derivation fails
        raise ValueError(f"Failed to compute alpha: {e}") from e
    
    return alpha_pred, lambda_m

