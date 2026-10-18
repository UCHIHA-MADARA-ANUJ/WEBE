# FRAME/SHIFT

**Not a list. A way in.** FRAME/SHIFT is an anime discovery index that changes its navigation and information hierarchy to match how a visitor explores. It is a small, static web app built for the “impossible interface” challenge.

## The Evolution Engine

FRAME/SHIFT keeps a lightweight profile in the visitor’s own browser (`localStorage`, key `frame-shift.profile.v1`). There is no account, backend, analytics request, or profile sent off-device. The profile is used to learn:

- **Topic affinity:** the story tags and moods attached to titles a visitor opens or saves.
- **Navigation pattern:** switches between different kinds of stories versus explicit “follow this thread” steps.
- **Reading pace and depth:** time spent on an opened title and the deepest scroll position reached while it is open.
- **Commitment and return:** titles saved to a personal shelf, repeat opens, and later visits.

Events are stored as a small rolling history; derived counts and saved titles remain local. The choice is deterministic—not random—and the engine exposes its live lens weights in **How it learns**. Scores are computed for each structural lens from behavior: topic variety and jumps contribute to Orbit; linear steps and deep reads to Run; quick skips and short reads to Pulse; saves, repeat opens, and return visits to Shelf. Eligibility gates prevent a single accidental click from causing a big structural change. Strong collection intent takes priority. Choosing a preview mode is not itself a signal; real opens, saves, skips, and reading actions continue to update Auto while you preview.

### Four structural states

| Lens | What changes in the interface | Behavior that favors it |
| --- | --- | --- |
| **Orbit** | A spatial constellation makes story relationships the primary navigation; selecting a node opens its neighbors and details. | Default on a new profile; broad jumps between themes also keep the map in front. |
| **Run** | The map gives way to a step-by-step route: chapter rail, focused reading pane, progress, and next/previous story actions. | Following a thread, or repeatedly reading deeply and linearly. |
| **Pulse** | A mood-led “tonight’s pick” and short ranked queue replace the map and long-form browsing. | Repeated quick skips / fast scans. |
| **Shelf** | A saved-title rail and side-by-side comparison workspace take over as the main navigation. | Saving two titles, or returning to a saved title on a later visit. |

The responsive versions preserve the interaction meaning: for example, Orbit becomes a connected, scannable two-column map on a narrow screen, while Shelf remains a selection rail plus comparison workspace.

## Try the adaptive behavior

1. Open any title in **Orbit**. Click **Follow this thread** to move into the sequential **Run** structure.
2. In **Pulse**, press **Not this one** twice to signal quick-pick behavior.
3. Save two different titles to make **Shelf** the primary workspace.
4. Open **How it learns** to inspect the evidence and live score bars. The lens control in the header lets you preview all four structures without changing the profile; choose **Follow my behavior** to return to Auto.
5. Use **Reset profile** in the footer or the engine panel to clear saved titles and local signals.

The first visit starts in Orbit so the relationships are immediately explorable. Automatic changes appear in real time; the small **AUTO LENS SHIFT** notice explains when the chosen structure changes.

## Run locally

No build step or third-party package is required. From the repository root, run:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`. (A static server is needed because the app uses JavaScript modules.)

## Deploy

The repository includes a GitHub Actions workflow at `.github/workflows/deploy.yml` that publishes the static site to GitHub Pages when `main` or the Arena working branch is pushed, provided Pages is enabled with **GitHub Actions** as the build source. All assets use relative paths, so the app works at the project Pages URL as well as at the root of a local static server.

## Design and content notes

- The covers are original, hand-authored geometric vector studies—not official key art or scraped images. Anime titles and their underlying rights belong to their respective owners; FRAME/SHIFT is an independent concept and is not affiliated with them.
- The design intentionally favors a dark editorial print/archive language over generic gradients, glass panels, or an AI-chat visual style.
- The interface is keyboard operable, includes focus states and a skip link, supports reduced motion, and adapts to mobile screens.
- Core files: `src/app.js` (four interface structures), `src/evolution.js` (local behavioral model), `src/data.js` (catalogue and vector art), `styles.css` (visual system).
