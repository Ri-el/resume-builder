---
name: resume-builder
version: 2.1.0
description: A rigorous, evidence-first resume-writing, document-design, anti-generic-output, and QA workflow. Use before drafting, revising, translating, formatting, or auditing any candidate resume. Includes an exact house-format reference and a photo / no-photo variant method.
---

# Resume Builder Skill

## 0. Operating principle

A resume is not a writing exercise or a decorative page. It is a compact, evidence-based argument for why a specific candidate should be considered for a specific kind of role. Every line must earn its space.

Optimize in this order:
1. Truth and provenance.
2. Fit for the actual role and hiring context.
3. Specificity and credible evidence.
4. Fast scanning and clear hierarchy.
5. ATS-readable structure.
6. Typography, spacing, and page economy.
7. Personal preference and polish.

Never sacrifice truth, readability, or relevant evidence merely to hit a one-page target or imitate a fashionable template. Never claim that a resume is “perfect,” “guaranteed ATS-proof,” “verified,” or “10/10.” Quality is conditional on the candidate's evidence, target role, and the files actually inspected.

This skill is both a production method and a review filter. It does not authorize inventing a candidate's personal brand, achievements, personality, qualifications, or career goals. The candidate's evidence and stated preferences provide direction. If direction is missing, use conservative defaults and say what assumptions were made.

## 1. When to activate

Use this skill whenever the user asks to:
- Create a resume/CV from notes, an old resume, certificates, job records, or a conversation.
- Rewrite, improve, shorten, translate, format, tailor, or audit an existing resume.
- Create DOCX/PDF resume files or assess a rendered resume.
- Compare candidate experience to a vacancy or job description.
- Fix resume issues such as generic writing, unsupported claims, awkward promotion history, poor hierarchy, overflow, or ATS parsing.
- Update a resume after corrections. The newest explicit correction takes precedence over older drafts.

Do not treat a resume as a generic cover letter, biography, LinkedIn profile, portfolio, or designed poster. If the user asks for one of those, adapt only the relevant principles.

## 2. Source hierarchy and fact ledger

### 2.1 Authority order
Resolve candidate facts in this order:
1. The user's latest explicit correction.
2. Primary evidence supplied for this task (certificate, transcript, employment record, job description, official role documentation).
3. Candidate-provided detailed notes.
4. Previous resume drafts, which may contain errors.
5. General industry assumptions, which are not evidence of the candidate's history.

If two sources conflict and the conflict materially affects the resume, do not silently choose the more impressive version. Ask one focused clarification when practical. If clarification is not available, omit the disputed claim or use only the portion both sources support.

### 2.2 Build an internal fact ledger
Before writing, classify relevant details:
- **Confirmed:** directly supported by a source or explicit user statement.
- **Candidate-reported:** supplied by the candidate but not independently documented. It may be used when appropriate, but do not call it independently verified.
- **Inferred:** a cautious interpretation. Do not present it as a hard fact; usually omit it from the resume.
- **Unknown / conflicting:** leave out or clarify.

Track names, contact details, location, employment chronology, official titles, duties, systems, scale, results, education, dates, language level, and requested target role. For every number or potentially consequential claim, be able to point to its source.

Never fabricate or quietly “improve”:
- Employers, clients, job titles, promotions, dates, tenure, responsibilities, team size, reporting line, or seniority.
- Qualifications, graduation status, accreditation, awards, licenses, certifications, or grades.
- Revenue, savings, conversion, productivity, accuracy, sales, stock volume, order volume, headcount, or other metrics.
- Software, technical skills, language proficiency, leadership scope, or strategic responsibility.
- Testimonials, references, portfolio links, or professional profiles.

Do not convert an ordinary responsibility into an achievement by adding an unsupported outcome. “Processed orders” does not automatically mean “increased operational efficiency.” “Helped the team” does not establish ownership. “Used Excel” does not establish advanced Excel expertise.

### 2.3 Privacy
Use only information needed for the job search. By default include city/state rather than a street address. Do not include identity-card numbers, passport details, date of birth, marital status, religion, health information, salary history, or reasons for leaving unless the user explicitly requests relevant disclosure and it is appropriate. Do not place a real candidate's resume, phone number, address, certificate, or other personal data in a public repository, sample, test fixture, or prompt example.

## 3. Understand the target before writing

