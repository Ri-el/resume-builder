#!/usr/bin/env python3
"""check_env.py - tell the user (or ChatGPT) exactly what is installed and what is missing before building."""
import os, shutil, subprocess, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def ver(*cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True).stdout.strip().splitlines()[0] or subprocess.run(cmd, capture_output=True, text=True).stderr.strip().splitlines()[0]
    except Exception: return None
rows = []
rows.append(("LibreOffice (soffice)", shutil.which("soffice") or shutil.which("libreoffice"), ver("soffice", "--version") if shutil.which("soffice") else None, True))
for t in ("pdfinfo", "pdffonts", "pdftotext", "pdftoppm"): rows.append((t + " (poppler-utils)", shutil.which(t), None, True))
rows.append(("Node.js", shutil.which("node"), ver("node", "-v") if shutil.which("node") else None, False))
rows.append(("node_modules/docx", os.path.isdir(os.path.join(root, "node_modules", "docx")) or None, "run: npm ci" if not os.path.isdir(os.path.join(root, "node_modules", "docx")) else None, False))
try:
    import docx; rows.append(("python-docx", "ok", getattr(docx, "__version__", "?"), False))
except ImportError: rows.append(("python-docx", None, "run: pip install -r requirements.txt", False))
try:
    import PIL; rows.append(("Pillow", "ok", PIL.__version__, False))
except ImportError: rows.append(("Pillow", None, "run: pip install -r requirements.txt", False))
fc = subprocess.run(["fc-list"], capture_output=True, text=True).stdout.lower() if shutil.which("fc-list") else ""
calibri, carlito = "calibri" in fc, "carlito" in fc
for name, path, v, required in rows:
    print(f"{'OK     ' if path else ('MISSING' if required else 'absent ')} {name:28s} {v or ''}")
print(f"{'OK     ' if calibri else 'absent '} Calibri font installed")
print(f"{'OK     ' if carlito else 'absent '} Carlito font installed (metric-compatible Calibri substitute)")
print()
if not (calibri or carlito): print("WARNING: neither Calibri nor Carlito is installed. LibreOffice will substitute another font and lines will break differently.\n         Linux fix: sudo apt-get install fonts-crosextra-carlito")
elif not calibri: print("NOTE: Calibri is not installed; PDFs will embed Carlito. This is what the approved PDF contains.")
print("Engine choice: " + ("node (exact original method)" if shutil.which("node") and os.path.isdir(os.path.join(root, "node_modules", "docx")) else "python (reconstructed port; verified pixel-identical on the approved resume)"))
