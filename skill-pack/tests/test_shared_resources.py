import unittest
from pathlib import Path


PACK_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = PACK_ROOT / "shared" / "references"
TEMPLATES = PACK_ROOT / "shared" / "assets" / "templates"
REFERENCE_FILES = {
    "positioning-and-audience.md",
    "materials-topics-and-hooks.md",
    "scripts-evidence-and-shots.md",
    "publishing-growth-live-and-review.md",
}
TEMPLATE_FILES = {
    "account-positioning-card.md",
    "audience-task-concern-card.md",
    "material-record-card.md",
    "topic-scorecard.md",
    "script-strategy-card.md",
    "claim-evidence-map.md",
    "shot-task-sheet.md",
    "content-review-checklist.md",
    "publish-experiment-record.md",
    "paid-growth-test.md",
    "live-conversion-checklist.md",
    "performance-review.md",
}


class SharedResourceTests(unittest.TestCase):
    def test_four_references_have_operational_contract(self):
        for name in REFERENCE_FILES:
            path = REFERENCES / name
            self.assertTrue(path.exists(), f"missing reference: {name}")
            text = path.read_text(encoding="utf-8")
            for heading in ["目的", "输入", "方法", "输出", "证据边界", "失败条件", "来源范围"]:
                self.assertIn(f"## {heading}", text, f"{name} missing {heading}")

    def test_twelve_templates_have_shared_metadata(self):
        for name in TEMPLATE_FILES:
            path = TEMPLATES / name
            self.assertTrue(path.exists(), f"missing template: {name}")
            text = path.read_text(encoding="utf-8")
            for label in ["jobId", "owner Skill", "必需输入", "产出字段", "reviewItems", "授权状态"]:
                self.assertIn(label, text, f"{name} missing {label}")


if __name__ == "__main__":
    unittest.main()
