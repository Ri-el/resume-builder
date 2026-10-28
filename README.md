# Resume and CV Builder

Single-column A4 resumes and CVs with a fixed visual style, evidence-based writing
and checked PDF output. Select content for the application, preserve the candidate's
facts and validate the actual files before delivery.

[View the sample PDF](vendor/claude-resume-generator/output/Sample_Resume.pdf) · [Download ZIP](https://github.com/Ri-el/resume-builder/archive/refs/heads/main.zip) · [Setup](docs/SETUP.md)

## Use with an AI assistant

Start a chat, attach your existing resume or career notes, and paste:

```text
Use https://github.com/Ri-el/resume-builder to create my resume or CV.
Read and follow https://raw.githubusercontent.com/Ri-el/resume-builder/main/SKILL.md
Obtain the complete repository. Establish the document type and page requirements.
Keep the approved visual style and any existing constraints unchanged.
Use only my supplied facts and latest corrections. Deliver PDF only.
Maintain a private evidence ledger, validate input and source coverage, then run
the verified generator. Inspect every output page and state checks actually done.
If the required tools or reference checks fail, explain the blocker and do not
substitute another template or claim that generation succeeded.

Document type and page limit: [resume / professional CV / academic CV; limit if any]
Target role or job description: [optional]
My information: [attach files or paste notes]
```

The assistant needs repository access and a code environment with the required
renderer, or Docker. A link supplies instructions; it does not install software or
give every AI session file-generation tools. If downloads are unavailable, attach
the ZIP. With text-only tools, prepare the content and run the generator locally.
See [intake and capabilities](references/intake-and-document-types.md). Cross-platform
AI compatibility is not established by the automated Python tests.

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

With Docker installed, from a downloaded or cloned copy of this repository:

```bash
docker build --platform linux/amd64 -t resume-builder .
mkdir -p private
cp vendor/claude-resume-generator/input/sample_resume.json private/candidate.json
# Replace the fictional sample with your own information before using the PDF.
docker run --rm --platform linux/amd64 --network none \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,source=$(pwd)/private,target=/work" \
  resume-builder --input /work/candidate.json \
  --output /work/resume.pdf --qa-dir /work/qa
```

Open `private/resume.pdf` and inspect every `private/qa/page-*.png` before using the resume. Run each revision with a fresh QA directory; use `--overwrite` for an authorised replacement. Add `--also-docx` only when you also want Word format. [Native setup and troubleshooting](docs/SETUP.md) cover systems without Docker and Windows users.

## What gets checked

Every build checks the renderer's source hashes, exact document library and converter, then reproduces the supplied fictional reference. The generated reference must match its DOCX XML, PDF text, measured word positions and pixel comparison. Candidate output is checked for complete text preservation and embedded fonts before release.

The automated report leaves visual inspection marked `not_checked`. Separately
review every page for factual issues, reading order, awkward wraps and title/date
collisions. These checks do not establish a universal ATS pass or guarantee a job outcome.

Before generation, validate native input and optional source coverage without any
document tools:

```bash
python scripts/build_verified_resume.py --check-input \
  --input evals/fixtures/fictional_candidate.json \
  --evidence evals/fixtures/fictional_evidence.json
python scripts/build_verified_resume.py --doctor
```

The first command demonstrates the fictional contract only. Replace all example
facts for an actual application. `valid_input` means the input and supplied ledger
are consistent; `ready_for_self_test` means dependencies and source hashes passed.
Neither means a PDF was generated. The build runs the full reference test itself.

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
