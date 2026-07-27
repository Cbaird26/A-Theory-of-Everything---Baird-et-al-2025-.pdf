"""Compute envelope (tightest bound) across multiple constraint curves."""

from pathlib import Path
from typing import Dict, Tuple, Optional, List
import pandas as pd
import numpy as np
from .registry import list_curves
from .constraints import max_alpha_allowed


def alpha_max_by_curve(
    lambda_m: float,
    curves: List[Dict],
) -> Dict[str, float]:
    """Get alpha_max from each curve at a given lambda_m.

    Args:
        lambda_m: Range in meters
        curves: List of curve metadata dicts (from registry.list_curves)

    Returns:
        Dictionary mapping source_id to alpha_max (only curves that cover this lambda)
    """
    result = {}
    
    for curve_info in curves:
        curve_path = curve_info["path"]
        source_id = curve_info["source_id"]
        lambda_min = curve_info["lambda_min"]
        lambda_max = curve_info["lambda_max"]
        
        # Skip if out of range
        if lambda_m < lambda_min or lambda_m > lambda_max:
            continue
        
        try:
            curve_df = pd.read_csv(curve_path)
            alpha_max = max_alpha_allowed(lambda_m, curve_df)
            result[source_id] = float(alpha_max)
        except Exception:
            # Skip curves that fail to load
            continue
    
    return result


def alpha_max_envelope(
    lambda_m: float,
    curves: Optional[List[Dict]] = None,
) -> Tuple[float, Optional[str]]:
    """Get the tightest (minimum) alpha_max across all curves.

    Args:
        lambda_m: Range in meters
        curves: List of curve metadata dicts (default: auto-discover)

    Returns:
        (alpha_env, tightest_source_id) where:
            alpha_env: minimum alpha_max across curves
            tightest_source_id: source_id of the curve providing the tightest bound
    """
    if curves is None:
        curves = list_curves()
    
    if not curves:
        raise ValueError("No curves available for envelope")
    
    by_curve = alpha_max_by_curve(lambda_m, curves)
    
    if not by_curve:
        raise ValueError(f"No curves cover lambda_m = {lambda_m}")
    
    # Find tightest (minimum alpha_max)
    tightest_source_id = min(by_curve, key=by_curve.get)
    alpha_env = by_curve[tightest_source_id]
    
    return alpha_env, tightest_source_id

