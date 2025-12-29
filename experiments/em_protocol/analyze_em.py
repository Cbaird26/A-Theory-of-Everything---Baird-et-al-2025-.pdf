#!/usr/bin/env python3
"""
Analyze EM modulation data: protocol-locked EM noise test.

Handles:
  - SDR spectral power data
  - Magnetometer time-series
  - Audio interface + coil pickup data

Fits modulation model: Power(t) = alpha + beta*s(t) + drift(t) + noise
"""
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import expit


def load_em_data(path: Path) -> pd.DataFrame:
    """
    Load EM data from CSV.
    Expected columns: t (time), power/magnitude/amplitude (signal), s (modulation), block_id (optional)
    """
    df = pd.read_csv(path)
    
    # Normalize column names
    colmap = {c.lower(): c for c in df.columns}
    
    # Find time column
    t_candidates = ["t", "time", "timestamp", "seconds"]
    t_col = next((colmap[c] for c in t_candidates if c in colmap), None)
    if t_col is None:
        raise ValueError(f"No time column found. Available: {df.columns.tolist()}")
    
    # Find signal column (power, magnitude, amplitude)
    signal_candidates = ["power", "magnitude", "amplitude", "signal", "value"]
    signal_col = next((colmap[c] for c in signal_candidates if c in colmap), None)
    if signal_col is None:
        raise ValueError(f"No signal column found. Available: {df.columns.tolist()}")
    
    # Find modulation column
    s_candidates = ["s", "mod", "signal", "condition", "modulation"]
    s_col = next((colmap[c] for c in s_candidates if c in colmap), None)
    if s_col is None:
        raise ValueError(f"No modulation column found. Available: {df.columns.tolist()}")
    
    out = pd.DataFrame()
    out["t"] = pd.to_numeric(df[t_col], errors="coerce")
    out["power"] = pd.to_numeric(df[signal_col], errors="coerce")
    out["s"] = pd.to_numeric(df[s_col], errors="coerce").astype(int)
    
    # Optional block_id
    block_candidates = ["block_id", "block", "block_idx"]
    block_col = next((colmap[c] for c in block_candidates if c in colmap), None)
    if block_col is not None:
        out["block_id"] = pd.to_numeric(df[block_col], errors="coerce").astype(int)
    
    # Drop NaN rows
    out = out.dropna(subset=["t", "power", "s"]).reset_index(drop=True)
    
    return out


