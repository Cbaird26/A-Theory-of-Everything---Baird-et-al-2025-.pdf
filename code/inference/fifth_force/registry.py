"""Discover and list available fifth-force constraint curves."""

from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd


def list_curves(processed_dir: Optional[Path] = None) -> List[Dict[str, any]]:
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
            
            curves.append({
                "source_id": source_id,
                "path": csv_path,
                "lambda_min": float(df["lambda_m"].min()),
                "lambda_max": float(df["lambda_m"].max()),
                "row_count": len(df),
            })
        except Exception:
            # Skip files that can't be read
            continue
    
    return curves

