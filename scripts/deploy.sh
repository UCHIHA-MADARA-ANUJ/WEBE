#!/usr/bin/env bash
set -e
# STRATA — deploy script for GitHub Pages
# Builds with basePath=/WEBE for org pages, preserves .nojekyll
echo "▸ Building STRATA for GitHub Pages (basePath=/WEBE)…"
GITHUB_PAGES=true npm run build
echo "▸ Ensuring GitHub Pages config…"
touch out/.nojekyll
# For SPA fallback — copy index to 404 for GH Pages deep links
cp out/index.html out/404.html 2>/dev/null || true
echo "▸ Build complete: out/ ready for gh-pages"
ls -lh out/*.html 2>&1 | head -5
echo "  lab: $(ls out/lab/index.html 2>&1 | head -1)"
