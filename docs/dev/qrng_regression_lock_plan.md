# QRNG Regression Lock + Data Contract Plan

This document is an engineering plan.
It specifies how to lock the QRNG calibration into automated regression tests,
and how to define a strict ingest contract for real QRNG logs.

---

## Step B: Regression Test Lock

### Current State

The BF10/CI logic is in `calibrate_qrng_physics.py`.

### Refactor Requirements

1. **Make the script import-safe:**

Ensure CLI code is guarded:

```py
if __name__ == "__main__":
    main()
```

Otherwise tests will execute the CLI on import and CI will explode.

2. **Extract BF10/CI into a pure function:**

Inside `calibrate_qrng_physics.py`:

```py
from __future__ import annotations
from typing import Tuple, Dict

def bf10_ci(k: int, n: int, prior_scale: float, ci_mass: float = 0.95) -> Tuple[float, float, float]:
    """
    Return (bf10, ci_low, ci_high) using the *existing* BF10 + CI logic.
    No math changes—just move the code into here.
    """
    # ---- paste your existing BF10 + CI computation here ----
    # must set: bf10, ci_low, ci_high
    return float(bf10), float(ci_low), float(ci_high)


def analyze_binomial(k: int, n: int, prior_scale: float = 1.0, ci_mass: float = 0.95) -> Dict[str, float]:
    """
    Convenience wrapper used by tests and downstream code.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if not (0 <= k <= n):
        raise ValueError("k must be in [0, n]")

    p_hat = k / n
    epsilon_hat = p_hat - 0.5
    bf10, ci_low, ci_high = bf10_ci(k, n, prior_scale, ci_mass)

    return {
        "n": float(n),
        "k": float(k),
        "p_hat": float(p_hat),
        "epsilon_hat": float(epsilon_hat),
        "bf10": float(bf10),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
    }
```

3. **Add the regression tests:**

Create: `tests/test_qrng_controls_regression.py`

```py
import pytest
from calibrate_qrng_physics import analyze_binomial

@pytest.mark.parametrize("prior_scale", [0.5, 1.0, 2.0])
def test_fair_control(prior_scale):
    n = 200_000
    k = n // 2
    r = analyze_binomial(k, n, prior_scale)
    assert r["bf10"] < (1.0 / 3.0)
    assert r["ci_low"] <= 0.0 <= r["ci_high"]

@pytest.mark.parametrize("prior_scale", [0.5, 1.0, 2.0])
def test_biased_control(prior_scale):
    n = 200_000
    k = 101_000  # p=0.505
    r = analyze_binomial(k, n, prior_scale)
    assert r["bf10"] > 10.0
    assert r["ci_low"] > 0.0
```

4. **Run tests:**

```bash
pytest -q
```

5. **Commit:**

```
test: lock QRNG control calibration
```

---

## Step C: Data Contract for Real QRNG Logs

### Schema Definition

Create `docs/qrng_data_contract.md` with schema:

- `timestamp`: ISO 8601
- `bit`: 0 or 1
- `source_id`: string (e.g., 'nist_beacon')

### Ingest Validation

Create `qrng_ingest.py` to validate logs against schema before processing.

This ensures real logs produce clean outputs with zero ambiguity.

### Example Contract

```python
from typing import Dict, List
from datetime import datetime
import pandas as pd

def validate_qrng_log(df: pd.DataFrame) -> bool:
    """
    Validate QRNG log against data contract.
    
    Required columns:
    - timestamp: ISO 8601 format
    - bit: 0 or 1
    - source_id: string identifier
    
    Returns True if valid, raises ValueError if invalid.
    """
    required_cols = ['timestamp', 'bit', 'source_id']
    
    # Check columns exist
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Validate timestamp format
    try:
        pd.to_datetime(df['timestamp'])
    except Exception as e:
        raise ValueError(f"Invalid timestamp format: {e}")
    
    # Validate bit values
    if not df['bit'].isin([0, 1]).all():
        raise ValueError("bit column must contain only 0 or 1")
    
    # Validate source_id
    if df['source_id'].isna().any():
        raise ValueError("source_id cannot be null")
    
    return True
```

