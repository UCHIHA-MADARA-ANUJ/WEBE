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

npm ci
npm run build

git subtree push --prefix dist -f origin gh-pages

echo
echo "published → https://uchiha-madara-anuj.github.io/WEBE/"
echo "(enable Pages for this branch in Settings → Pages if it is not live yet)"
