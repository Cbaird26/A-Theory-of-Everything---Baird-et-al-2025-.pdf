#!/usr/bin/env python3
"""
Check modulation stability across different block sizes.
Re-analyzes the same modulated dataset with different block sizes.
"""
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from analyze_qrng import load_bits_any, fit_logistic_modulation


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=str, default="data/raw/lfdr_withinrun/modulated.csv",
                    help="Path to modulated CSV with 'bit' and 's' columns")
    ap.add_argument("--block-sizes", type=str, default="2000,4000,8000",
                    help="Comma-separated block sizes to test")
    args = ap.parse_args()
    
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: {data_path} not found")
        return 1
    
    df = load_bits_any(data_path)
    bits = df["bit"].to_numpy(dtype=np.int8)
    
    if "s" not in df.columns:
        print("Error: Data must have 's' column for modulation signal")
        return 1
    
    s = df["s"].fillna(0.0).to_numpy(dtype=float)
    
    block_sizes = [int(x.strip()) for x in args.block_sizes.split(",")]
    
    print("=" * 60)
    print("BLOCK SIZE STABILITY CHECK")
    print("=" * 60)
    print(f"\nData: {data_path.name}")
    print(f"Total bits: {len(bits):,}")
    print(f"Block sizes to test: {block_sizes}")
    print("\n" + "=" * 60)
    
    results = []
    for block_size in block_sizes:
        n_blocks = len(bits) // block_size
        if n_blocks < 2:
            print(f"\n⚠️  Block size {block_size} too large (only {n_blocks} blocks)")
            continue
        
        # Reassign s signal based on new block size
        s_reassigned = np.zeros(len(bits), dtype=float)
        for i in range(n_blocks):
            start = i * block_size
            end = start + block_size
            # Alternating: even blocks = 0, odd blocks = 1
            s_reassigned[start:end] = 1.0 if (i % 2 == 1) else 0.0
        
        # Fit modulation
        try:
            modfit = fit_logistic_modulation(bits, s_reassigned)
            beta = modfit["beta"]
            alpha = modfit["alpha"]
            loglik = modfit["loglik"]
            
            results.append({
                "block_size": block_size,
                "n_blocks": n_blocks,
                "mod_alpha": alpha,
                "mod_beta": beta,
                "mod_loglik": loglik
            })
            
            print(f"\nBlock size: {block_size} bits ({n_blocks} blocks)")
            print(f"  mod_alpha = {alpha:.6f}")
            print(f"  mod_beta = {beta:.6f}")
            print(f"  mod_loglik = {loglik:.2f}")
            
        except Exception as e:
            print(f"\n✗ Error with block size {block_size}: {e}")
    
    if len(results) > 1:
        print("\n" + "=" * 60)
        print("STABILITY ASSESSMENT")
        print("=" * 60)
        
        betas = [r["mod_beta"] for r in results]
        print(f"\nmod_beta across block sizes: {[f'{b:.6f}' for b in betas]}")
        
        if all(b < 0 for b in betas) or all(b > 0 for b in betas):
            print("✓ Sign is consistent across block sizes")
        else:
            print("⚠️  Sign flips across block sizes (suggests noise)")
        
        beta_range = max(betas) - min(betas)
        if beta_range < 0.01:
            print(f"✓ Magnitude is stable (range = {beta_range:.6f})")
        else:
            print(f"⚠️  Magnitude varies (range = {beta_range:.6f})")
    
    return 0


if __name__ == "__main__":
    exit(main())

