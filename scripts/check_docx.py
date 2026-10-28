#!/usr/bin/env python3
"""Read-only, dependency-free preflight for a resume DOCX, not an ATS score."""

import argparse
import json
import math
import sys
import zipfile
import zlib
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS = {"w": W[1:-1]}
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_EXPANDED_BYTES = 64 * 1024 * 1024
MAX_XML_BYTES = 4 * 1024 * 1024
MAX_ENTRIES = 2048
LIMITATION = (
    "Static DOCX checks only. Factual accuracy, rendered pages, PDF reading "
    "order, and ATS behavior were not checked."
)
TRACKED_TAGS = {
    W + tag for tag in (
        "ins", "del", "moveFrom", "moveTo", "pPrChange", "rPrChange",
        "sectPrChange", "tblPrChange", "trPrChange", "tcPrChange",
    )
}


class InvalidDocument(ValueError):
    """The input cannot be safely inspected as a DOCX."""


def enabled(element):
    return element is not None and element.get(W + "val", "true").lower() not in {
        "0", "false", "off",
    }


def read_parts(path):
    """Read XML in memory without extracting files or following external links."""
    if path.suffix.lower() != ".docx":
        raise InvalidDocument("Expected a .docx file.")
    if path.stat().st_size > MAX_ARCHIVE_BYTES:
        raise InvalidDocument("DOCX exceeds the 32 MiB archive limit.")
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if len(entries) > MAX_ENTRIES or len(names) != len(set(names)):
            raise InvalidDocument("DOCX has too many entries or duplicate part names.")
        if sum(entry.file_size for entry in entries) > MAX_EXPANDED_BYTES:
            raise InvalidDocument("DOCX exceeds the 64 MiB expanded-size limit.")
        if "word/document.xml" not in names:
            raise InvalidDocument("DOCX is missing word/document.xml.")

        parts = {}
        for entry in entries:
            name = entry.filename
            relevant = name in {"word/document.xml", "word/styles.xml"} or (
                name.startswith(("word/header", "word/footer")) and name.endswith(".xml")
            )
            if not relevant:
                continue
            if entry.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
                raise InvalidDocument("Document XML uses an unsupported compression method.")
            if entry.file_size > MAX_XML_BYTES:
                raise InvalidDocument("A document XML part exceeds the 4 MiB limit.")
            data = archive.read(entry)
            # Reject declarations even in UTF-16/32 XML; ElementTree accepts both.
            declarations = data.replace(b"\x00", b"").upper()
            if b"<!DOCTYPE" in declarations or b"<!ENTITY" in declarations:
                raise InvalidDocument("Document XML contains unsupported declarations.")
            parts[name] = ET.fromstring(data)

    document = parts["word/document.xml"]
    if document.tag != W + "document" or document.find(W + "body") is None:
        raise InvalidDocument("Expected a WordprocessingML document with a body.")
    return parts


class Styles:
    """Resolve ordinary run properties through document and style defaults."""

    def __init__(self, root):
        self.styles = {}
        self.default_paragraph = None
        self.defaults = None
        if root is not None:
            self.defaults = root.find("w:docDefaults/w:rPrDefault/w:rPr", NS)
            for style in root.findall("w:style", NS):
                self.styles[style.get(W + "styleId")] = style
                if style.get(W + "type") == "paragraph" and enabled_default(style):
                    self.default_paragraph = style.get(W + "styleId")

    def chain(self, style_id):
        chain, seen = [], set()
        while style_id in self.styles and style_id not in seen:
            seen.add(style_id)
            style = self.styles[style_id]
            chain.append(style.find(W + "rPr"))
            parent = style.find(W + "basedOn")
            style_id = parent.get(W + "val") if parent is not None else None
        return list(reversed(chain))

    def run_properties(self, paragraph, run):
        paragraph_style = paragraph.find("w:pPr/w:pStyle", NS)
        style_id = (
            paragraph_style.get(W + "val")
            if paragraph_style is not None else self.default_paragraph
        )
        style_properties = self.chain(style_id)
        run_style = run.find("w:rPr/w:rStyle", NS)
        if run_style is not None:
            style_properties.extend(self.chain(run_style.get(W + "val")))
        # Visibility properties can toggle through style chains; do not certify
        # visibility from a simple last-property-wins approximation.
        visibility_review = any(
            prop is not None and any(prop.find(W + tag) is not None for tag in ("vanish", "webHidden"))
            for prop in style_properties
        )
        properties = [self.defaults, *style_properties, run.find(W + "rPr")]
        resolved = {}
        for prop in properties:
            if prop is not None:
                resolved.update({child.tag: child for child in prop})
        return resolved, visibility_review


def paragraph_runs(paragraph):
    """Include hyperlink/revision runs, but leave nested textbox paragraphs alone."""
    pending = list(paragraph)
    while pending:
        node = pending.pop()
        if node.tag == W + "r":
            yield node
        elif node.tag != W + "p":
            pending.extend(node)


def enabled_default(style):
    return style.get(W + "default", "false").lower() in {"1", "true", "on"}


