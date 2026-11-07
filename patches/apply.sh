#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# apply.sh — apply the audit-9 fixes to your local clones.
#
# I could not push these: this session's GitHub token is read-only on all nine
# repositories (empty OAuth scopes -> 403 "Resource not accessible by
# integration"). Run this yourself, or reconnect GitHub with write access.
#
# Usage:
#   ./apply.sh /path/to/S2S /path/to/Rakshbandhan /path/to/Nirmaan-Portfolio- /path/to/nirmaan-app
#   ./apply.sh            # or run it inside a parent folder containing the clones
#
# Every step is reversible. Nothing is deleted from history; files are only
# untracked, so `git reset --hard HEAD~1` undoes any single commit.
# ---------------------------------------------------------------------------
set -euo pipefail

S2S="${1:-S2S}"
RAKSH="${2:-Rakshbandhan}"
NIRMAAN_PORT="${3:-Nirmaan-Portfolio-}"
NIRMAAN_APP="${4:-nirmaan-app}"

NAME="UCHIHA-MADARA-ANUJ"
EMAIL="uchiha-madara-anuj@users.noreply.github.com"
C="git -c user.name=$NAME -c user.email=$EMAIL"

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

# ---------------------------------------------------------------------------
say "1/4  $S2S — remove hard-coded Supabase credentials"
# ---------------------------------------------------------------------------
if [ -d "$S2S/.git" ]; then
  cd "$S2S"
  if git apply --check ../../01-s2s-remove-hardcoded-credentials.patch 2>/dev/null; then
    git apply ../../01-s2s-remove-hardcoded-credentials.patch
  else
    echo "Patch did not apply cleanly - the file has probably changed."
    echo "Do it by hand: delete FALLBACK_URL / FALLBACK_ANON_KEY /"
    echo "FALLBACK_SERVICE_KEY from lib/supabase/server.ts and read env only."
  fi
  git add -A
  $C commit -q -m "security: remove hard-coded Supabase credentials

A service-role key was committed as a fallback. It bypasses row-level
security and grants full read/write access to every table. Credentials now
come from the environment only; callers already handle a null client."
  echo "committed: $(git log --oneline -1)"
  cd - >/dev/null
else
  echo "skip - $S2S not found"
fi

# ---------------------------------------------------------------------------
say "2/4  $RAKSH — stop committing .next/ and out/  (175 MB of the 209 MB)"
# ---------------------------------------------------------------------------
if [ -d "$RAKSH/.git" ]; then
  cd "$RAKSH"
  cat > .gitignore <<'EOF'
# dependencies
node_modules/

# next.js build output
.next/
out/
dist/

# misc
.DS_Store
*.pem
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env
.env
.env*.local
.vercel
*.tsbuildinfo
next-env.d.ts
EOF
  git rm -r --cached .next out -q 2>/dev/null || true
  git add .gitignore
  $C commit -q -m "chore: stop committing .next/ and out/

209 MB of repository, 175 MB of it webpack cache (227 tracked files,
largest 28.2 MB). Untracked; still present in history."
  echo "committed: $(git log --oneline -1)"
  cd - >/dev/null
else
  echo "skip - $RAKSH not found"
fi

# ---------------------------------------------------------------------------
say "3/4  $NIRMAAN_PORT — stop committing the exported out/ (14 MB)"
# ---------------------------------------------------------------------------
if [ -d "$NIRMAAN_PORT/.git" ]; then
  cd "$NIRMAAN_PORT"
  git rm -r --cached out -q 2>/dev/null || true
  $C commit -q -m "chore: stop committing out/

14 MB of static export tracked despite /out/ being in .gitignore."
  echo "committed: $(git log --oneline -1)"
  cd - >/dev/null
else
  echo "skip - $NIRMAAN_PORT not found"
fi

# ---------------------------------------------------------------------------
say "4/4  $NIRMAAN_APP — remove nested copy of the app and self-archives"
# ---------------------------------------------------------------------------
if [ -d "$NIRMAAN_APP/.git" ]; then
  cd "$NIRMAAN_APP"
  git rm -r --cached Nirmaan-App -q 2>/dev/null || true
  git rm --cached Nirmaan-App.zip -q 2>/dev/null || true
  git rm --cached Nirmaan-App/app.rar -q 2>/dev/null || true
  cat >> .gitignore <<'EOF'

# nested duplicate of this repo + archived copies of itself
Nirmaan-App/
Nirmaan-App.zip
*.rar

# exported AI prompt dumps
user_prompt-*.md
EOF
  git add .gitignore
  $C commit -q -m "chore: remove nested copy of the app and self-archives

2.6 MB copy of this repo inside itself, plus .zip and .rar archives."
  echo "committed: $(git log --oneline -1)"
  cd - >/dev/null
else
  echo "skip - $NIRMAAN_APP not found"
fi

# ---------------------------------------------------------------------------
cat <<'EOF'

--------------------------------------------------------------------
Done. Nothing has been pushed.

To push:
  for d in S2S Rakshbandhan Nirmaan-Portfolio- nirmaan-app; do
    git -C "$d" push origin main
  done

To reclaim the disk space (IRREVERSIBLE - rewrites history):
  git -C Rakshbandhan filter-repo --path .next --path out --invert-paths
  git -C Rakshbandhan push --force --all origin

STILL YOURS TO DO (I cannot rotate keys for you):
  [ ] Supabase -> Settings -> API -> rotate JWT secret  (project suxnpzpxlkhvpijpgdkh)
  [ ] Rotate the Gemini API key
  [ ] Set OTP_SECRET in nirmaan-app's environment
--------------------------------------------------------------------
EOF
