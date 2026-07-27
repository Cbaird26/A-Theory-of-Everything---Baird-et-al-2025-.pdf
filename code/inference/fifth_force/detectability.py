#!/usr/bin/env python3
"""Compute detectability map: r = alpha_pred / alpha_max for model points."""

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
import math

try:
    from .yukawa import model_point_to_alpha_lambda
    from .envelope import alpha_max_envelope, list_curves
    from .constraints import is_excluded
    from .registry import is_real_curve
except ImportError:
    # Handle case when run as script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
    from code.inference.fifth_force.yukawa import model_point_to_alpha_lambda
    from code.inference.fifth_force.envelope import alpha_max_envelope, list_curves
    from code.inference.fifth_force.constraints import is_excluded
    from code.inference.fifth_force.registry import is_real_curve

# Constants for frequency conversions (CODATA 2018)
C_LIGHT = 299792458.0  # Speed of light (m/s)
H_PLANCK = 6.62607015e-34  # Planck constant (J·s)
E_CHARGE = 1.602176634e-19  # Elementary charge (C)


def lambda_to_freq_eq(lambda_m: float) -> float:
    """Convert Yukawa range to equivalent frequency: f_eq ≈ c/(2πλ).
    
    Args:
        lambda_m: Interaction range in meters
        
    Returns:
        Equivalent frequency in Hz
    """
    if lambda_m <= 0:
        return np.nan
    return C_LIGHT / (2 * math.pi * lambda_m)


def freq_to_energy_eV(freq_hz: float) -> float:
    """Convert frequency to energy in eV: E = hf/e.
    
    Args:
        freq_hz: Frequency in Hz
        
    Returns:
        Energy in eV
    """
    return (H_PLANCK * freq_hz) / E_CHARGE


def sample_model_points(
    n_points: int = 1000,
    m_phi_min: float = 1e-16,
    m_phi_max: float = 1e-10,
    theta_min: float = 1e-22,
    theta_max: float = 1e-18,
    mu_sb_min: float = 1e-3,
    mu_sb_max: float = 1.0,
    seed: int = 42,
    target_lambda_ranges: Optional[List[Tuple[float, float]]] = None,
) -> List[Dict[str, float]]:
    """Sample model points uniformly in log space.
    
    Args:
        n_points: Number of points to sample
        m_phi_min, m_phi_max: Scalar mass range (GeV)
        theta_min, theta_max: Mixing angle range
        mu_sb_min, mu_sb_max: Scale-breaking mass range (as ratio mu_sb/m_h)
        seed: Random seed for reproducibility
        target_lambda_ranges: Optional list of (lambda_min, lambda_max) tuples in meters.
            If provided, points will be sampled such that lambda_m falls within these ranges.
            Requires additional computation: lambda_m = hbar*c / (m_phi * c^2) = hbar*c / (m_phi * GeV_to_eV * eV_to_kg * c^2)
            Simplified: m_phi_eV = m_phi_GeV * 1e9, lambda_m ≈ 1.973e-16 / m_phi_GeV
    
    Returns:
        List of model point dictionaries
    """
    rng = np.random.RandomState(seed)
    
    # CODATA: hbar*c in GeV*m
    HBAR_C_GEV_M = 1.973269804e-16
    
    points = []
    attempts = 0
    max_attempts = n_points * 10  # Safety limit
    
    while len(points) < n_points and attempts < max_attempts:
        attempts += 1
        
        # Log-uniform sampling
        log_m_phi = rng.uniform(np.log10(m_phi_min), np.log10(m_phi_max))
        log_theta = rng.uniform(np.log10(theta_min), np.log10(theta_max))
        log_mu_sb = rng.uniform(np.log10(mu_sb_min), np.log10(mu_sb_max))
        
        m_phi_GeV = 10.0 ** log_m_phi
        
        # If target_lambda_ranges specified, filter by lambda_m
        if target_lambda_ranges:
            # Compute lambda_m from m_phi
            lambda_m = HBAR_C_GEV_M / m_phi_GeV
            
            # Check if lambda_m is in any target range
            in_range = False
            for lam_min, lam_max in target_lambda_ranges:
                if lam_min <= lambda_m <= lam_max:
                    in_range = True
                    break
            
            if not in_range:
                continue  # Skip this point
        
        points.append({
            "m_phi_GeV": m_phi_GeV,
            "theta": 10.0 ** log_theta,
            "mu_sb_over_m_h": 10.0 ** log_mu_sb,
        })
    
    if len(points) < n_points:
        print(f"Warning: Only sampled {len(points)}/{n_points} points within target lambda ranges after {attempts} attempts")
    
    return points


