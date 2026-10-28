# What is exact, what is reconstructed

| Component | Status | Evidence |
|---|---|---|
| Helper functions (`sectionHeading`, `bullet`, `entryHeader`, `subLine`, `skillLine`), numbering config, every numeric value in `config/style.json` | **EXACT**: taken from the approved Node script | Generated DOCX is byte-identical to the approved DOCX (`evidence/fidelity_report.md`) |
| The approved script **files** from the earlier chat sessions | **LOST** in a sandbox reset. The BA script was **re-created verbatim from the chat transcript** and checked against the approved render | Same report, "Provenance" |
| `generate.js` data-driven wrapper (JSON input, `style.json`, section types) | **NEW refactor** of the exact functions above | Regenerating the approved resume from JSON gave identical XML |
| `generate_py.py` (python-docx) | **RECONSTRUCTED PORT.** It was never used to make the approved resume | Pixel-identical to the approved PDF after four documented fixes (0 differing pixels); identical to the Node output on all three samples |
| `scripts/build.py` page-fitting ladder | **CODIFIED.** The original was manual: tweak spacing, then margins, re-render, look | `docs/PAGE_FITTING.md` |
| `scripts/inspect_pdf.py` | **NEW automation.** Originally I counted pages, rendered pages to images and looked at them. `pdffonts` and `pdftotext` were not part of the original build loop; they were added for this package | `docs/INSPECTION.md` |
| Photo variant, `prepare_photo.py` | **EXTENSION**, not in the approved resume. Rendered in LibreOffice only | `docs/PHOTO_VARIANT.md` |
| Fonts | **MEASURED**, not assumed | `evidence/approved_pdf_pdffonts.txt` |
| PDF conversion | Approved PDFs were made with LibreOffice headless through a sandbox helper script. This package calls plain `soffice` with a separate profile. Output was pixel-identical in testing | `evidence/fidelity_report.md` |

## Known limits
- Only LibreOffice 24.2.7.2 on Ubuntu 24.04 was tested. Word, Google Docs and other converters were not.
- Real Calibri was not available, so every PDF embeds Carlito.
- If a different LibreOffice version or font set is used, expect small differences. Use `scripts/compare_pdfs.py` against `output/Sample_Resume.pdf` to measure them.
