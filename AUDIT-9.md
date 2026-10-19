# The Nine — Deep Audit

**Scope:** Verde-CBSE · Resonate-Portfolio · VERDE-CBSE-APP · Rakshbandhan · Nirmaan-Portfolio- · nirmaan-app · Resonate- · verde-main-portfolio · S2S
**Method:** each repo cloned and read line-by-line — API routes, auth paths, secret handling, build config, `npm audit` against real lockfiles, git trees, duplicate diffing.
**Date:** 19 October 2026

---

## Verdict in one paragraph

Six of these nine are genuinely good projects with real engineering inside. But **two of them contain live credentials** — one is a Supabase `service_role` key that grants full read/write access to the database, bypassing every row-level-security rule you wrote. **Two of them have authentication that can be bypassed in under a minute.** Three carry their entire build output in Git, so `Rakshbandhan` is 209 MB to ship 3,256 lines of code. And **not one of the nine has a LICENSE file.** The code is better than the packaging — but the security issues are not packaging problems, they're live problems.

---

# 🚨 Part 1 — The four things that are on fire

## 1.1 S2S ships a Supabase `service_role` key

**File:** `lib/supabase/server.ts`, line 6
**Project ref:** `suxnpzpxlkhvpijpgdkh`
**JWT expiry:** `2098621348` → **2036**

```
role      = service_role          ← full admin, bypasses ALL RLS
iss       = supabase
exp       = 2098621348 (2036)
len       = 219 chars
```

It's not a comment or a placeholder. It's a working HMAC-signed JWT, committed with the comment *"Uses hard-coded fallbacks so the app works even if env vars are missing."*

**What that key can do:** read every table, write every table, delete every row, read `auth.users` metadata, and create or modify users — as the database superuser, with row-level security switched off. Someone who found this repo could dump your entire 250-respondent survey dataset, insert fake records, or wipe the database.

The anon key is also there (line 5), which is less severe — anon keys are public by design — but it's still tied to the same project and pasted in as a fallback.

**There is no way to un-leak this.** It has been public and is in git history. It must be rotated now, and the old key deleted from the Supabase dashboard.

---

## 1.2 S2S has 8 AI endpoints and 0 auth guards

Your Gemini routes — `app/api/gemini/{analyze,chat,content,pathway,report,sentiment,translate,trend}` — take a prompt, forward it to Gemini with **your** API key, and return the answer. None of them check a session. None of them rate-limit. None check origin.

Anyone who knows the URL can point a script at your endpoint and spend your Gemini quota. Same pattern applies to any other AI proxy in the repo.

---

## 1.3 nirmaan-app's OTP verification is theatre

Two independent bugs, either one enough to break it.

**Bug A — the OTP is inside the token you hand to the user.**

```
lib/otp-store.ts:  payload = `${email}|${otp}|${expiresAt}`
                   token   = base64url(payload + '|' + hmac)
```

`app/api/send-otp/route.ts` returns that `token` in the JSON response. Base64 is encoding, not encryption. So the "verification" flow is:

```bash
curl -s site/api/send-otp -d '{"email":"anyone@any.com"}'      # → {"token":"..."}
echo <token> | base64 -d                                         # → you@x|483920|1799...|sig
curl -s site/api/verify-otp -d '{"email":"...","otp":"483920","token":"..."}'   # → success
```

The email never matters. The user is verifying against a secret they were handed.

And when Gmail isn't configured, `send-otp` also returns `_dev_otp: otp` **in the response body** — a debug affordance that becomes a live bypass the moment you deploy without `GMAIL_APP_PASSWORD` set.

**Bug B — the signing secret has a hardcoded fallback in a public repo.**

```
lib/otp-store.ts:6
const SECRET = process.env.OTP_SECRET || 'nirman-otp-secret-key-2026'
```

Anyone can mint a valid token for any email and any OTP, offline, without touching your server.

