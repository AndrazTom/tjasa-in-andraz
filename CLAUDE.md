# Save the Date — Tjaša & Andraž

A single-page animated save-the-date site. No build tools, no framework —
one static `index.html` plus two images.

## The wedding

- Date: **18 September 2027**, ceremony at **15:00 (3pm) CEST**
- Ceremony ("Slovesnost"): Vila Vipolže, Goriška Brda
- Party ("Zabava"): Posestvo Rouna, Vipavska dolina (Slap)
- Contact: tjasamiric@gmail.com, tomsic.andraz@gmail.com

Countdown target in the script is `2027-09-18T15:00:00+02:00`. DST shifts
back then forward again before that date, netting to the same +02:00
offset as when this was written — don't "fix" the offset without checking.

## Structure

```
index.html              the whole site (styles + markup + script inline)
images/
  vila-vipolze.jpg       real aerial photo of Vila Vipolže (from brda.si)
  vila-sketch.jpg        architectural elevation drawing, recolored as a
                          duotone (paper/ink) to match the palette
tools/
  build_artifact.py       generates the Claude Artifact build from index.html
inspiration/             reference material (not deployed, gitignored)
```

`index.html` is the source of truth. It's a normal standalone document
(`<!DOCTYPE html>`, `<head>` with viewport meta, `<body>`) because it's
served as-is by GitHub Pages — it does **not** assume any wrapping skeleton.

## Deployment (two targets, kept in sync manually)

1. **GitHub Pages** (primary, public): repo `AndrazTom/tjasa-in-andraz`,
   served from `main` at the repo root.
   → https://andraztom.github.io/tjasa-in-andraz/
   Deploy: commit + push to `main`; Pages rebuilds automatically
   (~30-60s — poll with `gh api repos/AndrazTom/tjasa-in-andraz/pages/builds/latest`).

2. **Claude Artifact** (private preview): a separate copy for quick sharing
   inside Claude, kept at a fixed artifact URL across sessions.
   Artifacts require *bare* content (no `<!DOCTYPE>`/`<html>`/`<head>`/`<body>`
   — the platform injects its own) and can't reference local image files,
   so it needs a different build of the same source.

   `tools/build_artifact.py` bridges the two: it strips the doctype/html/
   head/body wrapper back out of `index.html` and inlines every
   `images/...` reference as a base64 data URI. Run it, then publish the
   output with the Artifact tool using the *existing* artifact URL (not a
   new one) so it updates in place:

   ```
   python3 tools/build_artifact.py /tmp/artifact_build.html
   ```

   Then `Artifact(action: publish, file_path: /tmp/artifact_build.html, url: <existing artifact url>)`.

   **Whenever `index.html` changes, rebuild and republish the artifact in
   the same step** — the two should never be allowed to drift apart.

## Design

- Palette: cream/paper background (`--paper: #f8f3e7`), sage green ink
  (`--ink: #647353`) for all text/borders/outlines, gold only for the wax
  seal's own gradient (it's meant to look like an actual wax seal, not a
  UI accent).
- Fonts: Google Fonts — Cormorant Garamond (body), Cormorant SC (small
  caps labels/dates), Alex Brush (the cursive "Save"/"Date" script).
- The villa sketch (`images/vila-sketch.jpg`) is a duotone: original
  black-on-white line art remapped so black→ink color, white→paper color,
  baked into the image itself (not a CSS filter — an earlier invert+hue-
  rotate filter approach left a visible seam where the filtered white
  background didn't exactly match the page background). Regenerate it
  with the same paper/ink RGB values whenever the palette changes:
  see the inline duotone snippet used throughout this project's history
  (grayscale → per-channel LUT lerp between ink and paper).

## The envelope-opening intro

Sequence, roughly (every transition/animation in `index.html` has a short
inline comment like `/* flap opens */` or `/* 4: date */` — read those
before guessing at timings):

1. Page loads on a closed envelope (SVG-drawn: cream paper gradient, gold
   trim, gold wax seal) sitting over the real villa photo, full-bleed,
   with a soft light veil overlay. `body.locked` blocks scrolling.
2. Click → the flap opens first (~0.7s), *then* the whole envelope +
   sender line ("Tjaša in Andraž pošiljata pošto") + hint ("Klikni na
   kuverto") fade away together — sequential, not simultaneous.
3. A slow crossfade (~3.4s) reveals the cream page underneath, which has
   the villa **sketch** (not the photo) in its own band partway down —
   the photo/sketch roles are deliberately swapped between the intro and
   the page.
4. Text then fades in top-to-bottom, one block at a time ("Harry Potter
   letter" effect): sprig → headline → rule → date/venue → rule → names →
   countdown → locations → contact → footer.
5. `history.scrollRestoration = 'manual'` + forced `scrollTo(0,0)` on
   load, `pageshow`, and envelope-open — iOS Safari otherwise restores a
   guest's previous scroll offset on reload, which looked broken.

If you change one delay, the rest likely need shifting too (each stage's
start depends on the previous stage's total duration) — the numbered
comments (`/* 1: sprig */` etc.) make it easy to re-walk the chain.

## Versions

Tagged checkpoints on `main`, each with a GitHub Release:
- `v1` — first complete site (villa hero band, countdown, locations, contact)
- `v2` — light/paper theme + SVG envelope with sketch→photo reveal
- `v3` — envelope/page imagery swapped back, sequenced open animation,
  darker sage contrast pass, 3pm countdown

Tag before any major redesign so it's easy to roll back:
`git tag -a vN -m "..." && git push origin vN && gh release create vN ...`

## Known open items

- Screenshot-testing timing-based CSS animations with headless Chrome is
  unreliable on this machine (`--window-size` doesn't reliably set the
  actual viewport below ~500px, and `--virtual-time-budget` doesn't
  advance CSS transition/animation clocks). Workarounds used: wrap
  `index.html` in an iframe with fixed pixel dimensions inside a wrapper
  page for accurate mobile-width screenshots; force `.opened` classes and
  `animation:none!important;opacity:1!important` on a scratch copy to
  inspect static end-states. Always verify real interaction timing live
  in an actual browser, not just via screenshots.
