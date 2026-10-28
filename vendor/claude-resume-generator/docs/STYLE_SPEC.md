# Style specification (the approved house format)

All values live in `config/style.json`. `generate.js` converts points to docx units exactly as the approved script did: half-points = pt x 2, twips = pt x 20.
Do not change them to "improve" the look.

| Element | Value | docx units |
|---|---|---|
| Page | A4 | 11906 x 16838 twips |
| Margins | 0.55 in top and bottom, 0.7 in left and right | 792 / 1008 twips |
| Header / footer distance | docx-js default | 708 twips |
| Font requested | Calibri (see FONTS_AND_RENDERING.md) | |
| Colours | text `#000000`, dates and company lines `#595959`. No other colour | |
| Name | 16 pt bold, left, 2 pt after | size 32, after 40 |
| Headline | 9.5 pt bold, items joined by `"  |  "`, 2 pt after | size 19, after 40 |
| Contact line | 9.5 pt regular, items joined by `"  ·  "`, 2 pt after | size 19, after 40 |
| Section heading | 10.5 pt bold UPPERCASE, 7 pt before, 3 pt after, bottom border 0.75 pt black, 2 pt gap | size 21, before 140, after 60, border size 6, space 2 |
| Summary | 10 pt, **justified**, 4 pt after | size 20, after 80 |
| Entry line 1 | title 10 pt bold; dates 9.5 pt italic grey after ONE right tab; 0.25 pt after | size 20 / 19, after 5 |
| Right tab stop | 6.9 in from the left margin | 9936 twips |
| Entry line 2 (company, city) | 10 pt italic grey, **justified**, 2 pt after | size 20, after 40 |
| Bullets | real list bullets "•", 10 pt, **justified**, 1.8 pt after; indent left 0.22 in, hanging 0.18 in | after 36; left 316, hanging 259 (docx-js floors the inches) |
| Skills line | bold label + ": " + items joined by `" · "`, 10 pt, **justified**, 1.6 pt after | after 32 |
| Inline list (languages) | items joined by `"  ·  "`, 10 pt, **left aligned**, 0 after | after 0 |
| Line spacing | single, never overridden | no `w:line` anywhere |
| Space before body paragraphs | none | only section headings have space before |

## Alignment
Justified: summary, bullets, company/location lines, skills lines. Left: name, headline, contact line, headings, dates, languages line.

## The tab stop, honestly
The approved script used 6.9 in. At 0.7 in margins the text width is 6.87 in, so the stop sits 0.03 in past the right margin (dates end about 2 pt beyond justified text).
That is the **approved** behaviour, so `tab_stop_in` stays 6.9. If you change the left or right margin, set `tab_stop_in` to `8.268 - left - right` (the text width) or the dates will sit visibly inset from the right edge.

## Section order used in the approved resumes
Summary, Education, Experience, Skills, Achievements, Languages (Education before Experience for students and fresh graduates). In this package the order is simply the order of `sections` in the input JSON.
