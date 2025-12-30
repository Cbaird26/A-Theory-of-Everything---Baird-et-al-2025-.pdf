#!/usr/bin/env bash
# Continuously monitor for PR merge, then auto-verify
set -euo pipefail

echo "=== Monitoring for PR merge ==="
echo "Will auto-verify when merge is detected..."
echo "Press Ctrl+C to stop monitoring"
echo ""

CHECK_COUNT=0
MAX_CHECKS=60  # Check for up to 5 minutes (60 * 5 seconds)

while [ $CHECK_COUNT -lt $MAX_CHECKS ]; do
    CHECK_COUNT=$((CHECK_COUNT + 1))
    
    # Fetch latest
    git fetch origin main >/dev/null 2>&1
    
    # Check if merge happened
    if git log origin/main --oneline | grep -q "closeout\|QRNG\|kernel\|GKLS\|Add post-merge\|toe-closeout"; then
        echo ""
        echo "✅✅✅ PR MERGE DETECTED! ✅✅✅"
        echo ""
        echo "Running verification..."
        echo ""
        ./verify_merge.sh
        exit 0
    fi
    
    # Show progress every 10 checks
    if [ $((CHECK_COUNT % 10)) -eq 0 ]; then
        echo "  Still waiting... (checked $CHECK_COUNT times)"
    fi
    
    sleep 5
done

echo ""
echo "⏳ Monitoring stopped. PR not merged yet."
echo "Please merge the PR in GitHub, then run: ./verify_merge.sh"

