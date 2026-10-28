#!/usr/bin/env python3
"""Build a resume only after reproducing the supplied reference."""

import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zipfile

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "vendor/claude-resume-generator"
PARTS = ("document", "numbering", "styles", "settings", "fontTable")


class Blocked(Exception):
    pass


def run(command, env=None, cwd=None):
    result = subprocess.run(command, env=env, cwd=cwd, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise Blocked(f"Command failed: {Path(command[0]).name}; " + (result.stdout + result.stderr)[-1600:])
    return result.stdout


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Blocked(f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def input_fragments(resume):
    """Validate the native contract so unsupported data cannot disappear silently."""
    fragments = []

    def obj(value, required, optional=()):
        if not isinstance(value, dict) or set(required) - value.keys() or value.keys() - set(required) - set(optional):
            raise Blocked("Input has missing or unsupported fields; use the native input contract")

    def text(value):
        if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value) or "\u2014" in value:
            raise Blocked("Text must be non-empty plain text without control characters or em dashes")
        fragments.append(value)

    def array(value, nonempty=True):
        if not isinstance(value, list) or (nonempty and not value):
            raise Blocked("A required input list is empty or is not a list")

    obj(resume, ("name", "headline", "contact", "sections"), ("_comment",))
    text(resume["name"])
    for key in ("headline", "contact"):
        # The unchanged upstream inspector indexes item zero in both lists.
        array(resume[key])
        for item in resume[key]:
            text(item)
    array(resume["sections"])
    for section in resume["sections"]:
        if not isinstance(section, dict) or section.get("type") not in ("paragraph", "entries", "skills", "bullets", "inline_list"):
            raise Blocked("Unsupported section type")
        kind = section["type"]
        obj(section, ("heading", "type", "text" if kind == "paragraph" else "items"))
        text(section["heading"])
        fragments[-1] = fragments[-1].upper()
        if kind == "paragraph":
            text(section["text"])
            continue
        array(section["items"])
        for item in section["items"]:
            if kind == "entries":
                obj(item, ("title",), ("dates", "sub", "bullets"))
                text(item["title"])
                for key in ("dates", "sub"):
                    if key in item:
                        text(item[key])
                if "bullets" in item:
                    array(item["bullets"], nonempty=False)
                    for bullet in item["bullets"]:
                        text(bullet)
            elif kind == "skills":
                obj(item, ("label", "items"))
                text(item["label"])
                array(item["items"])
                for skill in item["items"]:
                    text(skill)
            else:
                text(item)
    return fragments


def claim_fields(value, path=""):
    """Return candidate text by JSON Pointer, excluding editorial field labels."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key not in {"_comment", "heading", "type", "label"}:
                escaped = key.replace("~", "~0").replace("/", "~1")
                yield from claim_fields(item, path + "/" + escaped)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from claim_fields(item, path + "/" + str(index))
    elif isinstance(value, str):
        yield path, value


def check_evidence(resume, ledger):
    """Check claim coverage and stale values, not the truth of source documents."""
    def obj(value, required, optional=()):
        if not isinstance(value, dict) or set(required) - value.keys() or value.keys() - set(required) - set(optional):
            raise Blocked("Evidence has missing or unsupported fields; use docs/EVIDENCE_FORMAT.md")

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    obj(ledger, ("schema_version", "sources", "claims"))
    if type(ledger["schema_version"]) is not int or ledger["schema_version"] != 1:
        raise Blocked("Unsupported evidence schema_version")
    if not isinstance(ledger["sources"], list) or not ledger["sources"]:
        raise Blocked("Evidence requires a non-empty sources list")
    sources = set()
    for source in ledger["sources"]:
        obj(source, ("id", "kind", "label"))
        source_id = source["id"]
        if not isinstance(source_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,63}", source_id) or source_id in sources:
            raise Blocked("Evidence source IDs must be unique lowercase identifiers")
        if source["kind"] not in ("candidate_notes", "document", "correction") or not nonempty(source["label"]):
            raise Blocked("Evidence source kind or label is invalid")
        sources.add(source_id)
    if not isinstance(ledger["claims"], list):
        raise Blocked("Evidence claims must be a list")
    expected = dict(claim_fields(resume))
    covered = set()
    for claim in ledger["claims"]:
        obj(claim, ("path", "value", "source_ids", "status"), ("note",))
        pointer = claim["path"]
        if not isinstance(pointer, str) or pointer not in expected or pointer in covered:
            raise Blocked("Evidence claim path is unsupported or duplicated")
        if claim["value"] != expected[pointer]:
            raise Blocked("Evidence value is stale or does not match input at " + pointer)
        refs = claim["source_ids"]
        if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or ref not in sources for ref in refs) or len(refs) != len(set(refs)):
            raise Blocked("Evidence claim must reference known, unique source IDs at " + pointer)
        if claim["status"] not in ("confirmed", "candidate_reported"):
            raise Blocked("Unresolved or unsupported evidence status at " + pointer)
        if "note" in claim and not nonempty(claim["note"]):
            raise Blocked("Evidence note must be non-empty text at " + pointer)
        covered.add(pointer)
    missing = expected.keys() - covered
    if missing:
        raise Blocked("Evidence is missing candidate text at " + sorted(missing)[0])
    return {"status": "passed", "claims": len(covered), "sources": len(sources),
            "scope": "Source references and matching input values only; factual truth requires review"}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)


def verify_sources():
    manifest = json.loads((UPSTREAM / "UPSTREAM.json").read_text())
    for relative, digest in manifest["files"].items():
        path = (UPSTREAM / relative).resolve()
        if not path.is_relative_to(UPSTREAM.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise Blocked("Supplied generator changed: " + relative)


def environment(work):
    env = os.environ.copy()
    node = env.get("CODEX_PRIMARY_RUNTIME_NODE") or shutil.which("node")
    office = shutil.which("soffice") or shutil.which("libreoffice")
    if not node or not office:
        raise Blocked("Node and LibreOffice 24.2.7.2 are required; no alternative renderer will be used")
    for program in ("pdfinfo", "pdffonts", "pdftotext", "pdftoppm"):
        if not shutil.which(program):
            raise Blocked("Missing required PDF tool: " + program)
    if env.get("CODEX_PRIMARY_RUNTIME_NODE_MODULES"):
        env["NODE_PATH"] = env["CODEX_PRIMARY_RUNTIME_NODE_MODULES"] + os.pathsep + env.get("NODE_PATH", "")
    check = "const fs=require('fs'),p=require('path');let d=p.dirname(require.resolve('docx'));while(!fs.existsSync(p.join(d,'package.json')))d=p.dirname(d);console.log(JSON.parse(fs.readFileSync(p.join(d,'package.json'),'utf8')).version)"
    if run([node, "-e", check], env=env, cwd=UPSTREAM).strip() != "9.6.1":
        raise Blocked("The supplied method requires docx 9.6.1")
    version = run([office, "--version"], env=env).strip()
    if not re.search(r"\b24\.2\.7\.2\b", version):
        raise Blocked("Reference converter unavailable: need LibreOffice 24.2.7.2; found " + version)
    # Isolate the export profile without changing the supplied script or PDF settings.
    bin_dir = work / "bin"
    bin_dir.mkdir()
    profile = (work / "office-profile").as_uri()
    launcher = bin_dir / "soffice"
    launcher.write_text("#!" + sys.executable + "\nimport os,sys\nreal=" + repr(office) + "\nprofile=" + repr(profile) + "\nargs=[('-env:UserInstallation='+profile) if a.startswith('-env:UserInstallation=') else a for a in sys.argv[1:]]\nos.execv(real,[real,*args])\n")
    launcher.chmod(0o700)
    env["PATH"] = str(bin_dir) + os.pathsep + str(Path(node).parent) + os.pathsep + env.get("PATH", "")
    return env, version


def build(input_path, destination, env, target_pages=1):
    return run([sys.executable, str(UPSTREAM / "scripts/build.py"), "--engine", "node", "--input", str(input_path), "--name", "Resume", "--outdir", str(destination), "--target-pages", str(target_pages)], env=env)


def compare_report(report):
    shift = re.search(r"max word shift \(pt\): ([\d.]+)", report)
    pixels = re.search(r"differing pixels: (\d+) of", report)
    if "pages: 1 vs 1" not in report or "text identical: True" not in report or not shift or float(shift[1]) != 0 or not pixels or int(pixels[1]) != 0:
        raise Blocked("Reference PDF reproduction failed; no candidate PDF will be released. " + report.strip())


def self_test(work, env):
    folder = work / "reference"
    build(UPSTREAM / "input/sample_resume.json", folder, env)
    with zipfile.ZipFile(UPSTREAM / "output/Sample_Resume.docx") as expected, zipfile.ZipFile(folder / "Resume.docx") as actual:
        for part in PARTS:
            key = "word/" + part + ".xml"
            if expected.read(key) != actual.read(key):
                raise Blocked("Reference DOCX differs: " + key)
    report = run([sys.executable, str(UPSTREAM / "scripts/compare_pdfs.py"), str(UPSTREAM / "output/Sample_Resume.pdf"), str(folder / "Resume.pdf")], env=env)
    compare_report(report)
    return report.strip()


def norm(value):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def check_content(pdf, fragments, qa, env, target_pages=1):
    expected = collections.Counter(re.findall(r"\w+", norm(" ".join(fragments)).casefold()))
    for name, flags in (("plain", []), ("layout", ["-layout"]), ("raw", ["-raw"])):
        value = run(["pdftotext", *flags, str(pdf), "-"], env=env)
        (qa / (name + ".txt")).write_text(value)
        actual = collections.Counter(re.findall(r"\w+", norm(value).casefold()))
        if any(norm(fragment) not in norm(value) for fragment in fragments) or expected - actual:
            raise Blocked("Complete text preservation failed in " + name + " extraction")
    fonts = run(["pdffonts", str(pdf)], env=env)
    (qa / "fonts.txt").write_text(fonts)
    rows = [line for line in fonts.splitlines()[2:] if line.strip()]
    if not rows:
        raise Blocked("PDF font metadata is missing")
    for line in rows:
        name = re.sub(r"^[A-Z]{6}\+", "", line.split()[0])
        flags = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line)
        if not name.startswith(("Carlito", "LiberationSerif")) or not flags or flags[1] != "yes":
            raise Blocked("Unexpected or unembedded PDF font: " + name)
    match = re.search(r"^Pages:\s+(\d+)\s*$", run(["pdfinfo", str(pdf)], env=env), re.MULTILINE)
    if not match or not 1 <= int(match[1]) <= target_pages:
        raise Blocked("PDF page count is missing or exceeds the requested maximum")
    pages = int(match[1])
    run(["pdftoppm", "-png", "-r", "150", str(pdf), str(qa / "page")], env=env)
    images = list(qa.glob("page-*.png"))
    if len(images) != pages or any(image.stat().st_size == 0 for image in images):
        raise Blocked("Every PDF page must have a non-empty QA image")
    return pages


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("Page maximum must be a positive integer")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--qa-dir", type=Path)
    parser.add_argument("--also-docx", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--target-pages", type=positive_int, help="Maximum allowed pages; default 1, never an instruction to cut content")
    parser.add_argument("--evidence", type=Path, help="Optional private claim ledger; all candidate text must be covered when supplied")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--doctor", action="store_true", help="Check dependencies and source integrity without rendering")
    modes.add_argument("--check-input", action="store_true", help="Validate native JSON and optional evidence without document tools")
    args = parser.parse_args(argv)
    released = []
    try:
        if (args.self_test or args.doctor) and any((args.input, args.output, args.qa_dir, args.evidence, args.also_docx, args.overwrite, args.target_pages is not None)):
            raise Blocked("Use --self-test or --doctor alone; candidate options would be ignored")
        if args.check_input and (not args.input or any((args.output, args.qa_dir, args.also_docx, args.overwrite, args.target_pages is not None))):
            raise Blocked("Use --check-input with --input and optional --evidence only")
        if not any((args.self_test, args.doctor, args.check_input)) and (not args.input or not args.output or not args.qa_dir):
            raise Blocked("Supply --input, --output and a fresh --qa-dir, or use --self-test")
        if args.output and args.output.suffix.lower() != ".pdf":
            raise Blocked("Output must be PDF; use --also-docx only when requested")
        if args.qa_dir and args.qa_dir.exists():
            raise Blocked("QA directory must be fresh")
        targets = [args.output] if args.output else []
        if args.also_docx and args.output:
            targets.append(args.output.with_suffix(".docx"))
        if not args.overwrite and any(p.exists() for p in targets):
            raise Blocked("Output already exists; use --overwrite for an authorised revision")
        for target in targets:
            if any(source and target.resolve() == source.resolve() for source in (args.input, args.evidence)):
                raise Blocked("An output must not replace an input or evidence file")
            if args.qa_dir and target.resolve().is_relative_to(args.qa_dir.resolve()):
                raise Blocked("Keep released outputs outside the QA directory")
        fragments = None
        evidence = {"status": "not_provided"}
        if args.input:
            resume = read_json(args.input)
            fragments = input_fragments(resume)
            if args.evidence:
                evidence = check_evidence(resume, read_json(args.evidence))
        verify_sources()
        if args.check_input:
            print(json.dumps({"status": "valid_input", "full_text_fragments": len(fragments), "evidence_validation": evidence,
                              "factual_verification": "not_checked", "rendering": "not_checked", "output_released": False}, indent=2))
            return 0
        with tempfile.TemporaryDirectory(prefix="resume-verified-") as temporary:
            work = Path(temporary)
            env, version = environment(work)
            if args.doctor:
                print(json.dumps({"status": "ready_for_self_test", "converter": version, "docx_version": "9.6.1",
                                  "source_integrity": "passed", "reference_comparison": "not_checked", "output_released": False}, indent=2))
                return 0
            reference = self_test(work, env)
            report = {"status": "passed", "engine": "node", "docx_version": "9.6.1", "converter": version, "reference_comparison": reference, "visual_inspection": "not_checked", "factual_verification": "not_checked", "reading_order": "not_checked", "ats_validation": "not_checked"}
            if not args.self_test:
                folder = work / "candidate"
                # Render the validated snapshot, even if the original file changes mid-build.
                snapshot = work / "candidate.json"
                snapshot.write_text(json.dumps(resume, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                page_limit = args.target_pages or 1
                log = build(snapshot, folder, env, target_pages=page_limit)
                pages = check_content(folder / "Resume.pdf", fragments, folder, env, target_pages=page_limit)
                (folder / "build.txt").write_text(log)
                report.update({"output": str(args.output.resolve()), "qa_directory": str(args.qa_dir.resolve()), "full_text_fragments": len(fragments), "expected_font": "Carlito (Calibri requested by source)", "fit_style": json.loads((folder / "Resume.style_used.json").read_text()), "page_count": pages, "target_pages": page_limit, "input_sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(), "evidence_validation": evidence})
                shutil.copytree(folder, args.qa_dir)
                (args.qa_dir / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
                for target in targets:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    staged = work / ("release" + target.suffix)
                    shutil.copyfile(folder / ("Resume" + target.suffix), staged)
                    # Copy beside the final file before atomic replacement across filesystems.
                    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
                        pending = Path(stream.name)
                        stream.write(staged.read_bytes())
                    os.replace(pending, target)
                    released.append(str(target))
            print(json.dumps(report, indent=2))
        return 0
    except (Blocked, OSError, ValueError, subprocess.TimeoutExpired, zipfile.BadZipFile) as error:
        print(json.dumps({"status": "blocked", "reason": str(error), "output_released": bool(released), "released_files": released}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
