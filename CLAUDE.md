# Save the Date — Tjaša & Andraž

A single-page animated save-the-date site. No build tools, no framework —
one static `index.html` plus a handful of images.

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
  vila-watercolour.png   aerial watercolour painting of Vila Vipolže, used
                          full-bleed behind the closed envelope
  vila-sketch.jpg        architectural elevation drawing, recolored as a
                          duotone (paper/ink) to match the palette; used
                          for the villa band on the main page
  envelope-closed.png    real cream envelope photos (AI-generated,
  envelope-open.png      background already removed), cropped/scaled/
                          aligned onto a shared canvas so the envelope's
                          body sits at the same spot in both — see
                          tools/prep_envelope_photos.py
  seal.png               real photographed wax seal (sage wax, gold "T&A"
                          monogram), resized down from the source photo
tools/                   gitignored — kept locally, not tracked/pushed
  prep_envelope_photos.py cuts out + aligns the raw envelope photos into
                          envelope-closed/open.png, see below
  build_artifact.py       generates the Claude Artifact build from
                          index.html
inspiration/             reference material (not deployed, gitignored)
```

`tools/prep_envelope_photos.py` cuts out + aligns a pair of envelope photos
into `envelope-closed/open.png`: crops each to content, scales both to the
same body width, and places them on a shared canvas anchored to the same
bottom-center point, so a closed/open crossfade doesn't jump. Re-run it
locally whenever the *source* envelope photos change.

The envelope's and seal's drop-shadows are a **live** CSS
`filter:drop-shadow`, not baked into the images (an earlier version baked
them in, and there was a script for it — both are gone now, see the
`.envelope-photo`/`.envelope-seal` comments in `index.html` for why the
live version doesn't hit the clipping bug that made baking seem necessary
in the first place: it wasn't about live-vs-baked, it was that the
envelope/seal PNGs fit their own canvas edge-to-edge with ~0 margin, and
the box the filter renders into needs room around the visible content for
the blur+offset to spread into. Fixed by making the CSS box itself larger
than the photo (negative `inset`) and shrinking the photo back down within
it (`background-size` < 100%), leaving transparent margin in the box for
the filter — no separate baking step needed. If you resize/replace
`envelope-closed/open.png` or `seal.png` with a source that has a
meaningfully different content-to-canvas margin, re-check the `inset`/
`background-size` percentages in `index.html` still leave enough room.

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
  (`--ink: #647353`) for all text/borders/outlines, gold reserved for the
  wax seal (a real photographed seal, `images/seal.png` — sage wax with a
  gold-embossed monogram — not a UI accent).
- Fonts: Google Fonts — Cormorant Garamond (body), Cormorant SC (small
  caps labels/dates), Pinyon Script (the ornate cursive used for the
  "Save"/"Date" headline and the envelope's sender line — chosen to match
  the swash calligraphy in the Etsy/Canva inspiration video under
  `inspiration/`; the wax seal's "T&A" monogram is baked into `seal.png`
  itself, not set in this font).
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

1. Page loads on a closed envelope (`envelope-closed.png`, see above —
   plus the wax seal, `seal.png`, overlaid on top) sitting over the villa
   watercolour, full-bleed, with a dark top/bottom veil behind the sender
   text/hint for legibility. `body.locked` blocks
   scrolling.
2. Click → the closed photo crossfades to the open one in place (~1.4s,
   there's no separate flap layer to rotate — the two photos are pre-aligned
   so only the flap area visibly changes), *then* the whole envelope +
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
- `v4` — real photographed envelope (closed/open crossfade) and wax seal
  replace the SVG-drawn versions, watercolour painting replaces the real
  aerial photo behind the envelope, Pinyon Script headline/sender text,
  slower open animation, darker text-legibility veil on the intro
- `v5` — intro page finalized: new fancier wax seal photo, envelope/seal
  drop-shadows moved from baked-in images to live CSS filters (a
  box-padding trick sidesteps the clipping bug that made baking seem
  necessary); fixed a mobile-only tap-highlight flash on envelope open
  (root cause found via screen-recording frame analysis, not guessing);
  sender line restructured to "Prispelo je pismo" / "Tjaše & Andraža"
  (Alex Brush ampersand) with a staggered pop-in entrance for the
  envelope+seal; villa alignment rebuilt from scratch in JS to exactly
  match the intro watercolour's villa to the main page sketch's villa
  (position and size) on any viewport, replacing guessed static
  `background-position` percentages; pinch-zoom locked via viewport meta

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
  in an actual browser, not just via screenshots — and for anything that
  only reproduces on a phone (a past bug: a gray flash on tap, turned out
  to be WebKit/Chrome's default tap-highlight, fixed with
  `-webkit-tap-highlight-color:transparent` on `.envelope-btn` and
  globally on `*`), get a screen recording and diff frames with
  `ffmpeg -i recording.mp4 frame_%03d.png` + PIL/numpy rather than
  guessing from a text description — several CSS-timing theories were
  tried and failed before a recording actually showed what was happening.

## Changes requested (mark a change as completed when completed)
- [x] Villa is too much on the left on phone display. I need perfect alignment.
- [x] In all dimensions (placement and size) watercolour villa needs to match sketched villa.
  So the animation transition is smooth.
  → Static `background-position` percentages can't do this exactly: the
  watercolour is a full-viewport `background-size:cover` while the sketch
  sits in a fixed-aspect-ratio box inside the 480px `.page` column, and how
  much of the watercolour gets cropped by `cover` depends on the live
  viewport's aspect ratio — no single hand-picked percentage holds for
  every phone. Fixed with a small script (in `index.html`'s `<script>`,
  search "Aligns the intro watercolour's villa") that measures where
  `.villa-hero`'s villa actually lands on screen via `getBoundingClientRect`
  (deterministic — that band always shows the full sketch uncropped), then
  solves `.reveal-photo`'s `background-position` so the watercolour's villa
  lands at that exact same point, given `cover`'s own scale/crop math. Runs
  on load, again once web fonts finish (they shift the text height above
  `.villa-hero`), and on resize/orientation change — exact for any viewport
  size rather than approximate for an assumed range. The villa-center
  fractions it solves against (`CX_S/CY_S`, `CX_W/CY_W` in that script) were
  measured directly off the two source images (grid-overlay + pixel
  coordinates); re-measure and update them if either image is ever replaced
  or re-cropped.
