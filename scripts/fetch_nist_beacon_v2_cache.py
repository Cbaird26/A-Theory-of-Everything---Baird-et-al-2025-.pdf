#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.request import urlopen, Request

# NIST Beacon 2.0 returns JSON at this endpoint (latest pulse)
NIST_LAST_PULSE = "https://beacon.nist.gov/beacon/2.0/pulse/last"

def fetch_json(url: str, timeout: int = 20) -> dict:
    req = Request(url, headers={"Accept": "application/json", "User-Agent": "mqgt-scf-qrng-cache/1.0"})
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def hex_to_bits(hex_str: str) -> str:
    hex_str = hex_str.strip()
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

def previous_uri(pulse: dict) -> str | None:
    # In /pulse/last response, listValues contains a "previous" entry with a uri
    for entry in pulse.get("listValues", []):
        if entry.get("type") == "previous" and entry.get("uri"):
            return entry["uri"]
    return None

def main() -> None:
    ap = argparse.ArgumentParser(description="Cache NIST Beacon 2.0 pulses into QRNG contract CSV (offline-first).")
    ap.add_argument("--pulses", type=int, default=400, help="Number of pulses to fetch (400 pulses ≈ 204,800 bits).")
    ap.add_argument("--sleep", type=float, default=0.05, help="Politeness sleep between requests (seconds).")
    ap.add_argument("--source-id", type=str, default="nist_beacon_v2", help="source_id written to CSV.")
    ap.add_argument("--out", type=str, default="data/raw/qrng_sources/nist_beacon_v2_last400.csv", help="Output contract CSV path.")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    data = fetch_json(NIST_LAST_PULSE)
    pulse = data["pulse"]

    rows = 0
    pulses_fetched = 0

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "bit", "source_id"])

        while pulses_fetched < args.pulses:
            ts = pulse["timeStamp"]
            out_hex = pulse["outputValue"]  # 512-bit value in hex
            bits = hex_to_bits(out_hex)

            # Write one row per bit (timestamp replicated; contract requires it)
            for b in bits:
                w.writerow([ts, int(b), args.source_id])
                rows += 1

            pulses_fetched += 1
            prev = previous_uri(pulse)
            if not prev:
                break

            time.sleep(args.sleep)
            pulse = fetch_json(prev)["pulse"]

    print(f"Wrote {rows} bits from {pulses_fetched} pulses -> {out_path}")

if __name__ == "__main__":
    main()
