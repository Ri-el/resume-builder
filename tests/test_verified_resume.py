"""The locked entry point must reject substitutions and incomplete preservation."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verified", ROOT / "scripts/build_verified_resume.py")
verified = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verified)


class VerifiedTests(unittest.TestCase):
    def test_all_native_input_fields_are_preserved_and_unsupported_fields_block(self):
        source = json.loads((verified.UPSTREAM / "input/sample_resume.json").read_text())
        self.assertEqual(len(verified.input_fragments(source)), 56)
        source["hidden_extra_experience"] = "An unsupported field must not disappear"
        with self.assertRaises(verified.Blocked):
            verified.input_fragments(source)

    def test_rounded_percentage_cannot_hide_differing_pixels(self):
        prefix = "pages: 1 vs 1\ntext identical: True\nmax word shift (pt): 0.0\n"
        verified.compare_report(prefix + "differing pixels: 0 of 967590 = 0.000%")
        with self.assertRaises(verified.Blocked):
            verified.compare_report(prefix + "differing pixels: 1 of 967590 = 0.000%")
        with self.assertRaises(verified.Blocked):
            verified.compare_report(prefix.replace("True", "False") + "differing pixels: 0 of 967590 = 0.000%")

    def test_blocked_environment_publishes_no_candidate_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "candidate.pdf"
            qa = Path(tmp) / "qa"
            log = io.StringIO()
            with mock.patch.object(verified, "environment", side_effect=verified.Blocked("Reference converter unavailable")), contextlib.redirect_stdout(log):
                code = verified.main(["--input", str(verified.UPSTREAM / "input/sample_resume.json"), "--output", str(output), "--qa-dir", str(qa)])
            self.assertEqual(code, 2)
            self.assertFalse(output.exists())
            self.assertFalse(qa.exists())
            self.assertFalse(json.loads(log.getvalue())["output_released"])

    def test_missing_repeated_text_cannot_pass_preservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(verified, "run", return_value="Excel"), self.assertRaises(verified.Blocked):
                verified.check_content(Path("example.pdf"), ["Excel", "Excel"], Path(tmp), {})


@unittest.skipUnless(os.environ.get("RESUME_RUN_CLAUDE_TESTS") == "1", "Requires the reference renderer environment")
class VerifiedRenderTests(unittest.TestCase):
    def test_requested_two_page_cv_uses_original_style_and_preserves_all_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "academic.json"
            ledger = Path(tmp) / "evidence.json"
            resume = {
                "name": "Alex Morgan",
                "headline": ["Teaching and Research"],
                "contact": ["alex.morgan@example.com"],
                "sections": [
                    {"heading": "Education", "type": "entries", "items": [
                        {"title": "PhD in Education", "dates": "2024", "sub": "Fictional University"}
                    ]},
                    {"heading": "Teaching Experience", "type": "entries", "items": [
                        {"title": "Tutor", "dates": "2022 – 2024", "sub": "Fictional University",
                         "bullets": ["Taught introductory research methods seminars"]}
                    ]},
                    {"heading": "Publications", "type": "bullets", "items": [
                        f"Morgan, A., and Shah, P. (2024). Teaching introductory research methods through collaborative seminar activities: fictional study {index}. Fictional Journal of Education, 10({index}), 101–120."
                        for index in range(1, 31)
                    ]}
                ]
            }
            source.write_text(json.dumps(resume), encoding="utf-8")
            ledger.write_text(json.dumps({
                "schema_version": 1,
                "sources": [{"id": "fictional-fixture", "kind": "document", "label": "Entirely fictional integration fixture"}],
                "claims": [{"path": path, "value": value, "source_ids": ["fictional-fixture"], "status": "candidate_reported"}
                           for path, value in verified.claim_fields(resume)]
            }), encoding="utf-8")
            output = Path(tmp) / "cv.pdf"
            qa = Path(tmp) / "qa"
            log = io.StringIO()
            with contextlib.redirect_stdout(log):
                code = verified.main(["--input", str(source), "--evidence", str(ledger),
                                      "--output", str(output), "--qa-dir", str(qa),
                                      "--target-pages", "2", "--also-docx"])
            self.assertEqual(code, 0, log.getvalue())
            report = json.loads(log.getvalue())
            self.assertEqual(report["page_count"], 2)
            self.assertEqual(report["target_pages"], 2)
            self.assertIn("L0 as approved: 2 page(s)", (qa / "build.txt").read_text())
            self.assertTrue(output.with_suffix(".docx").is_file())
            self.assertEqual(len(list(qa.glob("page-*.png"))), 2)
            self.assertEqual(report["reading_order"], "not_checked")
            self.assertEqual(report["evidence_validation"]["status"], "passed")

    def test_two_page_limit_does_not_bypass_orphan_heading_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "cv.pdf"
            qa = Path(tmp) / "qa"
            log = io.StringIO()
            # This fixture fits at L1 for one page, but L0 strands LANGUAGES.
            with contextlib.redirect_stdout(log):
                code = verified.main(["--input", str(verified.UPSTREAM / "input/sample_dense.json"),
                                      "--output", str(output), "--qa-dir", str(qa),
                                      "--target-pages", "2"])
            self.assertEqual(code, 2, log.getvalue())
            report = json.loads(log.getvalue())
            self.assertIn("heading is last line on page", report["reason"])
            self.assertFalse(report["output_released"])
            self.assertFalse(output.exists())
            self.assertFalse(qa.exists())

    def test_verified_entry_point_reproduces_and_checks_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "candidate.pdf"
            qa = Path(tmp) / "qa"
            log = io.StringIO()
            with contextlib.redirect_stdout(log):
                code = verified.main(["--input", str(verified.UPSTREAM / "input/sample_resume.json"), "--output", str(output), "--qa-dir", str(qa)])
            self.assertEqual(code, 0, log.getvalue())
            report = json.loads(log.getvalue())
            self.assertTrue(output.exists())
            self.assertEqual(report["engine"], "node")
            self.assertEqual(report["full_text_fragments"], 56)
            self.assertEqual(report["visual_inspection"], "not_checked")
            self.assertTrue((qa / "page-1.png").exists())
            self.assertFalse(output.with_suffix(".docx").exists())


if __name__ == "__main__":
    unittest.main()
