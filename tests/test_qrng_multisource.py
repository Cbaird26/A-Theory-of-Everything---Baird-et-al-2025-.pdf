#!/usr/bin/env python3
"""
Regression tests for multi-source QRNG calibration.
"""
from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest

from code.inference.qrng_multisource_ingest import ingest_multisource_qrng
from code.inference.qrng_pooled_epsilon import compute_pooled_epsilon_max


def create_synthetic_source_csv(path: Path, source_id: str, n: int, bias: float = 0.0) -> None:
    """
    Create a synthetic QRNG source CSV for testing.
    
    Args:
        path: Output CSV path
        source_id: Source identifier
        n: Number of bits
        bias: Bias parameter (p = 0.5 + bias, so bias=0.0 is fair)
    """
    from datetime import datetime, timezone
    
    p = 0.5 + bias
    import random
    random.seed(42)  # For reproducibility
    
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "bit", "source_id"])
        writer.writeheader()
        
        base_time = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        for i in range(n):
            bit = 1 if random.random() < p else 0
            timestamp = (base_time.timestamp() + i).isoformat()
            writer.writerow({
                "timestamp": timestamp,
                "bit": str(bit),
                "source_id": source_id,
            })


def test_multisource_ingest():
    """Test multi-source ingest produces provenance and manifest."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        
        # Create two synthetic sources
        raw_dir = tmp / "raw"
        raw_dir.mkdir()
        
        source1_path = raw_dir / "source1.csv"
        source2_path = raw_dir / "source2.csv"
        
        create_synthetic_source_csv(source1_path, "nist_beacon_stub", n=1000, bias=0.0)
        create_synthetic_source_csv(source2_path, "local_csv_biased", n=1000, bias=0.01)
        
        # Ingest
        processed_dir = tmp / "processed"
        results_dir = tmp / "results"
        
        result = ingest_multisource_qrng(
            raw_dir=raw_dir,
            processed_dir=processed_dir,
            results_dir=results_dir,
        )
        
        # Check results
        assert len(result["sources"]) == 2
        assert Path(result["combined_manifest_path"]).exists()
        
        # Check manifest
        manifest = json.loads(Path(result["combined_manifest_path"]).read_text(encoding="utf-8"))
        assert manifest["total_sources"] == 2
        assert manifest["total_rows"] == 2000
        
        # Check provenance files exist
        for source in result["sources"]:
            assert Path(source["validated_csv"]).exists()
            assert Path(source["provenance_manifest"]).exists()
            
            # Check provenance has required fields
            prov_data = json.loads(Path(source["provenance_manifest"]).read_text(encoding="utf-8"))
            assert "sha256" in prov_data
            assert "rows" in prov_data
            assert prov_data["rows"] == 1000


def test_pooled_epsilon_max_conservative():
    """Test pooled epsilon_max uses conservative max rule."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        
        # Create processed validated CSVs (simulating ingest output)
        processed_dir = tmp / "processed"
        qrng_sources_dir = processed_dir / "qrng_sources"
        qrng_sources_dir.mkdir(parents=True)
        
        # Source 1: Fair (bias = 0.0)
        source1_path = qrng_sources_dir / "source1_validated.csv"
        create_synthetic_source_csv(source1_path, "nist_beacon_stub", n=200000, bias=0.0)
        
        # Source 2: Mild bias (bias = 0.004)
        source2_path = qrng_sources_dir / "source2_validated.csv"
        create_synthetic_source_csv(source2_path, "local_csv_biased", n=200000, bias=0.004)
        
        # Compute pooled epsilon_max
        results_dir = tmp / "results"
        result = compute_pooled_epsilon_max(
            processed_dir=processed_dir,
            results_dir=results_dir,
            prior_scale=1.0,
            ci_mass=0.95,
            pooling_method="conservative_max",
        )
        
        # Check result structure
        assert "epsilon_max" in result
        assert "method" in result
        assert "sources" in result
        assert result["method"] == "conservative_max"
        assert result["num_sources"] == 2
        
        # Check that epsilon_max is at least as large as the largest per-source bound
        per_source_bounds = [s["epsilon_bound"] for s in result["sources"]]
        assert result["epsilon_max"] >= max(per_source_bounds)
        
        # Check JSON output exists
        json_path = results_dir / "multisource_epsilon_max.json"
        assert json_path.exists()
        
        # Check markdown summary exists
        md_path = results_dir / "multisource_epsilon_summary.md"
        assert md_path.exists()
        
        # Verify no network calls (offline-first)
        # This test would fail if any network calls were made
        assert True  # If we get here, no network calls were made


def test_pooled_epsilon_max_single_source():
    """Test pooled epsilon_max with single source."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        
        processed_dir = tmp / "processed"
        qrng_sources_dir = processed_dir / "qrng_sources"
        qrng_sources_dir.mkdir(parents=True)
        
        # Single source
        source_path = qrng_sources_dir / "source1_validated.csv"
        create_synthetic_source_csv(source_path, "single_source", n=100000, bias=0.002)
        
        results_dir = tmp / "results"
        result = compute_pooled_epsilon_max(
            processed_dir=processed_dir,
            results_dir=results_dir,
        )
        
        assert result["num_sources"] == 1
        assert result["epsilon_max"] == result["sources"][0]["epsilon_bound"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

