#!/bin/bash

# Script to push mqgt-scf-paper to GitHub
# Make sure you've created the repository on GitHub first!

GITHUB_USER="Cbaird26"  # Update if different
REPO_NAME="mqgt-scf-paper"

echo "🚀 Pushing MQGT-SCF Paper to GitHub..."
echo "Repository: $GITHUB_USER/$REPO_NAME"
echo ""

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    echo "Remote 'origin' already exists. Updating..."
    git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
else
    echo "Adding remote 'origin'..."
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
fi

# Ensure we're on main branch
git branch -M main

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "📄 Repository: https://github.com/$GITHUB_USER/$REPO_NAME"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   1. The repository exists on GitHub: https://github.com/$GITHUB_USER/$REPO_NAME"
    echo "   2. You have push access"
    echo "   3. You're authenticated (git credential helper or SSH key)"
fi

