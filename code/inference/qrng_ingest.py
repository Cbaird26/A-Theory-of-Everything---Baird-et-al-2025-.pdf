#!/usr/bin/env python3
"""
QRNG Data Ingest Validator + Provenance Generator

Validates QRNG CSV logs against the data contract and produces:
- Validated CSV (normalized format)
- Provenance manifest (SHA256, row counts, time ranges, source distribution)
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional, Dict, Any, Tuple


REQUIRED_COLUMNS = ("timestamp", "bit", "source_id")


@dataclass(frozen=True)
class Provenance:
    filename: str
    sha256: str
    rows: int
    time_min: Optional[str]
    time_max: Optional[str]
    source_counts: Dict[str, int]
    warnings: list[str]


def sha256_file(path: Path) -> str:
    """Compute SHA256 hash of file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_iso8601(ts: str) -> datetime:
    """
    Parse ISO 8601 timestamp.
    Accepts common ISO forms; handles 'Z' suffix for UTC.
    """
    # Replace 'Z' with '+00:00' for UTC
    ts_normalized = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts_normalized)


def validate_row(row: Dict[str, str]) -> Tuple[str, int, str]:
    """
    Validate a single CSV row against the contract.
    
    Returns:
        (timestamp, bit, source_id)
    
    Raises:
        ValueError if validation fails
    """
    for c in REQUIRED_COLUMNS:
        if c not in row:
            raise ValueError(f"Missing required column: {c}")

    ts = row["timestamp"].strip()
    if not ts:
        raise ValueError("Empty timestamp")
    _ = parse_iso8601(ts)  # Validate it parses

    bit_s = row["bit"].strip()
    if bit_s not in ("0", "1"):
        raise ValueError(f"Invalid bit value: {bit_s!r}")
    bit = int(bit_s)

    source_id = row["source_id"].strip()
    if not source_id:
        raise ValueError("Empty source_id")
    if len(source_id) > 64:
        raise ValueError("source_id too long (>64 chars)")

    return ts, bit, source_id


def ingest_qrng_csv(
    input_path: Path,
    processed_dir: Path,
    results_dir: Path,
) -> Tuple[Path, Path]:
    """
    Validate and normalize a QRNG CSV log.
    
    Args:
        input_path: Path to raw CSV file
        processed_dir: Directory for validated CSV output
        results_dir: Directory for provenance manifest
    
    Returns:
        (validated_csv_path, provenance_manifest_path)
    
    Raises:
        ValueError if validation fails
    """
    processed_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    digest = sha256_file(input_path)

    out_csv = processed_dir / f"{input_path.stem}_validated.csv"
    out_manifest = results_dir / f"{input_path.stem}_provenance.json"

    source_counts: Dict[str, int] = {}
    rows = 0
    tmin: Optional[datetime] = None
    tmax: Optional[datetime] = None
    warnings: list[str] = []

    with input_path.open("r", encoding="utf-8", newline="") as f_in, out_csv.open(
        "w", encoding="utf-8", newline=""
    ) as f_out:
        reader = csv.DictReader(f_in)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        for c in REQUIRED_COLUMNS:
            if c not in reader.fieldnames:
                raise ValueError(f"Missing required column in header: {c}")

        writer = csv.DictWriter(f_out, fieldnames=list(REQUIRED_COLUMNS))
        writer.writeheader()

        for i, row in enumerate(reader, start=2):  # header is line 1
            try:
                ts, bit, sid = validate_row(row)
            except Exception as e:
                raise ValueError(f"{input_path.name}: invalid row at line {i}: {e}") from e

            rows += 1
            dt = parse_iso8601(ts)
            tmin = dt if tmin is None else min(tmin, dt)
            tmax = dt if tmax is None else max(tmax, dt)
            source_counts[sid] = source_counts.get(sid, 0) + 1

            writer.writerow({"timestamp": ts, "bit": bit, "source_id": sid})

    prov = Provenance(
        filename=input_path.name,
        sha256=digest,
        rows=rows,
        time_min=tmin.isoformat() if tmin else None,
        time_max=tmax.isoformat() if tmax else None,
        source_counts=source_counts,
        warnings=warnings,
    )

    out_manifest.write_text(json.dumps(prov.__dict__, indent=2), encoding="utf-8")
    return out_csv, out_manifest


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Validate + normalize QRNG CSV logs")
    ap.add_argument("input_csv", type=str, help="Path to raw QRNG CSV")
    ap.add_argument("--processed-dir", type=str, default="data/processed", help="Output processed dir")
    ap.add_argument("--results-dir", type=str, default="results/qrng", help="Output provenance dir")
    args = ap.parse_args()

    out_csv, out_manifest = ingest_qrng_csv(
        input_path=Path(args.input_csv),
        processed_dir=Path(args.processed_dir),
        results_dir=Path(args.results_dir),
    )
    print(f"Validated CSV: {out_csv}")
    print(f"Provenance:    {out_manifest}")

