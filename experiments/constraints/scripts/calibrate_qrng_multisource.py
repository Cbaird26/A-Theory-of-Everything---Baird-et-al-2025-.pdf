#!/usr/bin/env python3
"""
Multi-source QRNG calibration system.

Computes epsilon_max from multiple independent QRNG sources with:
- Per-source epsilon_max + bootstrap CI
- Pooled epsilon_max (meta-analysis style)
- Sensitivity analysis (window size, filtering effects)
- Reproducibility hashes

Outputs:
- QRNG_CALIBRATION.json (per-source + pooled results)
- QRNG_CALIBRATION.png (per-source epsilon_max + pooled)
- QRNG_CALIBRATION_PROTOCOL.md (assumptions + falsifiability)
"""
import argparse
import json
import hashlib
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from qrng_sources import load_lfdr_source, StandardizedQRNGData


def compute_epsilon_max(
    bits: pd.Series,
    method: str = 'bootstrap_95',
    n_bootstrap: int = 1000,
    window_size: Optional[int] = None,
    random_state: Optional[int] = None
) -> Dict[str, float]:
    """
    Compute epsilon_max from bit sequence.
    
    Args:
        bits: Binary sequence (0 or 1)
        method: 'bootstrap_95', 'chi2_95', or 'max_deviation'
        n_bootstrap: Number of bootstrap samples
        window_size: Rolling window size (None = use full sequence)
    
    Returns:
        Dict with epsilon_max, ci_lower, ci_upper
    """
    if window_size is not None:
        # Use rolling window
        n_windows = len(bits) - window_size + 1
        window_epsilons = []
        for i in range(n_windows):
            window_bits = bits.iloc[i:i+window_size]
            p_hat = window_bits.mean()
            epsilon = abs(p_hat - 0.5)
            window_epsilons.append(epsilon)
        epsilon_hat = max(window_epsilons) if window_epsilons else 0.0
    else:
        # Use full sequence
        p_hat = bits.mean()
        epsilon_hat = abs(p_hat - 0.5)
    
    if method == 'max_deviation':
        return {
            'epsilon_max': float(epsilon_hat),
            'ci_lower': float(epsilon_hat),
            'ci_upper': float(epsilon_hat)
        }
    
    elif method == 'bootstrap_95':
        # Bootstrap confidence interval
        n = len(bits)
        bootstrap_epsilons = []
        
        for i in range(n_bootstrap):
            # Resample with replacement
            # Use random_state parameter for reproducibility
            if random_state is not None:
                # For pandas sample, we need to use a different approach
                # Create a generator with the seed offset by iteration
                sample_rng = np.random.RandomState(random_state + i)
                indices = sample_rng.randint(0, n, size=n)
                resampled = bits.iloc[indices]
            else:
                resampled = bits.sample(n=n, replace=True)
            p_hat_boot = resampled.mean()
            epsilon_boot = abs(p_hat_boot - 0.5)
            bootstrap_epsilons.append(epsilon_boot)
        
        bootstrap_epsilons = np.array(bootstrap_epsilons)
        ci_lower = np.percentile(bootstrap_epsilons, 2.5)
        ci_upper = np.percentile(bootstrap_epsilons, 97.5)
        
        return {
            'epsilon_max': float(epsilon_hat),
            'ci_lower': float(ci_lower),
            'ci_upper': float(ci_upper)
        }
    
    elif method == 'chi2_95':
        # Chi-square derived bound (95% CL)
        n = len(bits)
        k = bits.sum()
        # Binomial test for p != 0.5
        # 95% CI for p
        ci = stats.binomtest(k, n, p=0.5, alternative='two-sided').proportion_ci(confidence_level=0.95)
        p_lower, p_upper = ci
        epsilon_lower = abs(p_lower - 0.5)
        epsilon_upper = abs(p_upper - 0.5)
        epsilon_max = max(epsilon_lower, epsilon_upper)
        
        return {
            'epsilon_max': float(epsilon_max),
            'ci_lower': float(epsilon_lower),
            'ci_upper': float(epsilon_upper)
        }
    
    else:
        raise ValueError(f"Unknown method: {method}")


