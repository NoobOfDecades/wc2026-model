#!/bin/bash
# WC2026 GitHub + Cloudflare Pages pipeline setup
# Run once from the directory containing index.html
# Requires: git, gh (GitHub CLI)

set -e
REPO_NAME="wc2026-model"
DEPLOY_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== WC2026 Deploy Setup ==="
echo "Deploy directory: $DEPLOY_DIR"
cd "$DEPLOY_DIR"

# Install gh CLI if missing
if ! command -v gh &>/dev/null; then
  echo "Installing GitHub CLI..."
  sudo apt-get update -qq && sudo apt-get install -y gh
fi

# Git init if needed
if [ ! -d .git ]; then
  git init
  git checkout -b main
fi

# Ensure index.html exists
if [ ! -f index.html ]; then
  echo "ERROR: index.html not found in $DEPLOY_DIR"
  echo "Rename your wc2026-full-vX.Y.Z.html to index.html and re-run."
  exit 1
fi

# Create .gitignore
cat > .gitignore << 'EOF'
*.pyc
__pycache__/
.env
node_modules/
.DS_Store
*.log
EOF

# Authenticate with GitHub (opens browser)
echo ""
echo "Authenticating with GitHub (browser will open)..."
gh auth login --hostname github.com --git-protocol https --web

# Create private repo and push
echo ""
echo "Creating private GitHub repo '$REPO_NAME'..."
gh repo create "$REPO_NAME" --private --source=. --remote=origin --push 2>/dev/null || {
  # Repo may already exist - just add remote and push
  git remote remove origin 2>/dev/null || true
  gh repo set-default
  GITHUB_USER=$(gh api user --jq .login)
  git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
  git add -A
  git commit -m "Initial deploy v5.2.6" 2>/dev/null || true
  git push -u origin main
}

# Create dev branch
git checkout -b dev 2>/dev/null || git checkout dev
git push -u origin dev 2>/dev/null || true
git checkout main

echo ""
echo "=== Done ==="
echo "Repo is live. Now connect Cloudflare Pages:"
echo "  1. Cloudflare dashboard → Workers & Pages → fifa26 → Settings → Builds & deployments"
echo "  2. Click 'Connect to Git' → select $REPO_NAME"
echo "  3. Branch: main → Production (model26.xyz)"
echo "  4. Branch: dev → Preview (auto URL)"
echo "  5. Build command: (leave empty)"
echo "  6. Output directory: / (root)"
GITHUB_USER=$(gh api user --jq .login 2>/dev/null || echo "YOUR_USERNAME")
echo ""
echo "Repo URL: https://github.com/$GITHUB_USER/$REPO_NAME"
