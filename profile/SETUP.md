# Make the profile look expensive — in ~25 minutes

The profile page (`github.com/Anuj-Phulera`) is built from five things, in order of impact:

| # | Lever | Impact | Time |
|---|---|---|---|
| 1 | **Pinned repositories** | ⭐⭐⭐⭐⭐ people actually look here | 2 min |
| 2 | **Repo descriptions + topics** | ⭐⭐⭐⭐⭐ makes everything findable | 8 min |
| 3 | **Profile README** (`Anuj-Phulera/Anuj-Phulera`) | ⭐⭐⭐⭐ the "wow" | 10 min |
| 4 | **Avatar, bio, links** | ⭐⭐⭐ sets the tone | 3 min |
| 5 | **Stats widgets** | ⭐⭐ garnish, not the meal | 1 min |

Most people do #5 first and #1 last. That's why most profiles look generic.

---

## Step 0 — Transfer and rename your 8 repos

A beautiful README pointing at empty pinned slots looks worse than a plain one.
Transfers keep stars, issues and history, and old URLs 301-redirect.

> Old account → repo → **Settings → General → Danger Zone → Transfer ownership** → `Anuj-Phulera`

Then rename each one → **Settings → Repository name**:

| Old name | New name |
|---|---|
| `S2S` | `Skill-Verse` |
| `Resonate-Portfolio` | `Resonate` |
| `VERDE-CBSE-APP` | `Verde-APP` |
| `Verde-CBSE` | `Verde-Portfolio` |
| `Nirmaan-Portfolio-` | `NIrman-Portfolio` |
| `nirmaan-app` | `Nirmaan-APP` |
| `Rakshbandhan` | `Rakshabandhan` |
| `verde-main-portfolio` | `Verde-Previous-Portfolio` |
| `WEBE` | keep as `WEBE` — DEEP FIELD is the flagship |

**Do not transfer** `Portfolio`, `Project`, `Altior`, `Hacking-Tool`, `Resonate-` —
empty repos and duplicates are the fastest way to make a profile look abandoned.

> GitHub is case-insensitive in URLs, so `NIrman-Portfolio` and `Nirman-Portfolio`
> land on the same repo. The capital `I` is cosmetic — no link breaks either way.

---

## Step 1 — Create the profile README repo

This is the trick: a repo named **exactly your username** becomes your profile page.

1. New repository
2. Owner: `Anuj-Phulera` · Name: **`Anuj-Phulera`** (same as your handle)
3. Public ✅ · Add a README file ✅
4. Create

GitHub will say: *"You found a secret! `Anuj-Phulera/Anuj-Phulera` is a special repository."*

> ⚠️ A **private** profile repo shows nothing. It must be public.

## Step 2 — Drop in the files

Everything you need is in `github-profile-shinobi.zip`. Unzip it, then either:

**Browser (no git):**
1. **Add file → Upload files** → drag all **11 SVGs** → Commit
2. Open `README.md` → ✏️ → select all → delete → paste the new contents → Commit

**Terminal:**
```bash
git clone https://github.com/Anuj-Phulera/Anuj-Phulera.git
cd Anuj-Phulera
cp /path/to/unzipped/*.svg .
cp /path/to/unzipped/README.md .
sed -i 's/YOUR_EMAIL/you@example.com/g' README.md
git add -A && git commit -m "the seal is set" && git push
```

**All eleven SVGs must sit loose in the repo root** — flat, next to README.md.
The README references them as `./opening.svg`. In a subfolder, they break.

## Step 3 — Pin your eight

Profile → **Customize your pins** → pick the eight project repos.

Order matters — it's read left to right, top row first. Recommended:

| Slot | Repo | Why |
|---|---|---|
| 1 | WEBE | the thesis project, has a live link |
| 2 | Verde-APP | shows security thinking + IoT |
| 3 | Nirmaan-APP | biggest full-stack build |
| 4 | Skill-Verse | shows scale |
| 5 | Verde-Portfolio | shows visual range |
| 6 | Resonate | shows design ambition |

Never pin more than one repo of the same project. Two Verde repos side by side
reads as one project built twice.

## Step 4 — Descriptions and topics

A repo with no description shows as just a name. With one, it shows as a *thing*.
Topics make you appear in GitHub search.

See **`repo-metadata.md`** — copy-paste descriptions and topics for all 8.

## Step 5 — Profile settings

Settings → Public profile:

- **Avatar** — a real photo, high contrast, legible at 32px
- **Bio** — one line, 160 characters:
  > Interface engineer. I build sites that rebuild themselves around the person using them. DEEP FIELD, VERDE, NIRMAAN.
- **Location** — Jaipur, India
- **Website** — your DEEP FIELD Pages URL
- **Social links** — X, LinkedIn, Vercel deployments
- **Include private contributions** ✅ if you want private work counted

---

## What separates a good profile from a great one

**Do**
- Make the first line a claim, not a job title ("I build X" beats "Full-stack developer")
- Link to **live URLs**, not just source — three live links beat thirty repos
- Keep one visual identity: one accent colour, one mono font, hairline rules
- Put your best work in slot 1 and never let it move

**Don't**
- Don't stack six widget cards — stats, streak, trophies, activity graph, wakatime, visitor counter. It reads as a template, not a person.
- Don't use a typing SVG that says "Passionate Developer 🚀"
- Don't pin empty repos
- Don't let the README be longer than the work it describes

---

## Why this kit has no shields.io badges

Those badge images are rendered by a third-party service. When it rate-limits —
and it does — your profile shows a row of broken-image icons, permanently.
`projects.svg` and `stats.svg` are plain SVG files in your own repo, so they
render on GitHub's CDN and can never break.
