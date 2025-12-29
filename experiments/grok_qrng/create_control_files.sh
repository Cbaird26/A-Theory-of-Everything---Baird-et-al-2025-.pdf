#!/bin/bash
# Create control test files for pipeline validation
# Run this after installing dependencies: pip install -r requirements.txt

cd "$(dirname "$0")"
mkdir -p data/raw

echo "Creating CONTROL_random_200k.csv (known-fair coin)..."
python3 - <<'PY'
import numpy as np, pandas as pd
from pathlib import Path
bits = np.random.randint(0,2, size=200000, dtype=np.int8)
pd.DataFrame({"bit": bits}).to_csv("data/raw/CONTROL_random_200k.csv", index=False)
print("✓ Wrote data/raw/CONTROL_random_200k.csv")
PY

echo "Creating CONTROL_bias_p505_200k.csv (known-biased coin, p=0.505)..."
python3 - <<'PY'
import numpy as np, pandas as pd
from pathlib import Path
n = 200000
p = 0.505  # small but real bias
bits = (np.random.rand(n) < p).astype(np.int8)
pd.DataFrame({"bit": bits}).to_csv("data/raw/CONTROL_bias_p505_200k.csv", index=False)
print("✓ Wrote data/raw/CONTROL_bias_p505_200k.csv")
PY

echo ""
echo "Control files created. Now run:"
echo "  python analyze_qrng.py --data-dir data/raw --out-dir results --prior 1.0"
echo "  python sanity_checks.py --summary results/summary.csv --global results/global_summary.json"

