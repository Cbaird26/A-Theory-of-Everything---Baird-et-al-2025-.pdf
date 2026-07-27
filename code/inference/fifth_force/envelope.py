"""Compute envelope (tightest bound) across multiple constraint curves."""

from pathlib import Path
from typing import Dict, Tuple, Optional, List
import pandas as pd
import numpy as np
from .registry import list_curves, is_real_curve
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
    real_only: bool = False,
) -> Tuple[float, Optional[str]]:
    """Get the tightest (minimum) alpha_max across all curves.

    Args:
        lambda_m: Range in meters
        curves: List of curve metadata dicts (default: auto-discover)
        real_only: If True, exclude synthetic/placeholder curves (default: False)

    Returns:
        (alpha_env, tightest_source_id) where:
            alpha_env: minimum alpha_max across curves
            tightest_source_id: source_id of the curve providing the tightest bound
    """
    if curves is None:
        from .registry import list_curves
        curves = list_curves(real_only=real_only)
    
    if not curves:
        raise ValueError("No curves available for envelope")
    
    by_curve = alpha_max_by_curve(lambda_m, curves)
    
    if not by_curve:
        raise ValueError(f"No curves cover lambda_m = {lambda_m}")
    
    # Find tightest (minimum alpha_max)
    tightest_source_id = min(by_curve, key=by_curve.get)
    alpha_env = by_curve[tightest_source_id]
    
    return alpha_env, tightest_source_id


def get_envelope_dominance_map(
    lambda_range: tuple,
    n_points: int = 100,
    curves: Optional[List[Dict]] = None,
) -> pd.DataFrame:
    """Get which constraint dominates at different lambda ranges.
    
    Args:
        lambda_range: (lambda_min, lambda_max) in meters
        n_points: Number of points to sample
        curves: List of curve metadata dicts (default: auto-discover)
    
    Returns:
        DataFrame with columns: lambda_m, dominant_source_id, alpha_max, all_contributors
    """
    if curves is None:
        curves = list_curves()
    
    if not curves:
        raise ValueError("No curves available for envelope")
    
    lambda_min, lambda_max = lambda_range
    
    # Sample lambda values uniformly in log space
    log_lambda_min = np.log10(lambda_min)
    log_lambda_max = np.log10(lambda_max)
    log_lambdas = np.linspace(log_lambda_min, log_lambda_max, n_points)
    lambdas = 10.0 ** log_lambdas
    
    results = []
    for lambda_m in lambdas:
        by_curve = alpha_max_by_curve(lambda_m, curves)
        
        if not by_curve:
            continue
        
        # Find tightest
        tightest_source_id = min(by_curve, key=by_curve.get)
        alpha_env = by_curve[tightest_source_id]
        
        # Get all contributors
        all_contributors = list(by_curve.keys())
        
        results.append({
            "lambda_m": lambda_m,
            "dominant_source_id": tightest_source_id,
            "alpha_max": alpha_env,
            "all_contributors": ",".join(sorted(all_contributors)),
        })
    
    return pd.DataFrame(results)

