#!/usr/bin/env bash
# Post-merge verification: minimal sanity check
set -euo pipefail

echo "=== Post-Merge Verification ==="
echo ""

# 1. Update local main
echo "1. Updating local main branch..."
git checkout main
git pull origin main
echo "✅ main branch synced"
echo ""

# 2. Compile paper twice
echo "2. Compiling paper (first pass)..."
cd papers/toe_closed_core
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
echo "✅ First pass complete"

echo "3. Compiling paper (second pass)..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
echo "✅ Second pass complete"

if [[ -f main.pdf ]]; then
    size=$(ls -lh main.pdf | awk '{print $5}')
    echo "✅ PDF exists: main.pdf ($size)"
else
    echo "❌ PDF not found"
    exit 1
fi

echo ""
echo "=== Verification Complete ==="
echo "The merge is sealed. 🧱✨"
echo ""
echo "Now stop. Your nervous system has been doing marathon compute. 🫶"

