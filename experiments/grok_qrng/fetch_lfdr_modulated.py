#!/usr/bin/env python3
"""
Fetch QRNG bits with embedded modulation signal for within-run testing.

This creates a dataset where blocks of bits are labeled with a modulation
signal s_t, allowing testing of the operational link ε ∝ η(ΔE - ⟨ΔE⟩).

Usage:
  ./fetch_lfdr_modulated.py --n-bits 400000 --block-size 4000 --out data/raw/lfdr_modulated/lfdr_modulated.csv
"""
import argparse
from pathlib import Path
import time

import numpy as np
import pandas as pd
import requests

LFDR_URL = "https://lfdr.de/qrng_api/qrng"

def main():
    ap = argparse.ArgumentParser(description="Fetch QRNG with modulation signal")
    ap.add_argument("--n-bits", type=int, default=400_000, help="Total bits to fetch")
    ap.add_argument("--block-size", type=int, default=4000, help="Bits per block")
    ap.add_argument("--out", type=str, default="data/raw/lfdr_modulated/lfdr_modulated.csv")
    ap.add_argument("--protocol", type=str, default="alternating", 
                    choices=["alternating", "neutral", "coherence"],
                    help="Protocol: alternating (clock-driven: 60s neutral, 60s coherence), neutral, or coherence")
    args = ap.parse_args()

    n_bits = int(args.n_bits)
    block_size = int(args.block_size)
    n_blocks = n_bits // block_size
    n_bytes = (n_bits + 7) // 8

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {n_bits} bits ({n_bytes} bytes) from LfD QRNG...")
    print(f"Will create {n_blocks} blocks of {block_size} bits each")
    print(f"Protocol: {args.protocol}")
    
    # Fetch all bits in one request
    try:
        r = requests.get(LFDR_URL, params={"length": n_bytes, "format": "HEX"}, timeout=120)
        r.raise_for_status()
        j = r.json()

        hex_str = j.get("qrn", "")
        if not hex_str or len(hex_str) < 2:
            raise RuntimeError(f"Unexpected response: {j}")

        raw = bytes.fromhex(hex_str)
        raw = raw[:n_bytes]
        bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))[:n_bits]
        
        print(f"✓ Fetched {len(bits)} bits")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching from LfD QRNG: {e}")
        raise

    # Create blocks and assign modulation signal
    blocks = []
    for i in range(n_blocks):
        start_idx = i * block_size
        end_idx = start_idx + block_size
        block_bits = bits[start_idx:end_idx]
        
        # Assign modulation signal based on protocol
        # Clock-driven: follow external timer (60s neutral, 60s coherence, repeat)
        if args.protocol == "alternating":
            # Alternating: even blocks = neutral (s=0), odd blocks = coherence (s=+1)
            # IMPORTANT: Follow external timer during data collection
            # Block assignment is automatic; your job is to follow the timer
            s_val = 1.0 if (i % 2 == 1) else 0.0
        elif args.protocol == "neutral":
            s_val = 0.0
        elif args.protocol == "coherence":
            s_val = 1.0
        else:
            s_val = 0.0
        
        # Create DataFrame for this block
        block_df = pd.DataFrame({
            "bit": block_bits.astype(int),
            "t": np.arange(start_idx, end_idx),
            "block": i,
            "s": s_val
        })
        blocks.append(block_df)
    
    # Combine all blocks
    df = pd.concat(blocks, ignore_index=True)
    
    # Save as CSV
    df.to_csv(out_path, index=False)
    
    print(f"✓ Wrote {len(df)} bits to {out_path}")
    print(f"  Blocks: {n_blocks}")
    print(f"  Modulation signal s: {df['s'].unique()}")
    print(f"  Distribution: {df['s'].value_counts().to_dict()}")
    print(f"\nReady for analysis:")
    print(f"  ./quick_run.sh lfdr_modulated")

if __name__ == "__main__":
    main()