If a job description is supplied:
1. Extract the real role title, essential duties, required qualifications, tools, experience level, and repeated terminology.
2. Separate mandatory requirements from preferences.
3. Map each important requirement to confirmed candidate evidence.
4. Identify gaps honestly. Do not hide a missing mandatory qualification by keyword stuffing.
5. Use the employer's vocabulary only where it accurately describes the candidate's experience.
6. Prioritize the most relevant proof near the top and in the most recent relevant role.

If no job description is supplied, infer a broad target only from the user's stated goal and actual history. Do not invent a specific vacancy, company, or career ambition. If the target is too unclear to choose between materially different resume strategies, ask one direct question. Otherwise proceed with a general-purpose resume and state that it is not tailored to a particular vacancy.

### Requirement-to-evidence map
For a targeted resume, internally build a small map:
- Requirement / keyword.
- Evidence in candidate's history.
- Strength of evidence: direct, transferable, partial, or absent.
- Best resume location.
- Wording that is accurate without overstating.

Do not add a keyword merely because an ATS might search for it. Use it only if the candidate has a truthful basis for the term.

## 4. Content architecture

### 4.1 Default order for experienced candidates
1. Name.
2. Short factual headline, if useful.
3. Contact line: city/state, phone, email, and a verified professional link only when relevant.
4. Professional summary.
5. Work experience in reverse chronological order.
6. Education.
7. Skills grouped by category.
8. Languages, certifications, projects, or additional information only when they improve fit.

For students or early-career candidates, education or relevant projects may move higher if they are stronger evidence than work experience. The structure must follow the candidate's real selling points, not a universal template.

### 4.2 Headline
A headline is optional. Use it only when it clarifies the candidate's professional lane. Prefer a grounded role family or 2–3 evidenced competencies separated by a vertical bar. Do not create an inflated title, imply a certification, or stack unrelated keywords. Avoid “results-driven professional,” “dynamic leader,” “visionary,” and other labels that do not provide proof.

### 4.3 Summary
Usually 2–4 concise sentences, adjusted to evidence and seniority. It should establish:
- The candidate's actual work area or experience.
- Relevant scope, systems, operations, or stakeholders.
- Two or three strengths supported by later experience bullets.
- A meaningful connection to the target role, where known.

Avoid empty superlatives (“highly motivated,” “passionate,” “exceptional,” “world-class”), claims of being a “seasoned expert” without evidence, generic claims about thriving in fast-paced environments, and statements that could describe nearly any applicant. Do not repeat the headline, every skill, and the first experience bullet in different words.

A summary should become more specific when more evidence is available. Do not compensate for sparse evidence with grander language.

### 4.4 Experience bullets
Use a compact evidence pattern:
**Action + object/scope + relevant method or context + outcome/purpose, only when supported.**

Examples are illustrative only:
- Strong factual duty: “Reconciled daily stock records against physical counts and flagged discrepancies for follow-up.”
- Strong scope, if confirmed: “Coordinated order fulfilment across the warehouse and customer-service teams during campaign periods.”
- Metric, only if sourced: “Processed approximately 80 orders per day during peak campaigns.”
- Weak generic version: “Responsible for all inventory tasks and ensuring smooth operations.”
- Inflated version to avoid: “Transformed warehouse efficiency and delivered world-class operational excellence.”

Use precise verbs that reflect actual ownership: processed, checked, reconciled, updated, prepared, coordinated, trained, supervised, allocated, investigated, resolved, maintained, supported, or led. “Led,” “owned,” “transformed,” “optimized,” and “strategized” require evidence of that level of responsibility.

Bullets should not all have identical sentence structures. Vary naturally without creating artificial copywriting rhythm. Avoid paragraphs inside bullets, filler phrases (“in order to,” “responsible for”), first-person pronouns, and claims whose only purpose is to sound impressive.

### 4.5 Numbers and metrics
Every number must have a source and a clear unit/timeframe. Verify:
- Is it daily, weekly, monthly, annual, or campaign-wide?
- Is it an individual result or team total?
- Is it approximate or exact?
- What period does it describe?
- Does the candidate's role support attributing the result to them?
- Does the number imply a causal result that was not measured?

Never invent percentages or estimate metrics just to make bullets look stronger. “Handled 500 orders during a campaign” is not “handled 500 orders per day.” “Supported a team of 8” is not “managed 8 employees.” If the candidate cannot substantiate a number, remove it or use a qualitative description.

