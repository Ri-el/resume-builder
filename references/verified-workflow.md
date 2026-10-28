# Verified resume generation

Use `scripts/build_verified_resume.py` as the single entry point for the established
PDF format. Keep the supplied renderer, style and fitting helpers unchanged.

```bash
python scripts/build_verified_resume.py --self-test
python scripts/build_verified_resume.py --input private/candidate.json \
  --output private/resume.pdf --qa-dir private/resume-qa
```

The build runs its reference test every time. Use approved native JSON from
[content-preparation.md](content-preparation.md). Use a fresh QA directory and
`--overwrite` only for an authorised revision. Add `--also-docx` only when requested.
Keep candidate inputs, exports and QA files in the task workspace, outside the
installed skill folder. Never save private candidate information with the skill.

The entry point checks:

1. Every recorded source file still matches the supplied package hash.
2. The exact `docx` library version 9.6.1 and LibreOffice 24.2.7.2 are available.
3. A freshly generated fictional reference has the same five DOCX XML parts,
   identical PDF text, zero measured word shift and zero differing pixels in the
   supplied 100 dpi comparison. Read the integer pixel count, not a rounded percentage.
4. The candidate build succeeds using the unchanged Node method and fitting ladder.
5. Every native input field is supported and every complete text fragment and
   repeated-word count survives plain, layout-preserving and raw extraction.
6. PDF fonts are embedded and match the reference families, Carlito and the
   Liberation Serif bullet fallback.

Only after these checks does it release the requested output. Exit 2 and
`status: blocked` mean the workflow could not meet its requirements. Explain the
reported reason; do not produce an approximation or claim a passing check.
The fresh export profile prevents stale preferences from changing conversion.

## Visual and factual review

Open every final `page-*.png` in the QA directory. Review wrapping, collisions,
orphan headings and reading order. `visual_inspection: not_checked` is deliberate:
software cannot claim that an assistant actually looked at an image.
Review facts and target-role gaps independently. Never treat this as an ATS score.

## Reuse in new chats

Give the public repository link with the start prompt in [README.md](../README.md),
or select **Resume Builder** if you have installed a copy. Follow [setup](../docs/SETUP.md)
to obtain the complete repository and required tools. A GitHub link alone cannot
force every ChatGPT conversation to load or execute a workflow. If the tools,
fonts or pinned converter cannot be provided, stop and report the limitation.
Do not send private candidate information to public CI to work around a missing
local environment.

The supplied photo extension and reconstructed Python port remain source artifacts.
This verified entry point supports the established no-photo PDF layout. A request
for a different layout requires an explicit, separately validated change.
