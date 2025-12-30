"""
Adapter for LFDR (Learning from Data Run) QRNG source.

Loads from global_summary.json format.
"""
import json
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import numpy as np

from .base_adapter import QRNGSourceAdapter, StandardizedQRNGData


def load_lfdr_source(path: Path) -> StandardizedQRNGData:
    """
    Load LFDR QRNG data from global_summary.json.
    
    Args:
        path: Path to global_summary.json
    
    Returns:
        StandardizedQRNGData
    """
    adapter = LFDRAdapter()
    return adapter.load(path)


class LFDRAdapter(QRNGSourceAdapter):
    """Adapter for LFDR QRNG source."""
    
    def __init__(self):
        super().__init__("lfdr_withinrun")
    
    def load(self, path: Path, **kwargs) -> StandardizedQRNGData:
        """Load LFDR data from JSON summary."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        n = data['n']
        k = data['k']
        
        # Create synthetic timestamps (since we only have aggregate stats)
        # Use sequential timestamps assuming uniform spacing
        timestamps = pd.Series(pd.date_range(
            start='2024-01-01',
            periods=n,
            freq='1s'  # 1 second intervals (adjustable)
        ))
        
        # Create bit sequence: k ones, (n-k) zeros
        bits = np.concatenate([
            np.ones(k, dtype=int),
            np.zeros(n - k, dtype=int)
        ])
        # Shuffle with fixed seed for reproducibility (seed set at module level or caller)
        # If seed not set, this will use current random state
        np.random.shuffle(bits)  # Shuffle to avoid ordering artifacts
        bits = pd.Series(bits)
        
        meta = {
            'n': n,
            'k': k,
            'p_hat': data.get('p_hat'),
            'epsilon_hat': data.get('epsilon_hat'),
            'epsilon_lower_95': data.get('epsilon_lower_95'),
            'epsilon_upper_95': data.get('epsilon_upper_95'),
            'bf10': data.get('BF10'),
            'original_path': str(path)
        }
        
        result = StandardizedQRNGData(
            timestamp=timestamps,
            bit=bits,
            source_id=self.source_id,
            meta=meta
        )
        
        if not self.validate(result):
            raise ValueError(f"Validation failed for {self.source_id}")
        
        return result

