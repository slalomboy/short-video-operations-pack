import importlib.util
import tempfile
import unittest
from pathlib import Path


PACK_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = PACK_ROOT / "scripts" / "install_runtime_entrypoints.py"


class RuntimeDiscoveryTests(unittest.TestCase):
    def test_installer_creates_flat_runtime_entrypoints_for_all_skills(self):
        self.assertTrue(INSTALLER_PATH.exists(), "runtime entrypoint installer is missing")
        spec = importlib.util.spec_from_file_location("install_runtime_entrypoints", INSTALLER_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp)
            created = module.install_entrypoints(PACK_ROOT, skill_root)
            manifest = module.load_manifest(PACK_ROOT)
            expected = {item["name"] for item in manifest["skills"]}

            self.assertEqual(set(created), expected)
            for name in expected:
                wrapper = skill_root / name / "SKILL.md"
                self.assertTrue(wrapper.exists(), name)
                text = wrapper.read_text(encoding="utf-8")
                self.assertIn(f"name: {name}", text)
                self.assertIn(
                    f"../short-video-operations-pack/skills/{name}/SKILL.md",
                    text,
                )


if __name__ == "__main__":
    unittest.main()
