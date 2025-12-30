"""
QRNG source adapters for multi-source calibration.

Each adapter converts source-specific data to a standardized format:
{timestamp, bit, source_id, meta}
"""
from .lfdr_adapter import load_lfdr_source
from .base_adapter import QRNGSourceAdapter, StandardizedQRNGData

__all__ = [
    'QRNGSourceAdapter',
    'StandardizedQRNGData',
    'load_lfdr_source',
]

