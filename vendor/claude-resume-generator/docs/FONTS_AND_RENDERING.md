# Fonts: what the code requests vs what the PDF actually embeds

| | Font |
|---|---|
| **Requested in code** | `Calibri`, set on every run (`w:ascii`, `w:hAnsi`, `w:cs`, `w:eastAsia`) via `font_requested` in `config/style.json` |
| **Embedded in the approved PDF** (`pdffonts`) | `Carlito-Bold`, `Carlito-Regular`, `Carlito-Italic`, `LiberationSerif` |
| Calibri embedded? | **No.** Calibri was not installed in the environment that made the approved PDF |

Glyph breakdown of the approved PDF (counts only, from PyMuPDF; full output in `evidence/approved_pdf_pdffonts.txt`):

| Embedded font | Glyphs | What it draws |
|---|---|---|
| Carlito-Regular | 2,846 | body text, contact line, skills text, bullets' text, middle dots |
| Carlito-Bold | 395 | name, headline, headings, titles, skill labels |
| Carlito-Italic | 245 | dates, company/location lines (en dash inside dates) |
| LiberationSerif | 11 | **only the bullet character "•"** (11 bullets) |

## Why
- LibreOffice cannot find Calibri on Linux, so it substitutes **Carlito**, which is designed to be metric-compatible with Calibri (same character widths, so lines break in the same places). Letter shapes differ slightly from real Calibri.
- The bullet level in the numbering definition names no font, and docx-js leaves the document default font empty, so LibreOffice draws the bullet in its fallback, **Liberation Serif**. This is part of the approved look. Do not "fix" it.

## What to do
1. Run `python3 scripts/check_env.py`. On Linux, `sudo apt-get install fonts-crosextra-carlito` gives Carlito.
2. To reproduce the approved PDF's fonts exactly, convert on a machine that has Carlito **and not Calibri**. If Calibri is installed, LibreOffice embeds Calibri instead. Calibri is **untested** here, so say so if you use it.
3. After every conversion run `pdffonts` and **report which font was embedded**. Never claim Calibri if `pdffonts` shows Carlito. `scripts/inspect_pdf.py` prints this automatically and flags it as WARN (expected) or FAIL (neither font present).
4. The DOCX itself requests Calibri, so on a machine with Calibri, Word shows Calibri. That was not tested in this package.
