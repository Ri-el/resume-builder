# Generate with the supplied Claude method

Use [the supplied Node renderer](../vendor/claude-resume-generator/generate.js)
for the established resume format. Prepare wording using
[content-preparation.md](content-preparation.md). Keep the renderer and
[style file](../vendor/claude-resume-generator/config/style.json) unchanged.

## Source and boundaries

The user supplied `resume-generator.zip`. Its selected files are copied unchanged
under `vendor/claude-resume-generator/`; [UPSTREAM.json](../vendor/claude-resume-generator/UPSTREAM.json)
records the original archive hash and each copied file's hash.

The Node helpers were recovered from a chat transcript. The data wrapper is a
refactor, the Python file a reconstructed port, and the fitting ladder and photo
variant later extensions. Preserve these distinctions from
[the reconstruction notes](../vendor/claude-resume-generator/docs/RECONSTRUCTION_NOTES.md).
The private approved BA resume is not included, so local comparison establishes
reproduction of the supplied fictional samples, not independent verification of
that private resume or Claude's historical claims.

Use the Node engine explicitly. Do not silently switch to the earlier repository
renderer or the Python port, rewrite drawing code, or adjust style values.

## Environment and self-test

Use Node with `docx` **9.6.1**, Python with Pillow, LibreOffice and Poppler. Run
`npm ci --prefix vendor/claude-resume-generator` when the exact Node dependency is
not already supplied by the environment. See the supplied
[environment record](../vendor/claude-resume-generator/evidence/environment.txt).
Use the available bundled runtime for document work when applicable.

The reference uses **Carlito 1.104**, **Liberation Serif 2.1.5** for bullets, and
LibreOffice **24.2.7.2**. The DOCX requests Calibri, but installing Calibri or using
Fluent Calibri changes the rendering. Require the measured reference fonts for a
faithful reproduction and report the actual PDF fonts. Carlito 1.103 also changes
the result; a matching family name alone is insufficient. Ubuntu 24.04 supplies
Carlito 1.104 in `fonts-crosextra-carlito` version `20230309-2`.

From the repository root, use a fresh output directory:

```bash
python vendor/claude-resume-generator/scripts/build.py --engine node \
  --input vendor/claude-resume-generator/input/sample_resume.json \
  --name Sample_Resume --outdir private/claude-selftest
python vendor/claude-resume-generator/scripts/compare_pdfs.py \
  vendor/claude-resume-generator/output/Sample_Resume.pdf \
  private/claude-selftest/Sample_Resume.pdf
```

Record page counts, text equality, word-position shifts and differing pixels.
If text differs or more than 1% of pixels differ, investigate and disclose the
environment difference before proceeding with candidate content. Do not change
the style to conceal a renderer mismatch. Matching DOCX XML does not prove that
different converters render the same PDF. The comparison script reports values
but does not fail its exit status when those values disagree; read its output.

## Build the candidate file

Use [the verified entry point](verified-workflow.md) for delivery. It enforces the Node method and refuses an environment mismatch. The source package commands below document the underlying method; they do not replace the verified entry point.

```bash
python scripts/build_verified_resume.py --input private/candidate.json \
  --output private/resume.pdf --qa-dir private/resume-qa
```

Use the package's native JSON contract. The style intentionally keeps its 6.9-inch
date tab, original paragraph gaps, single line spacing and left-aligned language
list. Do not replace these with the earlier strict profile's measurements.
The fitting ladder scales paragraph spacing, then reduces only top/bottom
margins, with a 0.35-inch floor. Fonts and content stay unchanged. Record the
actual `<name>.style_used.json` and every fitting attempt.

Use `--variants both --photo supplied-and-prepared.jpg` only when requested.
The shipped silhouette is a fictional demonstration, never a candidate photo.
Do not send the internally generated DOCX, input JSON, inspection report or page
images when the requested deliverable is PDF only.

## Inspect the actual export

Inspect every generated page image, preferably rerendering at 150 dpi or more.
Run `pdfinfo`, `pdffonts`, and plain/layout/raw `pdftotext`. Check full text,
reading order, title/date rows, header wrapping and orphan headings yourself.
The supplied inspector is useful but partial: it does not prove complete text
preservation, all font embedding, sensible plain-text order or visual quality.
Never copy its passing labels into a broader claim that those checks passed.

Use a fresh output directory because the unchanged upstream builder does not
protect against stale exports or overwrite existing outputs. Do not publish a
file after a failed build, even if that file remains on disk.

The previous Python renderer remains available only for an explicitly requested
[legacy strict A4 profile](strict-a4.md). It is not the method used for the
supplied Claude baseline.
