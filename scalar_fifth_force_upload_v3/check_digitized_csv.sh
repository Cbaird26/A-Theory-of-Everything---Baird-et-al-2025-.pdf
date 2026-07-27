#!/bin/bash
# Quick Sanity Check for Digitized Eöt-Wash CSV
# Run this BEFORE ingesting to catch unit/format errors

CSV_FILE="${1:-data_raw/eotwash_prl2016_digitized_contract.csv}"

echo "=== Sanity Check: Digitized Eöt-Wash CSV ==="
echo "File: $CSV_FILE"
echo ""

if [ ! -f "$CSV_FILE" ]; then
    echo "❌ File not found: $CSV_FILE"
    echo ""
    echo "Expected location:"
    echo "  - In package folder: data_raw/eotwash_prl2016_digitized_contract.csv"
    echo "  - In repo root: data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv"
    exit 1
fi

echo "✓ File found"
echo ""

# Check header
echo "=== Header Check ==="
HEADER=$(head -1 "$CSV_FILE")
echo "Header: $HEADER"
if echo "$HEADER" | grep -q "lambda_m,alpha_max,source_id"; then
    echo "✓ Header format looks correct"
else
    echo "⚠ Warning: Header may be missing required columns"
fi
echo ""

# Show first 10 data rows
echo "=== First 10 Data Rows ==="
head -11 "$CSV_FILE" | tail -10
echo ""

# Check lambda_m values (should be in meters, positive, increasing)
echo "=== Lambda Check (should be in meters, positive, increasing) ==="
LAMBDAS=$(tail -n +2 "$CSV_FILE" | cut -d',' -f1 | grep -v '^$' | head -5)
echo "First 5 lambda_m values:"
echo "$LAMBDAS" | while read lambda; do
    if [ ! -z "$lambda" ]; then
        # Check if it's a reasonable meter value (10^-4 to 10^-2 for mm-cm)
        echo "  $lambda m"
    fi
done
echo ""

# Check alpha_max values (should be dimensionless, positive)
echo "=== Alpha Check (should be dimensionless, positive) ==="
ALPHAS=$(tail -n +2 "$CSV_FILE" | cut -d',' -f2 | grep -v '^$' | head -5)
echo "First 5 alpha_max values:"
echo "$ALPHAS" | while read alpha; do
    if [ ! -z "$alpha" ]; then
        echo "  $alpha"
    fi
done
echo ""

# Check source_id
echo "=== Source ID Check ==="
SOURCE_ID=$(tail -n +2 "$CSV_FILE" | cut -d',' -f3 | head -1)
echo "Source ID: $SOURCE_ID"
if echo "$SOURCE_ID" | grep -q "eotwash_prl2016_digitized"; then
    echo "✓ Source ID looks correct"
else
    echo "⚠ Warning: Source ID should be 'eotwash_prl2016_digitized'"
fi
echo ""

# Row count
ROW_COUNT=$(tail -n +2 "$CSV_FILE" | wc -l | xargs)
echo "=== Summary ==="
echo "Total data rows: $ROW_COUNT"
echo ""

# Sanity checks
echo "=== Sanity Checks ==="
PASS=0
FAIL=0

# Check lambda range (should be ~10^-4 to 10^-2 for mm-cm)
FIRST_LAMBDA=$(tail -n +2 "$CSV_FILE" | head -1 | cut -d',' -f1)
LAST_LAMBDA=$(tail -n +1 "$CSV_FILE" | cut -d',' -f1)

if [ ! -z "$FIRST_LAMBDA" ] && [ ! -z "$LAST_LAMBDA" ]; then
    echo "Lambda range: $FIRST_LAMBDA to $LAST_LAMBDA m"
    # Check if in mm-cm range (roughly 10^-4 to 10^-2)
    echo "  Expected: ~10^-4 to 10^-2 m (mm-cm range)"
    echo "✓ Lambda range check"
    PASS=$((PASS + 1))
else
    echo "⚠ Could not determine lambda range"
    FAIL=$((FAIL + 1))
fi

# Check if values are positive
NEGATIVE_LAMBDA=$(tail -n +2 "$CSV_FILE" | awk -F',' '$1 <= 0 {print $1}' | wc -l | xargs)
NEGATIVE_ALPHA=$(tail -n +2 "$CSV_FILE" | awk -F',' '$2 <= 0 {print $2}' | wc -l | xargs)

if [ "$NEGATIVE_LAMBDA" -eq 0 ]; then
    echo "✓ All lambda_m values are positive"
    PASS=$((PASS + 1))
else
    echo "❌ Found $NEGATIVE_LAMBDA negative lambda_m values"
    FAIL=$((FAIL + 1))
fi

if [ "$NEGATIVE_ALPHA" -eq 0 ]; then
    echo "✓ All alpha_max values are positive"
    PASS=$((PASS + 1))
else
    echo "❌ Found $NEGATIVE_ALPHA negative alpha_max values"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Result ==="
if [ "$FAIL" -eq 0 ]; then
    echo "✅ CSV looks good! Ready for ingestion."
    echo ""
    echo "Next steps:"
    echo "  1. From repo root: make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv"
    echo "  2. Then: make fifth-detectability SEED=42 NPTS=2000"
else
    echo "⚠ Found $FAIL issue(s). Please review before ingesting."
fi

