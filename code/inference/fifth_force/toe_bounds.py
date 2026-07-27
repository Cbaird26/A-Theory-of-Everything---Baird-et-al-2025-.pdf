"""Convert Eöt-Wash experimental bounds to ToE parameter constraints.

This module provides functions to convert digitized α_max(λ) curves from
experimental constraints (e.g., Eöt-Wash) into bounds on ToE parameters:
- α_max(λ) → θ_max(λ) (mixing angle bounds)
- θ_max(λ) → |κ_cH v_c| bounds (portal parameter bounds)

This enables direct falsification tests: experimental constraints → ToE parameter exclusions.
"""

import pandas as pd
import numpy as np
from typing import Optional
from pathlib import Path

from .toe_mapping import (
    toe_theta_max_from_alpha_max,
    toe_kappa_vc_max_from_theta_max,
    lambda_to_mphi_GeV,
    lambda_to_mphi_eV,
    F_N_DEFAULT,
    M_HIGGS_GEV,
    V_HIGGS_GEV,
)


def compute_theta_max_curve(
    alpha_max_curve_df: pd.DataFrame,
    f_n: float = F_N_DEFAULT,
) -> pd.DataFrame:
    """Convert digitized α_max(λ) curve to θ_max(λ) mixing-angle bounds.
    
    This function takes a DataFrame with experimental α_max(λ) bounds and
    converts them to mixing-angle bounds using the ToE normalization.
    
    Args:
        alpha_max_curve_df: DataFrame with columns:
            - lambda_m: Yukawa range in meters
            - alpha_max: Maximum allowed Yukawa strength (experimental bound)
        f_n: Nucleon scalar form factor (default: 0.30)
    
    Returns:
        DataFrame with columns:
            - lambda_m: Yukawa range in meters
            - alpha_max: Original experimental bound
            - theta_max: Maximum allowed mixing angle (radians)
            - mphi_eV: Scalar mediator mass in eV
            - mphi_GeV: Scalar mediator mass in GeV
    
    Example:
        >>> import pandas as pd
        >>> curve = pd.DataFrame({
        ...     'lambda_m': [3e-5, 9.3e-4],
        ...     'alpha_max': [4.4e5, 1.2e-1]
        ... })
        >>> theta_curve = compute_theta_max_curve(curve)
        >>> print(theta_curve[['lambda_m', 'theta_max']])
    """
    # Validate input
    required_cols = ['lambda_m', 'alpha_max']
    for col in required_cols:
        if col not in alpha_max_curve_df.columns:
            raise ValueError(f"Input DataFrame must have '{col}' column")
    
    # Create output DataFrame
    result = alpha_max_curve_df.copy()
    
    # Compute theta_max for each point
    theta_max_values = []
    mphi_eV_values = []
    mphi_GeV_values = []
    
    for _, row in alpha_max_curve_df.iterrows():
        lambda_m = row['lambda_m']
        alpha_max = row['alpha_max']
        
        # Convert to mixing-angle bound
        theta_max = toe_theta_max_from_alpha_max(alpha_max, f_n=f_n)
        theta_max_values.append(theta_max)
        
        # Compute mediator mass
        mphi_eV = lambda_to_mphi_eV(lambda_m)
        mphi_GeV = lambda_to_mphi_GeV(lambda_m)
        mphi_eV_values.append(mphi_eV)
        mphi_GeV_values.append(mphi_GeV)
    
    result['theta_max'] = theta_max_values
    result['mphi_eV'] = mphi_eV_values
    result['mphi_GeV'] = mphi_GeV_values
    
    return result


