# Verified resume generation

Use `scripts/build_verified_resume.py` as the single entry point for the established
PDF format. Keep the supplied renderer, style and fitting helpers unchanged.

For ordinary new PDFs, go to [portable exports](verified-workflow.md#new-exports-with-installed-libreoffice).
Use the [approved Word route](verified-workflow.md#routine-edits-to-an-approved-word-layout) for an
edit to a saved layout. The commands below apply when exact reference
reproduction is required.

```bash
python scripts/build_verified_resume.py --doctor
python scripts/build_verified_resume.py --check-input \
  --input private/candidate.json --evidence private/evidence.json
python scripts/build_verified_resume.py --input private/candidate.json \
  --evidence private/evidence.json --output private/resume.pdf --qa-dir private/resume-qa
```

The default build runs its reference test every time. Use approved native JSON from
[content-preparation.md](content-preparation.md). Use a fresh QA directory and
`--overwrite` only for an authorised revision. Add `--also-docx` only when requested.
Keep candidate inputs, exports and QA files in the task workspace, outside the
installed skill folder. Never save private candidate information with the skill.
For a longer professional or academic CV, add `--target-pages N`. This sets a
maximum, defaults to one page and never authorises content cuts. The fictional
reference self-test remains one page regardless of the candidate's maximum.

`--check-input` needs no document tools. It validates the native input and optional
[evidence ledger](../docs/EVIDENCE_FORMAT.md), returning `status: valid_input`;
it does not certify facts, fit or rendering. `--doctor` checks sources and required
tools without rendering, returning `status: ready_for_self_test` when those checks
pass. It does not verify fonts or PDF fidelity. Use `--self-test` alone to run the
full reference reproduction without candidate files. These modes reject options
they would otherwise ignore.

The entry point checks:

1. Every recorded source file still matches the supplied package hash.
2. The exact `docx` library version 9.6.1 and LibreOffice 24.2.7.2 are available.
3. A freshly generated fictional reference has the same five DOCX XML parts,
   identical PDF text, zero measured word shift and zero differing pixels in the
   supplied 100 dpi comparison. Read the integer pixel count, not a rounded percentage.
4. The candidate build succeeds using the unchanged Node method and fitting ladder,
   within the requested maximum. It renders a snapshot of the validated input,
   whose SHA-256 is recorded, rather than rereading a possibly changed source.
5. Every native input field is supported and every complete text fragment and
   repeated-word count survives plain, layout-preserving and raw extraction.
6. PDF fonts are embedded and match the reference families, Carlito and the
   Liberation Serif bullet fallback.
7. The PDF's measured page count is within the requested maximum, and every page
   has a non-empty QA PNG. When evidence is supplied, every candidate text field
   has matching ledger wording and references to declared sources.

Only after these checks does it release the requested output. Exit 2 and
`status: blocked` mean the workflow could not meet its requirements. Explain the
reported reason; do not produce an approximation or claim a passing check.
The fresh export profile prevents stale preferences from changing conversion.

## New exports with installed LibreOffice

Choose this route before building when the job requires the standard template
and a checked PDF, and pixel-level reference reproduction is unnecessary.

```bash
python scripts/build_verified_resume.py --doctor --portable
python scripts/build_verified_resume.py --portable --input private/candidate.json \
  --evidence private/evidence.json --output private/resume.pdf --qa-dir private/resume-qa
```

Portable mode uses the installed LibreOffice with the same `docx` 9.6.1 renderer,
approved font families and page-fitting rules. It skips rebuilding and comparing
the fictional reference and reuses the renderer's 100 dpi QA images. The PDF
still has to pass the renderer's layout checks, embed the expected fonts and
preserve the approved text in layout and raw extraction without extra words.
Plain extraction is saved for review. The report names the converter and sets
`reference_comparison: not_checked`. Rendering differences between converter
versions can affect wrapping and pagination, so inspect each page before delivery.
Use the default route for exact reference reproduction. A failed check blocks
release in either mode.

## Routine edits to an approved Word layout

Use this route only for a saved approved Word source when exporting with the
installed LibreOffice is authorised and a pixel comparison with the fictional
reference is unnecessary. Edit a private copy of the DOCX and update the native
JSON and evidence to match the approved wording. Keep the DOCX's styles, margins
and page breaks. Then run:

```bash
python scripts/build_verified_resume.py --approved-docx private/edited.docx \
  --input private/candidate.json --evidence private/evidence.json \
  --target-pages 2 --output private/resume.pdf --qa-dir private/revision-qa
```

Set `--target-pages` to the approved **exact** page count for this route. It
requires LibreOffice, the approved fonts and Poppler, and runs one export with a
20-second conversion limit. It uses the saved Word formatting without running
the fitting ladder. The PDF must retain the requested pages, embed Carlito
(and Liberation Serif where used), and preserve the approved text in layout and
raw extraction without extra words. Plain extraction is saved for review since
it can drop a visible hyphen at a line break. Review every rendered page as usual.

The report identifies the converter and records
`reference_comparison: not_checked`. If a check fails, report the specific
problem and keep the last approved PDF. Use the default workflow if exact
reference reproduction is required. Keep the approved editable source and its
matching JSON privately available for the next revision.

## Visual and factual review

Open every final `page-*.png` in the QA directory. Review wrapping, collisions,
orphan headings and reading order. `visual_inspection: not_checked` is deliberate:
software cannot claim that an assistant actually looked at an image.
Review facts and target-role gaps independently. Never treat this as an ATS score.
The report explicitly leaves `factual_verification`, `reading_order` and
`ats_validation` as `not_checked`, too. Describe actual manual reviews separately;
do not change an automated status to imply independent verification. The optional
ledger is checked for coverage, not authenticity. Builds without it report
`evidence_validation.status: not_provided`.

## Reuse in new chats

Share the [repository link](https://github.com/Ri-el/resume-builder) with the
resume request and attach career evidence if the chat does not already have it.
Follow [setup](../docs/SETUP.md) for the prerequisites of the selected mode.
When the chat lacks file or renderer access, continue with evidence-based content
and explain what is needed to finish the PDF.
Do not send private candidate information to public CI to work around a missing
local environment.

The supplied photo extension and reconstructed Python port remain source artifacts.
This verified entry point supports the established no-photo PDF layout. A request
for a different layout requires an explicit, separately validated change.
