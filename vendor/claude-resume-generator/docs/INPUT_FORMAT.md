# Input format and where each piece of information goes

The generator reads one JSON file. ChatGPT (or you) extracts the facts and puts them into these fields. The generator never rewrites wording.
A blank template is in `input/template_empty.json`; a complete fictional example is in `input/sample_resume.json` (rendered: `output/Sample_Resume_page-1.png`).

## Top-level fields
| JSON field | Type | Where it appears |
|---|---|---|
| `name` | string | Line 1, 16 pt bold. Written exactly as given |
| `headline` | list of strings | Line 2, bold. Items joined automatically with `  \|  `. **Do not type the bars** |
| `contact` | list of strings | Line 3. Items joined automatically with `  ·  `. **Do not type the dots**. With a photo it is split into two lines |
| `sections` | list of section objects | Everything below the header, **in the order listed** |

## Section objects (`heading` is printed UPPERCASE with a rule under it)
| `type` | Fields | Renders as |
|---|---|---|
| `paragraph` | `text` | One justified paragraph (the summary) |
| `entries` | `items`: list of `{title, dates?, sub?, bullets?}` | `title` bold on the left, `dates` italic grey on the right of the same line, `sub` italic grey line under it, then bullets |
| `skills` | `items`: list of `{label, items:[...]}` | `Label: item · item · item` (dots added automatically) |
| `bullets` | `items`: list of strings | A plain bullet list (achievements) |
| `inline_list` | `items`: list of strings | One line, items joined with `  ·  ` (languages) |

`dates`, `sub` and `bullets` are optional. If `dates` is missing no date is printed. Education uses `entries` with `sub` for a line such as `CGPA 3.60`.

## Worked example: where each piece of the fictional sample lands
| JSON path in `sample_resume.json` | Text in the rendered page |
|---|---|
| `name` | **Aisyah Rahman** (top line) |
| `headline[0..2]` | **Operations Analysis \| Client Coordination \| Reporting & Documentation** |
| `contact[0..3]` | Petaling Jaya, Selangor · +60 12-345 6789 · aisyah.rahman@example.com · linkedin.com/in/aisyah-example |
| `sections[0]` (`paragraph`, heading "Summary") | the justified paragraph under SUMMARY |
| `sections[1].items[0].title / dates / sub` | **Bachelor of Business Administration (Hons), Sample University** ... Mar 2023 – Jul 2026, then italic grey `CGPA 3.60` |
| `sections[2].items[0].title / dates / sub` | **Operations Associate** ... Aug 2026 – Present, then italic grey `Harbour Lane Leasing Sdn. Bhd., Kuala Lumpur, Malaysia` |
| `sections[2].items[0].bullets[n]` | the n-th bullet under that job |
| `sections[3].items[0]` = `{label:"Analysis & Reporting", items:[...]}` | **Analysis & Reporting:** Data Cleaning · Weekly Reporting · ... |
| `sections[4]` (`bullets`) | the two achievement bullets |
| `sections[5]` (`inline_list`) | Bahasa Melayu (Native) · English (Fluent) |

## Rules for whoever fills the fields (ChatGPT's job)
- Plain text only. No markdown, no HTML, no bullet characters, no trailing full stops added by you.
- Date ranges: `Mon YYYY – Mon YYYY` with a real en dash (`–`). Never an em dash.
- Keep official job titles exactly as the candidate gave them.
- A title plus dates that is too long for one line will wrap the date. Put only the job title in `title` and move the company into `sub`.
- Do not invent facts, numbers, tools or achievements. If a fact is missing, leave the field out and tell the user.
- Section order is the array order. For students and fresh graduates the approved order is Summary, Education, Experience, Skills, Achievements, Languages.
