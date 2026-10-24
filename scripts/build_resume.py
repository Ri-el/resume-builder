#!/usr/bin/env python3
"""Generate the strict A4 resume from approved JSON; PDF is the default output."""

import argparse
import collections
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path
from xml.etree import ElementTree as ET

if __package__:
    from .check_docx import check_docx
    from .resume_content import ContentError, content_fragments, load_content
    from .resume_layout import build_document, fitting_stages, load_profile
else:
    from check_docx import check_docx
    from resume_content import ContentError, content_fragments, load_content
    from resume_layout import build_document, fitting_stages, load_profile


class BuildError(ValueError):
    """Input, dependency, or export checks prevent publication."""


class OverflowError(BuildError):
    def __init__(self, attempts):
        super().__init__(
            "Content does not fit the page or entry-line layout after spacing and margin adjustments. "
            "Supply approved content or request a different layout. "
            "--allow-multiple-pages permits vertical overflow only."
        )
        self.attempts = attempts


def command(arguments):
    environment = dict(os.environ, LC_ALL="C")
    try:
        result = subprocess.run(
            [str(arg) for arg in arguments], check=False, capture_output=True,
            text=True, timeout=60, env=environment,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise BuildError(f"Could not run {Path(arguments[0]).name}; check the dependency and timeout.") from error
    if result.returncode:
        # Converter logs can contain filenames or document text. Do not include
        # them in the default public-facing JSON report.
        raise BuildError(f"{Path(arguments[0]).name} failed with exit code {result.returncode}.")
    return result.stdout


def find_tools():
    tools = {}
    for name in ("pdfinfo", "pdftotext", "pdffonts", "pdftoppm", "fc-match"):
        resolved = shutil.which(name)
        if not resolved:
            raise BuildError(f"Required tool is not on PATH: {name}.")
        tools[name] = resolved
    tools["soffice"] = shutil.which("soffice") or shutil.which("libreoffice")
    if not tools["soffice"]:
        raise BuildError("LibreOffice is required for conversion and page-count checks.")
    return tools


def check_font(family, tools):
    actual = command([tools["fc-match"], "-f", "%{family}", family]).strip()
    if family.casefold() not in {item.strip().casefold() for item in actual.split(",")}:
        raise BuildError(
            "The requested font is not installed. Install it or explicitly choose "
            "an available substitute with --font; silent substitution is disabled."
        )


def export_pdf(source, directory, tools):
    profile = directory / "lo-profile"
    options = "pdf:writer_pdf_Export:" + json.dumps({"UseTaggedPDF": {"type": "boolean", "value": "true"}})
    command([
        tools["soffice"], "-env:UserInstallation=" + profile.resolve().as_uri(),
        "--headless", "--convert-to", options, "--outdir", directory, source,
    ])
    result = directory / (source.stem + ".pdf")
    if not result.is_file() or not result.stat().st_size:
        raise BuildError("Conversion did not produce a fresh PDF.")
    return result


def page_count(pdf, tools):
    info = command([tools["pdfinfo"], pdf])
    pages = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
    size = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", info, re.MULTILINE)
    if not pages or int(pages[1]) < 1 or not size:
        raise BuildError("Could not establish PDF page count and dimensions.")
    if abs(float(size[1]) - 595.276) > 1 or abs(float(size[2]) - 841.89) > 1:
        raise BuildError("Exported PDF is not A4 portrait.")
    if not re.search(r"^Tagged:\s+yes\s*$", info, re.MULTILINE):
        raise BuildError("The PDF export did not retain the requested document structure tags.")
    return int(pages[1])


def fit_resume(candidate, directory, family, tools, *, allow_multiple_pages=False, profile=None):
    profile = profile or load_profile()
    attempts = []
    for index, stage in enumerate(fitting_stages(profile)):
        source = directory / f"resume-{index}.docx"
        layout = build_document(candidate, source, family, stage, profile)
        pdf = export_pdf(source, directory, tools)
        pages = page_count(pdf, tools)
        geometry_issues = inspect_geometry(pdf, candidate, layout, tools)
        attempts.append({"pages": pages, "geometry_issues": geometry_issues, **layout})
        if pages == 1 and not geometry_issues:
            return source, pdf, pages, layout, attempts
    if allow_multiple_pages and not geometry_issues:
        return source, pdf, pages, layout, attempts
    raise OverflowError(attempts)


def inspect_geometry(pdf, candidate, layout, tools):
    """Check text bounds and title/date baselines; visual review is still required."""
    xml = command([tools["pdftotext"], "-bbox-layout", pdf, "-"])
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as error:
        raise BuildError("Could not read PDF text geometry.") from error
    namespace = {"h": "http://www.w3.org/1999/xhtml"}
    tokens, issues, page_widths = [], set(), {}
    for number, page in enumerate(root.findall(".//h:page", namespace)):
        width, height = float(page.get("width")), float(page.get("height"))
        page_widths[number] = width
        if abs(width - 595.276) > 1 or abs(height - 841.89) > 1:
            issues.add("non_a4_page")
        margins = {side: inches * 72 for side, inches in layout["margins_inches"].items()}
        for word in page.findall(".//h:word", namespace):
            bounds = {key: float(word.get(key)) for key in ("xMin", "xMax", "yMin", "yMax")}
            if (bounds["xMin"] < margins["left"] - 1 or bounds["xMax"] > width - margins["right"] + 1
                    or bounds["yMin"] < margins["top"] - 1 or bounds["yMax"] > height - margins["bottom"] + 1):
                issues.add("text_outside_margins")
            for token in re.findall(r"\w+", unicodedata.normalize("NFKC", word.text or "")):
                tokens.append({"text": token, "page": number, **bounds})
    if not tokens:
        return ["no_text_geometry"]

    def occurrences(phrase):
        expected = re.findall(r"\w+", unicodedata.normalize("NFKC", phrase))
        matches = []
        for index in range(len(tokens) - len(expected) + 1):
            group = tokens[index:index + len(expected)]
            if [item["text"] for item in group] == expected:
                matches.append((index, group))
        return matches

    used = set()
    for section, field in (("education", "qualification"), ("experience", "title")):
        for entry in candidate.get(section, []):
            found = False
            for title_index, title in occurrences(entry[field]):
                for date_index, date in occurrences(entry["dates"]):
                    if (title_index, date_index) in used:
                        continue
                    combined = title + date
                    same_page = len({item["page"] for item in combined}) == 1
                    same_baseline = max(item["yMin"] for item in combined) - min(item["yMin"] for item in combined) <= 2
                    separated = min(item["xMin"] for item in date) >= max(item["xMax"] for item in title) + 4
                    right_edge = page_widths[date[0]["page"]] - layout["margins_inches"]["right"] * 72
                    right_aligned = abs(max(item["xMax"] for item in date) - right_edge) <= 2
                    if same_page and same_baseline and separated and right_aligned:
                        used.add((title_index, date_index))
                        found = True
                        break
                if found:
                    break
            if not found:
                issues.add("entry_title_date_wrap_or_collision")
    return sorted(issues)


def font_key(value):
    value = re.sub(r"^[A-Z]{6}\+", "", value)
    return re.sub(r"[^a-z0-9]", "", value.lower())


def inspect_fonts(pdf, family, tools):
    table = command([tools["pdffonts"], pdf])
    fonts = []
    for line in table.splitlines()[2:]:
        columns = line.split()
        if not columns:
            continue
        if len(columns) < 8:
            raise BuildError("Could not interpret the PDF font report.")
        name, embedded, unicode_map = columns[0], columns[-5], columns[-3]
        fonts.append({"name": name, "embedded": embedded == "yes", "unicode_map": unicode_map == "yes"})
    if not fonts:
        raise BuildError("The PDF font report contains no text fonts.")
    if any(not font_key(item["name"]).startswith(font_key(family)) for item in fonts):
        raise BuildError("PDF font substitution was detected; inspect pdffonts before delivery.")
    if any(not item["embedded"] for item in fonts):
        raise BuildError("The PDF contains an unembedded font.")
    return fonts, table


def word_counts(text):
    return collections.Counter(re.findall(r"\w+", unicodedata.normalize("NFKC", text)))


def entry_grouping(text, candidate):
    normalised = " ".join(unicodedata.normalize("NFKC", text).split())
    rows = []
    for section, title, organisation in (("education", "qualification", "institution"), ("experience", "title", "company")):
        for entry in candidate.get(section, []):
            expected = " ".join((entry[title], entry["dates"], entry[organisation]))
            rows.append(" ".join(unicodedata.normalize("NFKC", expected).split()))
    if not rows:
        return "not_applicable"
    return "passed" if all(row in normalised for row in rows) else "requires_review"


def inspect_text(pdf, candidate, headings, tools):
    plain = command([tools["pdftotext"], pdf, "-"])
    layout = command([tools["pdftotext"], "-layout", pdf, "-"])
    raw = command([tools["pdftotext"], "-raw", pdf, "-"])
    expected = word_counts(" ".join(content_fragments(candidate)))
    if expected - word_counts(plain):
        raise BuildError("Some supplied text is missing from PDF extraction; inspect before delivery.")
    lines = [line.strip() for line in plain.splitlines()]
    previous = -1
    for heading in headings:
        try:
            current = lines.index(heading, previous + 1)
        except ValueError as error:
            raise BuildError("PDF section headings are missing or out of order.") from error
        previous = current
    grouping = {name: entry_grouping(value, candidate) for name, value in (("plain", plain), ("layout", layout), ("raw", raw))}
    return plain, layout, raw, grouping


def create_previews(pdf, directory, pages, tools):
    directory.mkdir()
    command([tools["pdftoppm"], "-png", "-r", "120", pdf, directory / "page"])
    images = sorted(directory.glob("page-*.png"))
    if len(images) != pages or any(not item.stat().st_size for item in images):
        raise BuildError("Rendering did not produce an image for every PDF page.")
    return images


def atomic_copy(source, destination):
    descriptor, temporary = tempfile.mkstemp(prefix=".resume-", dir=destination.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream, source.open("rb") as incoming:
            shutil.copyfileobj(incoming, stream)
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def build(candidate_path, output, *, family=None, also_docx=False, allow_multiple_pages=False, qa_dir=None, overwrite=False):
    profile = load_profile()
    family = family or profile["font"]
    if not family.strip() or any(ord(char) < 32 for char in family):
        raise BuildError("Font family must be a non-empty name without control characters.")
    output = Path(output).resolve()
    if output.suffix.lower() not in {".pdf", ".docx"}:
        raise BuildError("Output must end in .pdf or .docx.")
    if also_docx and output.suffix.lower() != ".pdf":
        raise BuildError("--also-docx requires a PDF output path.")
    destinations = [output]
    if also_docx:
        destinations.append(output.with_suffix(".docx"))
    if not overwrite and any(path.exists() for path in destinations):
        raise BuildError("An output file already exists; choose another path or use --overwrite.")
    if qa_dir is not None:
        qa_dir = Path(qa_dir).resolve()
        if qa_dir.exists():
            raise BuildError("QA directory already exists; use a fresh path to avoid stale previews.")
        if qa_dir in destinations or any(qa_dir in path.parents for path in destinations):
            raise BuildError("The QA directory must be separate from deliverable paths.")
    candidate = load_content(candidate_path)
    tools = find_tools()
    check_font(family, tools)

    with tempfile.TemporaryDirectory(prefix="resume-builder-") as temporary:
        work = Path(temporary)
        source, pdf, pages, layout, attempts = fit_resume(
            candidate, work, family, tools, allow_multiple_pages=allow_multiple_pages, profile=profile,
        )
        preflight = check_docx(source)
        if preflight["status"] != "pass":
            raise BuildError("Generated DOCX did not pass static preflight.")
        fonts, font_table = inspect_fonts(pdf, family, tools)
        plain, extracted_layout, raw, grouping = inspect_text(pdf, candidate, layout["sections"], tools)
        previews = create_previews(pdf, work / "previews", pages, tools)
        if qa_dir is not None:
            qa_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(work / "previews", qa_dir)
            (qa_dir / "text.txt").write_text(plain, encoding="utf-8")
            (qa_dir / "text-layout.txt").write_text(extracted_layout, encoding="utf-8")
            (qa_dir / "text-raw.txt").write_text(raw, encoding="utf-8")
            (qa_dir / "fonts.txt").write_text(font_table, encoding="utf-8")
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            atomic_copy(pdf if destination.suffix.lower() == ".pdf" else source, destination)
        return {
            "schema_version": 1, "status": "generated", "profile": profile["id"],
            "outputs": [str(path) for path in destinations], "pages": pages,
            "font": {"requested": profile["font"], "used": family, "explicit_substitute": family.casefold() != profile["font"].casefold(), "pdf_fonts": fonts},
            "layout": layout, "attempts": attempts,
            "warnings": ["PDF text extraction separates some title/date/organisation groups. Review plain, layout, and raw extraction before delivery."] if "requires_review" in grouping.values() else [],
            "checks": {
                "docx_preflight": "passed", "a4_page_size": "passed", "page_count": "checked",
                "pdf_structure_tags": "passed", "entry_grouping_by_extraction_mode": grouping,
                "font_family_and_embedding": "passed", "text_preservation": "passed", "section_order": "passed",
                "text_bounds_and_entry_baselines": "passed",
                "page_images": {"rendered": len(previews), "retained_at": str(qa_dir) if qa_dir else None},
                "visual_inspection": "not_checked", "reading_order_review": "not_checked",
                "factual_accuracy": "not_checked", "job_description_fit": "not_checked",
            },
        }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="Approved candidate JSON; see examples/candidate.json")
    parser.add_argument("--output", type=Path, default=Path("private/resume.pdf"))
    parser.add_argument("--font", help="Explicit installed substitute for Calibri; recorded in the report")
    parser.add_argument("--also-docx", action="store_true", help="Also publish the editable DOCX beside the requested PDF")
    parser.add_argument("--allow-multiple-pages", action="store_true", help="Explicitly permit more than one page after fitting attempts")
    parser.add_argument("--qa-dir", type=Path, help="Retain every page image, extracted text, and font report in a fresh directory")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing requested deliverable files")
    args = parser.parse_args(argv)
    try:
        report = build(
            args.candidate, args.output, family=args.font, also_docx=args.also_docx,
            allow_multiple_pages=args.allow_multiple_pages, qa_dir=args.qa_dir, overwrite=args.overwrite,
        )
        exit_code = 0
    except OverflowError as error:
        report = {"schema_version": 1, "status": "needs_decision", "message": str(error), "outputs": [], "attempts": error.attempts}
        exit_code = 1
    except (BuildError, ContentError, OSError, ValueError) as error:
        message = str(error) if isinstance(error, (BuildError, ContentError)) else "Could not read or write the requested input/output files."
        report = {"schema_version": 1, "status": "error", "message": message, "outputs": []}
        exit_code = 2
    print(json.dumps(report, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