def check_docx(path):
    """Return a report without including candidate text or changing the file."""
    parts = read_parts(Path(path))
    document = parts["word/document.xml"]
    body = document.find(W + "body")
    findings = []
    codes = set()

    def add(code, message, severity="review"):
        if code not in codes:
            codes.add(code)
            findings.append({"code": code, "severity": severity, "message": message})

    if not any((node.text or "").strip() for node in body.iter(W + "t")):
        add("NO_BODY_TEXT", "The body has no ordinary selectable text.", "error")
    if any(node.tag in TRACKED_TAGS for root in parts.values() for node in root.iter()):
        add("TRACKED_CHANGES", "Resolve tracked changes in the authoritative source.", "error")
    if any(True for _ in body.iter(W + "tbl")):
        add("TABLE_CONTENT", "Check table content for a sensible linear reading order.")

    for name, root in parts.items():
        if name == "word/styles.xml":
            continue
        if any(True for _ in root.iter(W + "txbxContent")):
            add("TEXT_BOX", "Text boxes may disrupt extraction; review core content placement.")
        if any(node.tag in {W + "drawing", W + "pict"} for node in root.iter()):
            add("DRAWING", "Check that images or shapes contain no essential resume facts.")
        if any(node.tag in {W + "altChunk", W + "object", W + "subDoc", W + "contentPart"} for node in root.iter()):
            add("EXTERNAL_CONTENT", "Review embedded or linked content in the editor and final export.")
        if name.startswith(("word/header", "word/footer")) and any(
            (node.text or "").strip() for node in root.iter(W + "t")
        ):
            add("HEADER_FOOTER_TEXT", "Keep essential facts in the body; review header/footer text.")

    sections = list(body.iter(W + "sectPr"))
    if not sections:
        add("PAGE_SIZE_UNKNOWN", "Set an explicit page size before export.")
    for section in sections:
        size = section.find(W + "pgSz")
        try:
            width, height = (int(size.get(W + axis)) for axis in ("w", "h"))
            if width <= 0 or height <= 0:
                raise ValueError
        except (AttributeError, TypeError, ValueError):
            add("PAGE_SIZE_UNKNOWN", "A section has missing or invalid page dimensions.")
        else:
            # A4 portrait in twips; tolerate normal rounding by document libraries.
            if abs(width - 11906) > 20 or abs(height - 16838) > 20:
                add("NON_A4_PAGE", "A section is not A4 portrait; confirm the requested format.")
        columns = section.find(W + "cols")
        if columns is not None:
            try:
                count = int(columns.get(W + "num", "1"))
                if count < 1:
                    raise ValueError
            except ValueError:
                add("COLUMN_COUNT_UNKNOWN", "A section has an invalid column count.")
            else:
                if count > 1 or len(columns.findall(W + "col")) > 1:
                    add("MULTIPLE_COLUMNS", "Review multi-column content for linear extraction.")

    styles = Styles(parts.get("word/styles.xml"))
    for name, root in parts.items():
        if name == "word/styles.xml":
            continue
        for paragraph in root.iter(W + "p"):
            for run in paragraph_runs(paragraph):
                if not any((node.text or "").strip() for node in run.findall(W + "t")):
                    continue
                properties, visibility_review = styles.run_properties(paragraph, run)
                if visibility_review:
                    add("STYLE_VISIBILITY", "Style-defined text visibility requires review in the editor.")
                if any(enabled(properties.get(W + tag)) for tag in ("vanish", "webHidden")):
                    add("HIDDEN_TEXT", "Text has hidden-formatting flags; inspect visibility in the editor.")
                size = properties.get(W + "sz")
                try:
                    points = float(size.get(W + "val")) / 2
                    if not math.isfinite(points) or points <= 0:
                        raise ValueError
                except (AttributeError, TypeError, ValueError):
                    add("FONT_SIZE_UNKNOWN", "Some text has no resolvable valid font size.")
                else:
                    if points < 9:
                        add("SMALL_TEXT", "Some text is below 9 pt; check legibility after rendering.")

    status = "fail" if any(f["severity"] == "error" for f in findings) else (
        "review" if findings else "pass"
    )
    return {"schema_version": 1, "status": status, "findings": findings, "limitations": LIMITATION}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path, help="DOCX to inspect without modifying it")
    parser.add_argument("--json", action="store_true", help="Print a structured report to stdout")
    args = parser.parse_args(argv)
    try:
        report = check_docx(args.document)
    except (InvalidDocument, OSError, zipfile.BadZipFile, ET.ParseError, RuntimeError,
            NotImplementedError, EOFError, ValueError, zlib.error) as error:
        message = str(error) if isinstance(error, InvalidDocument) else (
            "Cannot read this file as a supported DOCX. Check the file and its permissions."
        )
        report = {
            "schema_version": 1, "status": "error",
            "findings": [{"code": "INVALID_INPUT", "severity": "error", "message": message}],
            "limitations": LIMITATION,
        }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("DOCX preflight: " + report["status"].upper())
        for finding in report["findings"]:
            print(f"[{finding['code']}] {finding['message']}")
        print(report["limitations"])
    return 2 if report["status"] == "error" else int(report["status"] != "pass")


if __name__ == "__main__":
    sys.exit(main())
