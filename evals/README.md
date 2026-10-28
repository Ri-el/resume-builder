# Assistant behaviour evaluations

Use fictional scenarios in [cases.json](cases.json) to measure instruction following
separately from Python tests and renderer fidelity. No cross-platform pass rate is
claimed by this repository. A list of prompts is not evidence of successful runs.

## Run a case

1. Start a fresh conversation with the target assistant and give it the public
   repository link and the same short start instructions a user would receive.
   For a locally installed skill test, record that route instead.
2. Provide the case's `prompt` without its criteria, a diagnosis or an expected
   answer. Keep independent runs isolated from previous responses and artifacts.
3. Record the actual response and requested output files, if any. Use fictional
   data only. Do not upload real resumes to public results or CI.
4. Assess each listed criterion as `pass`, `fail` or `not_assessed`, citing a
   concrete observation. Mark tool-dependent criteria unassessed if the tools were
   unavailable; do not infer a render or visual pass from a textual assertion.
5. Record limitations and retest failures after a change using a fresh conversation.

## Record a result

For each run, retain the case ID, date, repository commit, platform, exact model
identifier when exposed, available tools, installation/link route, actual response,
per-criterion observations and reviewer. Say `not exposed` for unknown model
metadata. Keep private local artifacts outside the repository.

Use this shape for a record; the entries below are a template, not a test result:

```json
{
  "case_id": "case-id-from-cases-json",
  "date": "YYYY-MM-DD",
  "repository_commit": "tested commit SHA",
  "platform": "observed platform",
  "model": "exact identifier or not exposed",
  "tools": ["observed capabilities"],
  "route": "repository link or installed skill",
  "response": "actual observed response",
  "criteria": [
    {"index": 0, "result": "not_assessed", "observation": "not run"}
  ],
  "reviewer": "reviewer",
  "limitations": ["unassessed aspects"]
}
```

Report results by platform, model and capabilities. A pass on one assistant does
not establish a pass on another. Do not combine factual, layout, parser and
tool-availability checks into a universal ATS score.

For generated files, require the verified entry point and inspect every page.
Evaluate one-page resumes and longer CVs separately. The Python integration suite
tests real rendering only when `RESUME_RUN_CLAUDE_TESTS=1` is set in the reference
environment; skipped integration tests are not passes.
