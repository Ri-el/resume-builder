# Resume Builder

An evidence-first skill for drafting, tailoring, translating, and auditing resumes. It pairs a restrained single-column A4 design with factual, content, and file-quality checks.

This is an assistant workflow, not a resume-generation application. Text-only work needs no document tools; DOCX/PDF deliverables need suitable generation, conversion, and rendering tools.

## Use

Give an assistant that can read URLs the [raw skill instructions](https://raw.githubusercontent.com/Ri-el/resume-builder/main/SKILL.md), the candidate's own source materials, and any target job description. Specify the language and output format. If URL access is unavailable, attach or paste SKILL.md instead.

Suggested prompt:

> Read and follow the resume-generation instructions at https://raw.githubusercontent.com/Ri-el/resume-builder/main/SKILL.md. Use the attached candidate information and latest corrections. Create a restrained single-column A4 resume, perform factual, content, and rendering QA, and deliver only the format I request. Do not invent facts.

For assistants that load skill folders, use the whole repository so the optional checker and UI metadata remain available. Reading a URL does not install a skill or grant access to private candidate documents.

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
python -m unittest discover -s tests -v
```

[GitHub Actions](.github/workflows/checks.yml) runs the same suite on Python 3.10, 3.12, and 3.13. It also validates skill metadata and local resource links. All DOCX test inputs are generated in temporary directories; no real resumes are needed.

For changes to the writing workflow, run the fictional prompts in [evals/cases.json](evals/cases.json) in fresh assistant conversations with SKILL.md and assess each criterion. These behavioral scenarios cover corrections, metric attribution, credentials, embedded instructions, limited evidence, bounded edits, and unavailable tools. They are not run by the Python suite.

## Privacy

Do not commit real candidates' details, resumes, certificates, outputs, or audit reports. Keep them outside this repository or in its git-ignored `private/` directory. Use only fictional data for examples and tests. Ignoring a directory does not protect files that were already tracked; review staged changes before publishing.