def compute_pooled_epsilon_max(
    source_results: List[Dict[str, Any]],
    method: str = 'meta_analysis'
) -> Dict[str, Any]:
    """
    Compute pooled epsilon_max from multiple sources.
    
    Args:
        source_results: List of per-source results
        method: 'meta_analysis' (inverse-variance weighted) or 'max' (conservative)
    
    Returns:
        Pooled result with epsilon_max, ci_lower, ci_upper
    """
    if method == 'max':
        # Conservative: take maximum across sources
        epsilon_max = max(r['epsilon_max'] for r in source_results)
        ci_upper = max(r.get('epsilon_max_ci_upper', r.get('ci_upper', r['epsilon_max'])) for r in source_results)
        ci_lower = min(r.get('epsilon_max_ci_lower', r.get('ci_lower', r['epsilon_max'])) for r in source_results)
        
        return {
            'epsilon_max': float(epsilon_max),
            'ci_lower': float(ci_lower),
            'ci_upper': float(ci_upper),
            'method': 'max_conservative'
        }
    
    elif method == 'meta_analysis':
        # Inverse-variance weighted meta-analysis
        # For each source, compute weight = 1 / variance
        weights = []
        epsilon_values = []
        
        for r in source_results:
            epsilon = r['epsilon_max']
            ci_upper = r.get('epsilon_max_ci_upper', r.get('ci_upper', epsilon))
            ci_lower = r.get('epsilon_max_ci_lower', r.get('ci_lower', epsilon))
            ci_width = ci_upper - ci_lower
            # Approximate variance from CI width (assuming normal)
            # CI width ≈ 2 * 1.96 * std, so std ≈ CI_width / 3.92
            if ci_width > 0:
                std = ci_width / 3.92
                weight = 1.0 / (std ** 2)
            else:
                weight = 1.0  # Default weight if CI is degenerate
            
            weights.append(weight)
            epsilon_values.append(epsilon)
        
        # Weighted average
        total_weight = sum(weights)
        pooled_epsilon = sum(w * e for w, e in zip(weights, epsilon_values)) / total_weight
        
        # Pooled variance
        pooled_var = 1.0 / total_weight
        pooled_std = np.sqrt(pooled_var)
        
        # 95% CI
        ci_lower = pooled_epsilon - 1.96 * pooled_std
        ci_upper = pooled_epsilon + 1.96 * pooled_std
        
        return {
            'epsilon_max': float(pooled_epsilon),
            'ci_lower': float(max(0, ci_lower)),  # Can't be negative
            'ci_upper': float(ci_upper),
            'method': 'meta_analysis_inverse_variance'
        }
    
    else:
        raise ValueError(f"Unknown method: {method}")


def compute_file_hash(path: Path) -> str:
    """Compute SHA256 hash of file."""
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def calibrate_multisource(
    source_paths: List[Tuple[str, Path]],
    method: str = 'bootstrap_95',
    n_bootstrap: int = 1000,
    window_size: Optional[int] = None,
    output_dir: Path = None,
    random_state: Optional[int] = None
) -> Dict[str, Any]:
    """
    Calibrate epsilon_max from multiple sources.
    
    Args:
        source_paths: List of (source_id, path) tuples
        method: Method for computing epsilon_max
        n_bootstrap: Number of bootstrap samples
        window_size: Rolling window size (None = full sequence)
        output_dir: Output directory
    
    Returns:
        Calibration results dictionary
    """
    print("="*60)
    print("MULTI-SOURCE QRNG CALIBRATION")
    print("="*60)
    print()
    
    source_results = []
    data_hashes = {}
    
    # Process each source
    for source_id, path in source_paths:
        print(f"Processing source: {source_id}")
        print(f"  Path: {path}")
        
        # Load source data
        if source_id == 'lfdr_withinrun':
            data = load_lfdr_source(path)
        else:
            raise ValueError(f"Unknown source: {source_id}")
        
        # Compute file hash for reproducibility
        file_hash = compute_file_hash(path)
        data_hashes[source_id] = file_hash
        print(f"  Data hash: {file_hash[:16]}...")
        
        # Compute epsilon_max
        result = compute_epsilon_max(
            data.bit,
            method=method,
            n_bootstrap=n_bootstrap,
            window_size=window_size,
            random_state=random_state
        )
        
        source_result = {
            'source_id': source_id,
            'timestamp_range': {
                'start': str(data.timestamp.iloc[0]),
                'end': str(data.timestamp.iloc[-1])
            },
            'n_trials': len(data.bit),
            'epsilon_max': result['epsilon_max'],
            'epsilon_max_ci_lower': result['ci_lower'],
            'epsilon_max_ci_upper': result['ci_upper'],
            'method': method,
            'preprocessing': {
                'window_size': window_size,
                'n_bootstrap': n_bootstrap
            },
            'meta': data.meta,
            'data_hash': file_hash
        }
        
        source_results.append(source_result)
        
        print(f"  n_trials: {len(data.bit):,}")
        print(f"  epsilon_max: {result['epsilon_max']:.6f}")
        print(f"  95% CI: [{result['ci_lower']:.6f}, {result['ci_upper']:.6f}]")
        print()
    
    # Compute pooled result
    print("Computing pooled epsilon_max...")
    pooled = compute_pooled_epsilon_max(source_results, method='meta_analysis')
    print(f"  Pooled epsilon_max: {pooled['epsilon_max']:.6f}")
    print(f"  95% CI: [{pooled['ci_lower']:.6f}, {pooled['ci_upper']:.6f}]")
    print()
    
    # Sensitivity analysis (window size effects)
    print("Sensitivity analysis...")
    sensitivity = {}
    if len(source_results) > 0:
        # Test different window sizes
        test_windows = [10000, 50000, 100000, None]  # None = full sequence
        window_effects = []
        
        # Use first source for sensitivity
        first_source_id, first_path = source_paths[0]
        if first_source_id == 'lfdr_withinrun':
            first_data = load_lfdr_source(first_path)
        
        for w in test_windows:
            sens_result = compute_epsilon_max(
                first_data.bit,
                method=method,
                n_bootstrap=n_bootstrap,
                window_size=w
            )
            window_effects.append({
                'window_size': w if w else 'full',
                'epsilon_max': sens_result['epsilon_max'],
                'ci_lower': sens_result['ci_lower'],
                'ci_upper': sens_result['ci_upper']
            })
        
        sensitivity['window_size_effects'] = window_effects
        print(f"  Tested {len(test_windows)} window sizes")
    
    # Compute script hash for reproducibility
    script_path = Path(__file__)
    script_hash = compute_file_hash(script_path) if script_path.exists() else None
    
    # Assemble results
    calibration_results = {
        'sources': source_results,
        'pooled': pooled,
        'sensitivity': sensitivity,
        'reproducibility': {
            'script_path': str(script_path),
            'script_hash': script_hash,
            'data_hashes': data_hashes,
            'method': method,
            'n_bootstrap': n_bootstrap,
            'seed_used': random_state,
            'python_version': sys.version.split()[0],  # e.g., '3.11.0'
            'numpy_version': np.__version__,
            'pandas_version': pd.__version__
        }
    }
    
    # Save results
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON output
        json_path = output_dir / 'QRNG_CALIBRATION.json'
        json_path.write_text(json.dumps(calibration_results, indent=2))
        print(f"✓ Saved calibration: {json_path}")
        
        # Plot
        plot_calibration_results(source_results, pooled, output_dir)
        
        # Protocol document
        create_calibration_protocol(calibration_results, output_dir)
    
    return calibration_results


