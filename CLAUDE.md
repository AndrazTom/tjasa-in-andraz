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
  vila-watercolour.jpg   aerial watercolour painting of Vila Vipolže, used
                          full-bleed behind the closed envelope — JPEG not
                          PNG (no alpha channel needed): ~3.1MB as a PNG,
                          ~580KB at quality 90, visually indistinguishable
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
  landscape-color.jpg     full-bleed landscape photo, edge-to-edge
                          background for .landscape-band, the section
                          below the villa sketch — center-cropped from a
                          raw source (not kept in the repo, same JPEG
                          rationale as vila-watercolour.jpg) to match this
                          file's own established 2:3 aspect ratio (cutting
                          off edges rather than stretching/squashing).
                          Whenever this image is swapped: re-sample
                          `--paper` from its top edge and regenerate
                          vila-sketch.jpg's baked paper tone to match (see
                          Design section below) or the villa/headline area
                          will show a visible seam against it again. The
                          seam is also softened by .landscape-band::before,
                          a long (380px) eased paper→transparent fade
                          (color-mix stops, not a flat linear-gradient, so
                          it clears slowly instead of at a steady rate).
  landscape-mono.jpg      unused leftover from an earlier duotone-style
                          treatment of the landscape band, superseded by
                          landscape-color.jpg — kept in the repo but not
                          referenced by index.html; fine to delete once
                          confirmed nothing still wants it.
  bottom-bracket.png      tall scalloped label/frame with a baked-in cream
                          fill (~#fdf9ef), overlaid on .landscape-band as
                          .bracket-frame's background; the T&A monogram/
                          countdown/locations/footer sit inside it
  swan.jpg                decorative motifs above the Vipolže/Rouna location
  plates.jpg              cards — originally AI-generated PNGs with a
                          transparent cutout background (a swan pair, a
                          plate+fork+knife setting), flattened onto
                          bottom-bracket.png's own cream fill color (see
                          `.loc-motif` in index.html) rather than kept as
                          PNGs, since they always sit on that one known
                          background and a photo doesn't need an alpha
                          channel. Both cropped tight to their own artwork
                          (minimal padding) rather than kept at their
                          source canvas size, which had a lot of dead
                          margin baked in.
  TA.png                  "T&A" monogram in an oval line-drawing (sage ink,
                          transparent background) — kept as a PNG, unlike
                          swan.jpg/plates.jpg, since it's flat line art that
                          needs real alpha to sit cleanly in the bracket's
                          scalloped top notch. Cropped tight to the artwork,
                          same reasoning as swan.jpg/plates.jpg.
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

Every image the intro/main page needs gets a `<link rel="preload" as="image">`
in `<head>` (the three visible before any interaction — watercolour, closed
envelope, seal — marked `fetchpriority="high"`) so a first, uncached load
doesn't stall mid-animation waiting on a fetch. `tools/build_artifact.py`
strips these when building the Artifact, since everything there is already
inlined as a data URI — keeping them would just duplicate each preloaded
image's bytes a second time in the output. Add a preload line here whenever
a new image is added to the intro/page.

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

- Palette: cream/paper background (`--paper` — kept re-sampled from
  whatever `landscape-color.jpg` currently is, from its top edge, so the
  villa sketch band meets the landscape band below with no visible seam;
  as of the 2026-09-15 photo swap this is `#f3efe8`, picked just to match
  that photo and not yet chosen for overall palette cohesion), sage green
  ink (`--ink: #647353`) for all text/borders/outlines, gold reserved for
  the wax seal (a real photographed seal, `images/seal.png` — sage wax
  with a gold-embossed monogram — not a UI accent). Two more one-off
  creams: `--envelope-cream` (scraped from images/envelope-open.png, used
  only for the intro popcard) and `--motif-cream` (scraped from the middle
  of images/plates.jpg, used only for the countdown squares) — both
  deliberately distinct from `--paper`, matching the specific surface each
  sits on rather than the page background.
- Fonts: Google Fonts — Cormorant Garamond (body), Cormorant SC (small
  caps labels/dates), Pinyon Script (headline + envelope sender names,
  matching the Etsy/Canva inspiration video under `inspiration/`), Alex
  Brush (just the sender line's "&" — Pinyon Script's own glyph looked off).
