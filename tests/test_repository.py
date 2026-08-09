import re
import unittest
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "building-chatgpt-plugins"


class PublicationFilesTests(unittest.TestCase):
    def test_required_publication_files_exist(self):
        for name in (
            "README.md",
            "LICENSE",
            "NOTICE.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
        ):
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).is_file(), name)

    def test_readme_states_independent_skills_only_scope(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("skills-only", readme.lower())
        self.assertIn("not affiliated with or endorsed by OpenAI", readme)
        self.assertIn("MCP", readme)
        self.assertIn("OAuth", readme)
        self.assertIn("custom UI", readme)

    def test_mit_license_and_notice_identify_owner(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 MerverliPy", license_text)
        self.assertIn("Copyright (c) 2026 MerverliPy", notice)
        self.assertIn("independent community project", notice.lower())

    def test_guided_build_is_the_selected_official_icon(self):
        official = SKILL / "assets" / "icon.svg"
        selected = ROOT / "icon-options" / "icon-a-guided-build.svg"
        self.assertEqual(official.read_bytes(), selected.read_bytes())
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Guided Build is the selected official icon", readme)
        self.assertNotIn("awaiting owner selection", readme.lower())

    def test_public_release_documents_record_v0_1_0_as_published(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        checklist = (ROOT / "RELEASE_CHECKLIST.md").read_text(encoding="utf-8")

        self.assertIn("`v0.1.0` is the first public release", readme)
        self.assertNotIn("Publication has not been performed", readme)
        self.assertIn("## [0.1.0] - 2026-08-09", changelog)
        self.assertNotIn("## [0.1.0] - Unreleased", changelog)
        self.assertIn(
            "- [x] GitHub repository visibility and publication are explicitly approved.",
            checklist,
        )


class SkillBoundaryRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        cls.checklist_text = (
            SKILL / "references" / "plugin-workflow-checklist.md"
        ).read_text(encoding="utf-8")

    def test_guided_creation_remains_primary(self):
        self.assertIn("## Primary purpose: guided creation", self.skill_text)
        self.assertIn("one focused question at a time", self.skill_text)

    def test_capabilities_require_selected_plugin_evidence(self):
        self.assertIn("Every skill, MCP server, OAuth flow, UI", self.skill_text)
        self.assertIn("Add MCP only for demonstrated live data", self.skill_text)
        self.assertIn("OAuth only for demonstrated identity", self.skill_text)
        self.assertIn("UI only for demonstrated visual interaction", self.skill_text)

    def test_benchmark_and_repairs_remain_secondary_and_bounded(self):
        self.assertIn("## Secondary support", self.skill_text)
        self.assertIn("Do not create standalone infrastructure", self.skill_text)
        self.assertIn("Never apply without explicit approval", self.skill_text)
        self.assertIn(
            "Do not replace the selected plugin with a reusable benchmark product",
            self.checklist_text,
        )

    def test_required_skill_paths_resolve(self):
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file())
        self.assertTrue((SKILL / "assets" / "icon.svg").is_file())
        self.assertTrue(
            (SKILL / "references" / "plugin-workflow-checklist.md").is_file()
        )


class IconCandidateTests(unittest.TestCase):
    def test_at_least_two_safe_original_svg_candidates_exist(self):
        candidates = sorted((ROOT / "icon-options").glob("*.svg"))
        self.assertGreaterEqual(len(candidates), 2)
        for candidate in candidates:
            with self.subTest(candidate=candidate.name):
                text = candidate.read_text(encoding="utf-8")
                root = ElementTree.fromstring(text)
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertRegex(text, r'viewBox="0 0 64 64"')
                content_without_namespace = text.replace(
                    'xmlns="http://www.w3.org/2000/svg"', ""
                )
                self.assertNotRegex(
                    content_without_namespace,
                    re.compile(r"<script|javascript:|https?://|xlink:href|data:", re.I),
                )


if __name__ == "__main__":
    unittest.main()