def plot_calibration_results(
    source_results: List[Dict],
    pooled: Dict,
    output_dir: Path
):
    """Create plot showing per-source and pooled epsilon_max."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Per-source results
    x_pos = np.arange(len(source_results))
    source_names = [r['source_id'] for r in source_results]
    epsilon_maxes = [r['epsilon_max'] for r in source_results]
    ci_lowers = [r['epsilon_max_ci_lower'] for r in source_results]
    ci_uppers = [r['epsilon_max_ci_upper'] for r in source_results]
    
    # Error bars
    yerr_lower = [em - cl for em, cl in zip(epsilon_maxes, ci_lowers)]
    yerr_upper = [cu - em for em, cu in zip(epsilon_maxes, ci_uppers)]
    
    ax.errorbar(x_pos, epsilon_maxes, yerr=[yerr_lower, yerr_upper],
                fmt='o', capsize=5, capthick=2, label='Per-source', markersize=8)
    
    # Pooled result
    ax.axhline(pooled['epsilon_max'], color='red', linestyle='--', linewidth=2,
               label=f"Pooled: {pooled['epsilon_max']:.6f}")
    ax.fill_between([-0.5, len(source_results)-0.5],
                     pooled['ci_lower'], pooled['ci_upper'],
                     alpha=0.2, color='red', label='Pooled 95% CI')
    
    ax.set_xlabel('Source', fontsize=12)
    ax.set_ylabel('ε_max', fontsize=12)
    ax.set_title('Multi-Source QRNG Calibration: ε_max Estimates', fontsize=14)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(source_names, rotation=45, ha='right')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = output_dir / 'QRNG_CALIBRATION.png'
    plt.savefig(plot_path, dpi=200, bbox_inches='tight')
    print(f"✓ Saved plot: {plot_path}")
    plt.close()


def create_calibration_protocol(
    results: Dict,
    output_dir: Path
):
    """Create calibration protocol documentation."""
    md_content = f"""# QRNG Calibration Protocol

## Date
{pd.Timestamp.now().strftime('%Y-%m-%d')}

## Overview
Multi-source calibration of QRNG_tilt constraint bound (ε_max) from independent QRNG data sources.

## Data Sources

"""
    
    for source in results['sources']:
        md_content += f"""### {source['source_id']}
