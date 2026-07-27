"""Load and evaluate fifth-force constraint curves."""

import pandas as pd
from pathlib import Path
from typing import Optional
import numpy as np
from scipy.interpolate import interp1d


def load_constraint_curve(path: Path) -> pd.DataFrame:
    """Load a validated constraint curve CSV.

    Returns:
        DataFrame with columns: lambda_m, alpha_max, source_id, (optional) ref
    """
    df = pd.read_csv(path)
    required = ["lambda_m", "alpha_max", "source_id"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def max_alpha_allowed(lambda_m: float, curve: pd.DataFrame) -> float:
    """Get the maximum allowed alpha at a given lambda using interpolation.

    Args:
        lambda_m: Range in meters
        curve: DataFrame with lambda_m and alpha_max columns

    Returns:
        Maximum allowed alpha at this lambda (interpolated)
    """
    if len(curve) == 0:
        raise ValueError("Empty constraint curve")

    # Handle edge cases
    if lambda_m <= curve["lambda_m"].min():
        return curve.loc[curve["lambda_m"].idxmin(), "alpha_max"]
    if lambda_m >= curve["lambda_m"].max():
        return curve.loc[curve["lambda_m"].idxmax(), "alpha_max"]

    # Interpolate (log space often more stable for constraint curves)
    # Use linear interpolation in log-log space for better behavior
    log_lambda = np.log10(curve["lambda_m"].values)
    log_alpha = np.log10(curve["alpha_max"].values)

    # Ensure monotonicity
    if not np.all(np.diff(log_lambda) > 0):
        raise ValueError("lambda_m must be strictly increasing")

    interp = interp1d(log_lambda, log_alpha, kind="linear", fill_value="extrapolate")
    log_alpha_pred = interp(np.log10(lambda_m))
    return 10.0 ** log_alpha_pred


def is_excluded(alpha: float, lambda_m: float, curve: pd.DataFrame) -> bool:
    """Check if a point (alpha, lambda_m) is excluded by the constraint curve.

    Args:
        alpha: Fifth-force strength (dimensionless)
        lambda_m: Range in meters
        curve: Constraint curve DataFrame

    Returns:
        True if excluded (alpha > alpha_max at this lambda)
    """
    if len(curve) == 0:
        raise ValueError("Empty constraint curve")
    
    alpha_max = max_alpha_allowed(lambda_m, curve)
    return alpha > alpha_max