def compute_coverage_report(
    lambda_samples: np.ndarray,
    curves: List[Dict],
) -> Dict[str, any]:
    """Compute coverage report for sampled points across real curves.
    
    Args:
        lambda_samples: Array of sampled lambda values (in meters)
        curves: List of curve metadata dictionaries (should already be filtered to real if real_only mode)
    
    Returns:
        Dictionary with coverage statistics for each real curve:
        {
            "real_curves": [
                {
                    "source_id": str,
                    "lambda_min": float,
                    "lambda_max": float,
                    "fraction_covered": float,
                    "count_covered": int,
                    "count_total": int
                },
                ...
            ],
            "total_points": int,
            "total_covered_by_any": int,
            "fraction_covered_by_any": float,
            "total_covered_by_all": int,  # Points covered by intersection of all curves
            "fraction_covered_by_all": float,
            "total_uncovered": int,  # Points outside all real curve supports
            "fraction_uncovered": float
        }
    """
    # Filter to real curves only (if not already filtered)
    # If curves were obtained with real_only=True, all are real
    # But check anyway to be safe
    real_curves = [c for c in curves]
    
    coverage_data = []
    total = len(lambda_samples)
    
    for curve_info in real_curves:
        lambda_min = curve_info["lambda_min"]
        lambda_max = curve_info["lambda_max"]
        source_id = curve_info["source_id"]
        
        # Count points within this curve's λ range
        in_range = (lambda_samples >= lambda_min) & (lambda_samples <= lambda_max)
        count_covered = int(in_range.sum())
        fraction_covered = count_covered / total if total > 0 else 0.0
        
        coverage_data.append({
            "source_id": source_id,
            "lambda_min": lambda_min,
            "lambda_max": lambda_max,
            "fraction_covered": fraction_covered,
            "count_covered": count_covered,
            "count_total": total,
        })
    
    # Count points covered by any real curve
    if real_curves:
        covered_by_any = np.zeros(total, dtype=bool)
        covered_by_all = np.ones(total, dtype=bool)  # Start with all True for intersection
        
        for curve_info in real_curves:
            lambda_min = curve_info["lambda_min"]
            lambda_max = curve_info["lambda_max"]
            in_range = (lambda_samples >= lambda_min) & (lambda_samples <= lambda_max)
            covered_by_any |= in_range
            covered_by_all &= in_range  # Intersection: must be in ALL curves
        
        total_covered_by_any = int(covered_by_any.sum())
        fraction_covered_by_any = total_covered_by_any / total if total > 0 else 0.0
        
        total_covered_by_all = int(covered_by_all.sum())
        fraction_covered_by_all = total_covered_by_all / total if total > 0 else 0.0
        
        # Uncovered: points outside all real curve supports
        total_uncovered = total - total_covered_by_any
        fraction_uncovered = total_uncovered / total if total > 0 else 0.0
    else:
        total_covered_by_any = 0
        fraction_covered_by_any = 0.0
        total_covered_by_all = 0
        fraction_covered_by_all = 0.0
        total_uncovered = total
        fraction_uncovered = 1.0
    
    return {
        "real_curves": coverage_data,
        "total_points": total,
        "total_covered_by_any": total_covered_by_any,
        "fraction_covered_by_any": fraction_covered_by_any,
        "total_covered_by_all": total_covered_by_all,
        "fraction_covered_by_all": fraction_covered_by_all,
        "total_uncovered": total_uncovered,
        "fraction_uncovered": fraction_uncovered,
    }


