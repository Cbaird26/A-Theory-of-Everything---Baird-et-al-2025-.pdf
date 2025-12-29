#!/usr/bin/env bash
# Adaptive grid refinement script for island tomography
# Run multiple passes, zooming in on the viable region each time

set -euo pipefail

RESULTS_DIR="experiments/constraints/results"
SCRIPT="experiments/constraints/scripts/check_overlap_region.py"

echo "=== Island Tomography: Adaptive Grid Refinement ==="
echo ""

# Pass 1: Coarse scan
echo "Pass 1: Coarse scan (250x250 grid)"
python "$SCRIPT" \
  --lambda-min 1e-6 \
  --lambda-max 1.0 \
  --alpha-min 1e-12 \
  --alpha-max 1e-3 \
  --n-lambda 250 \
  --n-alpha 250 \
  --out-json "$RESULTS_DIR/overlap_island_summary_pass1.json"

# Extract p05/p95 from pass 1
if [ -f "$RESULTS_DIR/overlap_island_summary_pass1.json" ]; then
  echo ""
  echo "Pass 1 complete. Extract p05/p95 from JSON to set zoom bounds for pass 2."
  echo "Example:"
  echo "  python $SCRIPT \\"
  echo "    --lambda-min <p05_lambda> --lambda-max <p95_lambda> \\"
  echo "    --alpha-min <p05_alpha> --alpha-max <p95_alpha> \\"
  echo "    --n-lambda 400 --n-alpha 400 \\"
  echo "    --out-json $RESULTS_DIR/overlap_island_summary_refined.json"
  echo ""
  echo "Current pass 1 summary:"
  cat "$RESULTS_DIR/overlap_island_summary_pass1.json" | python -m json.tool | grep -A 5 "lambda_m\|alpha" || true
else
  echo "Error: Pass 1 output not found"
  exit 1
fi

echo ""
echo "To run pass 2, manually set zoom bounds based on pass 1 p05/p95 values."

