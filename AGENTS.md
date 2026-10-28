# Repository workflow

For resume requests, read `SKILL.md` and follow its content and PDF workflow.
Use `scripts/build_verified_resume.py` as the only delivery entry point. Do not
replace the renderer when a check fails. Keep candidate inputs, outputs and QA
files in an external task directory or the ignored `private/` directory.

For code changes, preserve all files listed in
`vendor/claude-resume-generator/UPSTREAM.json`. Run the unit suite and the relevant
real renderer checks described in `CONTRIBUTING.md`. Use fictional fixtures only.
