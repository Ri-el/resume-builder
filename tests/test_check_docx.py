"""Generate synthetic OOXML fixtures in temporary directories; no candidate data."""

import contextlib
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts import check_docx as checker

URI = checker.NS["w"]
A4 = '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/></w:sectPr>'
TEXT = '<w:p><w:r><w:t>Entirely fictional sample content</w:t></w:r></w:p>'
STYLES = (
    f'<w:styles xmlns:w="{URI}"><w:docDefaults><w:rPrDefault>'
    '<w:rPr><w:sz w:val="20"/></w:rPr></w:rPrDefault></w:docDefaults></w:styles>'
)
SCRIPT = Path(checker.__file__).resolve()


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "sample.docx"

    def make_docx(self, body=TEXT, section=A4, styles=STYLES, extra=None):
        document = f'<w:document xmlns:w="{URI}"><w:body>{body}{section}</w:body></w:document>'
        with zipfile.ZipFile(self.path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("word/document.xml", document)
            if styles is not None:
                archive.writestr("word/styles.xml", styles)
            for name, data in (extra or {}).items():
                archive.writestr(name, data)
        return self.path

    def codes(self, **kwargs):
        return {f["code"] for f in checker.check_docx(self.make_docx(**kwargs))["findings"]}

    def invoke(self, *args):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.path), "--json", *args],
            text=True, capture_output=True, check=False, cwd=self.temporary.name,
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_clean_a4_passes_without_changing_input_or_leaking_text(self):
        self.make_docx()
        original = self.path.read_bytes()
        report = checker.check_docx(self.path)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["findings"], [])
        self.assertNotIn("fictional", json.dumps(report))
        self.assertNotIn(str(self.path), json.dumps(report))
        self.assertEqual(hashlib.sha256(original).digest(), hashlib.sha256(self.path.read_bytes()).digest())

    def test_all_sections_are_checked(self):
        letter = '<w:p><w:pPr><w:sectPr><w:pgSz w:w="12240" w:h="15840"/></w:sectPr></w:pPr></w:p>'
        self.assertIn("NON_A4_PAGE", self.codes(body=letter + TEXT))

    def test_missing_and_invalid_page_dimensions_need_review(self):
        for section in ("", "<w:sectPr/>", '<w:sectPr><w:pgSz w:w="bad" w:h="0"/></w:sectPr>'):
            with self.subTest(section=section):
                self.assertIn("PAGE_SIZE_UNKNOWN", self.codes(section=section))

    def test_a4_rounding_is_tolerated_but_landscape_is_reviewed(self):
        rounded = '<w:sectPr><w:pgSz w:w="11907" w:h="16839"/></w:sectPr>'
        landscape = '<w:sectPr><w:pgSz w:w="16838" w:h="11906"/></w:sectPr>'
        self.assertNotIn("NON_A4_PAGE", self.codes(section=rounded))
        self.assertIn("NON_A4_PAGE", self.codes(section=landscape))

    def test_columns_by_count_or_explicit_widths(self):
        for columns in ('<w:cols w:num="2"/>', '<w:cols><w:col w:w="3000"/><w:col w:w="3000"/></w:cols>'):
            with self.subTest(columns=columns):
                self.assertIn("MULTIPLE_COLUMNS", self.codes(section=A4.replace("</w:sectPr>", columns + "</w:sectPr>")))

    def test_invalid_columns_do_not_crash(self):
        section = A4.replace("</w:sectPr>", '<w:cols w:num="invalid"/></w:sectPr>')
        self.assertIn("COLUMN_COUNT_UNKNOWN", self.codes(section=section))

    def test_tables_text_boxes_and_drawings_need_review(self):
        body = '<w:tbl><w:tr><w:tc>' + TEXT + '</w:tc></w:tr></w:tbl>'
        body += '<w:p><w:r><w:pict><w:txbxContent>' + TEXT + '</w:txbxContent></w:pict></w:r></w:p>'
        self.assertTrue({"TABLE_CONTENT", "TEXT_BOX", "DRAWING"} <= self.codes(body=body))

    def test_header_and_footer_text_need_review(self):
        for kind in ("header", "footer"):
            with self.subTest(kind=kind):
                part = f'<w:hdr xmlns:w="{URI}">{TEXT}</w:hdr>'
                self.assertIn("HEADER_FOOTER_TEXT", self.codes(extra={f"word/{kind}1.xml": part}))

    def test_empty_header_does_not_trigger_review(self):
        self.assertNotIn("HEADER_FOOTER_TEXT", self.codes(extra={"word/header1.xml": f'<w:hdr xmlns:w="{URI}"/>'}))

    def test_pending_edits_fail_in_body_and_footer(self):
        for tag in ("ins", "del", "moveFrom", "moveTo", "rPrChange"):
            with self.subTest(tag=tag):
                self.make_docx(body=TEXT + f'<w:{tag}/>')
                self.assertEqual(checker.check_docx(self.path)["status"], "fail")
        footer = f'<w:ftr xmlns:w="{URI}"><w:del/></w:ftr>'
        self.assertIn("TRACKED_CHANGES", self.codes(extra={"word/footer1.xml": footer}))

    def test_no_text_or_image_only_body_fails(self):
        for body in ("", '<w:p><w:r><w:drawing/></w:r></w:p>'):
            with self.subTest(body=body):
                self.assertIn("NO_BODY_TEXT", self.codes(body=body))
                self.assertEqual(checker.check_docx(self.path)["status"], "fail")

    def test_hidden_and_small_text_are_reviewed_once(self):
        run = '<w:r><w:rPr><w:vanish/><w:sz w:val="16"/></w:rPr><w:t>Sample</w:t></w:r>'
        report = checker.check_docx(self.make_docx(body='<w:p>' + run * 3 + '</w:p>'))
        self.assertEqual([f["code"] for f in report["findings"]].count("HIDDEN_TEXT"), 1)
        self.assertEqual([f["code"] for f in report["findings"]].count("SMALL_TEXT"), 1)

    def test_false_visibility_flags_are_not_treated_as_hidden(self):
        for value in ("false", "0", "off"):
            with self.subTest(value=value):
                body = f'<w:p><w:r><w:rPr><w:vanish w:val="{value}"/><w:webHidden w:val="{value}"/></w:rPr><w:t>Sample</w:t></w:r></w:p>'
                self.assertNotIn("HIDDEN_TEXT", self.codes(body=body))

    def test_paragraph_and_character_style_inheritance(self):
        styles = STYLES.replace('</w:styles>', (
            '<w:style w:type="paragraph" w:styleId="Base"><w:rPr><w:sz w:val="16"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Child"><w:basedOn w:val="Base"/></w:style>'
            '<w:style w:type="character" w:styleId="Secret"><w:rPr><w:vanish/></w:rPr></w:style></w:styles>'
        ))
        body = '<w:p><w:pPr><w:pStyle w:val="Child"/></w:pPr><w:r><w:rPr><w:rStyle w:val="Secret"/></w:rPr><w:t>Sample</w:t></w:r></w:p>'
        self.assertTrue({"SMALL_TEXT", "HIDDEN_TEXT"} <= self.codes(body=body, styles=styles))

    def test_default_paragraph_style_and_direct_overrides(self):
        styles = STYLES.replace('</w:styles>', '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:rPr><w:sz w:val="16"/><w:vanish/></w:rPr></w:style></w:styles>')
        self.assertTrue({"SMALL_TEXT", "HIDDEN_TEXT"} <= self.codes(styles=styles))
        body = '<w:p><w:r><w:rPr><w:sz w:val="20"/><w:vanish w:val="0"/></w:rPr><w:t>Sample</w:t></w:r></w:p>'
        self.assertEqual(self.codes(body=body, styles=styles), {"STYLE_VISIBILITY"})

    def test_cyclic_styles_terminate(self):
        styles = STYLES.replace('</w:styles>', '<w:style w:styleId="A"><w:basedOn w:val="B"/></w:style><w:style w:styleId="B"><w:basedOn w:val="A"/></w:style></w:styles>')
        body = TEXT.replace('<w:p>', '<w:p><w:pPr><w:pStyle w:val="A"/></w:pPr>')
        self.assertEqual(self.codes(body=body, styles=styles), set())

    def test_style_visibility_toggles_cannot_silently_pass(self):
        styles = STYLES.replace('</w:styles>', '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:rPr><w:vanish w:val="0"/></w:rPr></w:style></w:styles>')
        self.assertIn("STYLE_VISIBILITY", self.codes(styles=styles))

    def test_nested_textbox_uses_its_own_paragraph_style(self):
        styles = STYLES.replace('</w:styles>', '<w:style w:styleId="Small"><w:rPr><w:sz w:val="16"/></w:rPr></w:style></w:styles>')
        body = '<w:p><w:pPr><w:pStyle w:val="Small"/></w:pPr><w:r><w:pict><w:txbxContent>' + TEXT + '</w:txbxContent></w:pict></w:r></w:p>'
        self.assertNotIn("SMALL_TEXT", self.codes(body=body, styles=styles))

    def test_external_content_requires_review(self):
        self.assertIn("EXTERNAL_CONTENT", self.codes(body=TEXT + '<w:altChunk/>'))

    def test_unknown_or_invalid_font_size_is_not_a_pass(self):
        self.assertIn("FONT_SIZE_UNKNOWN", self.codes(styles=None))
        for value in ("bad", "0", "NaN", "inf", "-20"):
            with self.subTest(value=value):
                self.assertIn("FONT_SIZE_UNKNOWN", self.codes(styles=STYLES.replace('w:val="20"', f'w:val="{value}"')))

    def test_cli_exit_codes_and_json_contract(self):
        for body, code, status in ((TEXT, 0, "pass"), (TEXT + '<w:tbl/>', 1, "review"), (TEXT + '<w:ins/>', 1, "fail")):
            with self.subTest(status=status):
                self.make_docx(body=body)
                exit_code, report = self.invoke()
                self.assertEqual((exit_code, report["status"]), (code, status))
                self.assertEqual(report["schema_version"], 1)
                self.assertIn("not checked", report["limitations"])

    def test_cli_handles_missing_corrupt_or_non_docx_without_tracebacks(self):
        self.assertEqual(self.invoke()[0], 2)
        self.path.write_bytes(b"Not a ZIP file")
        self.assertEqual(self.invoke()[0], 2)
        self.path = self.path.with_suffix(".pdf")
        self.path.write_bytes(b"Not a DOCX")
        self.assertEqual(self.invoke()[0], 2)

    def test_missing_document_invalid_xml_and_wrong_root_are_rejected(self):
        for name, xml in (("unrelated.xml", "<x/>"), ("word/document.xml", "broken"), ("word/document.xml", "<x/>")):
            with self.subTest(xml=xml):
                with zipfile.ZipFile(self.path, "w") as archive:
                    archive.writestr(name, xml)
                self.assertEqual(self.invoke()[0], 2)

    def test_duplicate_zip_parts_are_rejected(self):
        self.make_docx()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.path, "a") as archive:
                archive.writestr("word/document.xml", "<x/>")
        self.assertEqual(self.invoke()[0], 2)

    def test_unsupported_compression_is_rejected(self):
        with zipfile.ZipFile(self.path, "w", zipfile.ZIP_BZIP2) as archive:
            archive.writestr("word/document.xml", f'<w:document xmlns:w="{URI}"><w:body/></w:document>')
        self.assertEqual(self.invoke()[0], 2)

    def test_corrupt_deflate_stream_does_not_raise_a_traceback(self):
        self.make_docx()
        with zipfile.ZipFile(self.path) as archive:
            info = archive.getinfo("word/document.xml")
        data = bytearray(self.path.read_bytes())
        offset = info.header_offset + 30
        name_length = int.from_bytes(data[info.header_offset + 26:info.header_offset + 28], "little")
        extra_length = int.from_bytes(data[info.header_offset + 28:info.header_offset + 30], "little")
        data[offset + name_length + extra_length] = 0xFF
        self.path.write_bytes(data)
        self.assertEqual(self.invoke()[0], 2)

    def test_resource_limits_are_enforced_before_parsing(self):
        self.make_docx()
        for constant in ("MAX_ARCHIVE_BYTES", "MAX_EXPANDED_BYTES", "MAX_XML_BYTES", "MAX_ENTRIES"):
            with self.subTest(constant=constant), patch.object(checker, constant, 1):
                with self.assertRaises(checker.InvalidDocument):
                    checker.check_docx(self.path)

    def test_xml_declarations_are_rejected_in_utf8_and_utf16(self):
        xml = f'<!DOCTYPE w:document [<!ENTITY text "sample">]><w:document xmlns:w="{URI}"><w:body/></w:document>'
        for encoding in ("utf-8", "utf-16"):
            with self.subTest(encoding=encoding):
                with zipfile.ZipFile(self.path, "w") as archive:
                    archive.writestr("word/document.xml", xml.encode(encoding))
                self.assertEqual(self.invoke()[0], 2)

    def test_human_output_includes_scope_limitation(self):
        self.make_docx()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(checker.main([str(self.path)]), 0)
        self.assertIn("DOCX preflight: PASS", output.getvalue())
        self.assertIn("ATS behavior were not checked", output.getvalue())


if __name__ == "__main__":
    unittest.main()