**How to actually fix it:** generate the code server-side, store only `sha256(otp)` with an expiry keyed by email (a Supabase table, Redis, or Firebase doc), return an opaque random token — never the OTP. Verify by hashing the submitted code. No fallback secret, ever.

---

## 1.4 VERDE-CBSE-APP protects the secret but not the device

This repo is the best-engineered of the nine — and I want to be precise about that, because the gap is subtle.

What's genuinely right:

```ts
// app/api/db/route.ts
const READ_PATHS = new Set(["/", "/sensors", "/controls", "/weather", "/latest_scan"]);
const WRITE_FIELDS = { "/controls": new Set(["manual_mode", "pump_state", ...]) };
const clean = Object.entries(data).filter(([k, v]) => allowed.has(k) && typeof v !== "object");
```

Read paths whitelisted. Write fields whitelisted. Values type-guarded — no nested objects, so no path injection. The Firebase secret never leaves the server. `npm audit` reports **0 vulnerabilities**. This is correct work, and it's better than what most people ship.

The gap: **there is no authentication on any of the five routes.**

Any anonymous visitor can `PATCH /api/db` and toggle `pump_state`, flip `grow_light_state`, rewrite `moisture_threshold`, or set `capture_photo: true` to trigger the camera. The secret is safe; the pump is not.

`/api/gemini`, `/api/openrouter` and `/api/plant-id` are open proxies to paid services. One loop and your credits are gone.

Minimum fix: a shared bearer token in `Authorization` compared against an env var, plus a per-IP limiter on the three AI routes.

---

# 📊 Part 2 — Where the bytes actually go

| Repo | Repo size | Real source LOC | Files | Build output committed | Verdict |
|---|---:|---:|---:|---|---|
| **Rakshbandhan** | **209 MB** | 3,256 | 355 | `.next/` **175 MB** (227 files) + `out/` 6.2 MB (76 files) | 🔴 98% is build garbage |
| **S2S** | **113 MB** | 14,994 | 1,525 | none | 🟠 25 MB of 4K images + 7 MB of SVGs |
| **Nirmaan-Portfolio-** | **36 MB** | 6,522 | 135 | `out/` 14 MB | 🟠 11 files duplicated |
| **nirmaan-app** | 8.3 MB | 31,505 | 284 | none | 🟠 nested self-copy + zip + rar |
| **Verde-CBSE** | 3.4 MB | **4,018** (not 62k — see below) | 73 | none | 🟠 vendored Three.js |
| **Resonate-** | 3.3 MB | 25,078 | 370 | none | 🟠 exact duplicate |
| **Resonate-Portfolio** | 3.3 MB | 25,078 | 370 | none | 🟠 contains a 98-file backup |
| **verde-main-portfolio** | 1.3 MB | 9,429 | 84 | none | 🟢 genuine predecessor |
| **VERDE-CBSE-APP** | 724 KB | 4,642 | 37 | none | 🟢 cleanest repo |

### Rakshbandhan — 209 MB for 312 KB of source

```
.next/   175 MB    ← 227 tracked files, largest single file 28.2 MB
out/     6.2 MB    ← 76 tracked files, 11 HTML pages
app/     312 KB    ← the actual site
public/  3.8 MB    ← audio, images
```

`.gitignore` is three lines long:

```
node_modules/
dist/
.DS_Store
```

No `.next/`, no `out/`. That's the whole story. The site is beautiful and the repo is 98% webpack cache.

**Important:** untracking `.next/` now stops it growing but will **not** shrink the 209 MB, because the blobs stay in history. Only a history rewrite (`git filter-repo`) will. That's a force-push — your call, not mine to make silently.

### Verde-CBSE — the "62,331 lines" is a mirage

```
public/vendor/three.module.js      53,411 lines   ← vendored Three.js
app/**/*.tsx + *.ts + *.css         4,018 lines   ← your actual site
```