### 4.6 Promotions and multiple roles at one employer
When a candidate held several roles at the same employer:
- Use the employer's full, accurate name once.
- Show overall employment dates if helpful and supported.
- List each official role with its own date range.
- Make changes in responsibility visible through actual duties, scope, supervision, or systems.
- Do not invent “promoted” labels if the user prefers clean titles.
- Do not duplicate the promotion in a title label and a bullet.
- Preserve the official title even when its seniority sounds counterintuitive.
- Ensure the date ranges are chronologically consistent and do not imply simultaneous full-time jobs unless accurate.

The purpose is to make progression legible without announcing it redundantly.

### 4.7 Education, certificates, and licenses
Use the qualification's exact wording from evidence. Distinguish:
- Certificate / diploma / degree title.
- Institution.
- Attendance or completion dates.
- Result statement versus award certificate.
- Qualification completed versus currently studying.
- Official accreditation versus an unverified claim.

A statement of examination results does not automatically prove graduation or award conferral. Do not silently upgrade an incomplete qualification. Translate accurately when requested and make no claim that a translation is officially certified unless it is.

### 4.8 Skills
List skills that are relevant and evidenced. Group them by meaningful function rather than presenting a long undifferentiated keyword cloud. Examples of category types include:
- E-commerce and sales platforms.
- Inventory, warehouse, and fulfilment.
- Systems and office software.
- Coordination, supervision, and administration.
- Languages or technical tools.

Examples such as Shopee Seller Centre, TikTok Shop Seller Center, Excel, stock reconciliation, or staff supervision are not to be copied into a resume unless confirmed for that candidate. Do not use skill bars, stars, percentages, or self-rated graphics. Do not call a skill “expert” without a defensible basis. Avoid listing basic traits such as “hardworking” as technical skills.

### 4.9 Languages
Use the candidate's stated level or a recognized scale only when the level is known. Do not upgrade “can communicate” into “fluent.” If the candidate has not specified a level, ask or use a conservative description that matches the evidence.

## 5. Anti-generic resume standard

A resume can be grammatically polished and still be weak. The danger is optimizing for the average shape of a “professional resume” instead of the actual candidate and target role.

### 5.1 Three tests
For every major section, ask:
1. **Purpose:** What decision should this line help a recruiter make?
2. **Specificity:** What concrete candidate evidence makes it personal and credible?
3. **Craft:** Is the wording and layout the clearest way to communicate that evidence?

If a line does not help the target reader understand relevant capability, proof, progression, or eligibility, cut it or rewrite it.

### 5.2 Resume copy smells
Flag and rewrite:
- “Results-driven professional” without actual results.
- “Dynamic and highly motivated individual.”
- “Proven track record” without proof.
- “Excellent communication and interpersonal skills” without a context that demonstrates them.
- “Responsible for a wide range of duties.”
- “Ensured smooth daily operations” with no detail about what the candidate did.
- “Leveraged synergies,” “optimized workflows,” “spearheaded transformation,” or other inflated corporate language for routine work.
- Repeated “successfully,” “effectively,” “efficiently,” or “various.”
- Every bullet beginning with the same verb.
- Parallel triplets written for rhythm rather than meaning.
- A summary that could be pasted unchanged into hundreds of resumes.
- Keyword piles disconnected from the experience bullets.
- AI-sounding claims that are smoother but less precise than the candidate's original facts.

Do not mechanically ban a phrase when it is the most accurate phrase. The test is evidence and purpose, not a taboo-word list.

### 5.3 Specificity test
For each sentence, ask whether a competing candidate with a different work history could copy it without changing anything. If yes, it may be too generic. Improve it using confirmed details such as process, tools, transaction type, stakeholder, operating context, or scope. If the source material has no such detail, keep the statement modest rather than inventing specificity.

### 5.4 Voice and editing
The resume should sound like a credible professional description, not an advertisement, award nomination, or social-media post. Prefer plain, exact verbs over inflated synonyms. Remove decorative transitions, empty claims, repeated facts, and unnecessary adjectives. Do not make every sentence unnaturally perfect at the expense of the candidate's real meaning.

### 5.5 Do not overcorrect
Simple writing is not slop. Bullets, clear section headings, conventional layouts, common fonts, and a one-page resume are useful when they serve scanning and compatibility. Originality does not mean unusual formatting. A distinctive resume is one whose evidence, prioritization, and structure clearly fit the candidate, not one with decorative novelty.