- **Path:** {source['meta'].get('original_path', 'N/A')}
- **Time range:** {source['timestamp_range']['start']} to {source['timestamp_range']['end']}
- **n_trials:** {source['n_trials']:,}
- **ε_max:** {source['epsilon_max']:.6f}
- **95% CI:** [{source['epsilon_max_ci_lower']:.6f}, {source['epsilon_max_ci_upper']:.6f}]
- **Data hash:** {source['data_hash'][:16]}...

"""
    
    md_content += f"""## Pooled Result

- **Method:** {results['pooled']['method']}
- **ε_max:** {results['pooled']['epsilon_max']:.6f}
- **95% CI:** [{results['pooled']['ci_lower']:.6f}, {results['pooled']['ci_upper']:.6f}]

## Preprocessing

- **Method:** {results['reproducibility']['method']}
- **Bootstrap samples:** {results['reproducibility']['n_bootstrap']:,}
- **Window size:** {results['sources'][0]['preprocessing'].get('window_size', 'full sequence')}

## Sensitivity Analysis

### Window Size Effects

"""
    
    for w_effect in results['sensitivity'].get('window_size_effects', []):
        md_content += f"- **Window size {w_effect['window_size']}:** ε_max = {w_effect['epsilon_max']:.6f} "
        md_content += f"[{w_effect['ci_lower']:.6f}, {w_effect['ci_upper']:.6f}]\n"
    
    md_content += f"""

## Assumptions

1. **Stationarity:** QRNG bias is constant over the measurement period
2. **Independence:** Trials are independent (no autocorrelation)
3. **No systematic drift:** No time-dependent bias trends
4. **Representative sampling:** Sources are representative of QRNG behavior under test conditions

## What Would Falsify This Bound

If future QRNG data (with similar or larger sample sizes) produces:
- **ε_max < {results['pooled']['ci_lower']:.6f}:** Current bound is too conservative; viable region expands
- **ε_max > {results['pooled']['ci_upper']:.6f}:** Current bound is too optimistic; viable region shrinks significantly

**Quantitative impact:** If ε_max tightens by 10%, the viable parameter island shrinks by approximately X% (to be computed from constraint engine).

## Reproducibility

- **Script:** {results['reproducibility']['script_path']}
- **Script hash:** {results['reproducibility']['script_hash'][:16] if results['reproducibility']['script_hash'] else 'N/A'}...
- **Data hashes:** See per-source sections above

## Next Steps

1. Integrate pooled ε_max into constraint engine
2. Re-run μ phase diagram with calibrated bounds
3. Update regression tests if baseline changes
"""
    
    md_path = output_dir / 'QRNG_CALIBRATION_PROTOCOL.md'
    md_path.write_text(md_content)
    print(f"✓ Saved protocol: {md_path}")


def main():
    ap = argparse.ArgumentParser(description='Multi-source QRNG calibration')
    ap.add_argument('--lfdr-json', type=str,
                   default='experiments/grok_qrng/results/lfdr_withinrun/global_summary.json',
                   help='LFDR source JSON')
    ap.add_argument('--method', type=str, default='bootstrap_95',
                   choices=['bootstrap_95', 'chi2_95', 'max_deviation'],
                   help='Method for computing epsilon_max')
    ap.add_argument('--n-bootstrap', type=int, default=1000,
                   help='Number of bootstrap samples')
    ap.add_argument('--window-size', type=int, default=None,
                   help='Rolling window size (None = full sequence)')
    ap.add_argument('--seed', type=int, default=42,
                   help='Random seed for reproducibility (default: 42)')
    ap.add_argument('--out-dir', type=str,
                   default='experiments/constraints/results',
                   help='Output directory')
    args = ap.parse_args()
    
    # Build source list
    source_paths = []
    if Path(args.lfdr_json).exists():
        source_paths.append(('lfdr_withinrun', Path(args.lfdr_json)))
    
    if not source_paths:
        print("❌ No source files found!")
        return 1
    
    # Set global random seed for reproducibility
    np.random.seed(args.seed)
    
    # Run calibration
    results = calibrate_multisource(
        source_paths,
        method=args.method,
        n_bootstrap=args.n_bootstrap,
        window_size=args.window_size,
        output_dir=Path(args.out_dir),
        random_state=args.seed
    )
    
    print("\n" + "="*60)
    print("CALIBRATION COMPLETE")
    print("="*60)
    print(f"Pooled ε_max: {results['pooled']['epsilon_max']:.6f}")
    print(f"95% CI: [{results['pooled']['ci_lower']:.6f}, {results['pooled']['ci_upper']:.6f}]")
    print(f"\nResults saved to: {Path(args.out_dir)}")
    print(f"  - QRNG_CALIBRATION.json")
    print(f"  - QRNG_CALIBRATION.png")
    print(f"  - QRNG_CALIBRATION_PROTOCOL.md")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

