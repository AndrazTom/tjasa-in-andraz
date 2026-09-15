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
  bracket-top.png         decorative floral frame, split in half and
  bracket-bottom.png      downsized by tools/prep_bracket.py from a raw
                          source image (not kept in the repo), opened
                          around the headline/date/venue block on the
                          main page
tools/                   gitignored — kept locally, not tracked/pushed
  prep_envelope_photos.py cuts out + aligns the raw envelope photos into
                          envelope-closed/open.png, see below
  prep_bracket.py         splits + downsizes images/curvyBracket.png into
                          bracket-top/bottom.png, see below
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
`filter:drop-shadow`, not baked into the images. The photos fit their own
canvas edge-to-edge with ~0 margin, so the filter needs the CSS box made
larger than the photo (negative `inset`, `background-size` < 100%) to have
room to spread — see the `.envelope-photo`/`.envelope-seal` rules in
`index.html`. Re-check those percentages if you swap in source images with
a different content-to-canvas margin.

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
  caps labels/dates), Pinyon Script (headline + envelope sender names,
  matching the Etsy/Canva inspiration video under `inspiration/`), Alex
  Brush (just the sender line's "&" — Pinyon Script's own glyph looked off).
- The villa sketch (`images/vila-sketch.jpg`) is a duotone (black→ink,
  white→paper) baked into the image itself, not a CSS filter — an earlier
  filter approach left a visible seam at the edges. Regenerate with the
  same paper/ink RGB values if the palette ever changes.

## The envelope-opening intro

Sequence, roughly (every transition/animation in `index.html` has a short
inline comment like `/* flap opens */` or `/* 4: date */` — read those
before guessing at timings):

1. Page loads on a closed envelope (`envelope-closed.png` + `seal.png`)
   over the villa watercolour, full-bleed, dark top/bottom veil behind the
   text for legibility. `body.locked` blocks scrolling. Sender text
   ("Prispelo je pismo" / "Tjaše & Andraža") fades in, then envelope+seal
   pop in together, then the "Klikni na kuverto" hint.
2. Click → closed photo crossfades to open (~1.4s, no separate flap
   layer — the two photos are pre-aligned so only the flap area visibly
   changes), then envelope + sender + hint fade away together.
3. A slow crossfade (~3.4s) reveals the page underneath, with the villa
   **sketch** (not the photo) in its own band — photo/sketch roles are
   deliberately swapped between the intro and the page.
4. Page text fades in top-to-bottom, one block at a time: bracket-top →
   headline → rule → date/venue → bracket-bottom → names → countdown →
   locations → contact → footer.
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

- Headless Chrome on this machine is unreliable for testing timing-based
  CSS animations: `--window-size` doesn't reliably set the actual viewport
  below ~500px, and `--virtual-time-budget` doesn't advance animation
  clocks. Workarounds: force `.opened`/`animation:none!important` on a
  scratch copy to inspect static end-states; for anything mobile-only,
  get a screen recording and diff frames (`ffmpeg -i rec.mp4 frame_%03d.png`
  + PIL/numpy) rather than guessing — that's what found the tap-highlight
  flash bug after several wrong CSS-timing theories failed.

## Changes requested (mark a change as completed when completed)
- try Bickham Script Pro oziroma Bickham Script Pro 3 for the names in the front page and save the date font. These are similar to what we want. If i wont like themw e can try Burgues Script, Edwardian Script ITC.
-When loading the webpage we should wait half a second before loading anything but the picture to account for loading time of the image. Then we should again wait on the second page after watercolour to sketch transition before starting to show the text. Additional half a second.