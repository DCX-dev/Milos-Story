#!/bin/bash
# Setup script for GitHub repository

echo "Setting up Git repository for Milo's Story..."

# Initialize git repository (if not already done)
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Configure git (you may want to customize these)
git config user.name "Team Banana Labs"
git config user.email "team@bananalabs.com"

# Add all files
echo "Staging files..."
git add .

# Create initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: Milo's Story platformer game

- Core game mechanics (player, enemies, boss)
- Arrow shooting system
- Level system with 10 levels
- Save/load functionality
- Title screen, victory screen, credits screen
- Music system with level-specific tracks
- Animated player sprites (GIF-based)
- Dynamic backgrounds"

echo ""
echo "✅ Git repository initialized and initial commit created!"
echo ""
echo "Next steps to push to GitHub:"
echo "1. Create a new repository on GitHub (github.com/new)"
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/milos-story.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Or if you prefer SSH:"
echo "   git remote add origin git@github.com:YOUR_USERNAME/milos-story.git"
echo "   git branch -M main"
echo "   git push -u origin main"
