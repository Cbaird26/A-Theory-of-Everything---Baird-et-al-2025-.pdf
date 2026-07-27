#!/usr/bin/env python3
"""Import fifth-force constraint curve from Zenodo 5080965 (Heacock & Huber).

Downloads Data.zip, extracts Fig3.xls, parses it, and ingests via the standard pipeline.
"""

import argparse
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

# Zenodo record 5080965
ZENODO_RECORD_ID = "5080965"
ZENODO_DOI = "10.5281/zenodo.5080965"
ZENODO_BASE_URL = "https://zenodo.org/api/records"

# Expected file structure in Data.zip
FIG3_PATHS_TO_TRY = [
    "ScienceData/Fig3/Fig3.xls",  # Actual structure
    "Fig3/Fig3.xls",  # Alternative
    "Data/Fig3/Fig3.xls",
    "Fig3.xls",
]


def download_zenodo_record(record_id: str, output_dir: Path) -> Path:
    """Download Data.zip from Zenodo record.
    
    Args:
        record_id: Zenodo record ID (e.g., "5080965")
        output_dir: Directory to save the zip file
    
    Returns:
        Path to downloaded zip file
    """
    # Get record metadata
    url = f"{ZENODO_BASE_URL}/{record_id}"
    print(f"Fetching Zenodo record metadata from {url}...")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    record = response.json()
    
    # Find Data.zip file
    files = record.get("files", [])
    data_zip = None
    for file_info in files:
        if file_info.get("key") == "Data.zip" or file_info.get("filename") == "Data.zip":
            data_zip = file_info
            break
    
    if not data_zip:
        raise ValueError(f"Data.zip not found in Zenodo record {record_id}")
    
    # Download the file
    download_url = data_zip["links"]["self"]
    zip_path = output_dir / "Data.zip"
    
    print(f"Downloading Data.zip from Zenodo...")
    response = requests.get(download_url, timeout=300, stream=True)
    response.raise_for_status()
    
    with zip_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Downloaded {zip_path} ({zip_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return zip_path


def extract_fig3_xls(zip_path: Path, output_dir: Path) -> Path:
    """Extract Fig3.xls from Data.zip.
    
    Args:
        zip_path: Path to Data.zip
        output_dir: Directory to extract to
    
    Returns:
        Path to extracted Fig3.xls
    """
    print(f"Extracting Fig3.xls from {zip_path}...")
    
    with zipfile.ZipFile(zip_path, "r") as zf:
        # Try each possible path
        for path_to_try in FIG3_PATHS_TO_TRY:
            if path_to_try in zf.namelist():
                print(f"Found {path_to_try} in zip")
                zf.extract(path_to_try, output_dir)
                return output_dir / path_to_try
        
        # If none found, show available files
        available = [f for f in zf.namelist() if "Fig3" in f or "fig3" in f]
        raise ValueError(
            f"Fig3.xls not found in zip. Tried: {FIG3_PATHS_TO_TRY}\n"
            f"Files containing 'Fig3': {available[:10]}"
        )


def parse_fig3_xls(xls_path: Path) -> pd.DataFrame:
    """Parse Fig3.xls into contract CSV format.
    
    Args:
        xls_path: Path to Fig3.xls
    
    Returns:
        DataFrame with columns: lambda_m, alpha_max, source_id, ref
    """
    print(f"Parsing {xls_path}...")
    
    # Check for xlrd dependency upfront
    try:
        import xlrd
    except ImportError:
        raise ImportError(
            "xlrd is required to read .xls files.\n"
            "Install with: pip install xlrd\n"
            "Or: python -m pip install xlrd"
        )
    
    # Read Excel file
    try:
        df = pd.read_excel(xls_path, engine="xlrd")
    except Exception as e:
        raise ValueError(f"Failed to parse {xls_path}: {e}")
    
    # Identify columns (Heacock & Huber format may vary)
    # Common column names: lambda, alpha, range, coupling, etc.
    # We need to map to: lambda_m (meters), alpha_max (dimensionless)
    
    # Prefer "ThisWork" columns (likely the actual experimental constraint)
    # Fallback to other datasets if ThisWork not available
    lambda_col = None
    alpha_col = None
    
    # Check for ThisWork columns first
    thiswork_x = None
    thiswork_y = None
    for col in df.columns:
        col_lower = str(col).lower()
        if "thiswork" in col_lower or "this work" in col_lower:
            if ".x" in col_lower or col.endswith(".x"):
                thiswork_x = col
            elif ".y" in col_lower or col.endswith(".y"):
                thiswork_y = col
    
    if thiswork_x and thiswork_y:
        lambda_col = thiswork_x
        alpha_col = thiswork_y
        print(f"Using ThisWork columns: {lambda_col}, {alpha_col}")
    else:
        # Try to find lambda/range column
        for col in df.columns:
            col_lower = str(col).lower()
            if "lambda" in col_lower or "range" in col_lower:
                lambda_col = col
                break
        
        # Try to find alpha/coupling column
        for col in df.columns:
            col_lower = str(col).lower()
            if "alpha" in col_lower or "coupling" in col_lower or "strength" in col_lower:
                alpha_col = col
                break
        
        if lambda_col is None or alpha_col is None:
            # Fallback: use first two numeric columns
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            if len(numeric_cols) >= 2:
                lambda_col = numeric_cols[0]
                alpha_col = numeric_cols[1]
                print(f"Using first two numeric columns: {lambda_col}, {alpha_col}")
            else:
                raise ValueError(
                    f"Could not identify lambda and alpha columns. "
                    f"Available columns: {list(df.columns)}"
                )
    
    # Extract and convert
    result = pd.DataFrame({
        "lambda_m": pd.to_numeric(df[lambda_col], errors="coerce"),
        "alpha_max": pd.to_numeric(df[alpha_col], errors="coerce"),
        "source_id": "zenodo5080965_fig3",
        "ref": f"doi:{ZENODO_DOI}",
    })
    
    # Drop rows with NaN
    result = result.dropna()
    
    # Ensure lambda_m is in meters
    # Heacock & Huber Fig3 should cover λ ~ 10^-4 to 10^-2 m (0.1 mm to 1 cm)
    # If values are much smaller (picometers), they might need unit conversion
    # If values are much larger, they might already be in different units
    lambda_max = result["lambda_m"].max()
    lambda_min = result["lambda_m"].min()
    
    # Expected range: 10^-4 to 10^-2 m
    # If max is < 10^-6, likely need to scale up (maybe values are in wrong units)
    # If max is > 10^-1, likely need to scale down
    if lambda_max < 1e-6:
        # Values are very small - check if they should be scaled
        # If median is around 10^-11 to 10^-9, these might be picometers/nanometers
        # But Heacock & Huber should be mm-cm scale, so this might be wrong dataset
        print(f"Warning: lambda_m range ({lambda_min:.3e} to {lambda_max:.3e} m) is very small.")
        print("  Expected range for Heacock & Huber: 10^-4 to 10^-2 m (0.1 mm to 1 cm)")
        print("  Proceeding with values as-is - verify units are correct.")
    elif lambda_max > 1e-1:
        # Values are very large - might need conversion
        print(f"Warning: lambda_m range ({lambda_min:.3e} to {lambda_max:.3e} m) is very large.")
        print("  Expected range: 10^-4 to 10^-2 m. Check if units need conversion.")
    
    # Sort by lambda_m
    result = result.sort_values("lambda_m").reset_index(drop=True)
    
    # Ensure positive and monotonic
    result = result[result["lambda_m"] > 0]
    result = result[result["alpha_max"] > 0]
    
    # Remove duplicates
    result = result.drop_duplicates(subset=["lambda_m"], keep="first")
    
    print(f"Parsed {len(result)} constraint points")
    print(f"  lambda_m range: {result['lambda_m'].min():.3e} to {result['lambda_m'].max():.3e} m")
    print(f"  alpha_max range: {result['alpha_max'].min():.3e} to {result['alpha_max'].max():.3e}")
    
    return result


def ingest_via_pipeline(df: pd.DataFrame, output_dir: Path) -> Path:
    """Write contract CSV and call ingest pipeline.
    
    Args:
        df: DataFrame with contract columns
        output_dir: Directory to write contract CSV
    
    Returns:
        Path to contract CSV
    """
    contract_csv = output_dir / "zenodo5080965_fig3_contract.csv"
    df.to_csv(contract_csv, index=False)
    
    print(f"Wrote contract CSV: {contract_csv}")
    
    # Call ingest pipeline
    print("Calling fifth-force ingest pipeline...")
    import sys
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
        description="Import Zenodo 5080965 Fig3 curve for fifth-force analysis"
    )
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw/fifth_force"),
        help="Directory to save downloaded and processed files (default: data/raw/fifth_force)",
    )
    ap.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip download if Data.zip already exists",
    )
    
    args = ap.parse_args()
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Download
    zip_path = args.output_dir / "Data.zip"
    if args.skip_download and zip_path.exists():
        print(f"Using existing {zip_path}")
    else:
        zip_path = download_zenodo_record(ZENODO_RECORD_ID, args.output_dir)
    
    # Extract
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        xls_path = extract_fig3_xls(zip_path, tmp_path)
        
        # Parse
        df = parse_fig3_xls(xls_path)
        
        # Ingest
        contract_csv = ingest_via_pipeline(df, args.output_dir)
    
    print(f"\n✅ Successfully imported Zenodo 5080965 Fig3 curve")
    print(f"   Contract CSV: {contract_csv}")
    print(f"   Validated CSV: data/processed/zenodo5080965_fig3_validated.csv")
    print(f"   Provenance: results/fifth_force/zenodo5080965_fig3_provenance.json")


if __name__ == "__main__":
    main()