def fit_modulation_with_drift(df: pd.DataFrame, drift_order: int = 1) -> Dict:
    """
    Fit: Power(t) = alpha + beta*s(t) + drift(t) + noise
    
    Args:
        df: DataFrame with columns t, power, s
        drift_order: Order of polynomial drift (0=constant, 1=linear, 2=quadratic)
    
    Returns:
        Dict with fit parameters, standard errors, and statistics
    """
    t = df["t"].to_numpy()
    power = df["power"].to_numpy()
    s = df["s"].to_numpy()
    
    # Standardize time to avoid numerical issues
    t_mean = np.mean(t)
    t_std = np.std(t) + 1e-12
    t_norm = (t - t_mean) / t_std
    
    # Build design matrix
    # Columns: [1, s, t_norm, t_norm^2, ...]
    n = len(t)
    X = np.ones((n, 2 + drift_order))
    X[:, 0] = 1  # Intercept
    X[:, 1] = s  # Modulation signal
    
    # Add drift terms
    for i in range(drift_order):
        X[:, 2 + i] = t_norm ** (i + 1)
    
    # Fit using least squares
    try:
        coeffs, residuals, rank, s_vals = np.linalg.lstsq(X, power, rcond=None)
        y_pred = X @ coeffs
        residuals_vec = power - y_pred
        
        # Compute standard errors (assuming homoscedastic errors)
        mse = np.sum(residuals_vec ** 2) / (n - len(coeffs))
        cov_matrix = mse * np.linalg.pinv(X.T @ X)
        std_errors = np.sqrt(np.diag(cov_matrix))
        
        # Extract coefficients
        alpha = float(coeffs[0])
        beta = float(coeffs[1])
        alpha_std = float(std_errors[0])
        beta_std = float(std_errors[1])
        
        # Compute t-statistic and p-value for beta
        t_stat = beta / beta_std if beta_std > 0 else 0.0
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - len(coeffs)))
        
        # 95% confidence interval for beta
        t_crit = stats.t.ppf(0.975, df=n - len(coeffs))
        beta_lower = beta - t_crit * beta_std
        beta_upper = beta + t_crit * beta_std
        
        # R-squared
        ss_res = np.sum(residuals_vec ** 2)
        ss_tot = np.sum((power - np.mean(power)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        
        return {
            "alpha": alpha,
            "alpha_std": alpha_std,
            "beta": beta,
            "beta_std": beta_std,
            "beta_lower_95": beta_lower,
            "beta_upper_95": beta_upper,
            "t_stat": float(t_stat),
            "p_value": float(p_value),
            "r_squared": float(r_squared),
            "n": n,
            "drift_order": drift_order,
        }
    except np.linalg.LinAlgError as e:
        return {
            "error": str(e),
            "n": n,
        }


def permutation_test(df: pd.DataFrame, n_permutations: int = 1000, drift_order: int = 1) -> Dict:
    """
    Permutation test: randomly shuffle s(t) and recompute beta.
    Returns p-value for beta under null hypothesis.
    """
    # Get observed beta
    observed_fit = fit_modulation_with_drift(df, drift_order=drift_order)
    if "error" in observed_fit:
        return {"error": observed_fit["error"]}
    
    observed_beta = observed_fit["beta"]
    
    # Permute s and recompute beta
    permuted_betas = []
    for _ in range(n_permutations):
        df_perm = df.copy()
        df_perm["s"] = np.random.permutation(df_perm["s"].values)
        perm_fit = fit_modulation_with_drift(df_perm, drift_order=drift_order)
        if "error" not in perm_fit:
            permuted_betas.append(perm_fit["beta"])
    
    if len(permuted_betas) == 0:
        return {"error": "All permutations failed"}
    
    permuted_betas = np.array(permuted_betas)
    
    # Two-tailed p-value
    p_value_perm = np.mean(np.abs(permuted_betas) >= np.abs(observed_beta))
    
    return {
        "observed_beta": float(observed_beta),
        "permutation_p_value": float(p_value_perm),
        "n_permutations": n_permutations,
        "permuted_beta_mean": float(np.mean(permuted_betas)),
        "permuted_beta_std": float(np.std(permuted_betas)),
    }


def block_size_stability(df: pd.DataFrame, block_sizes: List[int] = [30, 60, 120]) -> Dict:
    """
    Test stability of beta across different block sizes.
    """
    results = {}
    
    for block_size in block_sizes:
        # Resample data with new block size
        # Simple approach: aggregate by time windows
        df_copy = df.copy()
        df_copy["block_new"] = (df_copy["t"] // block_size).astype(int)
        
        # Aggregate: take mean power and mode of s per block
        agg = df_copy.groupby("block_new").agg({
            "power": "mean",
            "s": lambda x: int(np.round(x.mode()[0])) if len(x.mode()) > 0 else 0,
            "t": "mean"
        }).reset_index()
        
        if len(agg) < 4:  # Need at least a few blocks
            continue
        
        fit = fit_modulation_with_drift(agg, drift_order=1)
        if "error" not in fit:
            results[f"block_size_{block_size}s"] = {
                "beta": fit["beta"],
                "beta_std": fit["beta_std"],
                "n_blocks": len(agg),
            }
    
    return results


def main():
    ap = argparse.ArgumentParser(description="Analyze EM modulation data")
    ap.add_argument("--data", type=str, required=True, help="Path to EM data CSV")
    ap.add_argument("--out-dir", type=str, default="results", help="Output directory")
    ap.add_argument("--drift-order", type=int, default=1, help="Polynomial drift order (0=const, 1=linear, 2=quad)")
    ap.add_argument("--n-permutations", type=int, default=1000, help="Number of permutations for permutation test")
    args = ap.parse_args()
    
    data_path = Path(args.data)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print(f"Loading: {data_path}")
    df = load_em_data(data_path)
    print(f"Loaded {len(df)} data points")
    
    # Fit modulation model
    print("\nFitting modulation model...")
    fit = fit_modulation_with_drift(df, drift_order=args.drift_order)
    
    if "error" in fit:
        print(f"Error: {fit['error']}")
        return 1
    
    print(f"  α (baseline) = {fit['alpha']:.6e} ± {fit['alpha_std']:.6e}")
    print(f"  β (modulation) = {fit['beta']:.6e} ± {fit['beta_std']:.6e}")
    print(f"  95% CI: [{fit['beta_lower_95']:.6e}, {fit['beta_upper_95']:.6e}]")
    print(f"  t-stat = {fit['t_stat']:.3f}, p-value = {fit['p_value']:.6e}")
    print(f"  R² = {fit['r_squared']:.6f}")
    
    # Permutation test
    print("\nRunning permutation test...")
    perm_result = permutation_test(df, n_permutations=args.n_permutations, drift_order=args.drift_order)
    if "error" not in perm_result:
        print(f"  Permutation p-value = {perm_result['permutation_p_value']:.6e}")
        fit.update(perm_result)
    
    # Block size stability
    print("\nTesting block size stability...")
    stability = block_size_stability(df)
    fit["block_stability"] = stability
    for key, val in stability.items():
        print(f"  {key}: β = {val['beta']:.6e} ± {val['beta_std']:.6e} (n={val['n_blocks']} blocks)")
    
    # Save results
    json_path = out_dir / "em_modulation_summary.json"
    json_path.write_text(json.dumps(fit, indent=2), encoding="utf-8")
    print(f"\n✓ Saved: {json_path}")
    
    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Time series
    ax1 = axes[0]
    ax1.plot(df["t"], df["power"], "b-", alpha=0.5, label="Power")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Power")
    ax1.set_title(f"EM Signal Time Series (β = {fit['beta']:.6e} ± {fit['beta_std']:.6e})")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Modulation overlay
    ax2 = axes[1]
    neutral_mask = df["s"] == 0
    coherence_mask = df["s"] == 1
    ax2.scatter(df.loc[neutral_mask, "t"], df.loc[neutral_mask, "power"], 
                c="gray", alpha=0.3, label="Neutral (s=0)", s=1)
    ax2.scatter(df.loc[coherence_mask, "t"], df.loc[coherence_mask, "power"], 
                c="red", alpha=0.3, label="Coherence (s=1)", s=1)
    
    # Add fitted line
    t_pred = np.linspace(df["t"].min(), df["t"].max(), 1000)
    t_mean = np.mean(df["t"])
    t_std = np.std(df["t"]) + 1e-12
    t_norm_pred = (t_pred - t_mean) / t_std
    
    # Predict for s=0 and s=1
    X0 = np.column_stack([np.ones(len(t_pred)), np.zeros(len(t_pred)), t_norm_pred])
    X1 = np.column_stack([np.ones(len(t_pred)), np.ones(len(t_pred)), t_norm_pred])
    y0 = X0 @ np.array([fit["alpha"], fit["beta"], fit.get("drift_coeff", 0)])
    y1 = X1 @ np.array([fit["alpha"], fit["beta"], fit.get("drift_coeff", 0)])
    
    ax2.plot(t_pred, y0, "g--", linewidth=2, label=f"Fit (s=0)")
    ax2.plot(t_pred, y1, "r--", linewidth=2, label=f"Fit (s=1)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Power")
    ax2.set_title("Modulation Fit")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = out_dir / "em_modulation_plot.png"
    plt.savefig(plot_path, dpi=200, bbox_inches="tight")
    print(f"✓ Saved: {plot_path}")
    plt.close()
    
    print("\nDone.")
    return 0


if __name__ == "__main__":
    exit(main())

