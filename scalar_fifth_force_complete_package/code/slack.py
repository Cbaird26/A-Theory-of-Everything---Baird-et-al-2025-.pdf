"""Compute fifth-force constraint slack and normalized slack."""

import pandas as pd
from typing import Dict
from .constraints import max_alpha_allowed


def fifth_force_slack(
    alpha_pred: float,
    lambda_m: float,
    curve: pd.DataFrame,
) -> Dict[str, float]:
    """Compute fifth-force slack and normalized slack.

    Args:
        alpha_pred: Predicted fifth-force strength
        lambda_m: Range in meters
        curve: Constraint curve DataFrame

    Returns:
        Dictionary with:
            - alpha_max: maximum allowed alpha at this lambda
            - slack: alpha_max - alpha_pred
            - bound: alpha_max (for normalization)
            - normalized_slack: slack / bound (or 0 if bound <= 0)
            - is_allowed: True if normalized_slack >= 0
    """
    alpha_max = max_alpha_allowed(lambda_m, curve)
    
    slack = alpha_max - alpha_pred
    bound = alpha_max
    
    # Normalized slack (defensive against alpha_max <= 0)
    if bound > 0:
        normalized_slack = slack / bound
    else:
        normalized_slack = float('inf') if slack > 0 else float('-inf')
    
    is_allowed = normalized_slack >= 0
    
    return {
        "alpha_max": float(alpha_max),
        "slack": float(slack),
        "bound": float(bound),
        "normalized_slack": float(normalized_slack),
        "is_allowed": bool(is_allowed),
    }

