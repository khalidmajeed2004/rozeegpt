# Logo slots

Drop the real brand files in here and re-run `python3 page.py && node shot.js`.
Each is embedded into the HTML as a base64 data URI — the report must stay
self-contained, so external image URLs will not load.

| File | Slot |
|---|---|
| `rozeegpt.svg` (or `.png` / `.jpg` / `.webp`) | "Prepared by" |
| `efulife.svg` (or `.png` / `.jpg` / `.webp`) | "Prepared for" |

`.svg` is preferred, then `.png` with a transparent background. Logos render at
up to 46px tall and 190px wide, aspect ratio preserved. With no file present the
cover falls back to a typographic lockup.

## Dark mode

The cover card is near-black in dark mode, so `DARK_MODE` in `page.py` sets the
treatment per logo:

- `invert` — flips a black-on-transparent mark to white. Monochrome marks only.
- `plate` — sits the logo on a white rounded plate. Correct for colour marks.
- `none` — the mark already reads on a dark ground.

Current settings: `rozeegpt` → `invert` (the wordmark is solid black),
`efulife` → `plate` (the mark is teal). Print always uses the untouched
original.