def compute_kappa_vc_bounds(
    theta_max_curve_df: pd.DataFrame,
    v_GeV: float = V_HIGGS_GEV,
    m_h_GeV: float = M_HIGGS_GEV,
) -> pd.DataFrame:
    """Convert θ_max(λ) curve to |κ_cH v_c| portal parameter bounds.
    
    This function takes mixing-angle bounds and converts them to bounds on
    the ToE portal parameter combination |κ_cH v_c| using the inverted
    ToE Eq. (13).
    
    Args:
        theta_max_curve_df: DataFrame with columns:
            - lambda_m: Yukawa range in meters
            - theta_max: Maximum allowed mixing angle (radians)
            - mphi_GeV (optional): Scalar mediator mass in GeV
            If mphi_GeV is not provided, it will be computed from lambda_m
        v_GeV: Higgs vev in GeV (default: 246.0)
        m_h_GeV: Higgs mass in GeV (default: 125.0)
    
    Returns:
        DataFrame with columns:
            - lambda_m: Yukawa range in meters
            - theta_max: Maximum allowed mixing angle (radians)
            - mphi_GeV: Scalar mediator mass in GeV
            - kappa_vc_max_GeV: Maximum allowed |κ_cH v_c| in GeV
    
    Example:
        >>> theta_curve = compute_theta_max_curve(alpha_curve)
        >>> kappa_bounds = compute_kappa_vc_bounds(theta_curve)
        >>> print(kappa_bounds[['lambda_m', 'kappa_vc_max_GeV']])
    """
    # Validate input
    required_cols = ['lambda_m', 'theta_max']
    for col in required_cols:
        if col not in theta_max_curve_df.columns:
            raise ValueError(f"Input DataFrame must have '{col}' column")
    
    # Create output DataFrame
    result = theta_max_curve_df.copy()
    
    # Compute |κ_cH v_c| bounds for each point
    kappa_vc_max_values = []
    mphi_GeV_values = []
    
    for _, row in theta_max_curve_df.iterrows():
        lambda_m = row['lambda_m']
        theta_max = row['theta_max']
        
        # Get or compute m_phi
        if 'mphi_GeV' in row and pd.notna(row['mphi_GeV']):
            mphi_GeV = row['mphi_GeV']
        else:
            mphi_GeV = lambda_to_mphi_GeV(lambda_m)
        
        mphi_GeV_values.append(mphi_GeV)
        
        # Convert to portal parameter bound
        kappa_vc_max = toe_kappa_vc_max_from_theta_max(
            theta_max=theta_max,
            m_phi_GeV=mphi_GeV,
            v_GeV=v_GeV,
            m_h_GeV=m_h_GeV,
        )
        kappa_vc_max_values.append(kappa_vc_max)
    
    result['mphi_GeV'] = mphi_GeV_values
    result['kappa_vc_max_GeV'] = kappa_vc_max_values
    
    return result


def compute_full_toe_bounds(
    alpha_max_curve_df: pd.DataFrame,
    f_n: float = F_N_DEFAULT,
    v_GeV: float = V_HIGGS_GEV,
    m_h_GeV: float = M_HIGGS_GEV,
) -> pd.DataFrame:
    """Complete conversion: α_max(λ) → θ_max(λ) → |κ_cH v_c| bounds.
    
    Convenience function that performs the full conversion chain in one call.
    
    Args:
        alpha_max_curve_df: DataFrame with columns lambda_m, alpha_max
        f_n: Nucleon scalar form factor (default: 0.30)
        v_GeV: Higgs vev in GeV (default: 246.0)
        m_h_GeV: Higgs mass in GeV (default: 125.0)
    
    Returns:
        DataFrame with all intermediate and final bounds
    
    Example:
        >>> import pandas as pd
        >>> eotwash = pd.read_csv('data/raw/eotwash_prl2016_digitized.csv')
        >>> toe_bounds = compute_full_toe_bounds(eotwash)
        >>> print(toe_bounds[['lambda_m', 'alpha_max', 'theta_max', 'kappa_vc_max_GeV']])
    """
    # Step 1: α_max → θ_max
    theta_curve = compute_theta_max_curve(alpha_max_curve_df, f_n=f_n)
    
    # Step 2: θ_max → |κ_cH v_c|
    kappa_bounds = compute_kappa_vc_bounds(theta_curve, v_GeV=v_GeV, m_h_GeV=m_h_GeV)
    
    return kappa_bounds


