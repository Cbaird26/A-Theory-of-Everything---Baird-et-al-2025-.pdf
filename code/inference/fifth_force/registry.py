"""Discover and list available fifth-force constraint curves."""

from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd


def is_real_curve(curve_info: Dict[str, any]) -> bool:
    """Check if a curve is real experimental data (not synthetic/placeholder).
    
    Args:
        curve_info: Curve metadata dictionary with 'source_id' key
    
    Returns:
        True if real experimental curve, False if synthetic/placeholder
    
    Note:
        Real curves are identified by absence of synthetic/placeholder indicators.
        Common real curve source_id patterns include:
        - zenodo5080965 (machine-readable data)
        - eotwash_prl2016_digitized (digitized experimental data)
        - kapner_prl2007_digitized (digitized experimental data)
        - lee_arxiv2020_digitized (digitized experimental data)
        - bennu_osiris_rex (experimental constraint)
    """
    source_id = curve_info.get("source_id", "").lower()
    path_str = str(curve_info.get("path", "")).lower()
    
    # Real curves typically have: zenodo, prl, digitized, eotwash (without synthetic/placeholder)
    # Synthetic curves have: synthetic, placeholder
    synthetic_indicators = ["synthetic", "placeholder"]
    
    for indicator in synthetic_indicators:
        if indicator in source_id or indicator in path_str:
            return False
    
    # If it doesn't have synthetic indicators, treat as real
    # This correctly identifies kapner_prl2007_digitized and lee_arxiv2020_digitized as real curves
    return True


def list_curves(
    processed_dir: Optional[Path] = None,
    real_only: bool = False,
) -> List[Dict[str, any]]:
    """Discover all processed fifth-force constraint curves.

    Args:
        processed_dir: Directory to search (default: data/processed)

    Returns:
        List of curve metadata dictionaries with keys:
            - source_id: identifier
            - path: Path to validated CSV
            - lambda_min: minimum lambda_m in curve
            - lambda_max: maximum lambda_m in curve
            - row_count: number of constraint points
    """
    if processed_dir is None:
        processed_dir = Path("data/processed")
    
    if not processed_dir.exists():
        return []
    
    curves = []
    
    # Find all validated CSV files
    for csv_path in processed_dir.glob("*_validated.csv"):
        try:
            df = pd.read_csv(csv_path)
            
            # Check if it has the required columns
            required = ["lambda_m", "alpha_max", "source_id"]
            if not all(col in df.columns for col in required):
                continue
            
            # Get source_id (should be consistent across rows)
            source_ids = df["source_id"].unique()
            if len(source_ids) != 1:
                continue  # Skip if mixed sources
            
            source_id = source_ids[0]
            
            curve_info = {
                "source_id": source_id,
                "path": csv_path,
                "lambda_min": float(df["lambda_m"].min()),
                "lambda_max": float(df["lambda_m"].max()),
                "row_count": len(df),
            }
            
            # Filter by real_only if requested
            if real_only and not is_real_curve(curve_info):
                continue
            
            curves.append(curve_info)
        except Exception:
            # Skip files that can't be read
            continue
    
    return curves

