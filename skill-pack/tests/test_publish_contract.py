import importlib.util
import unittest
from pathlib import Path


PACK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PACK_ROOT / "addons" / "multi-platform-publish-contract" / "scripts" / "validate_publish_job.py"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("publish_contract", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_job():
    return {
        "job_id": "pub-demo-001",
        "asset_package_id": "pkg-demo-001",
        "asset_owner": "Example Studio",
        "account_asset_package": {
            "account_key": "douyin:example-studio",
            "platform": "douyin",
            "video_ref": "assets/demo-video.mp4",
            "cover_ref": "assets/demo-cover.png",
            "caption": "A verified demo caption",
        },
        "authorization": {"submit": False, "schedule": False, "publish": False},
        "status": "ready_for_operator",
        "platform_result": None,
    }


class PublishContractTests(unittest.TestCase):
    def test_valid_local_job_is_ready_for_operator_without_claiming_publish(self):
        module = load_module(SCRIPT)
        self.assertEqual(module.validate_publish_job(valid_job()), [])
        self.assertEqual(module.highest_proven_state(valid_job()), "ready_for_operator")

    def test_account_or_platform_mismatch_is_blocked(self):
        module = load_module(SCRIPT)
        job = valid_job()
        job["account_asset_package"]["account_key"] = "youtube:example-studio"
        self.assertIn("account_asset_package platform mismatch", module.validate_publish_job(job))

    def test_upload_or_submit_is_not_publication_proof(self):
        module = load_module(SCRIPT)
        for status in ("uploaded", "submitted", "scheduled"):
            job = valid_job()
            job["status"] = status
            self.assertEqual(module.highest_proven_state(job), status)

    def test_published_verified_requires_public_url_and_platform_id(self):
        module = load_module(SCRIPT)
        job = valid_job()
        job["status"] = "published_verified"
        self.assertIn("published_verified requires public_url and platform_content_id", module.validate_publish_job(job))
        job["platform_result"] = {
            "public_url": "https://example.invalid/video/123",
            "platform_content_id": "123",
        }
        self.assertEqual(module.validate_publish_job(job), [])


if __name__ == "__main__":
    unittest.main()
