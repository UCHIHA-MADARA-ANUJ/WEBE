# Patches — the 9 repos

**Status:** written, tested locally, **not pushed.** This session's GitHub token is read-only on every repository except `WEBE` (empty OAuth scopes → `403 Resource not accessible by integration`).

Two ways forward:

- **You run them** — `cd patches && ./apply.sh /path/to/clones`
- **You reconnect GitHub with write access in Arena**, tell me, and I'll push all four commits myself.

---

## What's in here

| File | Repo | Change | Risk |
|---|---|---|---|
| `01-s2s-remove-hardcoded-credentials.patch` | S2S | Deletes the project URL, anon key and **service_role key** fallbacks; env-only. Adds `SECURITY.md`. | none — `createServiceClient()` has zero callers, and `createSupabaseServer()` already returns `null` safely |
| `apply.sh` step 2 | Rakshbandhan | `.gitignore` += `.next/`, `out/`; untracks both | none — files stay on disk |
| `apply.sh` step 3 | Nirmaan-Portfolio- | untracks `out/` (14 MB) | none |
| `apply.sh` step 4 | nirmaan-app | untracks the nested `Nirmaan-App/` copy, `.zip`, `.rar` | none |
| `AUDIT-9.md` (repo root) | — | the full audit | — |

All four commits were made and verified locally against real clones before being turned into patches.

---

## Why the S2S patch is safe

```ts
// before
const FALLBACK_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIs...";  // service_role, exp 2036
const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY || FALLBACK_SERVICE_KEY;

// after
const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!url || !serviceKey) return null;
```

`createServiceClient()` is defined but **never called anywhere in the repo** — I grepped. `createSupabaseServer()` is called by `auth/session` and `auth/signup`, and both already handle a `null` return (`if (supabase) { ... }`). So there is no runtime change beyond the credentials no longer being embedded.

---

## What I deliberately did **not** do

These change live behaviour and need matching client-side changes, so they're yours to green-light:

| Repo | Fix | Why I held |
|---|---|---|
| nirmaan-app | OTP rewrite — store `sha256(otp)` server-side, return an opaque token, drop `_dev_otp`, remove the `'nirman-otp-secret-key-2026'` fallback | The signup client reads `token` and `_dev_otp` from the response; server-only changes would break signup |
| VERDE-CBSE-APP | Bearer-token guard + rate limit on `/api/db`, `/api/gemini`, `/api/openrouter`, `/api/plant-id` | Needs the dashboard to send the token; a half-done guard locks you out of your own pump |
| All 9 | MIT LICENSE, descriptions, topics, homepage | Cosmetic-but-permanent authorship choice — yours to make |
| Rakshbandhan | `git filter-repo` to reclaim ~180 MB | Force-push, irreversible |

---

## The one thing no patch can fix

Rotating the Supabase `service_role` key. It's in git history, in every clone, and in whatever has crawled the repo. Removing it from the working tree does not revoke it.

**Supabase → project `suxnpzpxlkhvpijpgdkh` → Settings → API → Rotate JWT secret.**

Until that's done, the key is still valid.
