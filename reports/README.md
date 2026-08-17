# EFU Life — utilisation & user summary

Utilisation report for EFU Life's use of the Rozee KPI Generator, built from
`efukpidataaug2026.xlsx` (sheets `KPIs` and `Data`).

## Output

- `efu-utilisation-summary.html` — the report (responsive, light/dark, print-ready)
- `EFU-Utilisation-Summary.pdf` — 3-page A4 print version

## Regenerating

```
pip install openpyxl pandas
python3 build.py     # reads the source xlsx -> data.json
python3 charts.py    # data.json -> charts.json (inline SVG)
python3 page.py      # -> efu-utilisation-summary.html
node shot.js         # -> EFU-Utilisation-Summary.pdf (needs playwright + chromium)
```

`build.py` holds the source path and `PURCHASED = 500`, the contracted ticket
count. That figure is supplied separately — the raw sheet carries no
entitlement or commercial fields.

## Counting basis

- **Ticket** = one KPI-generation request. 852 submitted; 838 returned KPIs.
- **User** = distinct email in the `KPIs` sheet.
- **Job title** = the `title` column, which the platform derives from the
  opening words of each request rather than a role name entered by the user.
