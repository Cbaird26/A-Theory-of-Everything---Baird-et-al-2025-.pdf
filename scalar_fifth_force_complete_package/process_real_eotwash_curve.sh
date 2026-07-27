#!/bin/bash
# Process Real Eöt-Wash Digitized Curve
# Automates Steps 2-5: Ingest, Detectability, Canonical Statement, Updates
#
# Usage: ./process_real_eotwash_curve.sh
# (Run from within the package folder, or from repo root)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# CSV file path relative to package folder
CSV_FILE="data_raw/eotwash_prl2016_digitized_contract.csv"

echo "=== Processing Real Eöt-Wash Digitized Curve ==="
echo ""

# Check if CSV exists
if [ ! -f "$CSV_FILE" ]; then
    echo "❌ ERROR: Digitized CSV not found: $CSV_FILE"
    echo ""
    echo "Please complete Step 1 (digitization) first:"
    echo "  1. Use WebPlotDigitizer to digitize Eöt-Wash PRL 2016 curve"
    echo "  2. Save as: $CSV_FILE"
    echo "  3. See: docs/dev/eotwash_digitization_guide.md for instructions"
    exit 1
fi

echo "✓ Found digitized CSV: $CSV_FILE"
echo ""

# Step 2: Ingest
echo "=== Step 2: Ingesting Digitized Curve ==="
echo "Note: This script expects to be run from the repo root, not the package folder."
echo "If running from package folder, you'll need to adjust paths or run from repo root."
echo ""
echo "From repo root, run:"
echo "  make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv"
echo "  make fifth-detectability SEED=42 NPTS=2000"
echo ""
echo "Or copy the CSV to the repo location first."
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# Check if we're in repo root (has Makefile)
if [ -f "Makefile" ]; then
    make fifth-ingest INPUT="data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv"
    echo "✓ Ingestion complete"
    echo ""
    
    # Step 3: Rerun Detectability
    echo "=== Step 3: Rerunning Detectability Analysis ==="
    make fifth-detectability SEED=42 NPTS=2000
    echo "✓ Detectability analysis complete"
    echo ""
    
    # Step 4: Extract key statistics for canonical statement
    echo "=== Step 4: Extracting Statistics ==="
    RESULTS_FILE="results/fifth_force/detectability_summary.md"
else
    echo "⚠ Not in repo root. Please run from repo root or manually execute:"
    echo "  make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv"
    echo "  make fifth-detectability SEED=42 NPTS=2000"
    echo ""
    RESULTS_FILE=""
fi

if [ -f "$RESULTS_FILE" ]; then
    echo "✓ Results file: $RESULTS_FILE"
    echo ""
    echo "Key statistics:"
    grep -A 5 "| Threshold" "$RESULTS_FILE" | head -6
    echo ""
    echo "Top 5 points (non-excluded):"
    grep -A 6 "| m_phi_GeV" "$RESULTS_FILE" | head -7 | tail -6
    echo ""
else
    echo "⚠ Warning: Results file not found: $RESULTS_FILE"
fi

# Step 5: Reminder about document updates
echo "=== Step 5: Document Updates Needed ==="
echo ""
echo "Next steps (manual):"
echo "  1. Review results/fifth_force/detectability_summary.md"
echo "  2. Update docs/fifth_force_detectability_summary.md with:"
echo "     - Real curve source (eotwash_prl2016_digitized)"
echo "     - Updated statistics"
echo "     - Canonical statement: 'Scalar not detected; not ruled out; maximally testable at λ ≈ ___ mm'"
echo "  3. Update docs/fifth_force_summary.md (add note about real curve)"
echo "  4. Update data/raw/fifth_force/README.md (mark digitized curve as complete)"
echo ""
echo "See: docs/dev/eotwash_digitization_guide.md for full workflow"
echo ""
echo "=== Processing Complete ==="
echo ""
echo "Check results/fifth_force/detectability_summary.md for updated analysis"

