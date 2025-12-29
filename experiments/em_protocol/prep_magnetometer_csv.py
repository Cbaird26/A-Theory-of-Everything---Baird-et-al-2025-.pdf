#!/usr/bin/env python3
"""
Convert raw magnetometer CSV → em_modulated.csv format.

Handles various CSV formats and computes "power" metric from magnetic field magnitude.
"""
import argparse
import pandas as pd
import numpy as np


def main():
    ap = argparse.ArgumentParser(
        description="Convert raw magnetometer CSV to em_modulated.csv format"
    )
    ap.add_argument("--in", dest="inp", required=True, help="Raw magnetometer CSV")
    ap.add_argument("--out", dest="out", default="data/raw/em_modulated.csv",
                    help="Output CSV path")
    ap.add_argument("--sample-hz", type=float, default=None,
                    help="Sample rate (Hz) if raw CSV has no timestamps")
    ap.add_argument("--block-sec", type=int, default=60,
                    help="Protocol block length in seconds")
    ap.add_argument("--start", type=int, default=0,
                    help="0=neutral first, 1=coherence first")
    args = ap.parse_args()

    # Load raw CSV
    print(f"Loading: {args.inp}")
    df = pd.read_csv(args.inp)
    print(f"Columns: {df.columns.tolist()}")

    # Try common column names (case-insensitive)
    cols = {c.lower(): c for c in df.columns}
    
    def pick(*names):
        """Pick first matching column name."""
        for n in names:
            if n in cols:
                return cols[n]
        return None

    # Find magnetometer columns
    cx = pick("mx", "magx", "x", "bx", "magnetic_x", "m_x")
    cy = pick("my", "magy", "y", "by", "magnetic_y", "m_y")
    cz = pick("mz", "magz", "z", "bz", "magnetic_z", "m_z")
    ct = pick("t", "time", "timestamp", "elapsed", "seconds", "sec")

    if cx is None or cy is None or cz is None:
        print(f"Error: Could not find magnetometer columns.")
        print(f"Expected: mx/my/mz or magx/magy/magz or x/y/z or bx/by/bz")
        print(f"Found columns: {df.columns.tolist()}")
        print(f"\nPlease rename columns to mx, my, mz (and optionally t for time).")
        return 1

    print(f"Found magnetometer columns: {cx}, {cy}, {cz}")
    if ct:
        print(f"Found time column: {ct}")
    else:
        print("No time column found. Will use --sample-hz to generate timestamps.")

    # Extract data
    x = pd.to_numeric(df[cx], errors="coerce")
    y = pd.to_numeric(df[cy], errors="coerce")
    z = pd.to_numeric(df[cz], errors="coerce")
    
    # Keep only rows with valid data
    keep = x.notna() & y.notna() & z.notna()
    x = x[keep]
    y = y[keep]
    z = z[keep]
    
    print(f"Valid data points: {len(x)}")

    # Handle timestamps
    if ct is not None:
        t = pd.to_numeric(df.loc[keep, ct], errors="coerce")
        t = t.fillna(method="ffill")  # Forward fill any NaN timestamps
        t = t.to_numpy(dtype=float)
        # Normalize to seconds from start
        t = t - t[0]
        print(f"Time range: {t[0]:.1f} to {t[-1]:.1f} seconds")
    else:
        if args.sample_hz is None:
            print("Error: No time column found and --sample-hz not provided.")
            print("Please provide --sample-hz (e.g., 10 or 50 Hz).")
            return 1
        t = np.arange(len(x), dtype=float) / float(args.sample_hz)
        print(f"Generated timestamps using sample rate: {args.sample_hz} Hz")
        print(f"Time range: {t[0]:.1f} to {t[-1]:.1f} seconds")

    # Compute magnetic field magnitude
    B = np.sqrt(x.to_numpy()**2 + y.to_numpy()**2 + z.to_numpy()**2)
    print(f"Magnetic field magnitude range: {B.min():.2f} to {B.max():.2f} µT")

    # Bin into 1-second windows and compute "power" as within-second std dev
    sec = np.floor(t).astype(int)
    out = []
    for s in range(sec.min(), sec.max() + 1):
        mask = sec == s
        if mask.sum() < 3:  # Need at least 3 samples per second
            continue
        power = float(np.std(B[mask]))  # Simple, robust pilot metric
        out.append((s, power))

    outdf = pd.DataFrame(out, columns=["t", "power"])
    print(f"Binned into {len(outdf)} one-second windows")

    # Add protocol label s(t): alternating blocks
    block = (outdf["t"] // args.block_sec).astype(int)
    outdf["s"] = ((block + args.start) % 2).astype(int)  # 0/1 alternating
    
    # Count blocks
    n_neutral = (outdf["s"] == 0).sum()
    n_coherence = (outdf["s"] == 1).sum()
    print(f"Protocol blocks: {n_neutral} neutral (s=0), {n_coherence} coherence (s=1)")

    # Save
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    outdf.to_csv(out_path, index=False)
    print(f"\n✓ Wrote: {out_path}")
    print(f"  Columns: t, power, s")
    print(f"  Total duration: {outdf['t'].max():.1f} seconds ({outdf['t'].max()/60:.1f} minutes)")

    return 0


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.exit(main())