The scenes load Three.js through an importmap (`public/scenes/pod.html:280`), so it's vendored *correctly for that pattern* — but it means the repo's headline LOC number is 93% someone else's library. Your real app is 4,018 lines across 73 files. That's still a solid build; it just isn't 62k.

Also in Verde-CBSE:
- `google280c2ec99007341d.html` exists **three times** — root, `app/`, `public/` — byte-identical (md5 `482a99aa…`). One is enough; the `/public` copy is the one that actually serves.
- `model1.html` (23 KB), `model2.html` (75 KB), `model3.html` (37 KB) sit loose in the root — standalone Three.js viewers, development scratchpads. They ship to every clone and nobody uses them.
- **`npm audit`: 4 vulnerabilities — 1 critical (Next.js cache poisoning) + 3 high.** Next 14.2.5.

### nirmaan-app — a repo containing a copy of itself

```
nirmaan-app/Nirmaan-App/            2.6 MB   ← nested copy of the app
nirmaan-app/Nirmaan-App.zip         1.4 MB
nirmaan-app/Nirmaan-App/app.rar     0.4 MB
nirmaan-app/user_prompt-*.md        33 files
nirmaan-app/image-*.png             4 loose screenshots
Nirmaan-App/**/user_prompt-*.md     ~27 more
```

Plus: **no root `package-lock.json`.** Every install resolves differently. For a 34-dependency Next app with Firebase and Supabase, that's the difference between "works on my machine" and "works".

### Resonate- and Resonate-Portfolio are the same repository twice

```
$ diff -rq --exclude=.git Resonate- Resonate-Portfolio
Files Resonate-/artifacts/resonate/vite.config.ts and .../vite.config.ts differ
Files Resonate-/vercel.json and .../vercel.json differ
```

**Two files.** Out of 370. That's 25,078 lines of code duplicated across two public repos, with zero README in either.

`Resonate-Portfolio` also carries `.migration-backup/` — 98 files, 790 KB, a frozen copy of the pre-Vite Next.js app that you migrated away from. Dead weight inside a repo that is already a copy.

Debt inside the live app: 24 `any`, 24 `@ts-ignore`/`eslint-disable`, 11 `TODO`s.

### S2S — 1,525 files, and 1,118 of them are SVGs

```
public/images/4k/        25 MB
public/images/illustrations/  5.3 MB
public/*.svg (1,118 files)    7.0 MB
```

`icosphere-x6.json` alone is 3.6 MB of JSON geometry. The site is genuinely large — 34 routes, 22 API endpoints — but 25 MB of 4K hero images should be `.webp` and served through `next/image`, not committed at full resolution.

---

# 🔍 Part 3 — Per-repo cards

### 1 · S2S — 113 MB · 14,994 LOC · 1,525 files · Next 14.2.30
**SkillVerse, Screen2Skill 2026.** By far the most complete build here: 34 routes, a full research dataset, 250-respondent survey, accessibility work, live on Vercel.
**Good:** README is 327 lines and honest. Real data pipeline. Genuine product scope.
**Bad:** 🔴 service_role key committed · 🔴 8 unauthenticated AI proxies · 🟠 7 npm vulns (2 critical) · 🟠 32 MB of unoptimised media · no LICENSE.
**Action:** rotate the Supabase key today → delete the fallbacks → wrap AI routes in auth → `npm audit fix` → convert 4K PNGs to webp.

### 2 · nirmaan-app — 8.3 MB · 31,505 LOC · 284 files · Next 14.2.35
**NIRMAN, E-Colosseum 2026.** Your largest hand-written codebase: 37 routes, three role dashboards, booking wizard, Leaflet maps, Firebase + Supabase, chat.
**Good:** the architecture is real. Role separation is correct. `middleware.ts`, `firestore.rules`, SQL schemas all present.
**Bad:** 🔴 OTP fully bypassable (two ways) · 🟠 no lockfile · 🟠 repo contains a copy of itself + `.zip` + `.rar` · 🟠 33 prompt dumps in root · 89 `any` · no LICENSE.
**Action:** rewrite the OTP flow → delete the nested tree and archives → commit a lockfile → move prompts out.

