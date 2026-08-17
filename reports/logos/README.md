# Cover logos

`rozeegpt.svg` and `efulife.svg` are rebuilt by `make_logos.py`. Wordmarks are
converted from live font outlines into vector paths, so the files carry no font
dependency and render identically in the browser and in print.

```
pip install fonttools brotli
npm i @fontsource/poppins          # FDIR in make_logos.py points at the install
python3 make_logos.py
```

`page.py` embeds whatever it finds here as a base64 data URI — the report must
stay self-contained, so external image URLs will not load. Replacing either file
(`.svg`, `.png`, `.jpg` or `.webp` all work) and re-running the build swaps the
mark with no other changes.

## Sizing

Each mark is sized on its own, so a wide wordmark and a square app icon balance
optically rather than sharing one cap: see `.lg-rozeegpt` and `.lg-efulife` in
`page.py`. Both sit in a fixed-height box so the two slots share a centre line.

## Dark mode

The cover card is near-black in dark mode, so `DARK_MODE` in `page.py` sets the
treatment per logo:

- `invert` — flips a black-on-transparent mark to white. Monochrome marks only.
- `plate` — sits the logo on a white rounded plate. For a colour mark with a
  transparent background.
- `none` — the mark already reads on a dark ground.

Current settings: `rozeegpt` → `invert` (the wordmark is solid black),
`efulife` → `none` (the app icon carries its own white ground). Print always
uses the untouched original.
