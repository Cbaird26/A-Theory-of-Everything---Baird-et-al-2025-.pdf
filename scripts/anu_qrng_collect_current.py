#!/usr/bin/env python3
"""Collect ANU QRNG bits with provenance.

Modes:
- aqn: current keyed API at https://api.quantumnumbers.anu.edu.au
- legacy: public legacy endpoint at https://qrng.anu.edu.au/API/jsonI.php
- auto: use aqn when ANU_QRNG_API_KEY is set, otherwise legacy

The script never writes API keys to output. It records raw request metadata,
the normalized QRNG CSV required by docs/qrng_data_contract.md, and hashes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


AQN_URL = "https://api.quantumnumbers.anu.edu.au"
LEGACY_URL = "https://qrng.anu.edu.au/API/jsonI.php"
SOURCE_IDS = {
    "aqn": "anu_aqn_api",
    "legacy": "anu_legacy_public_jsonI",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit(repo: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return None


def flatten_data(data: Any) -> list[int]:
    if isinstance(data, list) and data and isinstance(data[0], list):
        out: list[int] = []
        for block in data:
            out.extend(int(x) for x in block)
        return out
    if isinstance(data, list):
        return [int(x) for x in data]
    raise ValueError(f"Unsupported data payload type: {type(data).__name__}")


def bytes_to_bits(values: list[int], limit: int | None = None) -> list[int]:
    bits: list[int] = []
    for value in values:
        if value < 0 or value > 255:
            raise ValueError(f"uint8 value out of range: {value}")
        for shift in range(7, -1, -1):
            bits.append((value >> shift) & 1)
            if limit is not None and len(bits) >= limit:
                return bits
    return bits


def fetch_uint8_once(mode: str, length: int, api_key: str | None, timeout: float) -> tuple[list[int], dict[str, Any]]:
    if mode == "aqn":
        headers = {"x-api-key": api_key or ""}
        params = {"length": int(length), "type": "uint8", "size": 1}
        url = AQN_URL
    elif mode == "legacy":
        headers = {}
        params = {"length": int(length), "type": "uint8"}
        url = LEGACY_URL
    else:
        raise ValueError(f"unsupported mode: {mode}")

    started = iso_now()
    response = requests.get(url, params=params, headers=headers, timeout=timeout)
    finished = iso_now()
    response.raise_for_status()
    payload = response.json()
    data = flatten_data(payload.get("data", []))
    if not data:
        raise ValueError(f"No data in response keys={sorted(payload.keys())}")
    record = {
        "started_at_utc": started,
        "finished_at_utc": finished,
        "mode": mode,
        "url": url,
        "params": params,
        "status_code": response.status_code,
        "response_keys": sorted(payload.keys()),
        "byte_count": len(data),
        "response_success": payload.get("success"),
    }
    return data, record


def fetch_uint8(mode: str, length: int, api_key: str | None, timeout: float, retries: int, backoff: float) -> tuple[list[int], dict[str, Any]]:
    last_error: str | None = None
    for attempt in range(1, retries + 1):
        try:
            data, record = fetch_uint8_once(mode, length, api_key, timeout)
            record["attempt"] = attempt
            return data, record
        except Exception as exc:
            last_error = repr(exc)
            if attempt >= retries:
                break
            time.sleep(backoff * attempt)
    raise RuntimeError(f"ANU QRNG request failed after {retries} attempts: {last_error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect ANU QRNG bits with provenance.")
    parser.add_argument("--mode", choices=["auto", "aqn", "legacy"], default="auto")
    parser.add_argument("--n-bits", type=int, default=200_000)
    parser.add_argument("--sleep", type=float, default=0.5, help="seconds between requests")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--retry-backoff", type=float, default=2.0)
    parser.add_argument("--max-values-per-request", type=int, default=1024)
    parser.add_argument("--run-label", default=None)
    parser.add_argument("--raw-dir", default="data/raw/qrng_sources")
    parser.add_argument("--results-dir", default="results/qrng/provenance")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    api_key = os.environ.get("ANU_QRNG_API_KEY", "")
    mode = args.mode
    if mode == "auto":
        mode = "aqn" if api_key else "legacy"
    if mode == "aqn" and not api_key:
        raise SystemExit("ANU_QRNG_API_KEY is required for --mode aqn")

    max_values = max(1, min(1024, int(args.max_values_per_request)))
    n_bits = int(args.n_bits)
    bytes_needed = (n_bits + 7) // 8
    run_stamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_label or f"anu_{mode}_{run_stamp}_{n_bits}bits"
    source_id = SOURCE_IDS[mode]

    raw_dir = repo / args.raw_dir
    results_dir = repo / args.results_dir
    raw_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    csv_path = raw_dir / f"{run_id}.csv"
    requests_path = raw_dir / f"{run_id}_requests.jsonl"
    manifest_path = results_dir / f"{run_id}_collection_manifest.json"
    sha_path = results_dir / f"{run_id}_SHA256SUMS.txt"

    print(f"Collecting {n_bits:,} bits from ANU QRNG")
    print(f"Mode: {mode}; endpoint: {AQN_URL if mode == 'aqn' else LEGACY_URL}")
    print(f"Output CSV: {csv_path}")

    bit_count = 0
    one_count = 0
    request_count = 0
    first_timestamp: str | None = None
    last_timestamp: str | None = None

    with csv_path.open("w", encoding="utf-8", newline="") as f_csv, requests_path.open("w", encoding="utf-8") as f_req:
        writer = csv.DictWriter(f_csv, fieldnames=["timestamp", "bit", "source_id"])
        writer.writeheader()
        while bit_count < n_bits:
            remaining_bits = n_bits - bit_count
            take_bytes = min(max_values, (remaining_bits + 7) // 8)
            request_count += 1
            data, record = fetch_uint8(mode, take_bytes, api_key, args.timeout, args.retries, args.retry_backoff)
            bits = bytes_to_bits(data, limit=remaining_bits)
            timestamp = record["finished_at_utc"]
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            for bit in bits:
                writer.writerow({"timestamp": timestamp, "bit": bit, "source_id": source_id})
            bit_count += len(bits)
            one_count += sum(bits)
            record["request_index"] = request_count
            record["bits_written"] = len(bits)
            f_req.write(json.dumps(record, sort_keys=True) + "\n")
            print(f"request {request_count}: {len(data)} bytes -> {len(bits)} bits; total={bit_count:,}/{n_bits:,}", flush=True)
            if bit_count < n_bits and args.sleep > 0:
                time.sleep(args.sleep)

    csv_sha = sha256_file(csv_path)
    requests_sha = sha256_file(requests_path)
    script_sha = sha256_file(Path(__file__).resolve())
    p_hat = one_count / bit_count if bit_count else None
    epsilon_hat = (p_hat - 0.5) if p_hat is not None else None

    manifest = {
        "run_id": run_id,
        "collected_at_utc": iso_now(),
        "mode": mode,
        "source_id": source_id,
        "endpoint": AQN_URL if mode == "aqn" else LEGACY_URL,
        "api_key_present": bool(api_key) if mode == "aqn" else False,
        "api_key_recorded": False,
        "n_bits_requested": n_bits,
        "n_bits_collected": bit_count,
        "bytes_needed": bytes_needed,
        "requests": request_count,
        "max_values_per_request": max_values,
        "sleep_seconds": args.sleep,
        "time_min": first_timestamp,
        "time_max": last_timestamp,
        "ones": one_count,
        "zeros": bit_count - one_count,
        "p_hat": p_hat,
        "epsilon_hat": epsilon_hat,
        "csv_path": str(csv_path),
        "requests_jsonl_path": str(requests_path),
        "csv_sha256": csv_sha,
        "requests_jsonl_sha256": requests_sha,
        "collector_script_sha256": script_sha,
        "git_commit": git_commit(repo),
        "python": sys.version,
        "platform": platform.platform(),
        "boundary": "real ANU QRNG collection; local author-run pilot/proof-object only, not independent external reproduction",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    sha_path.write_text(
        "\n".join(
            [
                f"{csv_sha}  {csv_path}",
                f"{requests_sha}  {requests_path}",
                f"{sha256_file(manifest_path)}  {manifest_path}",
                f"{script_sha}  {Path(__file__).resolve()}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote manifest: {manifest_path}")
    print(f"Wrote SHA256SUMS: {sha_path}")
    print(f"p_hat={p_hat:.8f}; epsilon_hat={epsilon_hat:+.8f}")


if __name__ == "__main__":
    main()
