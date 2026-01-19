"""
Adapter for local CSV files conforming to QRNG data contract.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from .base import QRNGSourceAdapter


class LocalCSVAdapter(QRNGSourceAdapter):
    """
    Adapter for local CSV files that already conform to the QRNG data contract.
    
    This adapter simply validates that the file exists and can be read.
    The actual validation against the contract is done by qrng_ingest.
    """
    
    def load(self, path: Path, **kwargs) -> Path:
        """
        Load a local CSV file.
        
        Args:
            path: Path to CSV file
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
            "name": "local_csv",
            "description": "Adapter for local CSV files conforming to QRNG data contract",
            "offline_only": True,
        }

