# Setup

Use the complete repository, not only `SKILL.md`. The generator needs its source,
style settings and reference fixtures. Clone it with Git or use **Code → Download
ZIP** on GitHub and extract it.

## Docker

Docker is the simplest way to keep the renderer separate from your machine's
fonts and LibreOffice settings. The image uses Ubuntu 24.04 and runs the reference
test during the build. If distribution packages change and no longer reproduce
the reference, the image build fails instead of releasing a different layout.

Run from the repository root in a POSIX shell. On Windows, use WSL with Docker
Desktop's WSL integration enabled.

```bash
docker build --platform linux/amd64 -t resume-builder .
docker run --rm --platform linux/amd64 --network none resume-builder --self-test
mkdir -p private
cp vendor/claude-resume-generator/input/template_empty.json private/candidate.json
```

Replace every placeholder with your own facts. Remove optional sections that
have no evidence. Keep at least one real headline item, one contact item and one
section; the unchanged source inspector requires these. Read the
[input contract](../vendor/claude-resume-generator/docs/INPUT_FORMAT.md) and
[content guide](../references/content-preparation.md).

```bash
docker run --rm --platform linux/amd64 --network none \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,source=$(pwd)/private,target=/work" \
  resume-builder --input /work/candidate.json \
  --output /work/resume.pdf --qa-dir /work/qa-1
```

Generation runs without network access. Only the directory you mount is exposed
to the running container. Never put candidate files in the image or publish them
as CI artifacts. Run the build from the repository, with private files inside
the ignored `private/` folder or outside the repository; `.dockerignore` uses an
allowlist so the image does not receive other files.

Output is PDF only. `--also-docx` adds Word format. For a revision, use a new QA
directory, such as `/work/qa-2`, and `--overwrite` when replacing an approved output.

## Native Ubuntu 24.04

The reference uses Linux x86-64, `docx` 9.6.1, LibreOffice 24.2.7.2, Carlito 1.104,
Liberation Serif 2.1.5, Python 3.10+ and Poppler. Matching version labels alone is
insufficient; the entry point also reproduces the reference PDF.

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  nodejs npm python3 python3-venv libreoffice-writer poppler-utils \
  fontconfig fonts-crosextra-carlito fonts-liberation
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
npm ci --prefix vendor/claude-resume-generator
python scripts/build_verified_resume.py --self-test
```

If the self-test passes:

```bash
python scripts/build_verified_resume.py --input /absolute/task/candidate.json \
  --output /absolute/task/resume.pdf --qa-dir /absolute/task/qa-1
```

The DOCX asks for Calibri; the measured reference uses Carlito. Do not add Calibri,
Fluent Calibri or a different Carlito version to make the build pass. Use a clean
reference environment. On macOS, Windows or another Linux distribution, prefer
the Linux Docker image rather than expecting the installed Word converter to
produce the same result.

## Review the result

Before a full build, run `python scripts/build_verified_resume.py --doctor` (or
`docker run --rm --network none resume-builder --doctor`). It checks source
integrity and required program/library versions without rendering. A result of
`ready_for_self_test` does not establish font fidelity; the reference self-test
still runs during generation. A blocker must be fixed in the reference environment.

Validate private native input and the separate ledger without Node or LibreOffice:

```bash
python scripts/build_verified_resume.py --check-input \
  --input /absolute/task/candidate.json --evidence /absolute/task/evidence.json
```

See [evidence format](EVIDENCE_FORMAT.md) for the ledger contract. This check never
releases files or verifies factual truth. Manual builds may omit the ledger; the
report marks it `not_provided`. Assistant-authored file builds supply it.

For a multipage professional or academic CV, add `--target-pages N` to the normal
generation command. This sets a positive maximum; it does not force exactly N
pages, change the original visual style or authorise cuts. Keep an explicit
one-page instruction unless the candidate changes it. The same options work after
the Docker image name, with candidate and ledger paths inside the mounted folder.
Keep the released PDF/DOCX outside the fresh QA directory.

Require exit 0 and `status: passed`. Open every `page-*.png` in the QA directory
and inspect the PDF. Read `fonts.txt`, `plain.txt`, `layout.txt` and `raw.txt`.
Check the candidate's facts, section sequence, dates and titles, awkward wraps,
overflow and orphan headings. The JSON report leaves visual inspection marked
`not_checked`; an automated build cannot claim someone looked at a page.

## Common blockers

| Message or condition | Action |
| --- | --- |
| No repository download or URL access | Attach the repository ZIP to the chat. |
| Chat cannot execute code or run Docker | Prepare content in chat, then run the commands on your computer. No PDF was generated in that chat. |
| Reference converter unavailable | Use the reference environment or Docker. Do not switch converters. |
| Reference DOCX or PDF differs | Check tools, fonts and unmodified source. Do not edit the reference to make it pass. |
| Required list is empty | Supply a truthful headline/contact item or required section; do not invent one. |
| Evidence is missing, stale or references an unknown source | Reconcile the native input and private ledger against actual supplied sources; rerun `--check-input`. |
| Diagnostic says `valid_input` or `ready_for_self_test` | No PDF has been verified or released. Continue with the normal generation command. |
| QA directory must be fresh | Choose a new path for the next build. |
| Input will not fit or a title/date collides | Ask the candidate about content cuts or a separately approved layout change. Do not shorten titles or shrink fonts. |
| PDF text preservation fails | Inspect the full source and extraction. Do not deliver partial content. |

For an assistant, the [public instructions](../SKILL.md) define when to stop and
what can be reported. A repository link does not install a personal skill or
guarantee tools are available in every ChatGPT account.
