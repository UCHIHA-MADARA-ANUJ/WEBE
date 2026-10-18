#!/usr/bin/env bash
set -e
# STRATA — deploy script for GitHub Pages
# Builds with basePath=/WEBE for org pages, preserves .nojekyll
echo "▸ Building STRATA for GitHub Pages (basePath=/WEBE)…"
GITHUB_PAGES=true npm run build
echo "▸ Ensuring GitHub Pages config…"
touch dist/.nojekyll
# For SPA fallback — copy index to 404 for GH Pages deep links
cp dist/index.html dist/404.html 2>/dev/null || true
echo "▸ Build complete: dist/ ready for gh-pages"
ls -lh dist/*.html 2>&1 | head -5
echo "  lab: $(ls dist/lab/index.html 2>&1 | head -1)"