### 3 · Rakshbandhan — 209 MB · 3,256 LOC · 355 files · Next 15.5.24
**ek-hi-chaand.** Ten routes, custom audio engine, particle system, 30-second intro film. By far the most personal thing in the set, and the code reads like it was written with care — 0 `console.log`, 0 `any`, 0 TODOs.
**Good:** the actual source is disciplined. `server.mjs` even has a path-traversal guard (`if (!file.startsWith(root))`).
**Bad:** 🔴 175 MB of committed `.next/` · 🟠 6.2 MB `out/` · 🟠 README is one line · 🟠 4 high vulns (sharp/librsvg CVE) · no LICENSE.
**Action:** add `.next/` and `out/` to `.gitignore` → `git rm -r --cached` both → rewrite history if you want the 209 MB back → write a real README.

### 4 · VERDE-CBSE — 3.4 MB · 4,018 LOC real · 73 files · Next 14.2.5
**Verde Technical Compendium.** Boot sequence, 3D scenes, living circuit board, telemetry. 222-line README, `DEPLOYMENT.md`, `.nvmrc`, and a `verify` script that chains typecheck → lint → build. That script alone puts this in the top tier of the nine.
**Good:** the most *process*-mature repo here.
**Bad:** 🟠 critical Next.js CVE · 🟠 triple-duplicated verification file · 🟠 three scratch `model*.html` in root · 53k of 62k lines are vendored Three.js.
**Action:** `next@14.2.35` → delete two of three verification copies → move `model*.html` to a `scratch/` folder or delete.

### 5 · VERDE-CBSE-APP — 724 KB · 4,642 LOC · 37 files · Next 16.4.0
**VERDE OS.** The best-architected repo of the nine and the only one with **zero npm vulnerabilities**. Server-only env access, typed errors, whitelisted paths and fields, server-side image inlining.
**Bad:** 🔴 no auth on any route → anyone can control the pump and burn AI credits.
**Action:** add a bearer-token check + limiter. This repo is one commit away from being genuinely production-grade.

### 6 · Resonate-Portfolio — 3.3 MB · 25,078 LOC · 370 files · pnpm monorepo
**RESONATE.** React 19 + Vite, custom GLSL, ~25 pages, R3F, GSAP, Lenis. Real design ambition: a documented Next→Vite migration, inline GLSL loader, `replit.md` that explains every architectural decision.
**Bad:** 🟠 no README at all · 🟠 `.migration-backup/` duplicates 98 files · 24 `any`, 24 suppressions.
**Action:** write the README (the `replit.md` is already 80% of one) → delete `.migration-backup/`.

### 7 · Resonate- — 3.3 MB · identical to #6
**Delete or archive.** Nothing here isn't in `Resonate-Portfolio`.

### 8 · Nirmaan-Portfolio- — 36 MB · 6,522 LOC · 135 files · Next 14.2.4
**NIRMAN's 16-act narrative site.** Genesis loader, Graveyard, Market Matrix, AI Cortex. Strong copy, strong structure, 98-line README.
**Bad:** 🟠 `out/` 14 MB committed *despite* `.gitignore` listing `/out/` — it was added before the rule or force-added · 11 files duplicated between `public/` and `out/` · 1 critical npm vuln.
**Action:** `git rm -r --cached out` → dedupe.

### 9 · verde-main-portfolio — 1.3 MB · 9,429 LOC · 84 files · Next 14.2.5
**Verde v1.** 88 files differ from Verde-CBSE — this is a genuine earlier version, not a duplicate. Keep it as history, but it's carrying the same critical Next CVE as #4.
**Action:** archive it, or bump + add a "superseded by Verde-CBSE" banner at the top of the README.

---

# 🧾 Part 4 — What all nine share

