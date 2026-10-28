# Resume Builder

Single-column A4 resumes with a fixed layout, evidence-based writing and checked PDF output.

[View the sample PDF](vendor/claude-resume-generator/output/Sample_Resume.pdf) · [Download ZIP](https://github.com/Ri-el/resume-builder/archive/refs/heads/main.zip) · [Setup](docs/SETUP.md)

## Use with ChatGPT

Start a chat, attach your existing resume or career notes, and paste:

```text
Use https://github.com/Ri-el/resume-builder to create my resume.
Read and follow https://raw.githubusercontent.com/Ri-el/resume-builder/main/SKILL.md
Download the repository and run its verified generator. Keep its layout unchanged.
Use only my supplied facts and latest corrections. Deliver PDF only.
If the required tools or reference checks fail, explain the blocker and do not
substitute another template or claim that generation succeeded.

Target role or job description: [optional]
My information: [attach files or paste notes]
```

The chat needs repository access and a code environment with the required renderer, or Docker. A link supplies instructions; it does not install software or give every ChatGPT session file-generation tools. If downloads are unavailable, attach the ZIP. If code execution is unavailable, use ChatGPT to prepare the content and run the generator on your own computer using the setup below.

## Layout

A4, one column, black text and grey dates/company lines. A 16 pt name, 10.5 pt section headings, 10 pt body and 9.5 pt headline/contact/dates keep the page compact. Entries use right-aligned dates and round bullets. There are no photos, tables, icons, skill bars or watermarks in the supported layout.

Default section order: **Summary → Education → Experience → Skills → Achievements → Languages**. Empty sections are omitted. The page-fitting steps reduce spacing, then vertical margins, without shrinking text or cutting content.

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

The report leaves visual inspection marked `not_checked` until a person or assistant actually looks at every page. Review facts, reading order, awkward wraps and title/date collisions. These checks do not establish a universal ATS pass or guarantee a job outcome.

## Project files

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Instructions for a new assistant conversation |
| [Content guide](references/content-preparation.md) | Facts, wording and JSON field placement |
| [Input format](vendor/claude-resume-generator/docs/INPUT_FORMAT.md) | Supported fields and section types |
| [Verified workflow](references/verified-workflow.md) | Build, checks and review requirements |
| [Source record](references/claude-generation.md) | Renderer origin, dependencies and boundaries |
| `scripts/build_verified_resume.py` | The supported PDF entry point |
| `vendor/claude-resume-generator/` | Unmodified renderer, style and reference fixtures |

## Contributing

Run `python -m pip install -r requirements.txt`, then `python -m unittest discover -s tests -v`. The CI also builds the Docker image and tests real PDF generation in the reference environment. See [CONTRIBUTING.md](CONTRIBUTING.md) for renderer checks and fictional writing scenarios.

Keep real resumes, contact details and certificates out of commits, issues and public CI. Use the ignored `private/` folder or a directory outside the repository. The Docker build excludes candidate files, and generation can run without network access.

[MIT licence](LICENSE). Dependencies and separately installed fonts retain their own licences.
