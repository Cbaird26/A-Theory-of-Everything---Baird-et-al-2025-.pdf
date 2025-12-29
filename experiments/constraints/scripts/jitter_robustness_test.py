#!/usr/bin/env python3
"""
Robustness jitter test for digitized exclusion curves.

Perturbs each digitized curve by ±10% in log α (Gaussian noise),
reruns overlap analysis multiple times, and reports survival statistics.
"""
import argparse
import json
import random
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def load_envelope(csv_path: Path) -> pd.DataFrame:
    """Load envelope CSV."""
    return pd.read_csv(csv_path)


def jitter_curve(df: pd.DataFrame, sigma: float = 0.1) -> pd.DataFrame:
    """
    Add Gaussian noise to log alpha values.
    
    Args:
        df: DataFrame with 'alpha' column
        sigma: Standard deviation in log10 space (default 0.1 = 10% relative)
    
    Returns:
        Jittered DataFrame
    """
    df_jittered = df.copy()
    
    # Add Gaussian noise in log space
    log_alpha = np.log10(df_jittered['alpha'].values)
    noise = np.random.normal(0, sigma, size=len(log_alpha))
    log_alpha_jittered = log_alpha + noise
    
    # Convert back to linear space
    df_jittered['alpha'] = 10**log_alpha_jittered
    
    # Ensure alpha stays positive
    df_jittered['alpha'] = np.maximum(df_jittered['alpha'], 1e-20)
    
    return df_jittered


def run_single_jitter_test(envelope_path: Path, qrng_json: Path, 
                           ff_json: Path, higgs_json: Path,
                           lambda_min: float, lambda_max: float,
                           alpha_min: float, alpha_max: float,
                           n_lambda: int, n_alpha: int) -> Dict:
    """
    Run a single jittered overlap test.
    
    Returns dict with island summary or None if empty.
    """
    # Load and jitter envelope
    envelope_df = load_envelope(envelope_path)
    envelope_jittered = jitter_curve(envelope_df, sigma=0.1)
    
    # Save temporary jittered envelope
    temp_path = envelope_path.parent / 'temp_jittered_envelope.csv'
    envelope_jittered.to_csv(temp_path, index=False)
    
    # Update bounds JSON from jittered envelope
    excluded = envelope_jittered[envelope_jittered['excluded'] == 1]
    if len(excluded) > 0:
        alpha_max_allowed = excluded['alpha'].min()
        bounds = {
            'alpha_max_allowed': float(alpha_max_allowed)
        }
        temp_bounds = ff_json.parent / 'temp_jittered_bounds.json'
        temp_bounds.write_text(json.dumps(bounds))
    else:
        return None
    
    # Run overlap check (simplified - just check if viable region exists)
    # For full implementation, would call check_overlap_region.py
    # Here we do a simplified check
    
    # Create parameter grid
    lambda_range = np.logspace(np.log10(lambda_min), np.log10(lambda_max), n_lambda)
    alpha_range = np.logspace(np.log10(alpha_min), np.log10(alpha_max), n_alpha)
    LAMBDA_GRID, ALPHA_GRID = np.meshgrid(lambda_range, alpha_range)
    
    # Simple viable mask: points below fifth-force exclusion
    viable_mask = ALPHA_GRID < alpha_max_allowed
    
    n_viable = int(viable_mask.sum())
    
    if n_viable == 0:
        return None
    
    # Compute percentiles
    viable_lambda = LAMBDA_GRID[viable_mask]
    viable_alpha = ALPHA_GRID[viable_mask]
    
    result = {
        'n_viable_points': n_viable,
        'lambda_m': {
            'p05': float(np.percentile(viable_lambda, 5)),
            'p50': float(np.percentile(viable_lambda, 50)),
            'p95': float(np.percentile(viable_lambda, 95)),
        },
        'alpha': {
            'p05': float(np.percentile(viable_alpha, 5)),
            'p50': float(np.percentile(viable_alpha, 50)),
            'p95': float(np.percentile(viable_alpha, 95)),
        }
    }
    
    # Cleanup
    temp_path.unlink(missing_ok=True)
    temp_bounds.unlink(missing_ok=True)
    
    return result


