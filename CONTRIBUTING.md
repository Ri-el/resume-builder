# Contributing

Keep changes focused. Use fictional candidate data in tests, screenshots and
issues. Keep the original renderer and source manifest intact; change content
guidance or the verification wrapper instead of creating a competing renderer.

## Unit checks

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Tests cover input preservation, claim-ledger coverage and stale values, input-only
validation, diagnostics, page-limit forwarding, refusal to release failed output,
source hashes, DOCX preflight and resource links. Real renderer tests include
multipage generation and remain opt-in locally because
they require the exact environment in [setup](docs/SETUP.md).

```bash
RESUME_RUN_CLAUDE_TESTS=1 python -m unittest discover -s tests -v
```

CI runs that suite in Ubuntu 24.04, then builds and exercises the public Docker
image using the fictional reference input. A reference mismatch is a failed check,
not a reason to rewrite the baseline or relax the comparison.

## Writing behaviour

Try the prompts in [evals/cases.json](evals/cases.json) in fresh conversations with
`SKILL.md`. Assess each listed criterion against the actual result. These are
manual scenarios, not tests run by the Python suite. In particular, check latest
corrections, team versus personal metrics, qualification status, bounded edits
and honest handling of missing tools. Follow [the evaluation procedure](evals/README.md)
to record model/environment information, observed responses and criterion results.
Keep unrun cases unassessed. Python tests validate the scenarios' structure, not
the quality of an AI's answers or compatibility with every platform.

## Pull requests

Explain the concrete change and the checks actually run. Do not attach real
resumes, private QA logs or candidate documents. Retain dependency and font
licences; no proprietary fonts are distributed with this project.
