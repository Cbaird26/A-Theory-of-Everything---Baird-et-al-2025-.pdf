"""
Base class for QRNG source adapters.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional


class QRNGSourceAdapter(ABC):
    """
    Abstract base class for QRNG source adapters.
    
    All adapters must be offline-first: they read from locally cached files.
    No network calls are allowed in adapters.
    """
    
    @abstractmethod
    def load(self, path: Path, **kwargs) -> Path:
        """
        Load a QRNG source and return path to validated CSV.
        
        Args:
            path: Path to source file (or cached location)
            **kwargs: Additional adapter-specific options
        
        Returns:
            Path to validated CSV file (must conform to QRNG data contract)
        
        Raises:
            FileNotFoundError if source file is not found
            ValueError if source file is invalid
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this adapter.
        
        Returns:
            Dictionary with keys like 'name', 'description', 'offline_only', etc.
        """
        pass
    
    def validate_path(self, path: Path) -> None:
        """
        Validate that the path exists and is readable.
        
        Raises:
            FileNotFoundError if path does not exist
        """
        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

