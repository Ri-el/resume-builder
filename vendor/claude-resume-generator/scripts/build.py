#!/usr/bin/env python3
"""
build.py - generate DOCX, convert to PDF, fit to the target page count, inspect.

  python3 scripts/build.py --input input/sample_resume.json --name Sample_Resume --outdir output
  python3 scripts/build.py --input my.json --name Jane_Doe --outdir out --variants both --photo assets/photo.jpg
  Options: --engine node|python (default: node if installed, else python)   --target-pages 1   --no-fit

PAGE FITTING (codified from what was done by hand; see docs/PAGE_FITTING.md). Font size is NEVER reduced.
Level 0 uses config/style.json unchanged. If the PDF has too many pages the next level is tried:
  L1 spacing x0.85 | L2 spacing x0.70 | L3 spacing x0.70 + top/bottom margin 0.45 in
  L4 spacing x0.60 + 0.40 in | L5 spacing x0.60 + 0.35 in (floor). If L5 still overflows: STOP, exit code 2,
  and ask the user which content to cut. Never delete content silently.
"""
import argparse, copy, json, os, re, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True); ap.add_argument("--name", required=True); ap.add_argument("--outdir", default="output")
ap.add_argument("--engine", choices=["node", "python"]); ap.add_argument("--variants", choices=["nophoto", "photo", "both"], default="nophoto")
ap.add_argument("--photo"); ap.add_argument("--target-pages", type=int, default=1); ap.add_argument("--no-fit", action="store_true")
ap.add_argument("--style", default=os.path.join(ROOT, "config", "style.json"))
A = ap.parse_args()
engine = A.engine or ("node" if shutil.which("node") and os.path.isdir(os.path.join(ROOT, "node_modules", "docx")) else "python")
soffice = shutil.which("soffice") or shutil.which("libreoffice")
if not soffice: sys.exit("LibreOffice not found (need `soffice` or `libreoffice` on PATH). Cannot make the PDF.")
if A.variants in ("photo", "both") and not A.photo: sys.exit("--photo is required for the photo variant (use scripts/prepare_photo.py first)")
os.makedirs(A.outdir, exist_ok=True); work = os.path.join(A.outdir, ".work"); os.makedirs(work, exist_ok=True)
base = json.load(open(A.style, encoding="utf-8"))
LADDER = [("L0 as approved", 1.0, None), ("L1 spacing x0.85", 0.85, None), ("L2 spacing x0.70", 0.70, None),
          ("L3 spacing x0.70, top/bottom 0.45in", 0.70, 0.45), ("L4 spacing x0.60, top/bottom 0.40in", 0.60, 0.40),
          ("L5 spacing x0.60, top/bottom 0.35in (floor)", 0.60, 0.35)]

def make_style(scale, tb):
    s = copy.deepcopy(base)
    for k, v in s["spacing_pt"].items(): s["spacing_pt"][k] = round(v * scale * 20) / 20 if v else v
    if tb: s["page"]["margin_top_in"] = s["page"]["margin_bottom_in"] = tb
    return s

def pages_of(pdf): return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True).stdout).group(1))

def build(name, photo):
    docx, pdf = os.path.join(A.outdir, name + ".docx"), os.path.join(A.outdir, name + ".pdf")
    for label, scale, tb in (LADDER[:1] if A.no_fit else LADDER):
        style_file = os.path.join(work, f"{name}.style.json"); json.dump(make_style(scale, tb), open(style_file, "w", encoding="utf-8"), indent=1)
        gen = ["node", os.path.join(ROOT, "generate.js")] if engine == "node" else [sys.executable, os.path.join(ROOT, "generate_py.py")]
        cmd = gen + ["--input", A.input, "--out", docx, "--style", style_file] + (["--photo", photo] if photo else [])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([soffice, "-env:UserInstallation=file:///tmp/lo_resume_profile", "--headless", "--convert-to", "pdf", "--outdir", A.outdir, docx],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        n = pages_of(pdf); print(f"[{name}] {label}: {n} page(s)")
        if n <= A.target_pages:
            shutil.copy(style_file, os.path.join(A.outdir, name + ".style_used.json")); return True, style_file
    return False, style_file

ok_all = True; inspect_failed = False
variants = [("nophoto", A.name, None)] if A.variants == "nophoto" else [("photo", A.name + "_Photo", A.photo)] if A.variants == "photo" else [("nophoto", A.name, None), ("photo", A.name + "_Photo", A.photo)]
for kind, name, photo in variants:
    ok, style_file = build(name, photo)
    if not ok:
        print(f"[{name}] STILL OVER {A.target_pages} PAGE(S) at the tightest allowed level. Not cutting content. Ask the user what to trim."); ok_all = False
    insp = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "inspect_pdf.py"), os.path.join(A.outdir, name + ".pdf"), "--input", A.input,
                           "--style", A.style, "--target-pages", str(A.target_pages), "--png-dir", A.outdir], capture_output=True, text=True)
    open(os.path.join(A.outdir, name + ".inspection.txt"), "w").write(f"engine={engine}\n" + insp.stdout); print(insp.stdout)
    if insp.returncode != 0: inspect_failed = True
shutil.rmtree(work, ignore_errors=True)
sys.exit(2 if not ok_all else 3 if inspect_failed else 0)   # 2 = does not fit, 3 = an inspection check FAILED
