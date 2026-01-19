#!/usr/bin/env python3
"""
Multi-Source QRNG Ingest Pipeline

Validates multiple independent QRNG sources, produces per-source provenance,
and generates a combined manifest.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from .qrng_ingest import ingest_qrng_csv, Provenance


def ingest_multisource_qrng(
    raw_dir: Path,
    processed_dir: Path,
    results_dir: Path,
    source_pattern: str = "*.csv",
) -> Dict[str, Any]:
    """
    Ingest all QRNG sources from a directory.
    
    Args:
        raw_dir: Directory containing raw source CSV files
        processed_dir: Directory for validated CSV outputs
        results_dir: Directory for provenance manifests
        source_pattern: Glob pattern for source files (default: "*.csv")
    
    Returns:
        Dictionary with 'sources' list and 'combined_manifest_path'
    
    Raises:
        ValueError if any source fails validation
    """
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)
    results_dir = Path(results_dir)
    
    processed_dir.mkdir(parents=True, exist_ok=True)
    provenance_dir = results_dir / "provenance"
    provenance_dir.mkdir(parents=True, exist_ok=True)
    
    source_files = sorted(raw_dir.glob(source_pattern))
    if not source_files:
        raise ValueError(f"No source files found in {raw_dir} matching {source_pattern}")
    
    sources: List[Dict[str, Any]] = []
    
    for source_file in source_files:
        # Use per-source subdirectories to avoid name conflicts
        source_processed_dir = processed_dir / "qrng_sources"
        source_processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Ingest this source using existing validator
        validated_csv, provenance_manifest = ingest_qrng_csv(
            input_path=source_file,
            processed_dir=source_processed_dir,
            results_dir=provenance_dir,
        )
        
        # Load provenance to get metadata
        prov_data = json.loads(provenance_manifest.read_text(encoding="utf-8"))
        
        # Extract source_id from the validated CSV (first row after header)
        source_id = None
        if validated_csv.exists():
            with validated_csv.open("r", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) > 1:  # Has header + at least one data row
                    import csv
                    reader = csv.DictReader(lines)
                    for row in reader:
                        source_id = row.get("source_id", "unknown")
                        break
        
        sources.append({
            "source_id": source_id or source_file.stem,
            "raw_file": str(source_file),
            "validated_csv": str(validated_csv),
            "provenance_manifest": str(provenance_manifest),
            "sha256": prov_data.get("sha256"),
            "rows": prov_data.get("rows", 0),
            "time_min": prov_data.get("time_min"),
            "time_max": prov_data.get("time_max"),
            "source_counts": prov_data.get("source_counts", {}),
        })
    
    # Write combined manifest
    combined_manifest = {
        "ingest_timestamp": None,  # Will be set by caller if needed
        "sources": sources,
        "total_sources": len(sources),
        "total_rows": sum(s.get("rows", 0) for s in sources),
    }
    
    manifest_path = results_dir / "multisource_manifest.json"
    manifest_path.write_text(
        json.dumps(combined_manifest, indent=2),
        encoding="utf-8"
    )
    
    return {
        "sources": sources,
        "combined_manifest_path": str(manifest_path),
    }


if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser(description="Ingest multiple QRNG sources")
    ap.add_argument(
        "--raw-dir",
        type=str,
        default="data/raw/qrng_sources",
        help="Directory containing raw source CSVs",
    )
    ap.add_argument(
        "--processed-dir",
        type=str,
        default="data/processed",
        help="Directory for validated CSVs",
    )
    ap.add_argument(
        "--results-dir",
        type=str,
        default="results/qrng",
        help="Directory for provenance manifests",
    )
    ap.add_argument(
        "--pattern",
        type=str,
        default="*.csv",
        help="Glob pattern for source files",
    )
    args = ap.parse_args()
    
    result = ingest_multisource_qrng(
        raw_dir=Path(args.raw_dir),
        processed_dir=Path(args.processed_dir),
        results_dir=Path(args.results_dir),
        source_pattern=args.pattern,
    )
    
    print(f"Ingested {len(result['sources'])} sources")
    print(f"Combined manifest: {result['combined_manifest_path']}")

