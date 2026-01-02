"""
Test QRNG data contract validation.

Ensures the ingest validator enforces the contract strictly:
- Required columns must exist
- bit must be 0 or 1
- timestamp must parse as ISO 8601
- source_id must be non-empty and <= 64 chars
"""
from pathlib import Path
import csv
import json
import pytest
import sys

# Add code/inference to path
code_dir = Path(__file__).parent.parent / "code" / "inference"
sys.path.insert(0, str(code_dir))

from qrng_ingest import ingest_qrng_csv


def test_ingest_valid_csv(tmp_path: Path) -> None:
    """Test that a valid CSV is ingested correctly."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "timestamp,bit,source_id\n"
        "2026-01-01T00:00:00Z,0,nist_beacon\n"
        "2026-01-01T00:00:01Z,1,nist_beacon\n",
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    out_csv, out_manifest = ingest_qrng_csv(raw, processed_dir, results_dir)

    assert out_csv.exists()
    assert out_manifest.exists()

    # Check provenance
    with out_manifest.open("r", encoding="utf-8") as f:
        prov = json.load(f)
    assert prov["rows"] == 2
    assert prov["source_counts"]["nist_beacon"] == 2
    assert prov["time_min"] is not None
    assert prov["time_max"] is not None

    # Check validated CSV
    with out_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2
    assert rows[0]["bit"] == "0"
    assert rows[1]["bit"] == "1"


def test_ingest_rejects_bad_bit(tmp_path: Path) -> None:
    """Test that invalid bit values are rejected."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "timestamp,bit,source_id\n"
        "2026-01-01T00:00:00Z,2,nist_beacon\n",
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    with pytest.raises(ValueError, match="Invalid bit value"):
        ingest_qrng_csv(raw, processed_dir, results_dir)


def test_ingest_rejects_missing_column(tmp_path: Path) -> None:
    """Test that missing required columns are rejected."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "timestamp,bit\n"
        "2026-01-01T00:00:00Z,0\n",
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    with pytest.raises(ValueError, match="Missing required column"):
        ingest_qrng_csv(raw, processed_dir, results_dir)


def test_ingest_rejects_invalid_timestamp(tmp_path: Path) -> None:
    """Test that invalid timestamps are rejected."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "timestamp,bit,source_id\n"
        "not-a-timestamp,0,nist_beacon\n",
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    with pytest.raises(ValueError):
        ingest_qrng_csv(raw, processed_dir, results_dir)


def test_ingest_rejects_empty_source_id(tmp_path: Path) -> None:
    """Test that empty source_id is rejected."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "timestamp,bit,source_id\n"
        "2026-01-01T00:00:00Z,0,\n",
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    with pytest.raises(ValueError, match="Empty source_id"):
        ingest_qrng_csv(raw, processed_dir, results_dir)

