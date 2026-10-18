# DEEP FIELD

**A living atlas of the cosmos — a website with no fixed interface.**

DEEP FIELD is a web application that observes how you move through it and then
rebuilds *itself* around that behaviour. Not its colours, not its fonts: its
**layout paradigm, information hierarchy, available actions, element placement
and navigation model** are all decided at runtime by an engine that is watching
you.

Two people who interact with it differently will end up navigating structurally
different versions of the same website. A third visit starts from a different
place again, because the site remembers.

> Live site: **[uchiha-madara-anuj.github.io/WEBE](https://uchiha-madara-anuj.github.io/WEBE)**
> Source: **github.com/UCHIHA-MADARA-ANUJ/WEBE**

### Proof, not promise

`node scripts/live-check.mjs` drives the built site in a real browser with two
visitors and shows the same URL becoming two different applications:

```
▌ HURRIED VISITOR
  PASS  structure changed on its own — constellation → mosaic
  PASS  it moved to a dense board — paradigm=mosaic
  PASS  it explained itself — You sweep the surface — the interface unfolded
        out of Constellation and into Mosaic.
  PASS  status bar reports the read — mosaic · read skimmer 73% · gen 2 · 6 seen

▌ PATIENT VISITOR
  PASS  structure changed on its own — constellation → codex
  PASS  it moved to a reading column — paradigm=codex
  PASS  status bar reports the read — codex · read reader 66% · gen 1 · 3 seen
```

One visitor who clicks without reading gets a dense, re-sorting **mosaic
board**. One who opens an object, lingers, and follows a relation gets a
single-column **codex**. Nobody chose that. The engine decided, and it told
them why.

---

## 1. What the site actually is

A curated knowledge graph of **35 objects** in astronomy and cosmology
(`src/content/graph.ts`) — quasars, gravitational lensing, the cosmic microwave
background, magnetars, the Event Horizon Telescope — wired together by **79
typed relations** (`origin-of`, `evidence-for`, `powered-by`, `measured-by`,
`contrasts-with` …). The content is real and accurate; the engine never edits
it. The engine reorganises *everything around it*.

---

## 2. The Evolution Engine

### 2.1 What it tracks

Eleven continuous features are derived from the raw event stream every time the
interface re-renders (`src/engine/classify.ts`):

| feature | what it measures | why it matters |
|---|---|---|
| `linearity` | share of moves between objects that follow a stated relation | a reader follows the graph, a scouter ignores it |
| `breadth` | distinct objects ÷ objects opened | wide vs. deep |
| `revisit` | share of opens that are re-opens | comparison vs. consumption |
| `volume` | how much of the corpus has been touched | one object vs. many |
| `dwell` | milliseconds of attention per object | reading vs. skimming |
| `cadence` | mean gap between two objects (0.4 s → 1, 4 s → 0) | impatience |
| `scan` | motion in px/s — scroll **or** pointer travel | skimming vs. settling |
| `command` | share of actions that were typed verbs | pointer vs. keyboard |
| `spatial` | share of actions that were drags / zooms | map-thinking vs. list-thinking |
| `query` | share of actions that were searches or filters | interrogation |
| `edge` | share of travel done by an explicit relation link | graph-navigation |

Two details matter more than they look:

- **Motion is not only scrolling.** In the Constellation nothing scrolls, so a
  visitor can move the cursor quickly and the page never moves. The engine
  therefore tracks pointer velocity as well and takes the faster of the two as
  `scan` — otherwise a map-shaped paradigm would make every visitor look
  sedentary. Single-event cursor teleports are discarded, so a flick of the
  wrist counts as motion but a programmatic jump does not.
- **`edge` means an explicit relation, not an arrival.** Clicking a node on the
  map is a *jump*; only pressing a relation chip (in the dossier, the mosaic
  sheet, the lattice) counts as travelling by relation. Without that
  distinction every click on the map would look like graph-navigation and the
  engine would never learn that someone is wandering.

The raw counters behind them (opens, relation steps, cross-field jumps, scroll
pixels, peak velocity, focus time, elapsed time, commands, queries, filters and
every action counter) are all visible in the **Mind panel**, so the algorithm
is never a black box.

### 2.2 How it decides

**Step 1 — score.** Each of six archetypes has an *ideal signature* (a target
value for every feature) and a set of weights saying how much it cares about
each one. The engine scores an archetype by **affinity**: how close the
visitor's normalised features are to that ideal, weighted by the archetype's
concern.

```
affinity(feature) = 1 − |actual − ideal| / max(ideal, 1 − ideal)
score(archetype)  = Σ weight × affinity / Σ weight
```

| archetype | behaviour | wants |
|---|---|---|
| **Reader** ¶ | lingers, follows one thread deep | a reading column |
| **Contemplative** ◐ | reads one thing for a long time | a single full-bleed object |
| **Scout** ✦ | hops widely, jumps between distant relatives | a spatial map |
| **Skimmer** ≈ | scrolls fast, skims surfaces | a dense, re-sorting board |
| **Analyst** ⊞ | filters, queries, re-reads, compares | a two-pane instrument |
| **Commander** ❯ | drives the site by keyboard | a command prompt |

**Step 2 — verify.** Some archetypes are defined by the *absence* of behaviour
and a single stray click can fake them, so every read must clear an
evidentiary bar before it is allowed to become the headline: a Contemplative
needs ≥ 5 s of real attention; a Commander needs ≥ 2 typed commands; a Skimmer
needs ≥ 2 fast scroll bursts **or** an impatient cadence (objects opened less
than a second apart). If the winning read is not credible, the engine falls
through to the next credible one.

**Step 3 — decide, conservatively.** The engine only restructures when the
read is confident (≥ 0.42) and the margin over the runner-up is clear (≥ 0.05),
and never more than once every 9 seconds. A wrong restructure is far more
damaging than a late one, so it holds its nerve.

**Step 4 — act.** The chosen archetype maps to a structural paradigm, the
interface cross-fades into it, and a **reconfiguration manifest** appears
stating exactly what changed and why:

> *You sweep — the interface unfolded out of Constellation and into Mosaic.*
> **layout** Constellation → Mosaic · **verbs** scan, peek, filter, shuffle ·
> **promoted** Inflation, Accretion Disk, Quasar · **because** scroll velocity
> sits at 84 % of the fast band…

### 2.3 The six structural states

These are not skins. Each one is a **different interaction contract** — a
different DOM, a different navigation model, different affordances, different
keyboard grammar.

| paradigm | contract |
|---|---|
| **Codex** § | *One column, one entry at a time.* The universe is folded into a thin rail; navigation is sequential; `j`/`k` walk the route. |
| **Constellation** ✧ | *A map you fly through.* Nothing is a list, everything is a position. Pan, zoom, trace relations by hovering, double-click to fly. |
| **Mosaic** ▦ | *A dense board that re-tiles itself.* Tiles physically slide to new positions as your interest shifts (FLIP animation). |
| **Lattice** ⊟ | *Index on the left, evidence on the right.* Sortable, filterable, with a comparison strip for holding several objects at once. |
| **Console** ❯ | *A text interface that talks back.* No chrome — a prompt. The set of valid verbs changes as the engine learns what you want. |
| **Zen** ◍ | *One object, full bleed.* No index, no rail, no alternatives. Only: go deeper, return, or let the site choose. |

### 2.4 What else changes besides the layout

The engine also mutates the site continuously, not just at the moment of a
switch:

- **Information hierarchy** — objects are re-ranked by an interest vector
  (tags weighted by dwell time), so the promoted entries change as you read.
- **Element placement** — the Mosaic board re-sorts every 2.6 s and tiles
  animate to their new coordinates; the Constellation force-layout is seeded
  from your own generation seed, so *your map is not the same map*.
- **Available actions** — the Console's command set grows as behaviour unlocks
  (`chapters` at generation 4, `compare` at generation 3); the top bar's primary
  action changes from *Enter* to *Follow your trail* to *Resume* as the engine
  decides what you are likely to want next.
- **Your route** — a `TRAIL` is computed greedily over the graph from your
  cumulative interest, always preferring unseen and high-affinity neighbours.
- **The vocabulary** — the verbs the site offers differ per paradigm
  (*continue / back / branch* in a Codex, *scan / peek / shuffle* in a Mosaic).

### 2.5 Procedural state across visits

Everything is stored in `localStorage` under `deepfield.genome.v2`
(`src/engine/genome.ts`). Each visit increments a **generation** counter, and
each generation unlocks behaviour and re-seeds the arrangement:

| generation | unlocks |
|---|---|
| 1 | the base six paradigms, interest model, generation log |
| 2 | **TRAIL** — a personalised route through the graph |
| 3 | **COMPARE** (hold two objects side by side) and **MEMORY** (the site remembers where you left off) |
| 4 | **CHAPTERS** — a syllabus synthesised from your trail |
| 5+ | compounding mutations: the seed, the ordering and the relation weighting all change |

A returning visitor therefore arrives in a *different structure* from the one
they left: the paradigm they converged to, the memory of their last position,
their accumulated interest vector, and the behaviour they have unlocked.

You can force a generation by hand with the **gen** badge in the top bar, or
read the whole history in the **evolution log** inside the Mind panel.

---

## 3. The Golden Rule: it stays usable

Radical is not the same as chaotic. Every paradigm obeys the same contract:

- **It is always navigable.** Every paradigm has a complete, self-contained way
  to reach any object in the corpus. The switcher in the top bar is always
  present, so you are never trapped in a structure you did not choose.
- **It is always explicable.** The moment a restructure happens you are told
  what changed and why, in plain language, with the evidence behind it.
- **It is never worse than the one you had.** The engine only switches on a
  confident, verified read; otherwise it holds. You can pin a structure with one
  click, and the engine then observes without touching anything.
- **It never loses your place.** Your path, your interest, your route and your
  unlocked behaviour survive every restructure.

---

## 4. Running it

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # type-check + production bundle into dist/
npm run preview    # serve the production build
```

### Tests

```bash
node scripts/smoke.mjs       # 30 headless assertions against the real app
node scripts/live-check.mjs  # 7 end-to-end assertions in a real browser
node scripts/screenshot.mjs  # renders every paradigm in headless Chromium
```

`scripts/smoke.mjs` mounts the actual application in jsdom and plays three
different visitors — a reader, a skimmer, an analyst — then asserts that the
engine *restructures itself* in response, that all six paradigms render, that
generations unlock behaviour, and that the Mind panel reports honestly.

`scripts/live-check.mjs` drives the built site in headless Chromium with two
genuinely different visitors — one clicks frantically and never stays, one opens
an object, reads it and follows a relation — and asserts that the same URL
restructures into **Mosaic** for the first and **Codex** for the second, and
that the interface explains itself each time. It is the executable form of the
claim this project is making.

---

## 5. How it is built

React 19 + TypeScript + Vite. No UI framework, no animation library, no state
library — the engine *is* the application logic, and everything is hand-rolled
so the structural transformations stay legible.

```
src/
  content/graph.ts     35 objects, 79 typed relations, the taxonomy
  engine/
    types.ts           the vocabulary: paradigms, archetypes, features, genome
    classify.ts        raw trace → feature vector → archetype affinity scores
    decide.ts          archetype → paradigm, trail synthesis, chapters
    genome.ts          persistence, generations, unlocks, interest model
    store.tsx          the live engine: observation → decision → restructure
  modes/               the six structural paradigms, one component each
  components/          chrome, mind panel, reconfiguration manifest, status bar
  styles/              design tokens, chrome, per-paradigm layouts
```

**Privacy:** there is no server and no analytics. The model of you lives in
your browser's `localStorage` and nowhere else. `Mind → Erase memory` deletes
it.

---

## 6. Design notes

The visual language is astronomical: near-black vacuum, a procedural starfield
seeded by your own generation, hairline rules, and three typefaces — Newsreader
for prose, Space Grotesk for the interface, JetBrains Mono for data. Each
paradigm shifts the accent hue and the geometry but never the typography, so
the *voice* of the site stays constant while its *shape* does not.
