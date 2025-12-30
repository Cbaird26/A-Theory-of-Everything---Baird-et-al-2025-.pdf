#!/usr/bin/env bash
# Wait for PR merge, then verify automatically
set -euo pipefail

echo "=== Waiting for PR merge ==="
echo "Checking if closeout commits are on origin/main..."
echo ""

# Fetch latest
git fetch origin main

# Check if merge happened (look for closeout commit)
if git log origin/main --oneline | grep -q "closeout\|QRNG\|kernel\|GKLS\|Add post-merge"; then
    echo "✅ PR merge detected!"
    echo ""
    ./verify_merge.sh
else
    echo "⏳ PR not merged yet."
    echo ""
    echo "Please merge the PR in GitHub, then run:"
    echo "  ./verify_merge.sh"
    echo ""
    echo "Or run this script again to auto-detect and verify."
fi

