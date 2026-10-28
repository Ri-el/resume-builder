#!/usr/bin/env python3
"""
inspect_pdf.py - the PDF inspection steps, automated.

  python3 scripts/inspect_pdf.py output/Sample_Resume.pdf --input input/sample_resume.json \
          [--style config/style.json] [--target-pages 1] [--png-dir output]

Checks (each prints PASS / WARN / FAIL; exit code 1 if any FAIL):
  1 page count and A4 size            4 every date sits on the same line as its title (no wrapped dates)
  2 fonts requested vs embedded       5 no section heading is the last line of a page (orphan heading)
  3 all input text is present         6 last page is not nearly empty
Also renders every page to PNG (pdftoppm WITHOUT -singlefile, so no page is skipped).
Needs poppler-utils (pdfinfo, pdffonts, pdftotext, pdftoppm).
"""
import argparse, json, os, re, subprocess, sys, unicodedata

ap = argparse.ArgumentParser()
ap.add_argument("pdf"); ap.add_argument("--input"); ap.add_argument("--style")
ap.add_argument("--target-pages", type=int, default=1); ap.add_argument("--png-dir")
A = ap.parse_args()
here = os.path.dirname(os.path.abspath(__file__))
style_path = A.style or os.path.join(here, "..", "config", "style.json")
requested = json.load(open(style_path, encoding="utf-8"))["font_requested"]

def run(*cmd): return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
def norm(t): return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", t)).strip()
results = []
def report(level, msg): results.append(level); print(f"{level:5s} {msg}")

# 1 pages and size
info = run("pdfinfo", A.pdf)
pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
w, h = map(float, re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info).groups())
report("PASS" if pages == A.target_pages else "FAIL", f"pages = {pages} (target {A.target_pages})")
report("PASS" if abs(w - 595.3) < 1.5 and abs(h - 841.9) < 1.5 else "FAIL", f"page size {w:.1f} x {h:.1f} pt (A4 = 595.3 x 841.9)")

# 2 fonts: requested vs embedded
fonts = [re.sub(r"^[A-Z]{6}\+", "", l.split()[0]) for l in run("pdffonts", A.pdf).splitlines()[2:] if l.strip()]
print(f"INFO  fonts requested in code : {requested}")
print(f"INFO  fonts embedded in PDF   : {', '.join(fonts)}")
if any(f.lower().startswith("calibri") for f in fonts):
    report("PASS", "Calibri itself is embedded")
elif any(f.lower().startswith("carlito") for f in fonts):
    report("WARN", "Calibri was requested but Carlito (metric-compatible substitute) is embedded. Expected on Linux; layout is unchanged. State this honestly.")
else:
    report("FAIL", "neither Calibri nor Carlito embedded: line breaks will differ from the approved look")
extra = [f for f in fonts if not f.lower().startswith(("calibri", "carlito"))]
if extra: print(f"INFO  other embedded fonts   : {', '.join(extra)} (in the approved PDF this is LiberationSerif and covers ONLY the bullet glyph)")

# text per page
page_text = [run("pdftotext", "-layout", "-f", str(i), "-l", str(i), A.pdf, "-") for i in range(1, pages + 1)]
all_text = norm(" ".join(page_text))

if A.input:
    R = json.load(open(A.input, encoding="utf-8"))
    # 3 content present
    wanted = [R["name"], R["headline"][0], R["contact"][0]]
    entries = []
    for s in R["sections"]:
        wanted.append(s["heading"].upper())
        if s["type"] == "paragraph": wanted.append(s["text"])
        elif s["type"] == "entries":
            for e in s["items"]:
                entries.append(e); wanted += [e["title"]] + ([e["sub"]] if e.get("sub") else []) + e.get("bullets", [])
        elif s["type"] == "skills": wanted += [x["label"] for x in s["items"]]
        elif s["type"] in ("bullets", "inline_list"): wanted += s["items"]
    missing = [t for t in wanted if norm(t)[:40] not in all_text or norm(t)[-25:] not in all_text]
    report("PASS" if not missing else "FAIL", "all input text present" if not missing else f"{len(missing)} text items missing or cut: {[m[:40] for m in missing[:3]]}")
    # 4 dates on the same line as the title
    bad = []
    lines = [norm(l) for t in page_text for l in t.splitlines()]
    for e in entries:
        if not e.get("dates"): continue
        hit = [l for l in lines if norm(e["dates"]) in l and norm(e["title"])[:20] in l]
        if not hit: bad.append(e["title"][:40])
    report("PASS" if not bad else "FAIL", "every date shares a line with its title" if not bad else f"date not on title line: {bad}")
    # 4b headline and contact items stay whole (a photo narrows the header column and can wrap them)
    hdr_lines = [norm(l) for l in page_text[0].splitlines()[:14]]
    split = [it for it in R["headline"] + R["contact"] if not any(norm(it) in l for l in hdr_lines)]
    report("PASS" if not split else "FAIL", "headline and contact items each sit on one line" if not split else f"header item wrapped across lines: {split}")
    # 5 orphan headings
    heads = {s["heading"].upper() for s in R["sections"]}
    orphans = []
    for i, t in enumerate(page_text, 1):
        ne = [norm(l) for l in t.splitlines() if l.strip()]
        if ne and ne[-1] in heads: orphans.append((i, ne[-1]))
    report("PASS" if not orphans else "FAIL", "no orphan section headings" if not orphans else f"heading is last line on page: {orphans}")

# 6 last page fill
if pages > 1:
    n = len([l for l in page_text[-1].splitlines() if l.strip()])
    report("PASS" if n >= 5 else "WARN", f"last page has {n} text lines")

# render every page
if A.png_dir:
    os.makedirs(A.png_dir, exist_ok=True)
    prefix = os.path.join(A.png_dir, os.path.splitext(os.path.basename(A.pdf))[0] + "_page")
    subprocess.run(["pdftoppm", "-png", "-r", "100", A.pdf, prefix], check=True)
    print("INFO  rendered pages:", ", ".join(sorted(f for f in os.listdir(A.png_dir) if f.startswith(os.path.basename(prefix)))))
print("RESULT", "FAIL" if "FAIL" in results else "OK")
sys.exit(1 if "FAIL" in results else 0)
