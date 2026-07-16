import json
import sys
import unittest
from pathlib import Path


PACK_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PACK_ROOT / "scripts"
FIXTURES = PACK_ROOT / "tests" / "fixtures"
sys.path.insert(0, str(SCRIPTS))
SCENARIOS = [
    "new-account-first-plan.json",
    "comment-question-one-video.json",
    "script-to-production-review.json",
    "reach-good-conversion-weak.json",
    "organic-to-paid-eligibility.json",
    "short-video-to-live-fulfillment.json",
    "weekly-review-to-material-next-task.json",
]


class EndToEndTests(unittest.TestCase):
    def test_seven_workflows_return_valid_jobs_and_gates(self):
        try:
            from workflow import run_scenario
        except ImportError as error:
            self.fail(f"workflow runner must be importable: {error}")
        for filename in SCENARIOS:
            with self.subTest(filename=filename):
                path = FIXTURES / filename
                self.assertTrue(path.exists(), f"missing fixture: {filename}")
                scenario = json.loads(path.read_text(encoding="utf-8"))
                result = run_scenario(scenario, PACK_ROOT)
                self.assertEqual(result["errors"], [])
                self.assertEqual(result["route"], scenario["expectedRoute"])
                self.assertEqual(result["gate"], scenario["expectedGate"])
                self.assertEqual(result["job"]["meta"]["status"], scenario["expectedStatus"])
                self.assertEqual(result["job"]["meta"]["version"], 1 + len(scenario["patches"]))
                self.assertIn(result["job"]["meta"]["jobId"], result["markdown"])
                self.assertTrue(result["nextAction"])


if __name__ == "__main__":
    unittest.main()
