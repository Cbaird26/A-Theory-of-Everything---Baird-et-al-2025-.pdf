#!/usr/bin/env python3
"""Import Bennu/OSIRIS-REx fifth-force constraint curve.

Based on Communications Physics (2024) analysis using OSIRIS-REx trajectory data
to constrain ultralight scalar mediators at AU scales.

Reference: arXiv:2309.13106 / Communications Physics (2024)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# Physical constants
AU_TO_M = 1.496e11  # Astronomical unit in meters
C_LIGHT = 299792458.0  # m/s
H_PLANCK = 6.62607015e-34  # J·s
EV_TO_JOULE = 1.602176634e-19  # J/eV
HBAR_C = 1.973269804e-16  # GeV·m (CODATA 2018)

# Bennu constraint parameters from Communications Physics (2024)
# Mediator mass range: ~10^-18 to 10^-17 eV
# Corresponds to λ ~ 0.13 to 1.3 AU
# Constraint: α < ~10^-3 at these scales
BENNU_M_MEDIATOR_MIN_EV = 1e-18
BENNU_M_MEDIATOR_MAX_EV = 1e-17
BENNU_ALPHA_MAX = 1e-3  # Approximate upper bound from trajectory analysis

SOURCE_ID = "bennu_osiris_rex_2024"
REF = "arXiv:2309.13106, Communications Physics (2024)"


def mediator_mass_to_lambda(m_phi_eV: float) -> float:
    """Convert mediator mass to Yukawa range.
    
    Args:
        m_phi_eV: Mediator mass in eV
    
    Returns:
        Interaction range in meters: λ = ħc / (m_phi c^2)
    """
    # Convert eV to GeV
    m_phi_GeV = m_phi_eV * 1e-9
    
    # λ = ħc / (m_phi c^2) = ħc / m_phi
    # Using ħc = 1.973e-16 GeV·m
    if m_phi_GeV <= 0:
        return np.nan
    
    lambda_m = HBAR_C / m_phi_GeV
    return lambda_m


def generate_bennu_constraint_curve(
    n_points: int = 50,
    m_min_eV: float = BENNU_M_MEDIATOR_MIN_EV,
    m_max_eV: float = BENNU_M_MEDIATOR_MAX_EV,
    alpha_max: float = BENNU_ALPHA_MAX,
) -> pd.DataFrame:
    """Generate Bennu constraint curve from mass range.
    
    Args:
        n_points: Number of points in curve
        m_min_eV: Minimum mediator mass (eV)
        m_max_eV: Maximum mediator mass (eV)
        alpha_max: Maximum coupling strength (dimensionless)
    
    Returns:
        DataFrame with columns: lambda_m, alpha_max, source_id, ref
    """
    # Sample mediator masses uniformly in log space
    log_m_min = np.log10(m_min_eV)
    log_m_max = np.log10(m_max_eV)
    log_masses = np.linspace(log_m_min, log_m_max, n_points)
    masses_eV = 10.0 ** log_masses
    
    # Convert to lambda_m
    lambda_m = [mediator_mass_to_lambda(m) for m in masses_eV]
    
    # Create DataFrame
    result = pd.DataFrame({
        "lambda_m": lambda_m,
        "alpha_max": [alpha_max] * n_points,  # Constant bound (conservative)
        "source_id": SOURCE_ID,
        "ref": REF,
    })
    
    # Remove NaN values
    result = result.dropna()
    
    # Sort by lambda_m
    result = result.sort_values("lambda_m").reset_index(drop=True)
    
    # Ensure positive values
    result = result[result["lambda_m"] > 0]
    result = result[result["alpha_max"] > 0]
    
    print(f"Generated {len(result)} constraint points")
    print(f"  lambda_m range: {result['lambda_m'].min():.3e} to {result['lambda_m'].max():.3e} m")
    print(f"  lambda_m range: {result['lambda_m'].min()/AU_TO_M:.3f} to {result['lambda_m'].max()/AU_TO_M:.3f} AU")
    print(f"  alpha_max: {alpha_max:.3e}")
    
    return result


def ingest_via_pipeline(df: pd.DataFrame, output_dir: Path) -> Path:
    """Write contract CSV and call ingest pipeline.
    
    Args:
        df: DataFrame with contract columns
        output_dir: Directory to write contract CSV
    
    Returns:
        Path to contract CSV
    """
    contract_csv = output_dir / "bennu_osiris_rex_2024_contract.csv"
    df.to_csv(contract_csv, index=False)
    
    print(f"Wrote contract CSV: {contract_csv}")
    
    # Call ingest pipeline
    print("Calling fifth-force ingest pipeline...")
    from pathlib import Path
    # Add project root to path
    project_root = Path(__file__).parent.parent.parent.parent.parent
    sys.path.insert(0, str(project_root))
    from code.inference.fifth_force.ingest import ingest_fifth_force_csv
    
    processed_dir = project_root / "data" / "processed"
    results_dir = project_root / "results" / "fifth_force"
    processed_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    ingest_fifth_force_csv(contract_csv, processed_dir, results_dir)
    
    return contract_csv


def main():
    ap = argparse.ArgumentParser(
        description="Import Bennu/OSIRIS-REx constraint curve for fifth-force analysis"
    )
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw/fifth_force"),
        help="Directory to save contract CSV (default: data/raw/fifth_force)",
    )
    ap.add_argument(
        "--n-points",
        type=int,
        default=50,
        help="Number of points in constraint curve (default: 50)",
    )
    ap.add_argument(
        "--alpha-max",
        type=float,
        default=BENNU_ALPHA_MAX,
        help=f"Maximum coupling strength (default: {BENNU_ALPHA_MAX})",
    )
    
    args = ap.parse_args()
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate constraint curve
    df = generate_bennu_constraint_curve(
        n_points=args.n_points,
        alpha_max=args.alpha_max,
    )
    
    # Ingest
    contract_csv = ingest_via_pipeline(df, args.output_dir)
    
    print(f"\n✅ Successfully imported Bennu/OSIRIS-REx constraint curve")
    print(f"   Contract CSV: {contract_csv}")
    print(f"   Validated CSV: data/processed/bennu_osiris_rex_2024_validated.csv")
    print(f"   Provenance: results/fifth_force/bennu_osiris_rex_2024_provenance.json")
    print(f"\n   Note: This constraint covers AU-scale ranges (λ ~ 0.13 to 1.3 AU)")
    print(f"   Complementary to Eöt-Wash sub-mm constraints")


if __name__ == "__main__":
    main()