def compute_detectability(
    model_points: List[Dict[str, float]],
    curves: List[Dict] = None,
    real_only: bool = False,
    alpha_mode: str = "A",
    kappa: float = 1.0,
    s_ff: float = 1.0,
    s_lambda: float = 1.0,
) -> pd.DataFrame:
    """Compute detectability ratio r = alpha_pred / alpha_max for each point.
    
    Args:
        model_points: List of model point dictionaries
        curves: List of curve metadata (default: auto-discover)
        real_only: If True, exclude synthetic/placeholder curves (default: False)
    
    Returns:
        DataFrame with columns: m_phi_GeV, theta, mu_sb_over_m_h, 
        alpha_pred, lambda_m, alpha_max, r, f_eq_hz, E_eq_eV,
        is_excluded, tightest_source_id
    """
    if curves is None:
        from .registry import list_curves
        curves = list_curves(real_only=real_only)
    
    if not curves:
        if real_only:
            raise ValueError("No real constraint curves available. Ingest real curves first or use real_only=False.")
        else:
            raise ValueError("No constraint curves available")
    
    results = []
    
    for point in model_points:
        try:
            # Convert to format expected by model_point_to_alpha_lambda
            model_dict = {
                "m_phi": point["m_phi_GeV"],
                "theta": point["theta"],
                "mu_sb": point["mu_sb_over_m_h"] * 125.0,  # Convert ratio to GeV
            }
            
            # Compute (alpha_pred, lambda_m) with specified mapping mode
            # Use mode parameters passed to compute_detectability function
            alpha_pred, lambda_m = model_point_to_alpha_lambda(
                model_dict,
                mode=alpha_mode,
                kappa=kappa,
                s_ff=s_ff,
                s_lambda=s_lambda,
            )
            
            # Get envelope alpha_max
            try:
                alpha_max, tightest_source_id = alpha_max_envelope(lambda_m, curves, real_only=real_only)
            except ValueError:
                # Out of range - in real-only mode, don't mark as excluded
                if real_only:
                    # Skip points outside real coverage in real-only mode
                    continue
                else:
                    # Out of range - skip
                    continue
            
            # Compute detectability ratio
            r = alpha_pred / alpha_max if alpha_max > 0 else np.inf
            
            # Compute equivalent frequency and energy
            f_eq_hz = lambda_to_freq_eq(lambda_m)
            E_eq_eV = freq_to_energy_eV(f_eq_hz) if not np.isnan(f_eq_hz) else np.nan
            
            # Check if excluded
            # In real-only mode, only mark as excluded if within real curve coverage
            excluded = False
            if real_only:
                # In real-only mode, check if point is within real curve coverage
                tightest_curve_info = None
                for curve_info in curves:
                    if curve_info["source_id"] == tightest_source_id:
                        tightest_curve_info = curve_info
                        break
                
                if tightest_curve_info and is_real_curve(tightest_curve_info):
                    # Check if lambda_m is within curve coverage
                    lambda_min = tightest_curve_info["lambda_min"]
                    lambda_max = tightest_curve_info["lambda_max"]
                    if lambda_min <= lambda_m <= lambda_max:
                        # Within coverage - can mark as excluded if r > 1
                        excluded = alpha_pred > alpha_max
                    else:
                        # Outside coverage - don't mark as excluded in real-only mode
                        excluded = False
                else:
                    # Not a real curve - don't mark as excluded in real-only mode
                    excluded = False
            else:
                # Standard mode - check exclusion normally
                tightest_curve_path = None
                for curve_info in curves:
                    if curve_info["source_id"] == tightest_source_id:
                        tightest_curve_path = curve_info["path"]
                        break
                
                if tightest_curve_path:
                    from .constraints import load_constraint_curve
                    tightest_curve = load_constraint_curve(tightest_curve_path)
                    excluded = is_excluded(alpha_pred, lambda_m, tightest_curve)
                else:
                    excluded = alpha_pred > alpha_max
            
            results.append({
                "m_phi_GeV": point["m_phi_GeV"],
                "theta": point["theta"],
                "mu_sb_over_m_h": point["mu_sb_over_m_h"],
                "alpha_pred": alpha_pred,
                "lambda_m": lambda_m,
                "alpha_max": alpha_max,
                "r": r,
                "f_eq_hz": f_eq_hz,
                "E_eq_eV": E_eq_eV,
                "is_excluded": excluded,
                "tightest_source_id": tightest_source_id,
            })
        except Exception as e:
            # Skip points that fail
            continue
    
    return pd.DataFrame(results)


