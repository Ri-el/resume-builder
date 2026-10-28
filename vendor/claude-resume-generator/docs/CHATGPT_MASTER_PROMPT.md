# Master prompt to paste into ChatGPT (upload the whole ZIP with it)

```
You are given a ZIP named resume-generator. Unzip it and use it exactly as documented. Do NOT redesign the resume or write your own
document-generation code.

STEP 0  Read README.md, docs/INPUT_FORMAT.md, docs/STYLE_SPEC.md and docs/RECONSTRUCTION_NOTES.md.
STEP 1  Run: python3 scripts/check_env.py   and tell me what is missing. Install what you can (pip install -r requirements.txt; npm ci if Node exists).
STEP 2  Self-test BEFORE touching my content:
        python3 scripts/build.py --input input/sample_resume.json --name Sample_Resume --outdir selftest
        python3 scripts/compare_pdfs.py output/Sample_Resume.pdf selftest/Sample_Resume.pdf
        Report the numbers. If text is not identical or more than 1% of pixels differ, tell me why before continuing.
STEP 3  Take MY facts (below) and put them into a new JSON file following docs/INPUT_FORMAT.md. Extracting facts, tailoring wording and
        choosing which facts to include is your job; the layout is not. Do not invent facts, numbers, tools, titles or achievements.
        Do not use em dashes. Keep my official job titles exactly.
STEP 4  Build: python3 scripts/build.py --input my_resume.json --name <Firstname_Lastname_Resume> --outdir out [--variants both --photo prepared.jpg]
        (prepare a supplied photo with scripts/prepare_photo.py; never generate or alter a face; no photo = no-photo version only.)
STEP 5  Look at EVERY rendered page PNG yourself, then run the inspection in docs/INSPECTION.md. Fix any FAIL.
STEP 6  Deliver only the file types I ask for (default: PDF only). Then report plainly:
        - which engine made it (node or python) and which fonts pdffonts shows (Carlito vs Calibri)
        - which page-fitting level was used (the .style_used.json file) and whether any content had to be cut (it must not be, without asking me)
        - every WARN or FAIL, and any check you could not run
        - any gap between my experience and the job description

NEVER: edit config/style.json, generate.js or generate_py.py unless I ask; shrink the font; replace the PDF step with another converter that changes
the look; claim a check you did not run; call the Python port the original method (the original is the Node script).

MY FACTS / JOB DESCRIPTION:
[paste here]
```

## If ChatGPT's sandbox lacks something
| Missing | What to do |
|---|---|
| Node.js | Use `--engine python` (verified pixel-identical to the Node output on the samples and the approved resume) |
| LibreOffice | Build the DOCX only, say the PDF could not be produced, and let the user export it from Word. Do not substitute another PDF route and claim the same look |
| Carlito/Calibri | Say so. Lines can break differently; show the `compare_pdfs.py` numbers |
| Internet (for `npm ci`) | Python engine |
