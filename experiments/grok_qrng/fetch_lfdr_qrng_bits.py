#!/usr/bin/env python3
import argparse, json
from pathlib import Path

import numpy as np
import requests

# LfD QRNG API docs: /qrng_api/qrng?length=<bytes>&format=HEX|BINARY|HEXDUMP
LFDR_URL = "https://lfdr.de/qrng_api/qrng"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-bits", type=int, default=200_000)
    ap.add_argument("--out", type=str, default="data/raw/lfdr_run_01/lfdr_bits.txt")
    args = ap.parse_args()

    n_bits = int(args.n_bits)
    n_bytes = (n_bits + 7) // 8

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {n_bits} bits ({n_bytes} bytes) from LfD QRNG (ID Quantique hardware)...")
    
    # Ask for HEX so we can reliably decode to bytes
    try:
        r = requests.get(LFDR_URL, params={"length": n_bytes, "format": "HEX"}, timeout=60)
        r.raise_for_status()
        j = r.json()

        hex_str = j.get("qrn", "")
        if not hex_str or len(hex_str) < 2:
            raise RuntimeError(f"Unexpected response: {json.dumps(j)[:300]}")

        raw = bytes.fromhex(hex_str)
        raw = raw[:n_bytes]

        bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))[:n_bits]
        out_path.write_text("".join(map(str, bits.tolist())), encoding="utf-8")

        print(f"✓ Wrote {n_bits} bits ({n_bytes} bytes) to {out_path}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching from LfD QRNG: {e}")
        print(f"  Response: {e.response.text[:200] if hasattr(e, 'response') else 'N/A'}")
        raise

if __name__ == "__main__":
    main()

