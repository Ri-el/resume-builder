# Photo variant (an EXTENSION, not part of the approved resume)

The approved resume has no photo. This variant exists because a with-photo and a without-photo copy were requested. It was tested only by rendering the fictional sample in LibreOffice.

- Use only a photo the candidate supplied. Never generate, retouch or beautify a face. If there is no photo, build the no-photo version and ask for the photo.
- Prepare it with `python3 scripts/prepare_photo.py in.jpg out.jpg` (centre crop to 5:6, 600 x 720, no stretching). It warns if the photo is under 600 px wide.
- Placement: floating picture anchored to the first paragraph, right edge on the right margin, top on the top margin, square wrap with text on the left, 1.0 in x 1.2 in, alt text "Profile photo". Not a table, not a text box, not in the Word header.
- A photo narrows the header text column to about 5.7 in. A one-line contact string wrapped mid-item in testing (the LinkedIn handle split in two), so the generators split the contact into two lines (`contact_split_at: 2`) and add 26 pt after the second line (`contact_after_pt_when_photo`) so the SUMMARY rule sits below the photo.
- Keep the headline under about 70 characters. A longer one wraps; `inspect_pdf.py` reports it as FAIL (tested).
- Build both: `python3 scripts/build.py --input my.json --name Jane_Doe --outdir out --variants both --photo prepared.jpg` writes `Jane_Doe` (no photo, use for portals and ATS) and `Jane_Doe_Photo`.
- Wording, order and styling are identical in both. Apply every edit to both.
- Never commit a real person's photo to a public repository.
