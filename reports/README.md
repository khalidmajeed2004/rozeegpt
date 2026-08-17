# EFU Life — credit utilisation & user summary

Utilisation report for EFU Life's use of the Rozee KPI Generator, built from
`efukpidataaug2026.xlsx` (sheets `KPIs` and `Data`).

## Output

- `efu-utilisation-summary.html` — the report (responsive, light/dark, print-ready)
- `EFU-Utilisation-Summary.pdf` — 3-page A4 print version (cover + 2 content pages)

The report itself does not name the source file; it attributes figures to KPI
Generator usage records for the account.

## Regenerating

```
pip install openpyxl pandas
python3 build.py     # reads the source xlsx -> data.json
python3 charts.py    # data.json -> charts.json (inline SVG)
python3 page.py      # + report.css + logos/ -> efu-utilisation-summary.html
node shot.js         # -> EFU-Utilisation-Summary.pdf (needs playwright + chromium)
```

`build.py` holds the source path and `PURCHASED = 500`, the contracted credit
count. That figure is supplied separately — the raw sheet carries no balance
or commercial fields.

Cover logos are built by `make_logos.py` into `logos/` — see `logos/README.md`.

## Counting basis

- **Credit** = one KPI-generation request. 852 submitted; 838 returned KPIs.
- **User** = distinct email in the `KPIs` sheet.
