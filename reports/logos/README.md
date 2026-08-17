# Logo slots

Drop the real brand files in here and re-run `python3 page.py` — each is
embedded into the HTML as a base64 data URI (the report must stay
self-contained, so external image URLs will not load).

| File | Slot |
|---|---|
| `rozeegpt.svg` (or `.png` / `.jpg` / `.webp`) | "Prepared by" |
| `efulife.svg` (or `.png` / `.jpg` / `.webp`) | "Prepared for" |

`.svg` is preferred, then `.png`. Logos render at up to 46px tall and 190px
wide, aspect ratio preserved. With no file present the cover falls back to a
typographic lockup.
