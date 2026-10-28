# Private evidence ledger

Keep the ledger beside the candidate's task files, outside the installed skill and
public repository. Pass it with `--evidence`; never put it inside native resume JSON.
The renderer still accepts only its original input format.

The ledger records which supplied sources support the selected wording. It does
not authenticate sources or prove that a candidate's statement is true. Check
source content and latest corrections separately. Do not create fictitious evidence
or copy facts from the example to complete a ledger.

## Version 1 contract

The top-level object has exactly `schema_version`, `sources` and `claims`.

| Field | Contract |
| --- | --- |
| `schema_version` | Integer `1` |
| `sources` | Non-empty array of `{id, kind, label}` objects |
| Source `id` | Unique lowercase identifier: 1–64 letters, digits, dots, underscores or hyphens; starts with a letter or digit |
| Source `kind` | `candidate_notes`, `document` or `correction` |
| Source `label` | Non-empty description of an actual supplied source; not a public upload or an instruction to fetch a URL |
| `claims` | Array of `{path, value, source_ids, status, note?}` objects |
| Claim `path` | Unique JSON Pointer to a candidate text field in the selected native input |
| Claim `value` | Exact current input text at that path; update it after every revision |
| Claim `source_ids` | Non-empty array of unique IDs from `sources` |
| Claim `status` | `candidate_reported` or `confirmed`; unresolved claims must be resolved or omitted before validation |
| Claim `note` | Optional non-empty private explanation, such as how team attribution was retained |

Use `candidate_reported` for notes or claims reported by the candidate, including
claims in an unverified existing resume. Use `confirmed` only after actually reviewing
the cited supporting evidence. Both remain candidate evidence, not independent
background checks. A job description is not a source for candidate qualifications.

Cover `name`, every `headline` and `contact` item, all paragraph text, entry titles,
dates, sub-lines, bullets, skill items and inline-list items. Editorial section
headings, section type tags, skill category labels and `_comment` are excluded.
Do not use those excluded fields to hide unsupported candidate claims.
All JSON objects reject duplicate or unsupported keys.

For example, `/sections/0/items/0/title` addresses the title of the first entry
in the first section. Array indices are zero-based. Array reordering changes paths;
update the ledger rather than reusing stale positions. Multiple claims may cite the
same real source. Multiple sources may support a single bullet.

The complete fictional pair is
[candidate input](../evals/fixtures/fictional_candidate.json) and
[evidence ledger](../evals/fixtures/fictional_evidence.json). These illustrate the
contract, not evidence that can be reused for a real candidate.

## Validate before rendering

```bash
python scripts/build_verified_resume.py --check-input \
  --input /absolute/task/candidate.json --evidence /absolute/task/evidence.json
```

This needs Python and the repository files, not Node, LibreOffice or PDF tools.
Exit 0 with `status: valid_input` confirms native input validity and complete
matching claim coverage. It does not render or release a document. Stale values,
unknown sources, missing claims, unresolved statuses and unsupported fields block.

For generation, use the same input and ledger:

```bash
python scripts/build_verified_resume.py --input /absolute/task/candidate.json \
  --evidence /absolute/task/evidence.json --target-pages 2 \
  --output /absolute/task/cv.pdf --qa-dir /absolute/task/fresh-qa
```

Select the page maximum from the actual request. The build renders an immutable
snapshot of the validated input and records its SHA-256 digest. The QA report
contains coverage counts, not the ledger's source labels or claim notes. Existing
QA text and images still contain candidate information and must remain private.

Manual builds may omit `--evidence` for compatibility; the report then explicitly
says `evidence_validation.status: not_provided`. Assistant-authored file builds
follow SKILL.md and supply the ledger. A passing coverage check never changes
`factual_verification`, `reading_order`, `visual_inspection` or `ats_validation`
from `not_checked` in the automated report.
