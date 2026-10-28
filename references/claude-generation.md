# Renderer source record

The renderer is preserved under `vendor/claude-resume-generator/`. The supplied
archive, `resume-generator.zip`, has SHA-256
`b51cdddf6811bf6684f8a4d31b2b15036ce82b650cb395b98942ddb91dca90ed`.
[UPSTREAM.json](../vendor/claude-resume-generator/UPSTREAM.json) records each
copied file's hash. Keep those files unchanged.

The package was supplied from a Claude session. Its Node helpers were recovered
from a transcript; the JSON wrapper is a refactor, the Python port a reconstruction,
and the fitting ladder, inspector and photo support are later additions. The
original [reconstruction notes](../vendor/claude-resume-generator/docs/RECONSTRUCTION_NOTES.md)
record these distinctions. The private resume discussed in those notes is not
included. Reproduction checks here establish a match to the shipped fictional
reference, not independent proof about that private document.

## Supported route

Use [the verified entry point](verified-workflow.md). It selects the Node engine
explicitly and enforces the reference before every candidate build. The source
package retains other scripts for provenance; its Python port and photo extension
are not supported delivery routes.

The reference stack is `docx` 9.6.1, LibreOffice 24.2.7.2, Carlito 1.104 and
Liberation Serif 2.1.5. Different font releases or converters can change wrapping
even when the DOCX XML is identical. Do not alter style settings to compensate.
See [setup](../docs/SETUP.md) for the tested environment.

The reference comparator uses layout text, word coordinates rounded to 0.01 pt,
and 100 dpi greyscale images, counting pixel differences greater than 40. The
verified entry point requires identical text, zero reported coordinate shift
and an integer count of zero differing pixels. It reads the report because the
upstream comparator does not itself fail its exit status on a mismatch.

The original 6.9-inch date tab sits about 2 pt beyond the nominal text width.
Languages remain left aligned. These are intentional source settings. The
fitting ladder changes paragraph spacing, then vertical margins down to 0.35 inch;
it preserves font sizes, horizontal margins and content.
