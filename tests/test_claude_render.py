"""Protect the supplied renderer and reproduce its fictional reference output."""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "vendor" / "claude-resume-generator"


class UpstreamSnapshotTests(unittest.TestCase):
    def test_supplied_renderer_files_are_unchanged(self):
        manifest = json.loads((UPSTREAM / "UPSTREAM.json").read_text())
        for relative, digest in manifest["files"].items():
            with self.subTest(path=relative):
                self.assertEqual(hashlib.sha256((UPSTREAM / relative).read_bytes()).hexdigest(), digest)


@unittest.skipUnless(os.environ.get("RESUME_RUN_CLAUDE_TESTS") == "1", "Enable the real supplied-renderer tests explicitly")
class ClaudeRenderTests(unittest.TestCase):
    def run_command(self, *args):
        result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_node_reproduces_reference_docx_xml(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node with docx 9.6.1 is required")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "Sample_Resume.docx"
            self.run_command(node, str(UPSTREAM / "generate.js"), "--input",
                             str(UPSTREAM / "input/sample_resume.json"), "--out", str(output))
            with zipfile.ZipFile(UPSTREAM / "output/Sample_Resume.docx") as reference, zipfile.ZipFile(output) as candidate:
                for part in ("document", "numbering", "styles", "settings", "fontTable"):
                    with self.subTest(part=part):
                        name = f"word/{part}.xml"
                        self.assertEqual(reference.read(name), candidate.read(name))

    def test_pdf_matches_supplied_sample_in_reference_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_command(sys.executable, str(UPSTREAM / "scripts/build.py"),
                                      "--engine", "node", "--input", str(UPSTREAM / "input/sample_resume.json"),
                                      "--name", "Sample_Resume", "--outdir", tmp)
            self.assertIn("L0 as approved: 1 page(s)", result)
            self.assertIn("RESULT OK", result)
            report = self.run_command(sys.executable, str(UPSTREAM / "scripts/compare_pdfs.py"),
                                      str(UPSTREAM / "output/Sample_Resume.pdf"), str(Path(tmp) / "Sample_Resume.pdf"))
            self.assertIn("pages: 1 vs 1", report)
            self.assertIn("text identical: True", report,
                          "Use the reference Carlito version and LibreOffice; do not adjust the style to pass")
            shift = re.search(r"max word shift \(pt\): ([\d.]+)", report)
            pixels = re.search(r"differing pixels: .* = ([\d.]+)%", report)
            self.assertIsNotNone(shift, report)
            self.assertIsNotNone(pixels, report)
            self.assertLessEqual(float(shift[1]), 0.1, report)
            self.assertLessEqual(float(pixels[1]), 1.0, report)


if __name__ == "__main__":
    unittest.main()
