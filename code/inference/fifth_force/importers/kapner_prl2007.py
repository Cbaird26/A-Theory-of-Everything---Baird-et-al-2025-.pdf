#!/usr/bin/env python3
"""Import Kapner et al. (2007) fifth-force constraint curve.

This importer validates and ingests a manually-digitized CSV file from Kapner et al. (2007).
The CSV must be placed in data/raw/fifth_force/mm_cm_constraints/ before running.

Source: Kapner et al., "Tests of the Gravitational Inverse-Square Law below the 
Dark-Energy Length Scale", Physical Review Letters 98, 021101 (2007)
arXiv: hep-ph/0611184
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from code.inference.fifth_force.ingest import ingest_fifth_force_csv

# Expected source_id
SOURCE_ID = "kapner_prl2007_digitized"

# Expected file location
EXPECTED_INPUT = project_root / "data" / "raw" / "fifth_force" / "mm_cm_constraints" / "kapner_prl2007_digitized_contract.csv"

# Expected coverage (approximate, for validation)
EXPECTED_LAMBDA_MIN = 5e-6  # ~10 μm
EXPECTED_LAMBDA_MAX = 1e-2  # ~10 mm


def validate_csv(csv_path: Path) -> pd.DataFrame:
    """Validate and load the digitized CSV file.
    
    Args:
        csv_path: Path to input CSV file
        
    Returns:
        Validated DataFrame with columns: lambda_m, alpha_max, source_id
        
    Raises:
        ValueError: If CSV is invalid or doesn't match expected format
    """
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Input CSV not found: {csv_path}\n"
            f"Please digitize Kapner 2007 Figure 6 and place the CSV at:\n"
            f"  {csv_path}\n"
            f"See docs/dev/mm_cm_constraints_digitization_guide.md for instructions."
        )
    
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Check required columns
    required = ["lambda_m", "alpha_max"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Found: {list(df.columns)}")
    
    # Add source_id if not present
    if "source_id" not in df.columns:
        df["source_id"] = SOURCE_ID
    else:
        # Verify it matches
        unique_ids = df["source_id"].unique()
        if len(unique_ids) != 1 or unique_ids[0] != SOURCE_ID:
            print(f"Warning: source_id in CSV ({unique_ids}) doesn't match expected ({SOURCE_ID})")
            print(f"  Setting source_id to {SOURCE_ID}")
            df["source_id"] = SOURCE_ID
    
    # Validate data ranges
    if (df["lambda_m"] <= 0).any():
        raise ValueError("lambda_m must be positive")
    if (df["alpha_max"] <= 0).any():
        raise ValueError("alpha_max must be positive")
    
    lambda_min = df["lambda_m"].min()
    lambda_max = df["lambda_m"].max()
    
    if lambda_min > EXPECTED_LAMBDA_MAX or lambda_max < EXPECTED_LAMBDA_MIN:
        print(f"Warning: lambda_m range ({lambda_min:.3e} to {lambda_max:.3e} m) is outside expected range")
        print(f"  Expected: {EXPECTED_LAMBDA_MIN:.3e} to {EXPECTED_LAMBDA_MAX:.3e} m")
        print(f"  Proceeding anyway - verify digitization is correct")
    
    # Sort by lambda_m
    df = df.sort_values("lambda_m").reset_index(drop=True)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=["lambda_m"], keep="first")
    
    print(f"✅ Validated CSV: {len(df)} points")
    print(f"   lambda_m range: {lambda_min:.3e} to {lambda_max:.3e} m")
    print(f"   alpha_max range: {df['alpha_max'].min():.3e} to {df['alpha_max'].max():.3e}")
    
    return df


def main():
    ap = argparse.ArgumentParser(
        description="Import Kapner et al. (2007) fifth-force constraint curve"
    )
    ap.add_argument(
        "--input-csv",
        type=Path,
        default=EXPECTED_INPUT,
        help=f"Path to digitized CSV file (default: {EXPECTED_INPUT})",
    )
    
    args = ap.parse_args()
    
    # Validate
    df = validate_csv(args.input_csv)
    
    # Write validated contract CSV
    contract_csv = project_root / "data" / "raw" / "fifth_force" / "kapner_prl2007_digitized_contract.csv"
    contract_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(contract_csv, index=False)
    print(f"✅ Contract CSV: {contract_csv}")
    
    # Ingest via pipeline
    processed_dir = project_root / "data" / "processed"
    results_dir = project_root / "results" / "fifth_force"
    processed_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    print("Calling fifth-force ingest pipeline...")
    ingest_fifth_force_csv(contract_csv, processed_dir, results_dir)
    
    print(f"\n✅ Successfully imported Kapner et al. (2007) constraint")
    print(f"   Contract CSV: {contract_csv}")
    print(f"   Validated CSV: data/processed/kapner_prl2007_digitized_contract_validated.csv")
    print(f"   Provenance: results/fifth_force/kapner_prl2007_digitized_contract_provenance.json")


if __name__ == "__main__":
    main()
