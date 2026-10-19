# Make the profile look expensive — in ~25 minutes

The profile page (`github.com/YOUR_USERNAME`) is built from five things, in order of impact:

| # | Lever | Impact | Time |
|---|---|---|---|
| 1 | **Pinned repositories** | ⭐⭐⭐⭐⭐ people actually look here | 2 min |
| 2 | **Repo descriptions + topics** | ⭐⭐⭐⭐⭐ makes everything findable | 8 min |
| 3 | **Profile README** (`username/username`) | ⭐⭐⭐⭐ the "wow" | 10 min |
| 4 | **Avatar, bio, links** | ⭐⭐⭐ sets the tone | 3 min |
| 5 | **Stats widgets** | ⭐⭐ garnish, not the meal | 1 min |

Most people do #5 first and #1 last. That's why most profiles look generic.

---

## Step 0 — Decide where your work lives

You're on a new account, so the profile is empty and every widget will show zeros. **A beautiful README pointing at nothing looks worse than a plain one.** Fix this first.

**Transfer** the 5–6 best repos from the old account (not forks — transfers keep stars, issues and history, and old URLs 301-redirect):

> Old account → repo → **Settings → General → Danger Zone → Transfer ownership** → new username

Transfer these, in this order:

1. `WEBE` — DEEP FIELD (your best work, live on Pages)
2. `Commit` — CommitQuest (polished, tested, self-contained)
3. `nirmaan-app` — NIRMAN (biggest full-stack build)
4. `S2S` — SkillVerse (largest codebase, live)
5. `VERDE-CBSE-APP` — VERDE OS (cleanest architecture)
6. `Resonate-Portfolio` — RESONATE

**Do not transfer** `Portfolio`, `Project`, `Altior`, `Hacking-Tool` — empty repos are the single fastest way to make a profile look abandoned. Leave them behind.

Once transferred, on the old account delete `Resonate-` (it's `Resonate-Portfolio` minus two files).

---

## Step 1 — Create the profile README repo

This is the trick: a repo named **exactly your username** becomes your profile page.

1. New repository
2. Owner: `YOUR_USERNAME` · Name: **`YOUR_USERNAME`** (same as your handle)
3. Public ✅ · Add a README file ✅
4. Create

GitHub will say: *"You found a secret! `YOUR_USERNAME/YOUR_USERNAME` is a special repository."*

> ⚠️ A **private** profile repo shows nothing. It must be public.

## Step 2 — Drop in the files

Copy `README.md` and `banner.svg` from this folder into that repo's root:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_USERNAME.git
cd YOUR_USERNAME
cp /path/to/profile/README.md .
cp /path/to/profile/banner.svg .
```

Then replace the placeholders everywhere at once:

```bash
sed -i 's/YOUR_USERNAME/actualusername/g; s/YOUR_EMAIL/you@example.com/g' README.md
git add -A && git commit -m "profile" && git push
```

`banner.svg` must sit **next to** README.md — the README references it as `./banner.svg`.

## Step 3 — Pin your six

Profile → **Customize your pins** → pick six.

Order matters — it's read left to right, top row first. Recommended:

| Slot | Repo | Why |
|---|---|---|
| 1 | WEBE | the thesis project, has a live link |
| 2 | nirmaan-app | shows full-stack + auth + maps + AI |
| 3 | Commit | shows polish, tests, zero-dependency engineering |
| 4 | S2S | shows scale |
| 5 | VERDE-CBSE-APP | shows security thinking |
| 6 | Resonate-Portfolio | shows visual range |

Never pin more than one repo of the same project. Six versions of Verde reads as one project built six times.

## Step 4 — Descriptions and topics (the unfashionable, highest-return step)

A repo with no description shows as just a name. With one, it shows as a *thing*. Topics make you appear in GitHub search.

See **`repo-metadata.md`** for copy-paste descriptions and topics for each repo.

## Step 5 — Profile settings

Settings → Public profile:

- **Avatar** — a real photo, high contrast, legible at 32px. Abstract art reads as a placeholder.
- **Bio** — one line, 160 characters, no emoji spam:
  > Interface engineer. I build sites that rebuild themselves around the person using them. DEEP FIELD, VERDE OS, NIRMAN.
- **Location** — Jaipur, India
- **Website** — your DEEP FIELD Pages URL (live links convert better than repos)
- **Social links** — X, LinkedIn, and your Vercel deployments
- **Include private contributions** ✅ if you do private work you want counted

---

## What separates a good profile from a great one

**Do**
- Make the first line a claim, not a job title ("I build X" beats "Full-stack developer")
- Link to **live URLs**, not just source — three live links beat thirty repos
- Keep one visual identity: one accent colour, one mono font, hairline rules
- Put your best work in slot 1 and never let it move

**Don't**
- Don't stack 6 widget cards — stats, streak, trophies, activity graph, wakatime, visitor counter. It reads as a template, not a person.
- Don't use a typing SVG that says "Passionate Developer 🚀" — it's the most-used header on GitHub
- Don't pin empty repos
- Don't let the README be longer than the work it describes

---

## Optional extras (only if you want them)

**Contribution snake** — fun, but needs a daily GitHub Action and a second branch. Add only after the rest is done.

**Activity graph** — one line under stats:
```html
<img src="https://github-readme-activity-graph.vercel.app/graph?username=YOUR_USERNAME&bg_color=06070A&color=9FB4FF&line=9FB4FF&point=E0B15C&hide_border=true" />
```

**Custom domain for DEEP FIELD** — `anujphulera.dev` pointing at the Pages site makes the profile link look deliberate instead of incidental.

---

## Reality check on the widgets

`github-readme-stats.vercel.app` is a free third-party service. It rate-limits, occasionally 502s, and GitHub caches images aggressively. If a card breaks, the README shows a broken-image icon — which looks worse than no card.

If you want a profile that never breaks: **delete the "By the numbers" section entirely.** The banner, the claim, and six pinned repos do all the work. The stats are decoration.
