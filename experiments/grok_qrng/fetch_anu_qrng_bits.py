#!/usr/bin/env python3
import argparse, time
from pathlib import Path
import urllib3

import numpy as np
import requests

# Suppress SSL warnings (ANU has certificate issues)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ANU_URL = "https://qrng.anu.edu.au/API/jsonI.php"

def fetch_uint8(n: int, max_retries: int = 3) -> np.ndarray:
    # ANU API: length 1..1024, type in {uint8,uint16,hex16}
    # Note: verify=False due to ANU's SSL certificate issues (common with research APIs)
    n = max(1, min(1024, int(n)))
    
    for attempt in range(max_retries):
        try:
            r = requests.get(ANU_URL, params={"length": n, "type": "uint8"}, timeout=30, verify=False)
            r.raise_for_status()
            j = r.json()
            data = j.get("data", [])
            if not data:
                raise ValueError(f"No data in response: {j}")
            return np.array(data, dtype=np.uint8)
        except (requests.exceptions.RequestException, ValueError) as e:
            if attempt < max_retries - 1:
                time.sleep(1.0 * (attempt + 1))  # Exponential backoff
                continue
            raise

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-bits", type=int, default=200_000)
    ap.add_argument("--sleep", type=float, default=65.0, help="delay between requests in seconds (ANU limit: 1 req/min, default 65s to be safe)")
    ap.add_argument("--out", type=str, default="data/raw/anu_run_01/anu_bits.txt")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    bits_target = int(args.n_bits)
    bytes_needed = (bits_target + 7) // 8

    chunks = []
    total = 0
    num_requests = (bytes_needed + 1023) // 1024
    estimated_time = num_requests * args.sleep / 60.0
    print(f"Fetching {bits_target} bits from ANU QRNG (requires {bytes_needed} bytes, {num_requests} requests)...")
    print(f"Note: ANU API rate limit is 1 request/minute. Estimated time: ~{estimated_time:.1f} minutes.")
    while total < bytes_needed:
        take = min(1024, bytes_needed - total)
        request_num = len(chunks) + 1
        print(f"  Request {request_num}/{(bytes_needed + 1023)//1024}: fetching {take} bytes...", end=" ", flush=True)
        try:
            chunks.append(fetch_uint8(take))
            total += take
            print(f"✓ ({total}/{bytes_needed} bytes)")
        except Exception as e:
            print(f"✗ Error: {e}")
            print(f"  Retrying in 2 seconds...")
            time.sleep(2.0)
            continue
        if total < bytes_needed:
            time.sleep(args.sleep)  # be nice to ANU servers

    raw = np.concatenate(chunks)[:bytes_needed]
    bits = np.unpackbits(raw)[:bits_target]

    # Write as plain 0/1 text (your parser already handles this)
    out_path.write_text("".join(map(str, bits.tolist())), encoding="utf-8")
    print(f"\n✓ Wrote {bits_target} bits to {out_path}")

if __name__ == "__main__":
    main()

