"""Tests for fifth-force data contract enforcement."""

import csv
import json
import tempfile
from pathlib import Path
import pytest

from code.inference.fifth_force.ingest import ingest_fifth_force_csv


def test_ingest_valid_csv(tmp_path: Path) -> None:
    """Test that valid CSV is ingested correctly."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "lambda_m,alpha_max,source_id,ref\n"
        "1e-6,1e-8,test_source,doi:10.1234/test\n"
        "1e-5,1e-9,test_source,doi:10.1234/test\n"
        "1e-4,1e-10,test_source,doi:10.1234/test\n",
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    out_csv, out_manifest = ingest_fifth_force_csv(raw, processed_dir, results_dir)

    assert out_csv.exists()
    assert out_manifest.exists()

    with out_manifest.open("r", encoding="utf-8") as f:
        prov = json.load(f)
    
    assert prov["rows"] == 3
    assert prov["source_counts"]["test_source"] == 3
    assert prov["lambda_min"] == 1e-6
    assert prov["lambda_max"] == 1e-4


def test_ingest_rejects_non_monotonic_lambda(tmp_path: Path) -> None:
    """Test that non-monotonic lambda_m is rejected."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "lambda_m,alpha_max,source_id\n"
        "1e-6,1e-8,test_source\n"
        "1e-5,1e-9,test_source\n"
        "1e-4,1e-10,test_source\n"
        "1e-5,1e-11,test_source\n",  # Not monotonic
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    with pytest.raises(ValueError, match="not monotonic"):
        ingest_fifth_force_csv(raw, processed_dir, results_dir)


def test_ingest_rejects_negative_alpha_max(tmp_path: Path) -> None:
    """Test that negative alpha_max is rejected."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "lambda_m,alpha_max,source_id\n"
        "1e-6,-1e-8,test_source\n",
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    with pytest.raises(ValueError, match="must be positive"):
        ingest_fifth_force_csv(raw, processed_dir, results_dir)


def test_ingest_rejects_missing_column(tmp_path: Path) -> None:
    """Test that missing required columns are rejected."""
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "lambda_m,alpha_max\n"  # Missing source_id
        "1e-6,1e-8\n",
        encoding="utf-8",
    )

    processed_dir = tmp_path / "processed"
    results_dir = tmp_path / "results"

    with pytest.raises(ValueError, match="Missing required columns"):
        ingest_fifth_force_csv(raw, processed_dir, results_dir)