def write_summary(
    df: pd.DataFrame,
    output_path: Path,
    curves: List[Dict] = None,
    coverage_report: Dict[str, any] = None,
    real_only: bool = False,
    alpha_mode: str = "A",
    alpha_params: Dict[str, float] = None,
    seed: int = None,
    git_commit: str = None,
) -> None:
    """Write detectability summary markdown.
    
    Args:
        df: DataFrame with detectability results
        output_path: Path to write summary
        curves: List of curve metadata (for reporting)
    """
    if len(df) == 0:
        output_path.write_text("# Detectability Summary\n\nNo points computed.\n")
        return
    
    # Get curve info
    if curves is None:
        curves = list_curves()
    
    curve_info = "Envelope (tightest bound across all curves)"
    curve_paths = []
    if curves:
        curve_ids = [c["source_id"] for c in curves]
        curve_paths = [str(c["path"]) for c in curves]
        curve_info = f"Envelope across: {', '.join(curve_ids)}"
        if len(curve_paths) == 1:
            curve_info += f"\n\nCurve used: {curve_ids[0]} ({curve_paths[0]})"
        else:
            curve_info += f"\n\nCurves used: {len(curve_ids)} curves"
            for cid, cpath in zip(curve_ids, curve_paths):
                curve_info += f"\n  - {cid}: {cpath}"
        
        # Add constraint dominance analysis if multiple curves
        if len(curves) > 1 and len(df) > 0:
            from .envelope import get_envelope_dominance_map
            
            lambda_min = df["lambda_m"].min()
            lambda_max = df["lambda_m"].max()
            
            try:
                dominance_df = get_envelope_dominance_map(
                    (lambda_min, lambda_max),
                    n_points=50,
                    curves=curves,
                )
                
                # Count how often each constraint dominates
                dominance_counts = dominance_df["dominant_source_id"].value_counts()
                
                curve_info += f"\n\n## Constraint Dominance Analysis\n\n"
                curve_info += f"Which constraint provides the tightest bound across the sampled λ range:\n\n"
                for source_id, count in dominance_counts.items():
                    fraction = count / len(dominance_df) * 100
                    curve_info += f"- **{source_id}**: {fraction:.1f}% of λ range ({count}/{len(dominance_df)} points)\n"
            except Exception as e:
                # Skip dominance analysis if it fails
                pass
    
    # Compute statistics
    total = len(df)
    r_gt_1 = (df["r"] > 1.0).sum()
    r_gt_01 = (df["r"] > 0.1).sum()
    r_gt_001 = (df["r"] > 0.01).sum()
    r_gt_0001 = (df["r"] > 0.001).sum()
    
    # Top points by r
    top_points = df.nlargest(25, "r")
    
    # Find lambda band where r is largest
    if len(df) > 0:
        max_r_idx = df["r"].idxmax()
        max_r_lambda = df.loc[max_r_idx, "lambda_m"]
        max_r_value = df.loc[max_r_idx, "r"]
        
        # Find band around max
        lambda_band_min = df["lambda_m"].quantile(0.1)
        lambda_band_max = df["lambda_m"].quantile(0.9)
        band_avg_r = df[(df["lambda_m"] >= lambda_band_min) & 
                        (df["lambda_m"] <= lambda_band_max)]["r"].mean()
        
        # Compute frequency ranges for hunt band (0.1 < r <= 1.0)
        hunt_band_df = df[(df["r"] > 0.1) & (df["r"] <= 1.0)]
        if len(hunt_band_df) > 0 and "f_eq_hz" in hunt_band_df.columns:
            hunt_f_eq_min = hunt_band_df["f_eq_hz"].min()
            hunt_f_eq_max = hunt_band_df["f_eq_hz"].max()
            hunt_lambda_min = hunt_band_df["lambda_m"].min()
            hunt_lambda_max = hunt_band_df["lambda_m"].max()
        else:
            hunt_f_eq_min = None
            hunt_f_eq_max = None
            hunt_lambda_min = None
            hunt_lambda_max = None
    else:
        max_r_lambda = None
        max_r_value = None
        lambda_band_min = None
        lambda_band_max = None
        band_avg_r = None
        hunt_f_eq_min = None
        hunt_f_eq_max = None
        hunt_lambda_min = None
        hunt_lambda_max = None
    
    # Write markdown
    lines = [
        "# Fifth-Force Detectability Summary",
        "",
        "## Run Metadata",
        "",
    ]
    
    # Add run metadata
    if seed is not None:
        lines.append(f"**Seed:** {seed}")
    if git_commit is not None:
        lines.append(f"**Git Commit:** {git_commit}")
    if real_only:
        lines.append(f"**Real-Only Mode:** Enabled (synthetic curves excluded)")
    else:
        lines.append(f"**Real-Only Mode:** Disabled (all curves included)")
    lines.append(f"**Alpha Mapping Mode:** {alpha_mode}")
    if alpha_params:
        for param, value in alpha_params.items():
            lines.append(f"**{param}:** {value}")
    lines.append("")
    
    # Add coverage report if provided
    if coverage_report and real_only:
        lines.append("## Real-Curve Coverage Report")
        lines.append("")
        lines.append("**Purpose:** Shows what fraction of sampled points fall within real experimental coverage.")
        lines.append("")
        lines.append("**Rule:** In real-only mode, points outside real curve coverage are NOT marked as 'excluded'.")
        lines.append("")
        
        if coverage_report.get("real_curves"):
            lines.append("### Coverage by Real Curve")
            lines.append("")
            lines.append("| Curve | λ_min (m) | λ_max (m) | Points Covered | Fraction |")
            lines.append("|-------|-----------|-----------|----------------|----------|")
            
            for curve_info in coverage_report["real_curves"]:
                source_id = curve_info["source_id"]
                lambda_min = curve_info["lambda_min"]
                lambda_max = curve_info["lambda_max"]
                count_covered = curve_info["count_covered"]
                fraction = curve_info["fraction_covered"]
                
                lines.append(f"| {source_id} | {lambda_min:.3e} | {lambda_max:.3e} | {count_covered}/{curve_info['count_total']} | {fraction:.2%} |")
            
            lines.append("")
        
        total_covered = coverage_report.get("total_covered_by_any", 0)
        fraction_covered = coverage_report.get("fraction_covered_by_any", 0.0)
        total_points = coverage_report.get("total_points", 0)
        total_covered_all = coverage_report.get("total_covered_by_all", 0)
        fraction_covered_all = coverage_report.get("fraction_covered_by_all", 0.0)
        total_uncovered = coverage_report.get("total_uncovered", 0)
        fraction_uncovered = coverage_report.get("fraction_uncovered", 0.0)
        
        lines.append(f"**Total Coverage:** {total_covered}/{total_points} points ({fraction_covered:.2%}) covered by at least one real curve")
        lines.append("")
        lines.append(f"**Intersection Coverage:** {total_covered_all}/{total_points} points ({fraction_covered_all:.2%}) covered by all real curves")
        lines.append("")
        
        if total_uncovered > 0:
            lines.append(f"⚠️ **Uncovered Points:** {total_uncovered}/{total_points} points ({fraction_uncovered:.2%}) outside all real curve supports")
            lines.append("   In real-only mode, these points are not marked as 'excluded' and should be interpreted cautiously.")
            lines.append("")
        else:
            lines.append(f"✅ **Uncovered Points:** 0/{total_points} (0.00%) - all points within real experimental coverage")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Add curve info
    lines.extend([
        "## Purpose",
        "",
        "This report quantifies where the scalar would be detectable if it exists by computing",
        "r = alpha_pred / alpha_max_envelope(lambda_m) for sampled model points.",
        "",
        "## Curve Used",
        "",
        f"{curve_info}",
        "",
    ])
    
    if real_only:
        lines.append("**Note:** Real-only mode enabled. Synthetic curves excluded from envelope.")
    else:
        lines.append("**Note:** Synthetic curves are for plumbing validation only; canonical detectability conclusions require real envelope curves with full provenance.")
    lines.append("")
    
    # Add statistics section
    lines.extend([
        "## Statistics",
        "",
        f"Total points computed: {total}",
        "",
        "| Threshold | Count | Fraction |",
        "|-----------|-------|----------|",
        f"| r > 1.0   | {r_gt_1:5d} | {r_gt_1/total*100:.1f}% |",
        f"| r > 0.1  | {r_gt_01:5d} | {r_gt_01/total*100:.1f}% |",
        f"| r > 0.01 | {r_gt_001:5d} | {r_gt_001/total*100:.1f}% |",
        f"| r > 0.001| {r_gt_0001:5d} | {r_gt_0001/total*100:.1f}% |",
        "",
        "## Top 25 Points by Detectability Ratio (r)",
        "",
        "These are the points closest to detection threshold:",
        "",
    ])
    
    # Add table header (include frequency columns if available)
    if "f_eq_hz" in df.columns and "E_eq_eV" in df.columns:
        lines.extend([
            "| m_phi_GeV | theta | mu_sb/m_h | alpha_pred | lambda_m (m) | f_eq (Hz) | E_eq (eV) | alpha_max | r | excluded | source |",
            "|-----------|-------|-----------|------------|--------------|-----------|-----------|-----------|---|----------|--------|",
        ])
    else:
        lines.extend([
            "| m_phi_GeV | theta | mu_sb/m_h | alpha_pred | lambda_m (m) | alpha_max | r | excluded | source |",
            "|-----------|-------|-----------|------------|--------------|-----------|---|----------|--------|",
        ])
    
    # Add top points
    for _, row in top_points.iterrows():
        if "f_eq_hz" in df.columns and "E_eq_eV" in df.columns:
            f_eq_str = f"{row['f_eq_hz']:.3e}" if not np.isnan(row['f_eq_hz']) else "N/A"
            E_eq_str = f"{row['E_eq_eV']:.3e}" if not np.isnan(row['E_eq_eV']) else "N/A"
            lines.append(
                f"| {row['m_phi_GeV']:.3e} | {row['theta']:.3e} | {row['mu_sb_over_m_h']:.3e} | "
                f"{row['alpha_pred']:.3e} | {row['lambda_m']:.3e} | {f_eq_str} | {E_eq_str} | "
                f"{row['alpha_max']:.3e} | {row['r']:.3e} | {row['is_excluded']} | {row['tightest_source_id']} |"
            )
        else:
            lines.append(
                f"| {row['m_phi_GeV']:.3e} | {row['theta']:.3e} | {row['mu_sb_over_m_h']:.3e} | "
                f"{row['alpha_pred']:.3e} | {row['lambda_m']:.3e} | {row['alpha_max']:.3e} | "
                f"{row['r']:.3e} | {row['is_excluded']} | {row['tightest_source_id']} |"
            )
    
    lines.extend([
        "",
        "## Where to Look",
        "",
    ])
    
    if max_r_lambda is not None:
        lines.extend([
            f"The highest detectability ratio is r = {max_r_value:.3e} at λ = {max_r_lambda:.3e} m.",
            "",
        ])
        
        # Add equivalent frequency if available
        if "f_eq_hz" in df.columns:
            max_r_idx = df["r"].idxmax()
            max_r_feq = df.loc[max_r_idx, "f_eq_hz"]
            max_r_Eeq = df.loc[max_r_idx, "E_eq_eV"]
            if not np.isnan(max_r_feq):
                lines.extend([
                    f"This corresponds to f_eq = {max_r_feq:.3e} Hz (equivalent frequency tag).",
                    "",
                ])
        
        lines.extend([
            f"Across the central 80% of the λ range ({lambda_band_min:.3e} to {lambda_band_max:.3e} m),",
            f"the average detectability ratio is r = {band_avg_r:.3e}.",
            "",
        ])
        
        # Add hunt band section if available
        if hunt_f_eq_min is not None and not np.isnan(hunt_f_eq_min):
            lines.extend([
                "## Hunt Band (Near-Detectable Range)",
                "",
                f"The hunt band (0.1 < r ≤ 1.0) spans:",
                f"- λ range: {hunt_lambda_min:.3e} to {hunt_lambda_max:.3e} m",
                f"- f_eq range: {hunt_f_eq_min:.3e} to {hunt_f_eq_max:.3e} Hz",
                f"- This corresponds to a **tens-of-GHz → low-THz equivalent scale** (translation tag, not literal oscillation).",
                "",
            ])
        
        lines.extend([
            "**Interpretation:**",
            "- r ≪ 1: scalar is well below current experimental sensitivity",
            "- r ≈ 0.1–1: scalar is in the detectable range; near-future experiments could see it",
            "- r > 1: scalar is excluded by current constraints",
            "",
            "**Frequency Translation:**",
            "The equivalent frequency f_eq = c/(2πλ) provides a translation layer to map",
            "fifth-force ranges onto a universal Hz axis, enabling comparison with other",
            "MQGT-SCF constraint channels (cosmology ~10⁻¹⁸ Hz, QRNG ~Hz–GHz, Higgs ~10²⁵ Hz).",
            "This is a unit-conversion tool, not evidence by itself.",
        ])
    else:
        lines.append("No points computed.")
    
    output_path.write_text("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(
        description="Compute fifth-force detectability map"
    )
    ap.add_argument(
        "--n-points",
        type=int,
        default=1000,
        help="Number of model points to sample (default: 1000)",
    )
    ap.add_argument(
        "--m-phi-min",
        type=float,
        default=1e-16,
        help="Minimum m_phi in GeV (default: 1e-16)",
    )
    ap.add_argument(
        "--m-phi-max",
        type=float,
        default=1e-10,
        help="Maximum m_phi in GeV (default: 1e-10)",
    )
    ap.add_argument(
        "--theta-min",
        type=float,
        default=1e-22,
        help="Minimum theta (default: 1e-22)",
    )
    ap.add_argument(
        "--theta-max",
        type=float,
        default=1e-18,
        help="Maximum theta (default: 1e-18)",
    )
    ap.add_argument(
        "--mu-sb-min",
        type=float,
        default=1e-3,
        help="Minimum mu_sb/m_h ratio (default: 1e-3)",
    )
    ap.add_argument(
        "--mu-sb-max",
        type=float,
        default=1.0,
        help="Maximum mu_sb/m_h ratio (default: 1.0)",
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)",
    )
    ap.add_argument(
        "--real-only",
        action="store_true",
        help="Exclude synthetic/placeholder curves, use only real experimental data",
    )
    ap.add_argument(
        "--alpha-mode",
        type=str,
        default="A",
        choices=["A", "B", "C"],
        help="Alpha mapping mode: A (placeholder), B (portal-proxy), C (agnostic scaling) (default: A)",
    )
    ap.add_argument(
        "--kappa",
        type=float,
        default=1.0,
        help="Portal coupling factor kappa for mode B (default: 1.0)",
    )
    ap.add_argument(
        "--s-ff",
        type=float,
        default=1.0,
        help="Scaling factor s_ff for mode C (default: 1.0)",
    )
    ap.add_argument(
        "--s-lambda",
        type=float,
        default=1.0,
        help="Lambda scaling factor s_lambda for mode C (default: 1.0)",
    )
    ap.add_argument(
        "--target-frac",
        type=float,
        default=0.0,
        help="Fraction of samples to target in real curve lambda range (default: 0.0 = uniform sampling)",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=Path("results/fifth_force/detectability_summary.md"),
        help="Output path for summary (default: results/fifth_force/detectability_summary.md)",
    )
    
    args = ap.parse_args()
    
    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    # Get git commit hash if available
    git_commit = None
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent.parent,
        )
        if result.returncode == 0:
            git_commit = result.stdout.strip()
    except Exception:
        pass
    
    # Get curves list for coverage reporting
    from .registry import list_curves, is_real_curve
    curves = list_curves(real_only=args.real_only)
    
    # Sample points (with enhanced mixture sampling if real_only mode)
    print(f"Sampling {args.n_points} model points...")
    
    # Enhanced mixture sampling: default to 50/50 split if real_only=True and target_frac not specified
    use_mixture = args.real_only and curves
    if use_mixture:
        if args.target_frac <= 0:
            # Default to 50/50 mixture sampling when real_only=True
            target_frac = 0.5
            print(f"  Using 50/50 mixture sampling (default for real-only mode)")
        else:
            target_frac = args.target_frac
        
        # Compute lambda coverage from real curves
        # Build list of all lambda ranges from real curves
        lambda_ranges = [(c["lambda_min"], c["lambda_max"]) for c in curves]
        lambda_min_overall = min(c["lambda_min"] for c in curves)
        lambda_max_overall = max(c["lambda_max"] for c in curves)
        
        # Sample with targeted fraction in coverage range
        n_targeted = int(args.n_points * target_frac)
        n_uniform = args.n_points - n_targeted
        
        # Targeted samples: constrain lambda_m to be within real curve coverage
        points_targeted = sample_model_points(
            n_points=n_targeted,
            m_phi_min=args.m_phi_min,
            m_phi_max=args.m_phi_max,
            theta_min=args.theta_min,
            theta_max=args.theta_max,
            mu_sb_min=args.mu_sb_min,
            mu_sb_max=args.mu_sb_max,
            seed=args.seed,
            target_lambda_ranges=lambda_ranges,
        )
        
        # Uniform samples (full range, no lambda constraint)
        points_uniform = sample_model_points(
            n_points=n_uniform,
            m_phi_min=args.m_phi_min,
            m_phi_max=args.m_phi_max,
            theta_min=args.theta_min,
            theta_max=args.theta_max,
            mu_sb_min=args.mu_sb_min,
            mu_sb_max=args.mu_sb_max,
            seed=args.seed + 1000000,  # Different seed for uniform samples
            target_lambda_ranges=None,  # No constraint
        )
        
        # Combine points
        points = points_targeted + points_uniform
        print(f"  - {len(points_targeted)} targeted in real curve λ ranges (union: [{lambda_min_overall:.3e}, {lambda_max_overall:.3e}] m)")
        print(f"  - {len(points_uniform)} uniform across full prior range")
    else:
        # Standard uniform sampling
        points = sample_model_points(
            n_points=args.n_points,
            m_phi_min=args.m_phi_min,
            m_phi_max=args.m_phi_max,
            theta_min=args.theta_min,
            theta_max=args.theta_max,
            mu_sb_min=args.mu_sb_min,
            mu_sb_max=args.mu_sb_max,
            seed=args.seed,
        )
    
    # Compute detectability
    print("Computing detectability ratios...")
    if args.real_only:
        print(f"  - Real-only mode: excluding synthetic/placeholder curves")
    print(f"  - Alpha mapping mode: {args.alpha_mode}")
    if args.alpha_mode == "B":
        print(f"    - kappa: {args.kappa}")
    elif args.alpha_mode == "C":
        print(f"    - s_ff: {args.s_ff}, s_lambda: {args.s_lambda}")
    
    df = compute_detectability(
        points,
        curves=curves,
        real_only=args.real_only,
        alpha_mode=args.alpha_mode,
        kappa=args.kappa,
        s_ff=args.s_ff,
        s_lambda=args.s_lambda,
    )
    
    print(f"Computed detectability for {len(df)} points")
    
    # Compute coverage report if real-only mode
    coverage_report = None
    if args.real_only and len(df) > 0:
        print("Computing coverage report...")
        lambda_samples = df["lambda_m"].values
        coverage_report = compute_coverage_report(lambda_samples, curves)
        print(f"  - {coverage_report['total_covered_by_any']}/{coverage_report['total_points']} points ({coverage_report['fraction_covered_by_any']:.2%}) covered by real curves")
    
    # Prepare alpha params for metadata
    alpha_params = {}
    if args.alpha_mode == "B":
        alpha_params["kappa"] = args.kappa
    elif args.alpha_mode == "C":
        alpha_params["s_ff"] = args.s_ff
        alpha_params["s_lambda"] = args.s_lambda
    
    # Write summary
    print(f"Writing summary to {args.output}...")
    write_summary(
        df,
        args.output,
        curves=curves,
        coverage_report=coverage_report,
        real_only=args.real_only,
        alpha_mode=args.alpha_mode,
        alpha_params=alpha_params,
        seed=args.seed,
        git_commit=git_commit,
    )
    
    # Also write run metadata JSON
    import json
    run_metadata_path = args.output.parent / "detectability_run.json"
    run_metadata = {
        "seed": args.seed,
        "n_points": args.n_points,
        "real_only": args.real_only,
        "alpha_mode": args.alpha_mode,
        "alpha_params": alpha_params,
        "target_frac": args.target_frac,
        "git_commit": git_commit,
        "curves_used": [c["source_id"] for c in curves] if curves else [],
    }
    if git_commit:
        run_metadata["git_commit"] = git_commit
    run_metadata_path.write_text(json.dumps(run_metadata, indent=2))
    print(f"  - Run metadata: {run_metadata_path}")
    
    print("Done.")


if __name__ == "__main__":
    main()

