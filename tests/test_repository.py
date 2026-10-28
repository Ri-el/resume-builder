"""Keep the skill loadable and its bundled resources discoverable."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_skill_frontmatter_and_size(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
        self.assertIsNotNone(frontmatter, "Skill must start with YAML frontmatter")
        fields = dict(line.split(": ", 1) for line in frontmatter[1].splitlines())
        self.assertEqual(set(fields), {"name", "description"})
        self.assertRegex(fields["name"], r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
        self.assertLessEqual(len(fields["name"]), 64)
        self.assertTrue(fields["description"].strip())
        self.assertLessEqual(len(fields["description"]), 1024)
        self.assertLess(len(skill.splitlines()), 500)

    def test_local_markdown_links_resolve(self):
        for filename in ("README.md", "SKILL.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                with self.subTest(filename=filename, target=target):
                    path = (ROOT / target.split("#", 1)[0]).resolve()
                    self.assertTrue(path.is_relative_to(ROOT))
                    self.assertTrue(path.is_file(), f"Missing linked resource: {target}")

    def test_ui_metadata_matches_skill(self):
        lines = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "interface:")
        fields = {}
        for line in lines[1:]:
            key, value = line.strip().split(": ", 1)
            fields[key] = json.loads(value)
        self.assertEqual(fields["display_name"], "Resume Builder")
        self.assertTrue(25 <= len(fields["short_description"]) <= 64)
        self.assertIn("$resume-builder", fields["default_prompt"])

    def test_behavioral_cases_have_unique_ids_and_assessable_criteria(self):
        evaluations = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        cases = evaluations["cases"]
        self.assertTrue(cases)
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                self.assertTrue(case["criteria"])
                self.assertTrue(all(isinstance(item, str) and item.strip() for item in case["criteria"]))


if __name__ == "__main__":
    unittest.main()
