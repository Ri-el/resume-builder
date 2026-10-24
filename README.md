# Resume Builder

An evidence-first skill for drafting, tailoring, translating, and auditing resumes. It pairs a restrained single-column A4 design with factual, content, and file-quality checks.

This repository combines an assistant writing workflow with an optional document generator. The assistant reviews evidence and prepares approved wording; the generator applies a repeatable layout. Text-only work needs no document tools.

## Use

Give an assistant that can read URLs the [raw skill instructions](https://raw.githubusercontent.com/Ri-el/resume-builder/main/SKILL.md), the candidate's own source materials, and any target job description. Specify the language and output format. If URL access is unavailable, attach or paste SKILL.md instead.

Suggested prompt:

> Read and follow the resume-generation instructions at https://raw.githubusercontent.com/Ri-el/resume-builder/main/SKILL.md. Use the attached candidate information and latest corrections. Create a restrained single-column A4 resume, perform factual, content, and rendering QA, and deliver only the format I request. Do not invent facts.

For assistants that load skill folders, use the whole repository so the optional checker and UI metadata remain available. Reading a URL does not install a skill or grant access to private candidate documents.

## Generate the strict A4 layout

The [strict profile](profiles/strict-a4.json) implements the specified single-column A4 format: Education before Experience, justified 10 pt body text, 9.5 pt headline/contact/date exceptions, right-aligned dates, real round bullets, and black/grey typography. The [full specification and input contract](references/strict-a4.md) explain the resolved rules.

Requirements: Python 3.10+, `python-docx` from `requirements.txt`, LibreOffice, Poppler, Fontconfig, and the requested font. On Ubuntu, the renderer tools are available as `libreoffice-writer`, `poppler-utils`, and `fontconfig`. Calibri must be installed separately; it is never silently replaced.

```bash
python -m pip install -r requirements.txt
python scripts/build_resume.py private/candidate.json --output private/resume.pdf --qa-dir private/qa
```

Use [examples/candidate.json](examples/candidate.json) to understand the accepted fields. It is entirely fictional. The generator preserves supplied wording and official titles, rejects unknown fields, and omits empty sections. It does not invent missing achievements or perform factual verification.

Default output is PDF only. A `.docx` output path requests DOCX only; `--also-docx` with a PDF output requests both. The generator converts internally, checks the tagged PDF export, and renders every page in all modes. `--qa-dir` retains page images and plain/layout/raw extraction plus font reports. Right-aligned dates can move in plain extraction; the report flags grouping differences for review. Visual inspection and factual checks remain **not checked** until someone actually performs them.

One-page fitting reduces paragraph spacing first, then margins down to 0.35 inches. Fonts and content are preserved. Remaining overflow or a title/date line collision returns `needs_decision` without publishing a deliverable. Use `--allow-multiple-pages` only after the user permits it. Date tabs always follow the current text width.

To demonstrate the layout with an explicitly chosen installed alternative, use `--font Carlito`. The output report identifies the substitution; it is not an exact Calibri result. The [sample PDF](examples/strict-a4-preview.pdf) uses Carlito and the fictional example content.

## DOCX preflight

Requires **Python 3.10+**, with no third-party Python dependencies. From the repository directory:

```bash
python scripts/check_docx.py /path/to/resume.docx
python scripts/check_docx.py /path/to/resume.docx --json
```

The checker reads the file without modifying it or printing candidate text. It flags:

- Missing/non-A4 page settings and multiple columns across all sections.
- Tables, text boxes, drawings, and header/footer text requiring reading-order review.
- Pending tracked changes, hidden text, and text below 9 pt, including ordinary style inheritance. Style-defined visibility is always flagged for review.
- Empty text content, unreadable archives, and unsupported XML inputs.

| Exit | Meaning | Next step |
| --- | --- | --- |
| `0` | No supported static issue found | Continue factual, rendering, and PDF extraction checks. |
| `1` | Review or fix required | Inspect the findings; correct defects or confirm intentional choices. |
| `2` | Invalid or unreadable input | Check the file, format, and access permissions. |

`--json` emits a versioned report with `status`, `findings`, and `limitations`. Status is `pass`, `review`, `fail`, or `error`; `fail` identifies blocking content problems such as pending tracked changes or no ordinary body text. Tables or a requested non-A4 layout may be intentional, so review findings are not automatic proof of a defect.

A preflight pass is **not** factual verification, a complete DOCX-format validation, a visual inspection, or an ATS guarantee. The checker supports ordinary WordprocessingML; advanced constructs, style toggle semantics, theme fonts, complex-script sizes, external content, and renderer-specific behavior require manual review. Inspect every exported page and compare both plain and layout-preserving PDF text extraction. See [the export workflow](SKILL.md#83-export-and-inspect).

## Checks and contributions

Run the synthetic document tests locally:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

[GitHub Actions](.github/workflows/checks.yml) runs the suite on Python 3.10, 3.12, and 3.13. A separate job runs real LibreOffice/Poppler export and overflow tests with Carlito. It also validates skill metadata and local resource links. All tests use fictional data and temporary directories.

To enable the real renderer tests locally with the required tools and Carlito installed:

```bash
RESUME_RUN_RENDER_TESTS=1 python -m unittest discover -s tests -p test_resume_render.py -v
```

For changes to the writing workflow, run the fictional prompts in [evals/cases.json](evals/cases.json) in fresh assistant conversations with SKILL.md and assess each criterion. These behavioral scenarios cover corrections, metric attribution, credentials, embedded instructions, limited evidence, bounded edits, and unavailable tools. They are not run by the Python suite.

## Privacy

Do not commit real candidates' details, resumes, certificates, outputs, or audit reports. Keep them outside this repository or in its git-ignored `private/` directory. Use only fictional data for examples and tests. Ignoring a directory does not protect files that were already tracked; review staged changes before publishing.
