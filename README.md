# Resume and CV Builder

Single-column A4 resumes and CVs with a fixed visual style, evidence-based writing
and checked PDF output. Select content for the application, preserve the candidate's
facts and validate the actual files before delivery.

## Make a resume with AI

Attach your current resume or paste your career notes, then send this message.

> Build my resume using https://github.com/Ri-el/resume-builder.

Add a job description if you want a tailored version. Add a page limit or
preferred language if you have one. For a small edit, attach the approved Word
file and its matching JSON if you have them.

### Instructions for AI assistants

When a resume request names `Ri-el/resume-builder` or links to this repository,
read [SKILL.md](SKILL.md) from the requested revision. Use the candidate evidence
already in the chat and ask only for missing information essential to the result.
With the needed tools available, build, inspect and return the PDF in the same turn.
Use portable export for ordinary new PDFs and the saved Word layout for approved
edits. Keep candidate files private and validate them with the renderer.

PDF delivery requires an assistant that can access the repository, run the
renderer and return files. With text-only tools, provide the content and explain
what is needed to finish the PDF. See [capabilities](references/intake-and-document-types.md#work-within-actual-capabilities).

[View the sample PDF](vendor/claude-resume-generator/output/Sample_Resume.pdf) · [Download ZIP](https://github.com/Ri-el/resume-builder/archive/refs/heads/main.zip) · [Setup](docs/SETUP.md)

## Layout

A4, one column, black text and grey dates/company lines. A 16 pt name, 10.5 pt section headings, 10 pt body and 9.5 pt headline/contact/dates keep the page compact. Entries use right-aligned dates and round bullets. There are no photos, tables, icons, skill bars or watermarks in the supported layout.

The new-graduate resume default is **Summary → Education → Experience → Skills →
Achievements → Languages**, omitting empty or unhelpful sections. New professional
and academic CVs can select and order the existing section types for relevant
experience, research, teaching, publications and funding. Preserve already approved
ordering during bounded edits. See [document types](references/intake-and-document-types.md).

The page-fitting steps reduce spacing, then vertical margins, without shrinking
text or cutting content. The default maximum is one page. `--target-pages N` allows
an explicitly selected longer CV without changing the one-page reference self-test.
It sets a maximum, not a reason to pad or discard content. Inspect every page.

The DOCX requests Calibri. The reference PDF embeds **Carlito 1.104**, with Liberation Serif for bullet dots. These are the fonts used to reproduce the sample. See the [style specification](vendor/claude-resume-generator/docs/STYLE_SPEC.md).

## Run locally

From a checkout with the [portable prerequisites](docs/SETUP.md#build-with-the-installed-libreoffice),
test the PDF workflow with the fictional fixture and its matching evidence.

```bash
python3 scripts/build_verified_resume.py --portable \
  --input evals/fixtures/fictional_candidate.json \
  --evidence evals/fixtures/fictional_evidence.json \
  --output private/sample.pdf --qa-dir private/sample-qa
```

Open `private/sample.pdf` and inspect every `private/sample-qa/page-*.png`.
For actual applications, use your own private input and evidence files.

With Docker installed, build the reference environment once and reuse the image.

```bash
docker build --platform linux/amd64 -t resume-builder .
mkdir -p private
cp vendor/claude-resume-generator/input/sample_resume.json private/candidate.json
# Replace the fictional sample with your own information before using the PDF.
docker run --rm --platform linux/amd64 --network none \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,source=$(pwd)/private,target=/work" \
  resume-builder --portable --input /work/candidate.json \
  --output /work/resume.pdf --qa-dir /work/qa
```

Open `private/resume.pdf` and inspect every `private/qa/page-*.png` before using the resume. Run each revision with a fresh QA directory; use `--overwrite` for an authorised replacement. Add `--also-docx` only when you also want Word format. [Native setup and troubleshooting](docs/SETUP.md) cover systems without Docker and Windows users.

## What gets checked

Portable builds check the renderer's source hashes, exact document library,
candidate text, page layout and embedded fonts. Add the evidence ledger to check
that every claim has a source and matches the approved wording. For exact
reference reproduction, run a strict build without `--portable`. It also
compares the fictional reference's DOCX XML, PDF text, word positions and pixels.

The automated report leaves visual inspection marked `not_checked`. Separately
review every page for factual issues, reading order, awkward wraps and title/date
collisions. These checks do not establish a universal ATS pass or guarantee a job outcome.

Use `--check-input` when you need to validate the JSON and evidence without
generating a PDF. Use `--doctor --portable` to diagnose missing dependencies.
The build command validates its input and supplied evidence itself.

```bash
python scripts/build_verified_resume.py --check-input \
  --input evals/fixtures/fictional_candidate.json \
  --evidence evals/fixtures/fictional_evidence.json
python scripts/build_verified_resume.py --doctor --portable
```

`valid_input` confirms that the input and supplied ledger are consistent.
`ready_for_portable_export` confirms that the prerequisite check passed.
A completed build reports `status: passed` and provides the PDF for visual review.

Assistant-authored file builds supply a private
[evidence ledger](docs/EVIDENCE_FORMAT.md) with `--evidence /work/evidence.json`.
Manual builds without one remain supported and report `not_provided`. Coverage
checks detect missing source references and stale wording; factual truth still
requires review. Reports separately mark factual verification, visual inspection,
reading order and ATS testing as `not_checked`. The validated input is snapshotted
before rendering, and measured page count and input digest are recorded.

## Project files

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Instructions for a new assistant conversation |
| [Content guide](references/content-preparation.md) | Facts, wording and JSON field placement |
| [Intake and document types](references/intake-and-document-types.md) | Resume/CV selection, application requirements and capability limits |
| [Evidence format](docs/EVIDENCE_FORMAT.md) | Separate private source ledger and coverage validation |
| [Input format](vendor/claude-resume-generator/docs/INPUT_FORMAT.md) | Supported fields and section types |
| [Verified workflow](references/verified-workflow.md) | Build, checks and review requirements |
| [Source record](references/claude-generation.md) | Renderer origin, dependencies and boundaries |
| `scripts/build_verified_resume.py` | The supported PDF entry point |
| `vendor/claude-resume-generator/` | Unmodified renderer, style and reference fixtures |

## Contributing

Run `python -m pip install -r requirements.txt`, then `python -m unittest discover -s tests -v`. The CI also builds the Docker image and tests real PDF generation in the reference environment. See [CONTRIBUTING.md](CONTRIBUTING.md) for renderer checks and fictional writing scenarios.
Use the [evaluation procedure](evals/README.md) to record observed assistant
behaviour separately from code tests; an unrun scenario is not a passed result.

Keep real resumes, contact details and certificates out of commits, issues and public CI. Use the ignored `private/` folder or a directory outside the repository. The Docker build excludes candidate files, and generation can run without network access.

[MIT licence](LICENSE). Dependencies and separately installed fonts retain their own licences.
