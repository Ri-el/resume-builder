# Intake and document types

## Establish the request

Read the supplied request and evidence before asking questions. Identify the task
(create, revise, tailor, translate or audit), target role/application, document
type, career stage, language convention, page limit, requested formats and any
approved reference. Use existing answers; do not require a questionnaire.

Ask only when an unresolved fact or choice materially changes the result. Missing
optional facts may be omitted. With no job description, prepare a general version
from the candidate's stated goal and disclose that it was not tailored to a vacancy.
Do not infer the target country from the candidate's name or nationality.

For bounded edits, preserve everything outside the requested change, including
earlier corrections, official titles, section order and page constraints. A request
to improve content allows selection and rewriting; it never authorises invention.

## Select the document

| Type | Content and ordering | Length |
| --- | --- | --- |
| Targeted resume | Select evidence relevant to the job. For new graduates, education may precede experience; experienced candidates usually lead with relevant experience. Include a summary only when it adds useful context. | Default to one page unless another limit is requested or established. |
| Professional CV | Treat this as an employment application document. Include relevant career detail, projects, professional development and credentials where supported. The word CV alone does not imply an academic record. | Select a disclosed maximum appropriate to the content, commonly one or two pages; obey application requirements and explicit user limits. |
| Academic CV | Select research, education, teaching, publications, presentations, funding and academic service from supplied evidence. Follow the institution's instructions. | Use the supplied limit. If none is given, choose and disclose an appropriate maximum for the supplied material; do not squeeze an academic history into a one-page resume by default. |
| Master career record | Keep the complete private history and source notes for later selection. This is source material, not automatically the application document. | Do not discard history merely because the selected application is shorter. |

These are selection guidelines, not universal hiring rules. Employer, institution
and user requirements override defaults. The reference renderer remains A4 with
the documented fonts. A Letter-size, photo, non-Latin font or institutional template
request requires a separately validated rendering change. Content work may continue;
never label an unsupported export as verified.

## Map CV material without changing the renderer

Use the five existing section types in the native input contract. Add descriptive
headings instead of inventing unsupported JSON fields.

| Material | Existing type | Preserve |
| --- | --- | --- |
| Research, teaching, projects, certifications | `entries` | Exact role/credential, organisation, supplied dates and supported contributions |
| Publications | `bullets` or `entries` | Supplied author order, title, venue, year, identifier and publication status |
| Presentations and funding | `entries` or `bullets` | Speaker/recipient role, event/funder, dates and individual versus team attribution |
| Academic service and memberships | `entries` or `bullets` | Actual role and membership status |

Keep accepted, published, submitted, under-review and in-progress work distinct.
Never invent a DOI, co-author, grant amount, principal-investigator role, licence,
publication acceptance or referee. Do not turn the titles of manuscripts under
review into published papers. Use a consistent citation style from supplied data;
this renderer does not look up or validate citations automatically.

Use `--target-pages N` through the verified entry point for a longer CV. It sets a
maximum and retains the original one-page reference test. Review every page for
split entries, orphan headings and title/date collisions; multipage output is not
an automatic academic-format certification.

## Tailor using evidence

Privately map each material requirement to direct, transferable, partial or absent
evidence. Select the strongest supported examples. Translate relevant experience
into the vacancy's terminology only when meaning and scope remain accurate.
Keep missing qualifications visible in a separate brief note rather than adding
them as keywords. Do not infer management, expertise or outcomes from a title alone.

## Work within actual capabilities

| Capability | Available work | Do not claim |
| --- | --- | --- |
| Text and source access only | Intake, drafting, tailoring, translation and a limited content audit | A generated file, visual review or parser result |
| File/code tools without the reference converter | Native JSON and evidence validation with `--check-input` | A verified PDF |
| Reference dependencies and repository files | `--doctor`, `--self-test` and verified file generation | That dependency detection alone reproduces the reference |
| Page-image access | Inspect all generated pages and report observed issues | That unread pages were inspected |

A repository link does not install tools, override the host AI's instructions or
prove platform compatibility. If retrieval is unavailable, use an attached complete
repository ZIP. Distinguish input checks, automated rendering checks, factual review,
visual review and actual ATS testing in the final delivery note.
