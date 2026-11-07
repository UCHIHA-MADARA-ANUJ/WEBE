# Setup

Flat files. No build step to run, no dependencies to install, nothing to host.

## What goes up

| File | What it is |
|---|---|
| `README.md` | the profile page |
| `hero-{light,dark}.svg` | portrait bleeding left, name, place, three facts |
| `stats-{light,dark}.svg` | four headline numbers on a wash |
| `about-{light,dark}.svg` | five lines, first person |
| `currently-{light,dark}.svg` | three study directions with status tags |
| `education-{light,dark}.svg` | a timeline: now, year two, ongoing |
| `stack-{light,dark}.svg` | eight languages, a note each, daily tools |
| `beyond-{light,dark}.svg` | club, badminton, tug of war |
| `hire-{light,dark}.svg` | what she brings, and what she is open to |
| `contact-{light,dark}.svg` | email, wired to `mailto:` |
| `footer-{light,dark}.svg` | closing rule in four colours |
| `avatar.png` | 640 x 640, circular, same artwork |
| `portrait.jpg` | the crop embedded inside the hero |

Twenty-four files. `source/` is the original upload and is **not** needed on
GitHub.

## Upload

1. The repository must be named exactly **`Mitali-Chincholikar`**. That is the
   only thing that makes GitHub render its README on her profile.
2. It must be **public**.
3. Upload every file to the **root**. No subfolders.
4. Set the same `avatar.png` as her GitHub profile picture: Settings → Profile
   picture.

## Why light and dark are separate files

GitHub has two themes and does not tell the image which one the reader chose.
Each panel is therefore drawn twice, and the README picks with `<picture>`:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./hero-dark.svg" />
  <img src="./hero-light.svg" alt="..." width="100%" />
</picture>
```

Upload both files of every pair. If one is missing, the other theme shows the
wrong-coloured panel — readable, but wrong.

## Why the text is outlines

The type is Inter and JetBrains Mono, converted to vector paths by
`../typekit.py`. No font is requested from the reader's machine, so the panels
cannot fall back to Segoe, Roboto or a Linux default and drift out of
alignment. It also means the files render identically in print, in Figma, in
Inkscape, and in any screenshot.

The cost: the text is no longer selectable when the SVG is opened directly.
The `alt` text on every `<img>` carries the full content for screen readers
and for search, so nothing is lost on the page.

## Rebuilding

```sh
python3 ../build_mitali_pro.py
```

That rewrites all ten panels. Text and colours live in that one file: the two
palettes at the top, and the strings inside each panel function.

## A note on embedding

The portrait is embedded inside the hero SVG as a data URI. GitHub serves SVGs
through an image proxy that will not fetch a second file referenced from
inside one — a linked `<image href="portrait.jpg">` renders as nothing there.
Anything raster has to travel inside the file.

## Check before uploading

```sh
python3 ../check_motion.py
```

There is no animation in this kit, so it should pass trivially. Run it anyway
after any edit.
