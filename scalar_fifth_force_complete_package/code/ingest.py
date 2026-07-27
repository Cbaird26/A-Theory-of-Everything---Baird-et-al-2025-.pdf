"""Validate and ingest fifth-force constraint curves.

Enforces the data contract, generates provenance manifests, and writes validated CSVs.
"""

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

REQUIRED_COLUMNS = ["lambda_m", "alpha_max", "source_id"]


@dataclass
class Provenance:
    """Provenance metadata for a constraint curve."""

    filename: str
    sha256: str
    rows: int
    lambda_min: Optional[float]
    lambda_max: Optional[float]
    source_counts: Dict[str, int]
    warnings: list


def sha256_file(path: Path) -> str:
    """Compute SHA256 hash of file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_row(row: Dict[str, str], row_num: int) -> Tuple[float, float, str]:
    """Validate a single row against schema.

    Returns:
        (lambda_m, alpha_max, source_id)

    Raises:
        ValueError: if validation fails
    """
    # Check required columns
    for col in REQUIRED_COLUMNS:
        if col not in row:
            raise ValueError(f"Missing required column: {col}")

    # Parse lambda_m
    try:
        lambda_m = float(row["lambda_m"])
        if lambda_m <= 0:
            raise ValueError(f"lambda_m must be positive, got {lambda_m}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid lambda_m value: {e}") from e

    # Parse alpha_max
    try:
        alpha_max = float(row["alpha_max"])
        if alpha_max <= 0:
            raise ValueError(f"alpha_max must be positive, got {alpha_max}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid alpha_max value: {e}") from e

    # Validate source_id
    source_id = row["source_id"].strip()
    if not source_id:
        raise ValueError("source_id cannot be empty")
    if len(source_id) > 64:
        raise ValueError(f"source_id too long (max 64 chars), got {len(source_id)}")

    return lambda_m, alpha_max, source_id


def ingest_fifth_force_csv(
    input_path: Path,
    processed_dir: Path,
    results_dir: Path,
) -> Tuple[Path, Path]:
    """Validate and ingest a fifth-force constraint CSV.

    Args:
        input_path: Path to raw CSV file
        processed_dir: Directory for validated outputs
        results_dir: Directory for provenance manifests

    Returns:
        (out_csv_path, out_manifest_path)

    Raises:
        ValueError: if validation fails
    """
    processed_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    # Compute file hash
    digest = sha256_file(input_path)

    # Output paths
    stem = input_path.stem
    out_csv = processed_dir / f"{stem}_validated.csv"
    out_manifest = results_dir / f"{stem}_provenance.json"

    # Track metadata
    rows = 0
    lambda_vals = []
    source_counts: Dict[str, int] = {}
    warnings = []

    # Validate and write
    with input_path.open("r", encoding="utf-8", newline="") as f_in, out_csv.open(
        "w", encoding="utf-8", newline=""
    ) as f_out:
        reader = csv.DictReader(f_in)
        header = reader.fieldnames
        if not header:
            raise ValueError("CSV file is empty or missing header")

        # Check required columns
        missing = set(REQUIRED_COLUMNS) - set(header or [])
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        writer = csv.DictWriter(
            f_out,
            fieldnames=REQUIRED_COLUMNS + ["ref"],
            extrasaction="ignore",
        )
        writer.writeheader()

        prev_lambda = None

        for i, row in enumerate(reader, start=2):
            try:
                lambda_m, alpha_max, sid = validate_row(row, i)

                # Check monotonicity
                if prev_lambda is not None and lambda_m <= prev_lambda:
                    raise ValueError(
                        f"lambda_m not monotonic: {lambda_m} <= {prev_lambda} at row {i}"
                    )
                prev_lambda = lambda_m

                lambda_vals.append(lambda_m)
                source_counts[sid] = source_counts.get(sid, 0) + 1

                # Write validated row
                output_row = {
                    "lambda_m": lambda_m,
                    "alpha_max": alpha_max,
                    "source_id": sid,
                }
                if "ref" in row and row["ref"].strip():
                    output_row["ref"] = row["ref"].strip()

                writer.writerow(output_row)
                rows += 1

            except Exception as e:
                raise ValueError(f"{input_path.name}: invalid row at line {i}: {e}") from e

    # Create provenance manifest
    prov = Provenance(
        filename=input_path.name,
        sha256=digest,
        rows=rows,
        lambda_min=min(lambda_vals) if lambda_vals else None,
        lambda_max=max(lambda_vals) if lambda_vals else None,
        source_counts=source_counts,
        warnings=warnings,
    )

    out_manifest.write_text(json.dumps(prov.__dict__, indent=2), encoding="utf-8")
    return out_csv, out_manifest


def main():
    """CLI entry point."""
    import argparse

    ap = argparse.ArgumentParser(description="Ingest and validate fifth-force constraint CSV")
    ap.add_argument("input", type=Path, help="Input CSV file")
    ap.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed"),
        help="Output directory for validated CSVs",
    )
    ap.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results/fifth_force"),
        help="Output directory for provenance manifests",
    )

    args = ap.parse_args()

    try:
        out_csv, out_manifest = ingest_fifth_force_csv(
            args.input, args.processed_dir, args.results_dir
        )
        print(f"✅ Validated: {out_csv}")
        print(f"✅ Provenance: {out_manifest}")
    except Exception as e:
        print(f"❌ Error: {e}", file=__import__("sys").stderr)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