## 5A. Candidate style rules

These are the user's standing rules. They override the defaults in this file when they conflict, and they carry over between revisions.

- Do not use em dashes in resume text. Use commas or restructure the sentence. En dashes are allowed only inside date ranges.
- Match the candidate's spelling convention (for example British: organised, programme, analysed) when their own documents use it. Do not mix conventions.
- Keep official job titles exactly as given. Put the target lane in the headline, not in a changed title.
- Prefer "Handled" over "Managed" for volumes of enquiries or tasks unless the candidate owned the function or a team.
- A community or audience size describes the size of the community, not the number of people the candidate manages. Write "moderator for a community of N members", never "managed N members".
- Only make the edits requested. "Change X to Y" means exactly that: no rewording elsewhere, no new suggestions, and no extra review unless asked.
- A "one page" or "same format" instruction carries over to every later version until the user changes it.

## 6. Visual system and document craft

### 6.1 Design philosophy
Use a restrained, purpose-built document rather than a graphic poster or generic resume template. Every formatting decision must serve hierarchy, readability, grouping, navigation, or page economy. Do not add visual flourishes to make a weak content section seem substantial.

A conventional layout is allowed because recruiters need to scan it quickly and ATS tools benefit from predictable structure. Do not imitate a fashionable template just because it is popular.