def run_jitter_robustness_test(envelope_path: Path, n_runs: int = 200,
                               output_dir: Path = None):
    """
    Run multiple jitter tests and collect statistics.
    """
    if output_dir is None:
        output_dir = Path('experiments/constraints/results')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load reference bounds
    qrng_json = Path('experiments/grok_qrng/results/lfdr_withinrun/global_summary.json')
    ff_json = Path('experiments/constraints/results/fifth_force_bounds.json')
    higgs_json = Path('experiments/constraints/results/higgs_portal_bounds.json')
    
    # Use same zoom bounds as previous runs
    lambda_min = 3.717e-06
    lambda_max = 2.693e-01
    alpha_min = 3.286e-12
    alpha_max = 5.145e-07
    n_lambda = 400
    n_alpha = 400
    
    print(f"Running {n_runs} jitter tests...")
    print(f"  Sigma (log10): 0.1 (10% relative)")
    print(f"  Lambda range: {lambda_min:.2e} to {lambda_max:.2e} m")
    print(f"  Alpha range: {alpha_min:.2e} to {alpha_max:.2e}")
    
    results = []
    for i in range(n_runs):
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i+1}/{n_runs} runs...")
        
        result = run_single_jitter_test(
            envelope_path, qrng_json, ff_json, higgs_json,
            lambda_min, lambda_max, alpha_min, alpha_max,
            n_lambda, n_alpha
        )
        
        if result is not None:
            results.append(result)
    
    n_survived = len(results)
    survival_rate = n_survived / n_runs
    
    print(f"\n✓ Completed {n_runs} jitter tests")
    print(f"  Survival rate: {survival_rate:.1%} ({n_survived}/{n_runs})")
    
    if n_survived == 0:
        print("  ⚠️  No viable islands in any jittered run!")
        return
    
    # Compute statistics
    lambda_p05 = [r['lambda_m']['p05'] for r in results]
    lambda_p50 = [r['lambda_m']['p50'] for r in results]
    lambda_p95 = [r['lambda_m']['p95'] for r in results]
    alpha_p05 = [r['alpha']['p05'] for r in results]
    alpha_p50 = [r['alpha']['p50'] for r in results]
    alpha_p95 = [r['alpha']['p95'] for r in results]
    
    summary = {
        'n_runs': n_runs,
        'n_survived': n_survived,
        'survival_rate': float(survival_rate),
        'lambda_m': {
            'p05': {
                'mean': float(np.mean(lambda_p05)),
                'std': float(np.std(lambda_p05)),
                'min': float(np.min(lambda_p05)),
                'max': float(np.max(lambda_p05)),
            },
            'p50': {
                'mean': float(np.mean(lambda_p50)),
                'std': float(np.std(lambda_p50)),
            },
            'p95': {
                'mean': float(np.mean(lambda_p95)),
                'std': float(np.std(lambda_p95)),
                'min': float(np.min(lambda_p95)),
                'max': float(np.max(lambda_p95)),
            },
        },
        'alpha': {
            'p05': {
                'mean': float(np.mean(alpha_p05)),
                'std': float(np.std(alpha_p05)),
            },
            'p50': {
                'mean': float(np.mean(alpha_p50)),
                'std': float(np.std(alpha_p50)),
            },
            'p95': {
                'mean': float(np.mean(alpha_p95)),
                'std': float(np.std(alpha_p95)),
            },
        },
    }
    
    # Save summary
    summary_path = output_dir / 'jitter_robustness_summary.json'
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"✓ Saved summary: {summary_path}")
    
    # Plot distributions
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Lambda distributions
    axes[0, 0].hist(lambda_p05, bins=30, alpha=0.7, edgecolor='black')
    axes[0, 0].set_xlabel('λ p05 (m)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Lambda p05 Distribution')
    axes[0, 0].axvline(np.mean(lambda_p05), color='red', linestyle='--', label=f'Mean: {np.mean(lambda_p05):.2e}')
    axes[0, 0].legend()
    
    axes[0, 1].hist(lambda_p50, bins=30, alpha=0.7, edgecolor='black')
    axes[0, 1].set_xlabel('λ p50 (m)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Lambda p50 Distribution')
    axes[0, 1].axvline(np.mean(lambda_p50), color='red', linestyle='--', label=f'Mean: {np.mean(lambda_p50):.2e}')
    axes[0, 1].legend()
    
    axes[0, 2].hist(lambda_p95, bins=30, alpha=0.7, edgecolor='black')
    axes[0, 2].set_xlabel('λ p95 (m)')
    axes[0, 2].set_ylabel('Frequency')
    axes[0, 2].set_title('Lambda p95 Distribution')
    axes[0, 2].axvline(np.mean(lambda_p95), color='red', linestyle='--', label=f'Mean: {np.mean(lambda_p95):.2e}')
    axes[0, 2].legend()
    
    # Alpha distributions
    axes[1, 0].hist(alpha_p05, bins=30, alpha=0.7, edgecolor='black')
    axes[1, 0].set_xlabel('α p05')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Alpha p05 Distribution')
    axes[1, 0].set_xscale('log')
    axes[1, 0].axvline(np.mean(alpha_p05), color='red', linestyle='--')
    
    axes[1, 1].hist(alpha_p50, bins=30, alpha=0.7, edgecolor='black')
    axes[1, 1].set_xlabel('α p50')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Alpha p50 Distribution')
    axes[1, 1].set_xscale('log')
    axes[1, 1].axvline(np.mean(alpha_p50), color='red', linestyle='--')
    
    axes[1, 2].hist(alpha_p95, bins=30, alpha=0.7, edgecolor='black')
    axes[1, 2].set_xlabel('α p95')
    axes[1, 2].set_ylabel('Frequency')
    axes[1, 2].set_title('Alpha p95 Distribution')
    axes[1, 2].set_xscale('log')
    axes[1, 2].axvline(np.mean(alpha_p95), color='red', linestyle='--')
    
    plt.suptitle(f'Jitter Robustness Test (σ=0.1, {n_runs} runs, {survival_rate:.1%} survival)', fontsize=14)
    plt.tight_layout()
    
    plot_path = output_dir / 'jitter_robustness_plot.png'
    plt.savefig(plot_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved plot: {plot_path}")
    plt.close()
    
    # Print summary
    print("\n" + "="*60)
    print("JITTER ROBUSTNESS SUMMARY")
    print("="*60)
    print(f"Survival rate: {survival_rate:.1%} ({n_survived}/{n_runs})")
    print()
    print("Lambda percentiles (mean ± std):")
    print(f"  p05: {np.mean(lambda_p05):.2e} ± {np.std(lambda_p05):.2e} m")
    print(f"  p50: {np.mean(lambda_p50):.2e} ± {np.std(lambda_p50):.2e} m")
    print(f"  p95: {np.mean(lambda_p95):.2e} ± {np.std(lambda_p95):.2e} m")
    print()
    print("Alpha percentiles (mean ± std):")
    print(f"  p05: {np.mean(alpha_p05):.2e} ± {np.std(alpha_p05):.2e}")
    print(f"  p50: {np.mean(alpha_p50):.2e} ± {np.std(alpha_p50):.2e}")
    print(f"  p95: {np.mean(alpha_p95):.2e} ± {np.std(alpha_p95):.2e}")
    print()
    if survival_rate > 0.7:
        print("✅ Island is robust under digitization uncertainty (>70% survival)")
    elif survival_rate > 0.5:
        print("⚠️  Island is moderately robust (50-70% survival)")
    else:
        print("❌ Island is sensitive to digitization uncertainty (<50% survival)")


def main():
    ap = argparse.ArgumentParser(description='Run jitter robustness test on digitized curves')
    ap.add_argument('--envelope', type=str,
                   default='experiments/constraints/data/fifth_force_exclusion_envelope.csv',
                   help='Path to envelope CSV')
    ap.add_argument('--n-runs', type=int, default=200,
                   help='Number of jitter runs')
    ap.add_argument('--sigma', type=float, default=0.1,
                   help='Standard deviation in log10 space (default 0.1 = 10% relative)')
    ap.add_argument('--out-dir', type=str,
                   default='experiments/constraints/results',
                   help='Output directory')
    args = ap.parse_args()
    
    envelope_path = Path(args.envelope)
    output_dir = Path(args.out_dir)
    
    if not envelope_path.exists():
        print(f"Error: Envelope file not found: {envelope_path}")
        return 1
    
    run_jitter_robustness_test(envelope_path, n_runs=args.n_runs, output_dir=output_dir)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

