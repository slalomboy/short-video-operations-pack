import json
import sys
import unittest
from pathlib import Path


PACK_ROOT = Path(__file__).resolve().parents[1]
SHARED = PACK_ROOT / "shared"
SCRIPTS = PACK_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
REQUIRED_FIELDS = {
    "meta", "business", "audience", "materials", "topics",
    "scriptStrategy", "evidence", "production", "review",
    "publishExperiment", "paidGrowth", "liveConversion",
    "metrics", "nextActions", "governance",
}
VALID_STATES = {
    "intake", "positioning", "planning", "script-ready",
    "production-ready", "review-ready", "publish-ready",
    "measuring", "reviewed", "completed", "blocked",
    "paused", "superseded",
}


class ContractFileTests(unittest.TestCase):
    def test_template_has_required_shape(self):
        path = SHARED / "templates" / "ShortVideoOpsJob.json"
        self.assertTrue(path.exists(), "ShortVideoOpsJob.json must exist")
        job = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(set(job), REQUIRED_FIELDS)
        self.assertTrue(job["meta"]["jobId"])
        self.assertEqual(job["meta"]["version"], 1)
        self.assertIn(job["meta"]["status"], VALID_STATES)
        self.assertIn("approvals", job["governance"])
        self.assertIn("reviewItems", job["governance"])
        self.assertIn("conflicts", job["governance"])

    def test_schema_and_ownership_are_complete(self):
        schema_path = SHARED / "short-video-ops-job.schema.json"
        ownership_path = SHARED / "field-ownership.json"
        self.assertTrue(schema_path.exists(), "job schema must exist")
        self.assertTrue(ownership_path.exists(), "field ownership must exist")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        ownership = json.loads(ownership_path.read_text(encoding="utf-8"))
        self.assertEqual(set(schema["required"]), REQUIRED_FIELDS)
        self.assertEqual(set(schema["properties"]["meta"]["properties"]["status"]["enum"]), VALID_STATES)
        self.assertEqual(len(ownership), 13)

    def test_public_rules_include_required_gates(self):
        rules_path = SHARED / "public-rules.md"
        self.assertTrue(rules_path.exists(), "public rules must exist")
        rules = rules_path.read_text(encoding="utf-8")
        for phrase in [
            "事实和证据优先于营销表达", "reviewItems", "当前官方来源核验",
            "发布", "付费支出", "直播操作", "全局安装", "外部写入", "明确授权",
        ]:
            self.assertIn(phrase, rules)


class JobToolTests(unittest.TestCase):
    def setUp(self):
        try:
            from job_contract import merge_owned_patch, new_job, render_markdown, validate_job
        except ImportError as error:
            self.fail(f"job tools must be importable: {error}")
        self.merge_owned_patch = merge_owned_patch
        self.new_job = new_job
        self.render_markdown = render_markdown
        self.validate_job = validate_job
        self.ownership = json.loads((SHARED / "field-ownership.json").read_text(encoding="utf-8"))
        self.job = self.new_job("sv-20260716-001", "operator", "2026-07-16T10:00:00+08:00")

    def test_new_job_is_valid_and_render_is_deterministic(self):
        self.assertEqual(self.validate_job(self.job), [])
        first = self.render_markdown(self.job)
        second = self.render_markdown(self.job)
        self.assertEqual(first, second)
        self.assertIn("sv-20260716-001", first)

    def test_owned_patch_increments_version(self):
        patch = {
            "jobId": "sv-20260716-001",
            "baseVersion": 1,
            "skill": "short-video-positioning",
            "writes": {"business": {"goal": "获客"}},
            "reviewItems": [],
        }
        updated = self.merge_owned_patch(self.job, patch, self.ownership)
        self.assertEqual(updated["meta"]["version"], 2)
        self.assertEqual(updated["business"]["goal"], "获客")
        self.assertEqual(self.job["meta"]["version"], 1)

    def test_stale_patch_is_rejected(self):
        patch = {"jobId": "sv-20260716-001", "baseVersion": 0,
                 "skill": "short-video-positioning", "writes": {"business": {}}}
        with self.assertRaisesRegex(ValueError, "stale task version"):
            self.merge_owned_patch(self.job, patch, self.ownership)

    def test_foreign_and_unknown_fields_are_rejected(self):
        for patch in [
            {"jobId": "sv-20260716-001", "baseVersion": 1,
             "skill": "short-video-positioning", "writes": {"audience": {}}},
            {"jobId": "sv-20260716-001", "baseVersion": 1,
             "skill": "unknown-skill", "writes": {"business": {}}},
            {"jobId": "sv-20260716-001", "baseVersion": 1,
             "skill": "short-video-positioning", "writes": {"unknownField": {}}},
        ]:
            with self.assertRaisesRegex(ValueError, "field ownership conflict"):
                self.merge_owned_patch(self.job, patch, self.ownership)

    def test_missing_field_invalid_state_and_unauthorized_action_are_explicit(self):
        missing = dict(self.job)
        missing.pop("audience")
        self.assertIn("missing required field: audience", self.validate_job(missing))
        invalid = json.loads(json.dumps(self.job))
        invalid["meta"]["status"] = "invented"
        self.assertIn("invalid state: invented", self.validate_job(invalid))
        gated = json.loads(json.dumps(self.job))
        gated["publishExperiment"] = {"action": "publish", "authorized": False}
        self.assertIn("unauthorized external action: publish", self.validate_job(gated))


if __name__ == "__main__":
    unittest.main()
