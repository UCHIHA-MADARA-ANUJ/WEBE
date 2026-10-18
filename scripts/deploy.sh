#!/usr/bin/env bash
# Publish DEEP FIELD to GitHub Pages.
#
#   ./scripts/deploy.sh
#
# Builds the app and force-pushes it to the `gh-pages` branch, which is what
# GitHub Pages serves for a project site at
# https://<owner>.github.io/<repo>/.
#
# One-time setup (repo owner, in Settings → Pages):
#   Source: Deploy from a branch → gh-pages / (root)
set -euo pipefail

cd "$(dirname "$0")/.."
REPO_ROOT="$(pwd)"

npm run build

# publish from a throwaway repository so the working tree is never touched
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
cp -r dist/. "$STAGE/"
touch "$STAGE/.nojekyll"

(
  cd "$STAGE"
  git init -q
  git add -A
  git -c user.name="Arena Agent" -c user.email="agent@arena.ai" commit -q -m "publish: DEEP FIELD build"
  git remote add origin "https://github.com/UCHIHA-MADARA-ANUJ/WEBE.git"
  git push -f origin HEAD:gh-pages
)

cd "$REPO_ROOT"
echo
echo "published → https://uchiha-madara-anuj.github.io/WEBE/"
echo "(enable Pages for this branch in Settings → Pages if it is not live yet)"