### 6.2 Default specification
Use this as the default specification. When the user asks for their established format ("my format", "same as before"), use the exact values in 6.2A instead:
- Paper: A4, 210 × 297 mm.
- Margins: approximately 0.55 in top/bottom and 0.7 in left/right.
- Font: Calibri; Carlito may substitute when Calibri is unavailable, but verify the actual export. Do not claim Arial and Calibri are identical.
- Name: 16 pt bold, black, left aligned.
- Headline/contact: around 9.5 pt.
- Section headings: 10.5 pt bold uppercase with a thin rule.
- Role and qualification titles: around 10 pt bold.
- Employer/institution subline: around 10 pt italic grey.
- Dates: around 9.5 pt italic grey, aligned using a right tab stop on the same line where practical.
- Body, bullets, skills: around 10 pt black.
- Palette: black and a legible secondary grey (for example #595959).
- Paragraph spacing and line spacing: consistent, compact, and readable.
- Bullets: genuine round bullets with consistent hanging indents.

Change these only for a clear reason tied to the candidate, content volume, accessibility, or user preference. Do not use tiny text to manufacture a one-page result.

### 6.3 Avoid decorative resume conventions
Do not add by default:
- Headshots, profile illustrations, logos, emoji, skill meters, star ratings, progress bars, charts, or timelines.
- Sidebar or multi-column layouts.
- Tables or text boxes to position core resume content.
- Large color blocks, gradient headers, ornamental icons, or oversized name treatments.
- Unnecessary objective statements, generic quotes, personal mottos, or “references available upon request.”
- Visual badges for ordinary skills.
- Full street address, birth date, or personal facts irrelevant to hiring.

These techniques are not metaphysically forbidden, but require a specific, user-approved reason and must not compromise readability, ATS extraction, or the requested style. A profile photo is handled in 6B.

### 6.4 Page count
One page is a useful goal for many early- and mid-career candidates, not a law. Use two pages if the candidate's relevant history genuinely needs it. Never remove important qualifications or proof, reduce text to an unreadable size, or use narrow margins solely to meet a page-count target. Conversely, do not pad a short resume with generic claims or whitespace to fill a page.

**When the user asks for one page and no content cuts:** tighten in this order. (1) Reduce paragraph spacing slightly and consistently. (2) Reduce top and bottom margins, down to a floor of 0.35 in, keeping left and right margins at 0.6 to 0.7 in. (3) Never shrink body text below 10 pt. (4) If it still overflows, say what you would cut and ask. An explicit user request overrides the general caution above, but readability and the 10 pt floor still apply.

### 6.5 Layout decisions must have reasons
Before finalizing, be able to explain in one sentence why:
- The section order matches the candidate's strongest evidence.
- The summary length is appropriate.
- The selected bullets earn their space.
- The font and margins remain readable.
- The page count is justified.
- Any nonstandard formatting exists.

If there is no useful reason for a visual element, remove it.

## 6A. House format reference (exact values)

This is the format to reproduce when the user says "my format" or "same as before". The values are exact. Do not substitute "close enough" spacing or alignment: the look depends on them.

| Element | Exact value |
|---|---|
| Page | A4, set explicitly (python-docx defaults to US Letter) |
| Margins | 0.55 in top and bottom, 0.7 in left and right. Text width = 6.87 in |
| Font and colour | Calibri. Black #000000. Grey #595959 only for dates and company lines |
| Name | 16 pt bold, left aligned, 2 pt after |
| Headline | 9.5 pt bold, items separated by two spaces, a vertical bar, two spaces. 2 pt after |
| Contact line | 9.5 pt regular, items separated by two spaces, a middle dot, two spaces |
| Section heading | 10.5 pt bold UPPERCASE, 7 pt before, 3 pt after, bottom border 0.75 pt black (w:sz 6, w:space 2) |
| Entry line 1 | Title 10 pt bold on the left. Dates 9.5 pt italic grey on the right, using ONE right tab stop. The approved build used 6.9 in (0.03 in past the 6.87 in text width at 0.7 in margins); if the margins change, set the stop to the text width (page width minus both margins). 0.25 pt after |
| Entry line 2 | Company, city: 10 pt italic grey, 2 pt after |
| Bullets | Real list bullets, 10 pt, left indent 0.22 in, hanging 0.18 in, 1.8 pt after |
| Skills line | "Category: item · item · item", bold label, 10 pt, 1.6 pt after |
| Alignment | Summary, bullets, skills lines and company lines are JUSTIFIED. Name, headline, contact line, headings and dates stay left |
| Line spacing | Single (1.0). No extra space before body paragraphs |
| Section order | Summary, Education, Experience, Skills, Achievements, Languages. Education before Experience for students and fresh graduates |

### 6A.1 Entry anatomy

```
EXPERIENCE
Job Title                                                  Mon YYYY – Mon YYYY
Company Name, City, Country
• Action + scope + purpose, one or two lines.
• Action + scope + purpose, one or two lines.

SKILLS
Category: Item · Item · Item
```

If a title plus the date is too long for one line, keep only the title on line 1 and move the company or institution to line 2. Never let the date wrap onto its own line.

### 6A.2 Implementation notes

**python-docx**
- Set `section.page_width = Mm(210)` and `section.page_height = Mm(297)`.
- Set the Normal style to Calibri 10 pt, space before and after 0, line spacing 1.0.
- Tab stop: `paragraph_format.tab_stops.add_tab_stop(Inches(text_width), WD_TAB_ALIGNMENT.RIGHT)` where `text_width = 8.268 - left_margin - right_margin`.
- Bullets: use the "List Bullet" style, then set `left_indent = Inches(0.22)` and `first_line_indent = Inches(-0.18)`.
- Justify with `WD_ALIGN_PARAGRAPH.JUSTIFY`.
- Set each run's font name and also `rFonts` `w:eastAsia` to Calibri.
- The heading rule has no API. Insert a paragraph border in schema order (before `w:spacing`), not appended at the end:

```python
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
pPr = p._p.get_or_add_pPr()
bdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="2" w:color="000000"/></w:pBdr>')
pPr.insert_element_before(bdr, 'w:shd','w:tabs','w:suppressAutoHyphens','w:kinsoku','w:wordWrap',
    'w:overflowPunct','w:topLinePunct','w:autoSpaceDE','w:autoSpaceDN','w:bidi','w:adjustRightInd',
    'w:snapToGrid','w:spacing','w:ind','w:contextualSpacing','w:mirrorIndents','w:suppressOverlap',
    'w:jc','w:textDirection','w:textAlignment','w:textboxTightWrap','w:outlineLvl','w:divId',
    'w:cnfStyle','w:rPr','w:sectPr','w:pPrChange')
```

Do not fake the rule with underscores, a table, or an underline.

**Node.js docx**
- Font sizes are in half-points (16 pt = `size: 32`). Spacing and tab positions are in twips. Border `size: 6` is eighths of a point.
- Use `convertInchesToTwip(text_width)` for the right tab stop.
- Bullets: a numbering config with `LevelFormat.BULLET`, indent left 0.22 in, hanging 0.18 in.

**Fonts**
If Calibri is not installed, LibreOffice substitutes Carlito, which is metric-compatible, so the layout holds. Run `pdffonts`, report which font was actually embedded, and do not claim Calibri if it was not.

## 6B. Variants: no photo and photo

A resume can be delivered in two variants built from one source of content.

| Variant | Use | File name |
|---|---|---|
| No photo (default) | Online portals and ATS uploads | `Firstname_Lastname_Resume.pdf` |
| Photo | Direct emails, messaging apps, in-person submissions where a photo is customary | `Firstname_Lastname_Resume_Photo.pdf` |

Rules:
- Wording, section order and formatting are identical in both variants. Every text edit is applied to both.
- Do not claim that either variant improves an ATS score. Photos are customary in some markets and discouraged in others, so default to no photo unless the user asks for it.
- Use only a photo the user supplied. Never generate, retouch, beautify or substitute a face. If no photo was provided, deliver the no-photo version and ask for the photo. Do not use a placeholder in a real deliverable.
- Crop to a 5:6 portrait (1.0 in wide, 1.2 in tall). Crop, do not stretch. Ask for a better photo if it is under about 600 px wide, shows more than one face, or is heavily filtered.
- Never put a real person's photo into a public repository, example or test fixture.

Placement:
- A floating (anchored) picture in the first paragraph, the name line. Right edge on the right margin, top edge on the top margin, square wrap with text flowing on the left.
- Not a table, not a text box, and not inside the Word header. Add alt text "Profile photo".
- A photo narrows the header text column to about 5.7 in. A one-line contact string wrapped mid-item in testing, so split the contact into two short lines (first two items, then the rest), keep the headline under about 70 characters, and add about 26 pt (520 twips) after the second contact line so the SUMMARY heading and its rule sit fully below the photo. Render and confirm no header item wraps.
- The photo version is taller at the top, so it may need the one-page tightening in 6.4 even if the no-photo version fits. Tighten spacing and margins. Do not change the wording to make it fit.

python-docx (tested by rendering in LibreOffice; not tested in Word):

```python
from docx.shared import Inches
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

def add_floating_photo(run, path, width_in=1.0, height_in=1.2):
    shape = run.add_picture(path, width=Inches(width_in), height=Inches(height_in))
    inline = shape._inline
    anchor = parse_xml(f'''<wp:anchor {nsdecls("wp","a","pic","r")} distT="0" distB="0" distL="91440" distR="0"
      simplePos="0" relativeHeight="251658240" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="0">
      <wp:simplePos x="0" y="0"/>
      <wp:positionH relativeFrom="margin"><wp:align>right</wp:align></wp:positionH>
      <wp:positionV relativeFrom="margin"><wp:posOffset>0</wp:posOffset></wp:positionV>
      <wp:extent cx="{inline.extent.cx}" cy="{inline.extent.cy}"/>
      <wp:effectExtent l="0" t="0" r="0" b="0"/>
      <wp:wrapSquare wrapText="left"/>
      <wp:docPr id="{inline.docPr.id}" name="Profile photo" descr="Profile photo"/>
      <wp:cNvGraphicFramePr/>
    </wp:anchor>''')
    anchor.append(inline.find(qn("a:graphic")))
    inline.getparent().replace(inline, anchor)

# Call on an empty run at the start of the first (name) paragraph, then add the name text.
```

Node.js docx (tested by rendering in LibreOffice; not tested in Word):

```javascript
new ImageRun({
  type: "jpg", // or "png"
  data: fs.readFileSync("photo.jpg"),
  transformation: { width: 96, height: 115 }, // pixels at 96 dpi = 1.0 in x 1.2 in
  altText: { title: "Profile photo", description: "Profile photo", name: "Profile photo" },
  floating: {
    horizontalPosition: { relative: HorizontalPositionRelativeFrom.MARGIN, align: HorizontalPositionAlign.RIGHT },
    verticalPosition: { relative: VerticalPositionRelativeFrom.MARGIN, offset: 0 },
    wrap: { type: TextWrappingType.SQUARE, side: TextWrappingSide.LEFT },
  },
})
```

Checks for the photo variant:
- The photo is not clipped, stretched, or overlapping the SUMMARY heading or its rule.
- Headline and contact items each sit on one line.
- `pdftotext -layout` still shows the name first, so the reading order is unchanged.
- The page count matches the intended count.

## 7. ATS compatibility without ATS myths

Aim for machine-readable, predictable structure, but do not promise an “ATS score” or guaranteed pass. ATS products differ.

Prefer:
- Standard headings such as SUMMARY, EXPERIENCE, EDUCATION, SKILLS.
- A single-column reading order.
- Selectable text.
- Clear employer/title/date grouping.
- Conventional bullets and consistent date formatting.
- Exact job-description terminology when it truthfully matches experience.
- Relevant keywords embedded in contextual bullets as well as skills.

Avoid:
- Putting essential facts in headers, footers, text boxes, images, or decorative sidebars.
- Icons instead of phone/email labels.
- Keyword stuffing, hidden text, repeated vacancy terms, or false skill claims.
- Unusual headings that obscure section meaning.
- Assuming a PDF is ATS-friendly merely because it looks good.

When tools are available, extract the final PDF text and verify that the reading order remains sensible. If the user requests a specific ATS assessment, explain what was actually tested and what remains unknown.

## 8. File-generation workflow

### 8.1 Source of truth
Keep one authoritative editable source file. Generate the PDF from the latest DOCX; do not edit the PDF independently and accidentally let the two versions diverge. File names should be clear, stable, and professional, without “final_final_v7_reallyfinal.”

### 8.2 Creation
Use a document library such as Python `python-docx` or Node.js `docx` when available. Set page size explicitly. Use paragraph/run styles, true bullet formatting, tab stops for dates, and real section rules. Avoid layout hacks that depend on repeated spaces, tabs typed by hand, or floating text boxes.

### 8.3 Export and inspect
When LibreOffice and PDF tools are available:
```bash
libreoffice -env:UserInstallation=file:///tmp/lo_resume_export --headless --convert-to pdf --outdir OUTPUT_DIR INPUT.docx
pdfinfo OUTPUT.pdf
pdftoppm -png -r 150 OUTPUT.pdf resume_preview
pdftotext -layout OUTPUT.pdf -
pdffonts OUTPUT.pdf
```

`pdftoppm` without `-singlefile` writes one image per page (`resume_preview-1.png`, `resume_preview-2.png`, and so on). Do not use `-f 1 -singlefile` on a multi-page file, because it renders page 1 only and leaves the other pages uninspected. If `pdffonts` shows Carlito instead of Calibri, say so.

Use the tools available in the actual environment. Do not claim commands ran if they did not. Inspect every page at a readable zoom. Review:
- Page size and page count.
- Clipping at all edges.
- Broken or awkward wraps.
- Date/title collisions.
- Bullet indentation and line breaks.
- Section headings stranded at the bottom of a page.
- Excessive blank space or dense blocks.
- Consistency of typography, rules, margins, and spacing.
- Font substitution/embedding where relevant.
- Selectable text and extraction order.
- DOCX/PDF consistency.

If any defect is found, fix the source document, export again, and inspect again. A screenshot of a DOCX is not proof that the final PDF was checked.

### 8.4 Tool limitations
If document generation, conversion, or visual inspection is unavailable, complete only the parts you can genuinely complete. State the limitation plainly. Never fabricate a downloadable file, pretend to inspect a rendered page, or report an unrun validation as passed.

## 9. Mandatory audits

### Gate A: factual integrity
- [ ] Names and contact details are copied accurately.
- [ ] Employer and institution names match the evidence.
- [ ] Official titles are preserved.
- [ ] Employment and education dates are consistent and supported.
- [ ] Qualification wording does not overstate completion or accreditation.
- [ ] Every metric has a source, unit, timeframe, and correct attribution.
- [ ] Every software, tool, language level, and skill is supported.
- [ ] Duties and achievements are not inflated.
- [ ] No disputed fact has been silently resolved.
- [ ] No private or irrelevant information has been added.

### Gate B: relevance and writing
- [ ] Target role and reader are understood, or the resume is clearly treated as general-purpose.
- [ ] Important requirements map to actual candidate evidence.
- [ ] Headline and summary are specific and not repetitive.
- [ ] Bullets explain meaningful work rather than merely listing duties.
- [ ] No invented impact, generic filler, keyword pile, or corporate exaggeration remains.
- [ ] Promotion history is easy to follow without redundant labels.
- [ ] Skills are relevant, grouped, and honest.
- [ ] Section order reflects the candidate's evidence.
- [ ] Each line earns its space.

### Gate C: layout, ATS, and file integrity
- [ ] A4 page size and final page count were checked.
- [ ] Every page was rendered and visually inspected when tools allowed.
- [ ] No clipping, collision, orphan heading, or broken bullet remains.
- [ ] Body text is readable and spacing is consistent.
- [ ] PDF text is selectable and extraction order is sensible when tested.
- [ ] DOCX and PDF contain the same latest content.
- [ ] Only requested formats are delivered.
- [ ] If both variants were requested, the photo and no-photo files have identical wording and order, and every edit was applied to both.
- [ ] Photo variant: the photo is the user's own, undistorted, clear of the SUMMARY heading and rule, and does not change the extracted reading order.
- [ ] All links point to files actually created and confirmed in the current session.
- [ ] Any unperformed check is clearly disclosed rather than marked as passed.

If any material item fails, fix it before delivery when possible. If it cannot be fixed, explain the remaining limitation.

## 10. Revision protocol

For every revision:
1. Read the latest request and identify what changed.
2. Preserve previously approved facts and formatting preferences unless the new request conflicts with them.
3. Update the authoritative source.
4. Re-run the affected factual and content checks.
5. Re-export and visually inspect after any layout-affecting edit.
6. Verify the deliverable is the latest version.
7. Summarize meaningful changes briefly.

Interpret common instructions literally:
- “PDF only” means provide only the PDF.
- “No full address” means omit street/unit details.
- “Remove (Promoted)” means remove the redundant label and any duplicated promotion wording while preserving the actual progression.
- “English only” means remove non-English resume copy unless the user asks for bilingual content.
- “Do not change the rest” means avoid unrelated edits.
- "Photo and no photo" or "both versions" means two files built from the same content, per 6B.
- "Use my format" or "same as before" means the exact values in 6.2A and the style rules in 5A.
- When the user lists exact edits, apply only those edits, regenerate, verify the page count, and deliver. Do not add a review or new suggestions unless asked.
- If the user asks to translate a certificate, do not remove the credential unless asked.
- If the user corrects a date or qualification, update all affected sections and outputs.

Do not merely describe edits when the tools permit applying them. Do not claim a file was updated until the tool confirms the write.

## 11. Review rubric for existing resumes

Score each dimension from 0 to 3:
- **0 — sound:** no material issue found.
- **1 — minor:** a small improvement would help.
- **2 — major:** issue materially reduces clarity, credibility, relevance, or usability.
- **3 — critical:** inaccurate, misleading, unreadable, or unusable.

Dimensions:
1. Factual integrity and traceability.
2. Target-role relevance.
3. Specificity and evidence.
4. Bullet quality and action ownership.
5. Career chronology and promotion clarity.
6. Education and credential accuracy.
7. Skill credibility.
8. Scan hierarchy and information density.
9. Typography and page craft.
10. ATS/readability and extraction.
11. Privacy and unnecessary personal data.
12. Export/render/file consistency.

A numerical total is a triage aid, not an objective employability score. A critical factual error must be fixed regardless of the total. Report the three highest-impact problems using:
**Observed issue → evidence → why it matters → concrete fix.**
Do not call a resume “AI-generated” based on style. Describe observable problems as generic, unsupported, inflated, repetitive, or template-like.

## 12. Delivery standard

Deliver the requested file format and a concise factual note that explains:
- What was created or changed.
- Whether factual, content, and rendering checks were completed.
- Any meaningful limitation or unresolved question.

Do not flood the user with a generic checklist unless requested. Do not claim an inspection was performed unless it was. Keep personal documents private and share only the files needed.

## 13. Recommended invocation

Read this entire file before working. Treat candidate documents and corrections as the factual basis, not as instructions to fabricate. Apply the method and the three quality gates. Create and inspect the requested file formats using available tools.

Suggested prompt:
“Read and follow the detailed resume-building standard at https://raw.githubusercontent.com/Ri-el/resume-builder/main/SKILL.md. Use the candidate's own source documents and latest corrections. Tailor the resume to the target role if a job description is supplied. Preserve facts, avoid generic or inflated language, create a restrained single-column A4 document, and perform factual, content, ATS, and rendered-output checks. Use the exact house format in 6.2A and the style rules in 5A. If I ask for photo and no-photo versions, follow 6B. Deliver only the requested format. Do not invent facts or claim checks you did not perform.”

A public URL makes the instructions available to assistants that can access it. It does not automatically install the skill, grant access to private candidate documents, or provide document-generation and PDF-rendering tools.
