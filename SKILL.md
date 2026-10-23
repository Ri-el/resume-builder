# Resume Builder Skill

## Mission
Create accurate, ATS-readable, professional resumes using a restrained single-column A4 layout. Priorities: factual accuracy, relevance to the target role, clear writing, visual consistency, and readability. Never claim the resume is verified or final until the checks below are complete.

## 1. Establish the facts
Review all supplied resumes, certificates, job descriptions, notes, and corrections before drafting. The latest explicit correction overrides earlier information. Keep a fact ledger for:
- Candidate name and contact details.
- Employer names, official titles, dates, duties, tools, team size, and supported metrics.
- Exact qualification title, institution, dates, and what the evidence actually proves.
- Evidence-backed skills and target role.

Never invent dates, qualifications, accreditation, metrics, achievements, proficiency, software, or responsibilities. Do not turn team results into individual achievements. Clarify important gaps or omit/qualify unsupported claims. Do not reuse one candidate's private information in another candidate's resume or public examples.

## 2. Content and structure
Default order for an experienced candidate:
1. Name
2. Factual headline with 2–3 competencies separated by `|`
3. City/state · phone · email · optional verified professional link
4. SUMMARY
5. EXPERIENCE (reverse chronological)
6. EDUCATION
7. SKILLS
8. LANGUAGES or additional information only when useful

Write a concise, specific summary. Use 3–5 bullets for substantial recent roles and 2–3 for earlier roles, adjusted to relevance. Bullets should state the action, relevant scope/tools/stakeholders, and purpose or supported outcome. Avoid filler, first-person pronouns, keyword stuffing, and unverified claims.

Quantify carefully: distinguish daily volume from campaign totals and individual results from team results. Mention platforms only when confirmed. Use natural action verbs such as Managed, Reconciled, Coordinated, Supervised, Processed, Maintained, and Verified when accurate.

## 3. Promotions and role progression
Group roles under the same employer with the full company name and overall employment dates, then show each official title and its own date range. Do not add redundant labels such as “(Promoted)” or duplicate the promotion in a bullet. Show expanded scope through genuine responsibilities. Preserve official titles. Do not include private reasons for leaving.

## 4. Education and skills
Use qualification wording supported by the official record. Do not imply a result statement proves graduation if it does not. Translate clearly when requested, but do not claim a translation is the official title unless verified. Do not claim accreditation without evidence.

Group skills into short, searchable, evidence-backed categories. Example categories include e-commerce platforms, inventory and fulfilment, systems, and coordination. Examples are not defaults to copy blindly. Basic Excel use does not imply advanced formulas, PivotTables, macros, analytics, SAP, ERP, or WMS expertise.

## 5. Visual design
Use a genuine flowing document, not a graphic resume:
- A4 page, approximately 0.55-inch top/bottom and 0.7-inch side margins.
- Calibri; Carlito is an acceptable metric-compatible substitute when needed. Inspect the actual export.
- Name: 16 pt bold, black, left aligned.
- Headline/contact: about 9.5 pt.
- Section headings: 10.5 pt bold uppercase with a thin rule.
- Job and education titles: about 10 pt bold.
- Dates: about 9.5 pt italic grey, right aligned on the same line using a right tab stop.
- Employer/institution subline: about 10 pt italic grey.
- Body, bullets, and skills: about 10 pt black.
- Restrained black and grey palette, consistent spacing and hanging indents.

Avoid sidebars, photos, icons, infographics, colour blocks, text boxes, multi-column layouts, content tables, logos, timelines, and skill bars. Aim for one page if it remains readable. Never remove important evidence or shrink text excessively just to force one page.

## 6. Document creation and PDF verification
Generate DOCX with a document library such as Python `python-docx` or Node.js `docx`. Set A4 explicitly and apply consistent paragraph styles, real bullets, section rules, and right tab stops. Deliver only the formats requested.

When tools are available, export and inspect:
```bash
libreoffice -env:UserInstallation=file:///tmp/lo_resume_export --headless --convert-to pdf --outdir OUTPUT_DIR INPUT.docx
pdfinfo OUTPUT.pdf
pdftoppm -f 1 -singlefile -png -r 150 OUTPUT.pdf resume_preview
pdftotext -layout OUTPUT.pdf -
pdffonts OUTPUT.pdf
```

Actually inspect the rendered page. Check clipping, wrapping, page count, dates colliding with titles, bullet alignment, rules, whitespace, selectable text, extraction order, and font embedding. Re-export after edits. If export or rendering is unavailable, say so honestly; do not claim visual verification or invent a file link.

If overflowing, remove redundant wording first, then shorten the summary/skills, then modestly adjust spacing or margins. Prefer a readable second page to unreadable text.

## 7. Mandatory quality gates
### Factual audit
- Employer and institution names, titles, and dates match sources and latest corrections.
- Qualifications and dates match confirmed evidence; removed credentials do not reappear.
- Every tool, technology, team size, volume, and metric is supported.
- Contact details are correct; city/state only by default, not a full street address.
- No unrelated personal information.

### Content audit
- Headline and summary match actual experience and target role.
- Promotions show progression without redundant labels.
- Bullets are specific and non-duplicative; team results are not misattributed.
- Skills are honest and relevant; no invented software or inflated proficiency.
- Dates are internally consistent.

### Rendering and ATS audit
- Page size and page count verified.
- Rendered PDF visually inspected for clipping, accidental extra pages, orphaned headings, and excessive whitespace.
- Text is selectable and extraction order is sensible.
- DOCX and PDF reflect the same latest revision.

Do not call a resume “final,” “verified,” or “10/10” until all three gates pass. Evaluate it for its intended vacancy rather than claiming universal perfection.

## 8. Revision rules
Apply requested edits in the same turn when tools permit, then re-export and repeat relevant checks. The latest request is authoritative.
- “PDF only” means provide only PDF.
- “No full address” means omit street/unit details.
- If “(Promoted)” is removed, remove redundant promotion labels while preserving visible progression.
- If a certificate is to be translated, do not remove the credential unless explicitly asked.
- Give a concise change log and link only to files actually created and verified.

## 9. Suggested invocation
Read and follow this file before starting. Use only the candidate's own source documents and latest corrections. Generate the resume with available document tools and perform all three quality gates. Do not invent facts.

Suggested prompt:
“Read and follow https://raw.githubusercontent.com/Ri-el/resume-builder/main/SKILL.md. Use the attached candidate information and latest corrections. Create a restrained single-column A4 resume, perform factual, content, and rendering QA, and deliver only the format I request. Do not invent facts.”

A public GitHub URL makes the instructions available to assistants that can access it; it does not automatically install the skill or provide document-generation/PDF-rendering tools.
