#!/usr/bin/env python3
"""
compare_pdfs.py - compare two resume PDFs (for example your output against output/Sample_Resume.pdf).
  python3 scripts/compare_pdfs.py reference.pdf candidate.pdf
Reports: page counts, whether pdftotext -layout output is identical, the largest word-position shift in points
(pdftotext -bbox), and the percentage of pixels that differ at 100 dpi. Needs poppler-utils and Pillow.
Rule of thumb from the evidence: identical text + max shift under 0.1 pt + under 1% differing pixels = same look.
"""
import re, subprocess, sys, tempfile, os
from PIL import Image, ImageChops
a, b = sys.argv[1], sys.argv[2]
def out(*c): return subprocess.run(c, capture_output=True, text=True, check=True).stdout
def pages(p): return int(re.search(r"Pages:\s+(\d+)", out("pdfinfo", p)).group(1))
def words(p):
    t = out("pdftotext", "-bbox", p, "-")
    return re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="[\d.]+" yMax="[\d.]+">(.*?)</word>', t)
pa, pb = pages(a), pages(b); print(f"pages: {pa} vs {pb}")
print("text identical:", out("pdftotext", "-layout", a, "-") == out("pdftotext", "-layout", b, "-"))
wa, wb = words(a), words(b)
if len(wa) == len(wb):
    print("max word shift (pt):", round(max(max(abs(float(x[0]) - float(y[0])), abs(float(x[1]) - float(y[1]))) for x, y in zip(wa, wb)), 2))
else: print(f"word counts differ: {len(wa)} vs {len(wb)}")
tmp = tempfile.mkdtemp()
tot = bad = 0
for i in range(1, min(pa, pb) + 1):
    for p, n in ((a, "a"), (b, "b")): subprocess.run(["pdftoppm", "-png", "-r", "100", "-f", str(i), "-l", str(i), "-singlefile", p, f"{tmp}/{n}{i}"], check=True)
    ia, ib = Image.open(f"{tmp}/a{i}.png").convert("L"), Image.open(f"{tmp}/b{i}.png").convert("L")
    d = ImageChops.difference(ia, ib).point(lambda v: 255 if v > 40 else 0)
    bad += sum(1 for v in d.tobytes() if v); tot += ia.size[0] * ia.size[1]
print(f"differing pixels: {bad} of {tot} = {100 * bad / tot:.3f}%")