- The villa sketch (`images/vila-sketch.jpg`) is a duotone (black→ink,
  white→paper) baked into the image itself, not a CSS filter — an earlier
  filter approach left a visible seam at the edges. **If `--paper` ever
  changes, regenerate this image's paper tone to match** (or it'll show as
  a mismatched "white" patch again) — solve each pixel's original duotone
  mix `t` from the image's own old baked paper/ink values, `t = (pixel -
  OLD_INK) / (OLD_PAPER - OLD_INK)`, then recompute `INK + t*(NEW_PAPER -
  INK)`; this only shifts the paper tone and leaves ink linework untouched,
  no need for the original pre-duotone source.

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
3. A small "Save the Date" card (`.popcard`, reusing bracket-top/bottom.png
   at mini scale) pops up out of the open envelope, holds for a beat, then
   fades itself out — self-contained one-shot animation (`popCard`
   keyframes, `both` fill mode) timed to finish exactly as the next stage's
   fade starts, so the two never overlap.
4. A slow crossfade (~3.4s) reveals the page underneath, with the villa
   **sketch** (not the photo) in its own band — photo/sketch roles are
   deliberately swapped between the intro and the page.
5. Page text fades in top-to-bottom, one block at a time: bracket-top →
   headline → rule → date/venue → bracket-bottom, then the villa sketch,
   then the landscape band (time-based fade) and finally the bracket-frame
   card (T&A monogram → countdown → locations → footer), scroll-gated via
   IntersectionObserver — see `openEnvelope()`'s `LANDSCAPE_DONE_AT`. The
   original names/contact-email sections were dropped in favor of the
   landscape band + bracket-frame redesign (v6) and the location cards'
   own motifs (v7).
6. `history.scrollRestoration = 'manual'` + forced `scrollTo(0,0)` on
   load, `pageshow`, and envelope-open — iOS Safari otherwise restores a
   guest's previous scroll offset on reload, which looked broken.

If you change one delay, the rest likely need shifting too (each stage's
start depends on the previous stage's total duration) — the numbered
comments (`/* 2: headline */` etc., plus the `openEnvelope()` `setTimeout`
which must keep matching the cover's fade delay+duration) make it easy to
re-walk the chain.

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
- `v6` — TJAŠA/ANDRAŽ names section replaced by a full-bleed landscape
  band + scalloped `bottom-bracket.png` card holding the countdown/
  locations/contact/footer; scroll locked until the band's time-based
  fade completes, then the bracket-frame reveals via IntersectionObserver;
  `--paper` retuned to the landscape photo's own tone and vila-sketch.jpg's
  duotone regenerated to match
- `v7` — location cards redesigned: removed the contact/email block and
  the "Obred"/"Zabava" labels/arrows, added a swan/plate motif image above
  each card (flattened from transparent cutouts onto the bracket's cream
  fill), cards now just pin+venue-name (centered as one unit) with the
  address centered independently below — no visible card background/
  border any more, just a large invisible (but still fully clickable)
  Google Maps link; added a T&A monogram in the bracket's top notch;
  landscape photo swapped to full color with a much longer, eased
  (color-mix) top fade instead of a flat linear one; countdown squares
  recolored to match the motifs' cream tone and un-bordered; popcard
  background recolored to the actual envelope photo's tone; various
  pixel-level repositioning of the bracket-frame/countdown/monogram

Tag before any major redesign so it's easy to roll back:
`git tag -a vN -m "..." && git push origin vN && gh release create vN ...`

## Known open items

- Plain `chrome --headless --window-size=W,H` is unreliable below ~500px —
  it silently renders at some other width (seen clamping to 500) regardless
  of what's requested, and `--virtual-time-budget` doesn't advance CSS
  animation clocks either. **`tools/cdp_render.py` fixes the viewport part**:
  drives Chrome directly over CDP (`Emulation.setDeviceMetricsOverride`)
  instead of the CLI flag, which reliably hits exact real-device widths —
  confirmed `window.innerWidth` matches for iPhone SE/13 mini/14/15/15 Pro
  Max and small Android sizes. `python3 tools/cdp_render.py URL W H OUT.png
  ["JS expr"] [port]` screenshots at that exact viewport and, if given a JS
  expression, prints its JSON-stringified result — much more reliable than
  eyeballing a screenshot for exact pixel/layout values. Still doesn't
  advance animation clocks, so for timing-based CSS animations the old
  workarounds still apply: force `.opened`/`animation:none!important` on a
  scratch copy for static end-states, or for anything mobile-only, get a
  screen recording and diff frames (`ffmpeg -i rec.mp4 frame_%03d.png` +
  PIL/numpy) — that's what found the tap-highlight flash bug after several
  wrong CSS-timing theories failed.
- Mobile Safari's actual `window.innerHeight` is smaller than the device's
  full CSS height (address bar + Dynamic Island eat into it), and changes
  as the address bar hides on scroll — `cdp_render.py` can't replicate this
  exactly, so pixel-matching work tuned against it (e.g. the villa Y
  alignment in the intro) should be treated as a close starting point,
  verified/adjusted against a real device rather than assumed exact.

## Changes requested (mark a change as completed when completed)
- try Bickham Script Pro oziroma Bickham Script Pro 3 for the names in the front page and save the date font. These are similar to what we want. If i wont like themw e can try Burgues Script, Edwardian Script ITC.
-When loading the webpage we should wait half a second before loading anything but the picture to account for loading time of the image. Then we should again wait on the second page after watercolour to sketch transition before starting to show the text. Additional half a second.