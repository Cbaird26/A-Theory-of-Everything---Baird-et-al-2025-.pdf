#!/usr/bin/env python3
"""
Sanity checks for QRNG analysis results.
Usage: python sanity_checks.py --summary results/summary.csv --global results/global_summary.json
"""
import argparse
import json
import pandas as pd
from pathlib import Path


def check_file_consistency(summary_csv: Path):
    """Check if bias is driven by one file or consistent across files."""
    df = pd.read_csv(summary_csv)
    
    print("=" * 60)
    print("SANITY CHECK 1: File-by-file consistency")
    print("=" * 60)
    
    if len(df) == 0:
        print("No files analyzed.")
        return
    
    print(f"\nAnalyzed {len(df)} files:\n")
    print(df[["file", "n", "epsilon_hat", "BF10"]].to_string(index=False))
    
    # Check for outliers
    eps_abs = df["epsilon_hat"].abs()
    max_eps = eps_abs.max()
    mean_eps = eps_abs.mean()
    
    if max_eps > 3 * mean_eps:
        print(f"\n⚠️  WARNING: Large variation in epsilon across files.")
        print(f"   Max |epsilon| = {max_eps:.6f}, Mean |epsilon| = {mean_eps:.6f}")
        print(f"   Check if one file is driving the bias.")
    else:
        print(f"\n✓ File-by-file consistency looks reasonable.")
    
    # Check BF10 consistency
    bf_high = (df["BF10"] > 3).sum()
    bf_low = (df["BF10"] < 1/3).sum()
    
    if bf_high > 0 and bf_low > 0:
        print(f"\n⚠️  WARNING: Mixed evidence across files ({bf_high} files favor bias, {bf_low} favor null)")
    else:
        print(f"\n✓ BF10 evidence is consistent across files.")


def check_temporal_drift(summary_csv: Path, data_dir: Path):
    """Check if bias shows temporal patterns."""
    print("\n" + "=" * 60)
    print("SANITY CHECK 2: Temporal drift")
    print("=" * 60)
    print("\n(Check cumulative epsilon plots for steady drift vs random walk)")
    print("If cumulative plot shows steady upward/downward trend, investigate:")
    print("  - Logging artifacts (repeated headers/footers)")
    print("  - Time-dependent bias (real effect vs artifact)")
    print("  - File ordering effects")


def check_format_artifacts(data_dir: Path):
    """Check for potential parsing artifacts."""
    print("\n" + "=" * 60)
    print("SANITY CHECK 3: Format artifacts")
    print("=" * 60)
    
    data_dir = Path(data_dir)
    files = [f for f in data_dir.glob("*") if f.is_file()]
    
    if not files:
        print("No data files found.")
        return
    
    print(f"\nFound {len(files)} data files.")
    print("\nManual checks to perform:")
    print("  1. Open a few files and verify they contain actual QRNG bits")
    print("  2. Check for repeated patterns (headers/footers parsed as data)")
    print("  3. Verify column names match expected format")
    print("  4. Check for encoding issues (special characters)")
    
    # Quick check: file sizes
    sizes = [f.stat().st_size for f in files]
    print(f"\nFile sizes: min={min(sizes)} bytes, max={max(sizes)} bytes, mean={sum(sizes)/len(sizes):.0f} bytes")
    
    if min(sizes) < 10:
        print("⚠️  WARNING: Some files are very small (< 10 bytes). Check for empty/corrupt files.")


def check_global_summary(global_json: Path):
    """Check global summary for sanity."""
    print("\n" + "=" * 60)
    print("SANITY CHECK 4: Global summary interpretation")
    print("=" * 60)
    
    with global_json.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    n = data["n"]
    eps = data["epsilon_hat"]
    BF10 = data["BF10"]
    
    print(f"\nGlobal results:")
    print(f"  n = {n:,} bits")
    print(f"  epsilon_hat = {eps:.8f}")
    print(f"  BF10 = {BF10:.4f}")
    
    # Interpret BF10
    if BF10 > 30:
        print(f"\n✓ STRONG evidence for bias (BF10 > 30)")
    elif BF10 > 10:
        print(f"\n✓ SUBSTANTIAL evidence for bias (BF10 > 10)")
    elif BF10 > 3:
        print(f"\n  MODERATE evidence for bias (BF10 > 3)")
    elif BF10 > 1/3:
        print(f"\n  INCONCLUSIVE (BF10 between 1/3 and 3)")
    else:
        print(f"\n✓ Evidence AGAINST bias (BF10 < 1/3) - tightens upper bounds")
    
    # Check epsilon magnitude
    if abs(eps) > 0.01:
        print(f"\n⚠️  WARNING: Large bias estimate |epsilon| = {abs(eps):.6f} > 0.01")
        print("   This is unusually large. Verify data quality.")
    elif abs(eps) > 0.001:
        print(f"\n  Moderate bias estimate |epsilon| = {abs(eps):.6f}")
    else:
        print(f"\n✓ Small bias estimate |epsilon| = {abs(eps):.6f} (expected for subtle effects)")


def main():
    ap = argparse.ArgumentParser(description="Run sanity checks on QRNG analysis")
    ap.add_argument("--summary", type=str, default="results/summary.csv",
                    help="Path to summary.csv")
    ap.add_argument("--global-json", type=str, default="results/global_summary.json",
                    help="Path to global_summary.json")
    ap.add_argument("--data-dir", type=str, default="data/raw",
                    help="Path to raw data directory")
    args = ap.parse_args()
    
    summary_path = Path(args.summary)
    global_path = Path(getattr(args, 'global_json', 'results/global_summary.json'))
    data_dir = Path(args.data_dir)
    
    if not summary_path.exists():
        print(f"Error: {summary_path} not found. Run analyze_qrng.py first.")
        return 1
    
    check_file_consistency(summary_path)
    check_temporal_drift(summary_path, data_dir)
    check_format_artifacts(data_dir)
    
    if global_path.exists():
        check_global_summary(global_path)
    else:
        print(f"\n⚠️  {global_path} not found. Skipping global summary check.")
    
    print("\n" + "=" * 60)
    print("Sanity checks complete.")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())

