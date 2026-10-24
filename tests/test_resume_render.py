"""Opt-in real LibreOffice/Poppler tests, always using fictional candidate input."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts.build_resume import OverflowError, build

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get("RESUME_RUN_RENDER_TESTS") == "1", "Set RESUME_RUN_RENDER_TESTS=1 with LibreOffice, Poppler, Fontconfig, and Carlito installed")
class RenderTests(unittest.TestCase):
    def test_real_pdf_preserves_content_and_renders_all_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sample.pdf"
            qa = Path(directory) / "qa"
            report = build(ROOT / "examples/candidate.json", output, family="Carlito", qa_dir=qa)
            self.assertEqual(report["pages"], 1)
            self.assertTrue(output.is_file())
            self.assertFalse(output.with_suffix(".docx").exists(), "PDF-only must not publish an editable source")
            self.assertEqual(len(list(qa.glob("page-*.png"))), report["pages"])
            self.assertTrue(report["font"]["explicit_substitute"])
            self.assertEqual(report["checks"]["text_preservation"], "passed")
            self.assertEqual(report["checks"]["pdf_structure_tags"], "passed")
            self.assertEqual(report["checks"]["entry_grouping_by_extraction_mode"]["raw"], "passed")
            self.assertEqual(report["checks"]["entry_grouping_by_extraction_mode"]["layout"], "passed")
            self.assertTrue((qa / "text-raw.txt").exists())
            self.assertEqual(report["checks"]["visual_inspection"], "not_checked")
            self.assertEqual(report["checks"]["reading_order_review"], "not_checked")
            self.assertEqual(report["checks"]["factual_accuracy"], "not_checked")

    def test_real_overflow_never_deletes_content_or_shrinks_font(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = {
                "schema_version": 1, "name": "Sample Candidate",
                "experience": [{"title": "Stock Assistant", "company": "Fictional Retail Co.", "dates": "2022–2024",
                                "bullets": [f"Recorded fictional stock movement {index} in the campaign register." for index in range(85)]}],
            }
            source = root / "candidate.json"
            source.write_text(json.dumps(candidate), encoding="utf-8")
            original = source.read_bytes()
            with self.assertRaises(OverflowError):
                build(source, root / "blocked.pdf", family="Carlito")
            self.assertFalse((root / "blocked.pdf").exists())
            self.assertEqual(source.read_bytes(), original)
            qa = root / "qa"
            report = build(source, root / "allowed.docx", family="Carlito", allow_multiple_pages=True, qa_dir=qa)
            self.assertGreater(report["pages"], 1)
            self.assertEqual(report["checks"]["text_preservation"], "passed")
            self.assertEqual(len(list(qa.glob("page-*.png"))), report["pages"])
            from docx import Document
            document = Document(root / "allowed.docx")
            self.assertEqual(document.styles["Resume Bullet"].font.size.pt, 10)
            paragraphs = [p.text for p in document.paragraphs if p.style.name == "Resume Bullet"]
            self.assertEqual(paragraphs, candidate["experience"][0]["bullets"])


if __name__ == "__main__":
    unittest.main()
