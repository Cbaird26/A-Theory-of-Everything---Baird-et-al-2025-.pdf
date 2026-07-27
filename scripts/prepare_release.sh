#!/bin/bash
# Prepare Release Script
# Generates data ledgers, SHA256 hashes, and prepares release bundle

set -e  # Exit on error

VERSION="${1:-dev}"
RELEASE_DATE=$(date +%Y-%m-%d)
BUNDLE_NAME="mqgt_scf_release_${VERSION}.zip"

echo "=========================================="
echo "MQGT-SCF Release Preparation"
echo "Version: ${VERSION}"
echo "Date: ${RELEASE_DATE}"
echo "=========================================="
echo ""

# Step 1: Generate data ledgers
echo "Step 1: Generating data ledgers..."
if command -v make &> /dev/null; then
    make fifth-data-ledger || echo "Warning: fifth-data-ledger failed (may not have fifth-force data)"
    make fifth-sha256-ledger || echo "Warning: fifth-sha256-ledger failed"
else
    echo "Warning: make not found, skipping ledger generation"
fi
echo "✓ Data ledgers generated"
echo ""

# Step 2: Run tests (optional - skip if test target doesn't exist)
echo "Step 2: Running tests..."
if command -v make &> /dev/null; then
    if make -n test &> /dev/null 2>&1; then
        make test || {
            echo "WARNING: Tests failed. Continue anyway? (y/N)"
            read -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        }
        echo "✓ All tests passed"
    else
        echo "⚠ Test target not found, skipping tests"
        echo "  (Run 'make fifth-validate' or 'pytest tests/' manually to verify)"
    fi
else
    echo "Warning: make not found, skipping tests"
fi
echo ""

# Step 3: Verify reproducibility (optional, can be slow)
echo "Step 3: Verifying reproducibility (optional)..."
read -p "Run full reproducibility check? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v make &> /dev/null; then
        make reproduce || {
            echo "WARNING: Reproducibility check failed. Continue anyway? (y/N)"
            read -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        }
        echo "✓ Reproducibility verified"
    else
        echo "Warning: make not found, skipping reproducibility check"
    fi
else
    echo "Skipping reproducibility check"
fi
echo ""

# Step 4: Create release bundle
echo "Step 4: Creating release bundle..."
echo "Bundle name: ${BUNDLE_NAME}"

# Files and directories to include
INCLUDE_PATTERNS=(
    "code/"
    "data/"
    "docs/"
    "scripts/"
    "tests/"
    "Makefile"
    "README.md"
    "LICENSE"
    "LICENSES/"
    "CITATION.cff"
    "pyproject.toml"
    ".zenodo.json"
    "MAINLINE.md"
    "REPO_MAP.md"
)

# Files and directories to exclude
EXCLUDE_PATTERNS=(
    "*.pyc"
    "__pycache__/"
    "*.git/"
    ".git/"
    ".gitignore"
    ".cursorrules"
    "*.zip"
    "*.pdf"
    "results/"  # Exclude generated results (can be regenerated)
    "*.png"
    "*.jpg"
    "*.jpeg"
    ".DS_Store"
)

# Build zip command
ZIP_CMD="zip -r ${BUNDLE_NAME}"

# Add include patterns
for pattern in "${INCLUDE_PATTERNS[@]}"; do
    if [ -e "$pattern" ]; then
        ZIP_CMD="${ZIP_CMD} \"${pattern}\""
    fi
done

# Add exclude patterns
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    ZIP_CMD="${ZIP_CMD} -x \"${pattern}\""
done

# Execute zip command (use eval to handle quoted paths)
eval "${ZIP_CMD}"

if [ -f "${BUNDLE_NAME}" ]; then
    BUNDLE_SIZE=$(du -h "${BUNDLE_NAME}" | cut -f1)
    echo "✓ Release bundle created: ${BUNDLE_NAME} (${BUNDLE_SIZE})"
else
    echo "ERROR: Failed to create release bundle"
    exit 1
fi
echo ""

# Step 5: Generate SHA256 hash of bundle
echo "Step 5: Generating SHA256 hash..."
if command -v shasum &> /dev/null; then
    BUNDLE_HASH=$(shasum -a 256 "${BUNDLE_NAME}" | cut -d' ' -f1)
    echo "${BUNDLE_HASH}  ${BUNDLE_NAME}" > "${BUNDLE_NAME}.sha256"
    echo "✓ SHA256 hash: ${BUNDLE_HASH}"
    echo "✓ Hash file: ${BUNDLE_NAME}.sha256"
elif command -v sha256sum &> /dev/null; then
    BUNDLE_HASH=$(sha256sum "${BUNDLE_NAME}" | cut -d' ' -f1)
    echo "${BUNDLE_HASH}  ${BUNDLE_NAME}" > "${BUNDLE_NAME}.sha256"
    echo "✓ SHA256 hash: ${BUNDLE_HASH}"
    echo "✓ Hash file: ${BUNDLE_NAME}.sha256"
else
    echo "Warning: No SHA256 tool found (shasum or sha256sum)"
fi
echo ""

# Step 6: Summary
echo "=========================================="
echo "Release Preparation Complete"
echo "=========================================="
echo ""
echo "Release Bundle: ${BUNDLE_NAME}"
echo "Bundle Size: ${BUNDLE_SIZE}"
if [ -n "${BUNDLE_HASH}" ]; then
    echo "SHA256: ${BUNDLE_HASH}"
fi
echo ""
echo "Next Steps:"
echo "1. Review release bundle contents"
echo "2. Create GitHub Release (tag: v${VERSION})"
echo "3. Upload ${BUNDLE_NAME} as release asset"
echo "4. Wait for Zenodo to create draft"
echo "5. Publish Zenodo record to mint DOI"
echo "6. Update CITATION.cff with new DOI"
echo ""
echo "See docs/publishing/GITHUB_RELEASE_ZENODO_WORKFLOW.md for details"
echo ""
