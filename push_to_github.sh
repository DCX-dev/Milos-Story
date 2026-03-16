#!/bin/bash
# Script to push Milo's Story to GitHub

echo "🚀 Pushing Milo's Story to GitHub..."
echo ""

# Update remote URL
echo "Setting remote URL..."
git remote set-url origin https://github.com/DCX-dev/Milos-Story.git

# Verify remote
echo ""
echo "Remote configured:"
git remote -v

# Ensure we're on main branch
echo ""
echo "Checking branch..."
git branch -M main

# Add all files (in case there are new ones)
echo ""
echo "Staging files..."
git add -A

# Check if there are changes to commit
if ! git diff --staged --quiet; then
    echo ""
    echo "Committing changes..."
    git commit -m "Update: Milo's Story platformer game

- Organized project structure (src/, screens/, assets/, data/, docs/, scripts/)
- Added comprehensive README with features and controls
- Added .gitignore for Python projects
- Added requirements.txt
- Added GitHub setup documentation"
fi

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Done! Check your repository at: https://github.com/DCX-dev/Milos-Story"
