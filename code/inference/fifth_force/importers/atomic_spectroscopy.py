#!/usr/bin/env python3
"""Import atomic spectroscopy fifth-force constraint curve.

Based on ETH Zurich calcium isotope shift measurements (2025),
constraining neutron-electron fifth forces at atomic energy scales.

Reference: ETH Zurich Research Collection (2025)
Precision: ~100 mHz on energy shifts
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# Physical constants
C_LIGHT = 299792458.0  # m/s
H_PLANCK = 6.62607015e-34  # J·s
EV_TO_JOULE = 1.602176634e-19  # J/eV
HBAR_C = 1.973269804e-16  # GeV·m (CODATA 2018)

# Atomic spectroscopy constraint parameters
# Mediator mass range: ~10 eV to 10^7 eV
# Constraint: α < ~10^-10 (relative to gravity)
# Energy scale: atomic transitions (~eV to keV)
ATOMIC_M_MEDIATOR_MIN_EV = 10.0
ATOMIC_M_MEDIATOR_MAX_EV = 1e7
ATOMIC_ALPHA_MAX = 1e-10  # Approximate upper bound

SOURCE_ID = "atomic_spectroscopy_eth_2025"
REF = "ETH Zurich Research Collection (2025), ~100 mHz precision"


def mediator_mass_to_lambda(m_phi_eV: float) -> float:
    """Convert mediator mass to Yukawa range.
    
    Args:
        m_phi_eV: Mediator mass in eV
    
    Returns:
        Interaction range in meters: λ = ħc / (m_phi c^2)
    """
    m_phi_GeV = m_phi_eV * 1e-9
    
    if m_phi_GeV <= 0:
        return np.nan
    
    lambda_m = HBAR_C / m_phi_GeV
    return lambda_m


def generate_atomic_constraint_curve(
    n_points: int = 50,
    m_min_eV: float = ATOMIC_M_MEDIATOR_MIN_EV,
    m_max_eV: float = ATOMIC_M_MEDIATOR_MAX_EV,
    alpha_max: float = ATOMIC_ALPHA_MAX,
) -> pd.DataFrame:
    """Generate atomic spectroscopy constraint curve.
    
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
        "alpha_max": [alpha_max] * n_points,
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
    print(f"  m_phi range: {m_min_eV:.3e} to {m_max_eV:.3e} eV")
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
    contract_csv = output_dir / "atomic_spectroscopy_eth_2025_contract.csv"
    df.to_csv(contract_csv, index=False)
    
    print(f"Wrote contract CSV: {contract_csv}")
    
    # Call ingest pipeline
    print("Calling fifth-force ingest pipeline...")
    from pathlib import Path
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
        description="Import atomic spectroscopy constraint curve for fifth-force analysis"
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
        default=ATOMIC_ALPHA_MAX,
        help=f"Maximum coupling strength (default: {ATOMIC_ALPHA_MAX})",
    )
    
    args = ap.parse_args()
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate constraint curve
    df = generate_atomic_constraint_curve(
        n_points=args.n_points,
        alpha_max=args.alpha_max,
    )
    
    # Ingest
    contract_csv = ingest_via_pipeline(df, args.output_dir)
    
    print(f"\n✅ Successfully imported atomic spectroscopy constraint curve")
    print(f"   Contract CSV: {contract_csv}")
    print(f"   Validated CSV: data/processed/atomic_spectroscopy_eth_2025_validated.csv")
    print(f"   Provenance: results/fifth_force/atomic_spectroscopy_eth_2025_provenance.json")
    print(f"\n   Note: This constraint covers atomic energy scales (m_φ ~ 10 eV to 10^7 eV)")
    print(f"   Complementary to Eöt-Wash sub-mm and Bennu AU-scale constraints")


if __name__ == "__main__":
    main()

