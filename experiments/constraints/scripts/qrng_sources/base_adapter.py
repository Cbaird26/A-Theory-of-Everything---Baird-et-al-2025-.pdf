"""
Base classes for QRNG source adapters.
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class StandardizedQRNGData:
    """Standardized QRNG data format."""
    timestamp: pd.Series  # Timestamps for each trial
    bit: pd.Series  # Binary outcomes (0 or 1)
    source_id: str  # Identifier for the source
    meta: Dict[str, Any]  # Source-specific metadata
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame for analysis."""
        return pd.DataFrame({
            'timestamp': self.timestamp,
            'bit': self.bit,
            'source_id': self.source_id
        })


class QRNGSourceAdapter:
    """Base class for QRNG source adapters."""
    
    def __init__(self, source_id: str):
        self.source_id = source_id
    
    def load(self, path: Path, **kwargs) -> StandardizedQRNGData:
        """
        Load source data and convert to standardized format.
        
        Args:
            path: Path to source data
            **kwargs: Source-specific options
        
        Returns:
            StandardizedQRNGData
        """
        raise NotImplementedError("Subclasses must implement load()")
    
    def validate(self, data: StandardizedQRNGData) -> bool:
        """Validate standardized data format."""
        if not isinstance(data.timestamp, pd.Series):
            return False
        if not isinstance(data.bit, pd.Series):
            return False
        if len(data.timestamp) != len(data.bit):
            return False
        if not data.bit.isin([0, 1]).all():
            return False
        return True

