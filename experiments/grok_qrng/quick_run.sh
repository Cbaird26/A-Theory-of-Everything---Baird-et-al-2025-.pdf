#!/bin/bash
# Quick analysis for a single dataset
# Usage: ./quick_run.sh grok_run_01

if [ -z "$1" ]; then
    echo "Usage: ./quick_run.sh <run_name>"
    echo "Example: ./quick_run.sh grok_run_01"
    exit 1
fi

RUN_NAME="$1"
source .venv/bin/activate

echo "Analyzing: $RUN_NAME"
python analyze_qrng.py --data-dir "data/raw/$RUN_NAME" --out-dir "results/$RUN_NAME" --prior 1.0

echo "Running sanity checks..."
python sanity_checks.py --summary "results/$RUN_NAME/summary.csv" --global-json "results/$RUN_NAME/global_summary.json"

echo "Generating LaTeX snippet..."
python generate_latex_snippet.py --json "results/$RUN_NAME/global_summary.json" --out "results/$RUN_NAME/qrng_results_snippet.tex"

echo ""
echo "✓ Results ready: results/$RUN_NAME/"
echo "  - summary.csv"
echo "  - global_summary.json"
echo "  - qrng_results_snippet.tex"
