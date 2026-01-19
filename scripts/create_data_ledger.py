#!/usr/bin/env python3
"""
Create data ledger for MQGT-SCF datasets.

Generates a CSV ledger tracking all datasets with SHA256 hashes,
provenance information, and commit hashes for reproducibility.
"""

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import subprocess


def sha256_file(path: Path) -> str:
    """Compute SHA256 hash of file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def get_git_commit_hash(repo_path: Path) -> Optional[str]:
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def find_datasets(data_dir: Path) -> List[Dict[str, str]]:
    """Find all dataset files in data directory."""
    datasets = []
    
    # Find all CSV files in data/raw and data/processed
    for pattern in ["**/*.csv", "**/*.json"]:
        for path in data_dir.rglob(pattern):
            if path.is_file():
                rel_path = path.relative_to(data_dir.parent)
                datasets.append({
                    "path": str(rel_path),
                    "full_path": str(path),
                    "type": "raw" if "raw" in str(rel_path) else "processed",
                })
    
    return datasets


def load_provenance(provenance_path: Path) -> Optional[Dict]:
    """Load provenance JSON if it exists."""
    if provenance_path.exists():
        try:
            with provenance_path.open() as f:
                return json.load(f)
        except Exception:
            return None
    return None


def create_ledger(
    repo_root: Path,
    output_path: Path,
    data_dir: Path = None,
) -> None:
    """Create the data ledger CSV."""
    if data_dir is None:
        data_dir = repo_root / "data"
    
    if not data_dir.exists():
        print(f"Warning: data directory not found: {data_dir}")
        return
    
    # Get git commit hash
    commit_hash = get_git_commit_hash(repo_root)
    
    # Find all datasets
    datasets = find_datasets(data_dir)
    
    # Create ledger entries
    ledger_rows = []
    
    for dataset in datasets:
        path = Path(dataset["full_path"])
        
        # Compute hash
        sha256 = sha256_file(path) if path.exists() else "N/A"
        
        # Try to load provenance
        provenance = None
        if dataset["type"] == "processed":
            # Look for corresponding provenance JSON
            prov_path = path.parent / f"{path.stem}_provenance.json"
            if not prov_path.exists():
                # Try alternative naming
                prov_path = path.parent / f"{path.stem.replace('_validated', '')}_provenance.json"
            provenance = load_provenance(prov_path)
        
        # Extract metadata
        source_id = provenance.get("source_id", "unknown") if provenance else "unknown"
        ref = provenance.get("ref", "") if provenance else ""
        rows = provenance.get("rows", "") if provenance else ""
        time_range = ""
        if provenance:
            if "time_min" in provenance and "time_max" in provenance:
                time_range = f"{provenance['time_min']} to {provenance['time_max']}"
        
        ledger_rows.append({
            "path": dataset["path"],
            "type": dataset["type"],
            "sha256": sha256,
            "source_id": source_id,
            "ref": ref,
            "rows": rows,
            "time_range": time_range,
            "commit_hash": commit_hash or "N/A",
            "last_updated": datetime.now().isoformat(),
        })
    
    # Write CSV
    if ledger_rows:
        fieldnames = [
            "path", "type", "sha256", "source_id", "ref",
            "rows", "time_range", "commit_hash", "last_updated"
        ]
        
        with output_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ledger_rows)
        
        print(f"Data ledger created: {output_path}")
        print(f"  Total datasets: {len(ledger_rows)}")
        print(f"  Commit hash: {commit_hash or 'N/A'}")
    else:
        print("No datasets found.")


def main():
    """Main entry point."""
    ap = argparse.ArgumentParser(
        description="Create MQGT-SCF data ledger"
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory (default: current directory)"
    )
    ap.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Data directory (default: repo_root/data)"
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=Path("results/DATA_LEDGER.csv"),
        help="Output CSV path (default: results/DATA_LEDGER.csv)"
    )
    
    args = ap.parse_args()
    
    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    create_ledger(
        repo_root=args.repo_root,
        output_path=args.output,
        data_dir=args.data_dir,
    )


if __name__ == "__main__":
    main()

