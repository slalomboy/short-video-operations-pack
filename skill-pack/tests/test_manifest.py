import json
import re
import subprocess
import unittest
from pathlib import Path


PACK_ROOT = Path(__file__).resolve().parents[1]
PACK_VERSION = "0.1.0-alpha.5"
EXPECTED_SKILLS = {
    "short-video-operations",
    "short-video-positioning",
    "short-video-audience-insight",
    "short-video-material-library",
    "short-video-topic-planning",
    "short-video-script-strategy",
    "short-video-evidence-planning",
    "short-video-shot-planning",
    "short-video-content-review",
    "short-video-publish-experiment",
    "short-video-paid-growth",
    "short-video-live-conversion",
    "short-video-performance-review",
}


class ManifestTests(unittest.TestCase):
    def setUp(self):
        manifest_path = PACK_ROOT / "pack.json"
        self.assertTrue(manifest_path.exists(), "pack.json must exist")
        self.manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    def test_manifest_inventory_and_boundaries(self):
        self.assertEqual(self.manifest["version"], PACK_VERSION)
        skills = self.manifest["skills"]
        names = {item["name"] for item in skills}
        self.assertEqual(len(skills), 13)
        self.assertEqual(names, EXPECTED_SKILLS)
        self.assertEqual(sum(item["role"] == "orchestrator" for item in skills), 1)
        self.assertEqual(sum(item["role"] == "specialist" for item in skills), 12)
        self.assertFalse(self.manifest["global_installed"])
        self.assertEqual(self.manifest["runtime_entrypoints"]["mode"], "flat-wrappers")
        self.assertEqual(self.manifest["runtime_entrypoints"]["skills"], 13)
        self.assertTrue((PACK_ROOT / self.manifest["runtime_entrypoints"]["installer"]).exists())
        self.assertEqual(
            set(self.manifest["downstream_dependencies"]),
            {"content-voiceover-copywriter", "talking-head-video-production", "video-use"},
        )

    def test_all_skill_interfaces_are_discoverable(self):
        for item in self.manifest["skills"]:
            name = item["name"]
            root = PACK_ROOT / item["path"]
            skill_path = root / "SKILL.md"
            yaml_path = root / "agents" / "openai.yaml"
            self.assertTrue(skill_path.exists(), f"missing SKILL.md: {name}")
            self.assertTrue(yaml_path.exists(), f"missing openai.yaml: {name}")
            skill = skill_path.read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
            self.assertIsNotNone(match, f"invalid frontmatter: {name}")
            lines = [line for line in match.group(1).splitlines() if line.strip()]
            self.assertEqual(len(lines), 2, f"frontmatter must have exactly two fields: {name}")
            self.assertEqual(lines[0], f"name: {name}")
            self.assertTrue(lines[1].startswith("description: Use when "))
            metadata = yaml_path.read_text(encoding="utf-8")
            self.assertRegex(metadata, r'display_name: "[^"]+"')
            short = re.search(r'short_description: "([^"]+)"', metadata)
            self.assertIsNotNone(short)
            self.assertGreaterEqual(len(short.group(1)), 25)
            self.assertLessEqual(len(short.group(1)), 64)
            self.assertIn(f'default_prompt: "Use ${name}', metadata)

    def test_each_skill_has_six_trigger_scenarios(self):
        path = PACK_ROOT / "tests" / "scenarios.json"
        self.assertTrue(path.exists(), "scenarios.json must exist")
        scenarios = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(set(scenarios), EXPECTED_SKILLS)
        for name, groups in scenarios.items():
            self.assertEqual(len(groups["positive"]), 3, name)
            self.assertEqual(len(groups["negative"]), 2, name)
            self.assertEqual(len(groups["boundary"]), 1, name)

    def test_local_pack_validator_passes(self):
        validator = PACK_ROOT / "scripts" / "validate_pack.py"
        self.assertTrue(validator.exists(), "validate_pack.py must exist")
        result = subprocess.run(
            ["python3", str(validator), str(PACK_ROOT)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["skills_total"], 13)
        self.assertEqual(summary["skills_passed"], 13)
        self.assertEqual(summary["errors"], [])
        self.assertEqual(summary["official_validation_status"], "passed")
        self.assertFalse(summary["global_installed"])


if __name__ == "__main__":
    unittest.main()
