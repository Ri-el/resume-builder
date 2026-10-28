"""Exercise source coverage, diagnostics and failure paths using fictional data."""

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from scripts import build_verified_resume as verified

FIXTURES = verified.ROOT / "evals/fixtures"


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.resume = verified.read_json(FIXTURES / "fictional_candidate.json")
        self.ledger = verified.read_json(FIXTURES / "fictional_evidence.json")

    def invoke(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = verified.main(list(args))
        return result, json.loads(output.getvalue())

    def test_complete_evidence_covers_candidate_text_without_claiming_truth(self):
        report = verified.check_evidence(self.resume, self.ledger)
        self.assertEqual(report["claims"], 7)
        self.assertEqual(report["status"], "passed")
        self.assertIn("factual truth requires review", report["scope"])
        self.assertNotIn("Fictional", json.dumps(report))

    def test_missing_stale_duplicate_and_unknown_claims_block(self):
        variants = []
        missing = copy.deepcopy(self.ledger)
        missing["claims"].pop()
        variants.append(missing)
        stale = copy.deepcopy(self.ledger)
        stale["claims"][-1]["value"] = "An unsupported achievement"
        variants.append(stale)
        duplicate = copy.deepcopy(self.ledger)
        duplicate["claims"].append(duplicate["claims"][0])
        variants.append(duplicate)
        unknown = copy.deepcopy(self.ledger)
        unknown["claims"][0]["path"] = "/sections/0/heading"
        variants.append(unknown)
        for ledger in variants:
            with self.subTest(ledger=ledger), self.assertRaises(verified.Blocked):
                verified.check_evidence(self.resume, ledger)

    def test_invalid_evidence_contracts_block_without_type_errors(self):
        mutations = [
            lambda x: x.update(schema_version=True),
            lambda x: x.update(schema_version=2),
            lambda x: x.update(sources=[]),
            lambda x: x.update(claims={}),
            lambda x: x["sources"].append(x["sources"][0]),
            lambda x: x["sources"][0].update(kind="job_description"),
            lambda x: x["sources"][0].update(id=[]),
            lambda x: x["claims"][0].update(source_ids=["missing"]),
            lambda x: x["claims"][0].update(source_ids=[{}]),
            lambda x: x["claims"][0].update(source_ids=["career-notes", "career-notes"]),
            lambda x: x["claims"][0].update(status="unresolved"),
            lambda x: x["claims"][0].update(status=[]),
            lambda x: x["claims"][0].update(note=""),
            lambda x: x["claims"][0].update(unsupported=True),
        ]
        for index, mutate in enumerate(mutations):
            ledger = copy.deepcopy(self.ledger)
            mutate(ledger)
            with self.subTest(index=index), self.assertRaises(verified.Blocked):
                verified.check_evidence(self.resume, ledger)

    def test_all_native_section_types_have_claim_paths(self):
        resume = verified.read_json(verified.UPSTREAM / "input/sample_resume.json")
        verified.input_fragments(resume)
        fields = dict(verified.claim_fields(resume))
        self.assertIn("/sections/0/text", fields)
        self.assertIn("/sections/1/items/0/title", fields)
        self.assertIn("/sections/3/items/0/items/0", fields)
        self.assertIn("/sections/4/items/0", fields)
        self.assertIn("/sections/5/items/0", fields)
        self.assertFalse(any(path.endswith(("/heading", "/type", "/label")) for path in fields))

    def test_input_check_needs_no_renderer_and_never_releases_files(self):
        with mock.patch.object(verified, "environment", side_effect=AssertionError("Must not run")):
            code, report = self.invoke("--check-input", "--input", str(FIXTURES / "fictional_candidate.json"),
                                       "--evidence", str(FIXTURES / "fictional_evidence.json"))
        self.assertEqual((code, report["status"]), (0, "valid_input"))
        self.assertEqual(report["evidence_validation"]["claims"], 7)
        self.assertEqual(report["factual_verification"], "not_checked")
        self.assertEqual(report["rendering"], "not_checked")
        self.assertFalse(report["output_released"])

    def test_legacy_input_without_ledger_is_explicitly_unassessed(self):
        code, report = self.invoke("--check-input", "--input", str(FIXTURES / "fictional_candidate.json"))
        self.assertEqual(code, 0)
        self.assertEqual(report["evidence_validation"]["status"], "not_provided")

    def test_duplicate_input_or_evidence_keys_block_before_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate.json"
            path.write_text('{"name":"First","name":"Second"}', encoding="utf-8")
            with mock.patch.object(verified, "environment", side_effect=AssertionError("Must not run")):
                for args in (("--check-input", "--input", str(path)),
                             ("--check-input", "--input", str(FIXTURES / "fictional_candidate.json"), "--evidence", str(path))):
                    code, report = self.invoke(*args)
                    self.assertEqual(code, 2)
                    self.assertIn("Duplicate JSON field", report["reason"])

    def test_doctor_checks_dependencies_but_does_not_run_reference(self):
        with mock.patch.object(verified, "environment", return_value=({}, "LibreOffice 24.2.7.2")), \
                mock.patch.object(verified, "self_test", side_effect=AssertionError("Must not render")):
            code, report = self.invoke("--doctor")
        self.assertEqual((code, report["status"]), (0, "ready_for_self_test"))
        self.assertEqual(report["reference_comparison"], "not_checked")
        self.assertFalse(report["output_released"])

    def test_diagnostic_modes_reject_ignored_options(self):
        for args in (("--self-test", "--input", "unused.json"),
                     ("--doctor", "--output", "unused.pdf"),
                     ("--doctor", "--target-pages", "2"),
                     ("--check-input", "--input", "unused.json", "--also-docx")):
            with self.subTest(args=args), mock.patch.object(verified, "environment", side_effect=AssertionError("Must not run")):
                code, report = self.invoke(*args)
                self.assertEqual(code, 2)
                self.assertFalse(report["output_released"])

    def test_page_maximum_is_forwarded_to_existing_builder(self):
        with mock.patch.object(verified, "run", return_value="") as run:
            verified.build(Path("input.json"), Path("output"), {}, target_pages=3)
        command = run.call_args.args[0]
        self.assertEqual(command[command.index("--target-pages") + 1], "3")

    def test_missing_fonts_over_limit_or_missing_page_images_block(self):
        fonts = "name type encoding emb sub uni object ID\n---\nAAAAAA+Carlito-Regular TrueType WinAnsi yes yes yes 1 0\n"
        for font_report, pages, images in (("name\n---\n", 1, 1), (fonts, 3, 3), (fonts, 2, 1)):
            with self.subTest(pages=pages, images=images), tempfile.TemporaryDirectory() as tmp:
                qa = Path(tmp)

                def run(command, **kwargs):
                    if command[0] == "pdftotext":
                        return "Candidate"
                    if command[0] == "pdffonts":
                        return font_report
                    if command[0] == "pdfinfo":
                        return f"Pages: {pages}\n"
                    if command[0] == "pdftoppm":
                        for index in range(images):
                            (qa / f"page-{index + 1}.png").write_bytes(b"image")
                        return ""
                    raise AssertionError(command)

                with mock.patch.object(verified, "run", side_effect=run), self.assertRaises(verified.Blocked):
                    verified.check_content(qa / "resume.pdf", ["Candidate"], qa, {}, target_pages=2)

    def test_build_uses_validated_snapshot_and_records_unperformed_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "candidate.json"
            source.write_text(json.dumps(self.resume), encoding="utf-8")

            def self_test(*args):
                source.write_text(json.dumps({"name": "Changed after validation"}), encoding="utf-8")
                return "reference passed"

            def build(input_path, folder, env, target_pages=1):
                self.assertNotEqual(input_path, source)
                self.assertEqual(verified.read_json(input_path), self.resume)
                self.assertEqual(target_pages, 2)
                folder.mkdir()
                (folder / "Resume.pdf").write_bytes(b"fictional mocked PDF")
                (folder / "Resume.style_used.json").write_text("{}")
                return "build passed"

            with mock.patch.object(verified, "environment", return_value=({}, "reference")), \
                    mock.patch.object(verified, "self_test", side_effect=self_test), \
                    mock.patch.object(verified, "build", side_effect=build), \
                    mock.patch.object(verified, "check_content", return_value=2):
                code, report = self.invoke("--input", str(source), "--output", str(root / "cv.pdf"),
                                           "--qa-dir", str(root / "qa"), "--target-pages", "2")
            self.assertEqual(code, 0)
            self.assertEqual(report["page_count"], 2)
            self.assertEqual(report["target_pages"], 2)
            self.assertEqual(len(report["input_sha256"]), 64)
            for key in ("visual_inspection", "factual_verification", "reading_order", "ats_validation"):
                self.assertEqual(report[key], "not_checked")


if __name__ == "__main__":
    unittest.main()
