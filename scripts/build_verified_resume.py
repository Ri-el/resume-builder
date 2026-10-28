#!/usr/bin/env python3
"""Run the supplied Claude method or stop; never silently substitute a renderer."""

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


def build(input_path, destination, env):
    return run([sys.executable, str(UPSTREAM / "scripts/build.py"), "--engine", "node", "--input", str(input_path), "--name", "Resume", "--outdir", str(destination)], env=env)


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


def check_content(pdf, fragments, qa, env):
    expected = collections.Counter(re.findall(r"\w+", norm(" ".join(fragments)).casefold()))
    for name, flags in (("plain", []), ("layout", ["-layout"]), ("raw", ["-raw"])):
        value = run(["pdftotext", *flags, str(pdf), "-"], env=env)
        (qa / (name + ".txt")).write_text(value)
        actual = collections.Counter(re.findall(r"\w+", norm(value).casefold()))
        if any(norm(fragment) not in norm(value) for fragment in fragments) or expected - actual:
            raise Blocked("Complete text preservation failed in " + name + " extraction")
    fonts = run(["pdffonts", str(pdf)], env=env)
    (qa / "fonts.txt").write_text(fonts)
    for line in fonts.splitlines()[2:]:
        name = re.sub(r"^[A-Z]{6}\+", "", line.split()[0])
        flags = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line)
        if not name.startswith(("Carlito", "LiberationSerif")) or not flags or flags[1] != "yes":
            raise Blocked("Unexpected or unembedded PDF font: " + name)
    run(["pdftoppm", "-png", "-r", "150", str(pdf), str(qa / "page")], env=env)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--qa-dir", type=Path)
    parser.add_argument("--also-docx", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    released = []
    try:
        if not args.self_test and (not args.input or not args.output or not args.qa_dir):
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
        fragments = None
        if args.input:
            fragments = input_fragments(json.loads(args.input.read_text(), object_pairs_hook=no_duplicates))
        verify_sources()
        with tempfile.TemporaryDirectory(prefix="resume-verified-") as temporary:
            work = Path(temporary)
            env, version = environment(work)
            reference = self_test(work, env)
            report = {"status": "passed", "engine": "node", "docx_version": "9.6.1", "converter": version, "reference_comparison": reference, "visual_inspection": "not_checked"}
            if not args.self_test:
                folder = work / "candidate"
                log = build(args.input.resolve(), folder, env)
                check_content(folder / "Resume.pdf", fragments, folder, env)
                (folder / "build.txt").write_text(log)
                report.update({"output": str(args.output.resolve()), "qa_directory": str(args.qa_dir.resolve()), "full_text_fragments": len(fragments), "expected_font": "Carlito (Calibri requested by source)", "fit_style": json.loads((folder / "Resume.style_used.json").read_text())})
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
