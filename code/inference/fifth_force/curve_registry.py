"""Select default constraint curve for evaluation."""

from pathlib import Path
from typing import Optional
from .registry import list_curves


def get_default_curve_path(
    processed_dir: Optional[Path] = None,
    prefer_zenodo: bool = True,
) -> Optional[Path]:
    """Get the default constraint curve path.

    Prefers real curves (zenodo*) over placeholder curves.

    Args:
        processed_dir: Directory to search (default: data/processed)
        prefer_zenodo: If True, prefer curves with "zenodo" in source_id

    Returns:
        Path to validated CSV, or None if no curves found
    """
    curves = list_curves(processed_dir)
    
    if not curves:
        return None
    
    # Prefer zenodo curves if requested
    if prefer_zenodo:
        zenodo_curves = [c for c in curves if "zenodo" in c["source_id"].lower()]
        if zenodo_curves:
            return zenodo_curves[0]["path"]
    
    # Otherwise return first available
    return curves[0]["path"]

