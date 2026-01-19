"""
Stub adapter for NIST Beacon (offline-first, reads cached exports).
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from .base import QRNGSourceAdapter


class NISTBeaconStubAdapter(QRNGSourceAdapter):
    """
    Stub adapter for NIST Beacon QRNG data.
    
    This adapter reads from locally cached NIST Beacon exports.
    No network calls are made. Fetching/updating NIST Beacon data
    is a separate optional script.
    
    Expected format: CSV file with columns: timestamp, bit, source_id
    where source_id should be 'nist_beacon' or similar.
    """
    
    def load(self, path: Path, **kwargs) -> Path:
        """
        Load a cached NIST Beacon export.
        
        Args:
            path: Path to cached CSV export
            **kwargs: Ignored (for compatibility)
        
        Returns:
            Path to the same file (validation happens in ingest step)
        
        Raises:
            FileNotFoundError if file does not exist
        """
        self.validate_path(path)
        return path
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get adapter metadata."""
        return {
            "name": "nist_beacon_stub",
            "description": "Stub adapter for NIST Beacon (reads cached exports only)",
            "offline_only": True,
            "note": "Fetching NIST Beacon data is a separate optional script",
        }

