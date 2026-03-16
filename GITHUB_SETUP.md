# GitHub Setup Instructions

This guide will help you set up your GitHub repository for Milo's Story.

## Prerequisites

- Git installed on your system
- A GitHub account

## Step 1: Run the Setup Script

Make the setup script executable and run it:

```bash
chmod +x setup_github.sh
./setup_github.sh
```

Or manually initialize git:

```bash
git init
git add .
git commit -m "Initial commit: Milo's Story platformer game"
```

## Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name it something like `milos-story` or `milos-story-game`
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 3: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use one of these:

### Option A: HTTPS (easier, requires password/token)

```bash
git remote add origin https://github.com/YOUR_USERNAME/milos-story.git
git branch -M main
git push -u origin main
```

### Option B: SSH (requires SSH key setup)

```bash
git remote add origin git@github.com:YOUR_USERNAME/milos-story.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username and `milos-story` with your repository name.

## Step 4: Verify

Visit your repository on GitHub - you should see all your files!

## Future Updates

To push future changes:

```bash
git add .
git commit -m "Description of your changes"
git push
```

## What's Included

The repository includes:
- ✅ All source code (`src/`, `screens/`)
- ✅ Game assets structure (`assets/`)
- ✅ Documentation (`docs/`, `README.md`)
- ✅ Build scripts (`scripts/`)
- ✅ `.gitignore` to exclude unnecessary files
- ✅ `requirements.txt` for Python dependencies

## Excluded Files

The `.gitignore` file excludes:
- Python cache files (`__pycache__/`)
- Virtual environments (`.venv/`)
- Build artifacts (`build/`, `dist/`)
- Save game files (`data/save_data/*.json`)
- IDE files (`.vscode/`, `.idea/`)
- macOS system files (`.DS_Store`)

## Repository Settings

Consider enabling these on GitHub:
- **Issues**: For bug reports and feature requests
- **Discussions**: For community discussions
- **Wiki**: For additional documentation
- **Releases**: For version tags and releases

## License

Don't forget to add a license file! Common choices:
- MIT License (permissive)
- GPL-3.0 (copyleft)
- Apache 2.0 (permissive with patent grant)

You can add a license file later or when creating the repository.