def load_curve_from_csv(
    csv_path: Path,
    lambda_col: str = 'lambda_m',
    alpha_col: str = 'alpha_max',
) -> pd.DataFrame:
    """Load experimental constraint curve from CSV file.
    
    Args:
        csv_path: Path to CSV file
        lambda_col: Name of lambda column (default: 'lambda_m')
        alpha_col: Name of alpha_max column (default: 'alpha_max')
    
    Returns:
        DataFrame with lambda_m and alpha_max columns
    
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If required columns are missing
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Rename columns to standard names if needed
    if lambda_col != 'lambda_m' and lambda_col in df.columns:
        df = df.rename(columns={lambda_col: 'lambda_m'})
    if alpha_col != 'alpha_max' and alpha_col in df.columns:
        df = df.rename(columns={alpha_col: 'alpha_max'})
    
    # Validate
    if 'lambda_m' not in df.columns:
        raise ValueError(f"CSV must have '{lambda_col}' or 'lambda_m' column")
    if 'alpha_max' not in df.columns:
        raise ValueError(f"CSV must have '{alpha_col}' or 'alpha_max' column")
    
    return df[['lambda_m', 'alpha_max']].copy()


def save_toe_bounds_to_csv(
    toe_bounds_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save ToE parameter bounds to CSV file.
    
    Args:
        toe_bounds_df: DataFrame with ToE bounds (from compute_full_toe_bounds)
        output_path: Path to output CSV file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    toe_bounds_df.to_csv(output_path, index=False)


if __name__ == "__main__":
    """Command-line interface for converting experimental bounds to ToE parameters."""
    import argparse
    
    ap = argparse.ArgumentParser(
        description="Convert Eöt-Wash α_max(λ) bounds to ToE parameter constraints"
    )
    ap.add_argument(
        "input_csv",
        type=str,
        help="Input CSV with lambda_m and alpha_max columns"
    )
    ap.add_argument(
        "--output-csv",
        type=str,
        default=None,
        help="Output CSV path (default: input_csv with '_toe_bounds' suffix)"
    )
    ap.add_argument(
        "--f-n",
        type=float,
        default=F_N_DEFAULT,
        help=f"Nucleon scalar form factor (default: {F_N_DEFAULT})"
    )
    
    args = ap.parse_args()
    
    # Load curve
    print(f"Loading curve from: {args.input_csv}")
    curve_df = load_curve_from_csv(args.input_csv)
    print(f"  Loaded {len(curve_df)} points")
    
    # Convert to ToE bounds
    print("Converting to ToE parameter bounds...")
    toe_bounds = compute_full_toe_bounds(curve_df, f_n=args.f_n)
    print(f"  Computed bounds for {len(toe_bounds)} points")
    
    # Determine output path
    if args.output_csv is None:
        input_path = Path(args.input_csv)
        output_path = input_path.parent / f"{input_path.stem}_toe_bounds.csv"
    else:
        output_path = Path(args.output_csv)
    
    # Save
    save_toe_bounds_to_csv(toe_bounds, output_path)
    print(f"✅ Saved ToE bounds to: {output_path}")
    
    # Print summary
    print("\nSummary:")
    print(f"  λ range: {toe_bounds['lambda_m'].min():.3e} - {toe_bounds['lambda_m'].max():.3e} m")
    print(f"  θ_max range: {toe_bounds['theta_max'].min():.3e} - {toe_bounds['theta_max'].max():.3e} rad")
    print(f"  |κ_cH v_c|_max range: {toe_bounds['kappa_vc_max_GeV'].min():.3e} - {toe_bounds['kappa_vc_max_GeV'].max():.3e} GeV")
