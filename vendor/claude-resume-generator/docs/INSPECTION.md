# PDF inspection steps

`scripts/build.py` runs these automatically through `scripts/inspect_pdf.py`; do them by hand if you build another way.

1. **Convert**: `soffice -env:UserInstallation=file:///tmp/lo_resume_profile --headless --convert-to pdf --outdir OUT FILE.docx` (the separate profile avoids lock-file problems).
2. **Pages and size**: `pdfinfo FILE.pdf`. Expect the target page count and A4 (595.3 x 841.9 pt).
3. **Fonts**: `pdffonts FILE.pdf`. Report requested vs embedded. Expected here: Carlito x3 plus Liberation Serif for the bullet glyph.
4. **Text and reading order**: `pdftotext -layout FILE.pdf -`. The name must come first; every bullet's first and last words must be present.
5. **Date lines**: each date sits on the same line as its title (no wrapped dates).
6. **Orphan headings**: no section heading is the last line of a page.
7. **Header lines**: headline and contact items each on one line (matters most with a photo).
8. **Render EVERY page and look at it**: `pdftoppm -png -r 100 FILE.pdf prefix` (no `-singlefile`; that option renders page 1 only). Open each PNG. Look for clipped text, uneven right edge, dates not flush right, and overlap with the photo.
9. **Compare with the reference** when reproducing the sample: `python3 scripts/compare_pdfs.py output/Sample_Resume.pdf YOUR.pdf`. Same look = text identical, max word shift < 0.1 pt, < 1% differing pixels.

## Reporting rules
- Say which engine (Node or Python) made the file and which font `pdffonts` shows.
- Report only checks you actually ran. If a tool is missing, say so instead of implying it passed.
- If any check prints FAIL, fix it or tell the user. Do not hand over a file with a known FAIL.