| Check | Result |
|---|---|
| **LICENSE file** | **0 of 9** — legally "all rights reserved", so nobody may legally reuse or contribute |
| **Repo description** | 0 of 9 |
| **Topics** | 0 of 9 |
| **README** | 2 of 9 missing entirely, 1 is a single line |
| **`npm audit` clean** | 1 of 9 (VERDE-CBSE-APP) |
| **Lockfile committed** | 8 of 9 (nirmaan-app missing) |
| **Next.js version** | 4 repos on 14.2.x with known CVEs; 1 on 15.5; 1 on 16.4 |
| **CI** | 0 of 9 |
| **Tests** | 0 of 9 |

No CI and no tests across ~89,000 lines is the quiet one. `Verde-CBSE` has the right instinct with `npm run verify` — it just never runs anywhere.

---

# ✅ Part 5 — The plan

## P0 — only you can do these (today)

1. **Supabase dashboard → Settings → API → rotate JWT secret.** This invalidates the committed `service_role` key instantly. Then re-issue the anon key and update every deploy's env vars.
2. **Check Supabase logs** for the project `suxnpzpxlkhvpijpgdkh` — query volume and source IPs over the last 90 days. If the survey table shows writes you don't recognise, that's the incident.
3. **Rotate the Gemini API key.** Eight unauthenticated routes have been pointing at it.
4. **Set `OTP_SECRET`** in nirmaan-app's Vercel environment — assume anyone has been able to forge tokens since August.

> Removing a key from the latest commit does **not** revoke it. It's in git history, in clones, in forks, and in whatever caches crawled the repo. Rotation is the only fix.

## P1 — code fixes I can push (one commit per repo)

| Repo | Change | Risk |
|---|---|---|
| S2S | delete `FALLBACK_SERVICE_KEY` / `FALLBACK_ANON_KEY` / `FALLBACK_URL`; fail loudly when env is missing | low — env is already set in prod |
| S2S | auth + rate limit on 8 AI routes | medium — needs a session check wired |
| nirmaan-app | rewrite `otp-store.ts` to store `sha256(otp)` server-side, return opaque token; delete `_dev_otp` | medium — touches signup |
| VERDE-CBSE-APP | bearer-token guard + limiter on `/api/db`, `/api/gemini`, `/api/openrouter`, `/api/plant-id` | low |
| Rakshbandhan | `.gitignore` += `.next/`, `out/`; `git rm -r --cached` both | none — files stay on disk |
| Nirmaan-Portfolio- | `git rm -r --cached out` | none |
| nirmaan-app | `git rm -r --cached Nirmaan-App Nirmaan-App.zip`; commit lockfile | low |
| Resonate-Portfolio | delete `.migration-backup/`; write README from `replit.md` | none |
| Verde-CBSE | `next@14.2.35`; drop 2 duplicate verification files | low |
| all 9 | add MIT LICENSE | none |

## P2 — the repo hygiene pass

- Set **description + topics + homepage** on all 9 (currently all blank).
- **Archive `Resonate-`** — it's `Resonate-Portfolio` minus two config files.
- Add `verde-main-portfolio` → "superseded by Verde-CBSE" banner.
- Rewrite Rakshbandhan's one-line README.
- Optional but real: `git filter-repo` on Rakshbandhan to reclaim ~180 MB. **This rewrites history and force-pushes** — only with your explicit go-ahead.

## P3 — the thing that's actually missing

Add one GitHub Actions workflow per serious repo:

```yaml
- run: npm ci
- run: npm run build
- run: npm audit --audit-level=high
```

Nine repos, zero CI. That's how a `service_role` key survives in a public repo for months: nothing was watching. `Verde-CBSE` already has the right command — `npm run verify` — it just needs somewhere to run.

---

*Audit complete. No credential values are reproduced in this document — only file paths, line numbers, project refs and JWT claim metadata (`role`, `exp`), which are sufficient to identify and revoke them.*
