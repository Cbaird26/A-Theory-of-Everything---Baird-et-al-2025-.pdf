#!/bin/bash
# Create SHA256 hash ledger for all data files
# Usage: ./create_sha256_ledger.sh [output_file]

set -e

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUTPUT="${1:-${REPO_ROOT}/results/DATA_LEDGER_SHA256.txt}"

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT")"

# Get commit hash
COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "N/A")

echo "Creating SHA256 ledger..."
echo "Repository: $REPO_ROOT"
echo "Commit: $COMMIT_HASH"
echo "Output: $OUTPUT"
echo ""

# Write header
cat > "$OUTPUT" << EOF
# MQGT-SCF Data Ledger (SHA256)
# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
# Commit: $COMMIT_HASH
#
# Format: SHA256  PATH
#

EOF

# Find all data files and compute hashes
find "$REPO_ROOT/data" -type f \( -name "*.csv" -o -name "*.json" \) -print0 | \
    xargs -0 shasum -a 256 >> "$OUTPUT"

echo "✅ Ledger created: $OUTPUT"
echo "   Total files: $(grep -v '^#' "$OUTPUT" | grep -v '^$' | wc -l | tr -d ' ')"

