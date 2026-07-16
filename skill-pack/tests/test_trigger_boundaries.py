import unittest
from pathlib import Path


PACK_ROOT = Path(__file__).resolve().parents[1]
SKILLS = PACK_ROOT / "skills"


def read_skill(name):
    path = SKILLS / name / "SKILL.md"
    if not path.exists():
        raise AssertionError(f"missing Skill: {name}")
    return path.read_text(encoding="utf-8")


class OrchestratorBoundaryTests(unittest.TestCase):
    def test_orchestrator_routes_full_workflow_and_continuation(self):
        text = read_skill("short-video-operations")
        for phrase in ["一套短视频运营方案", "从定位到复盘", "继续", "ShortVideoOpsJob"]:
            self.assertIn(phrase, text)
        for dependency in ["content-voiceover-copywriter", "talking-head-video-production", "video-use"]:
            self.assertIn(dependency, text)

    def test_orchestrator_rejects_copy_only_and_edit_only_scope(self):
        text = read_skill("short-video-operations")
        self.assertIn("只润色口播", text)
        self.assertIn("剪掉口误", text)
        self.assertIn("不得代替", text)


class PositioningAudienceBoundaryTests(unittest.TestCase):
    def test_positioning_contract(self):
        text = read_skill("short-video-positioning")
        for phrase in ["账号定位", "变现", "主页承诺", "offer", "targetUser", "contentPillars", "exclusions"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `business`", text)

    def test_audience_contract(self):
        text = read_skill("short-video-audience-insight")
        for phrase in ["用户处境", "顾虑", "判断标准", "评论问题", "verbatimLanguage", "evidence source"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `audience`", text)

    def test_boundary_routes_positioning_before_audience(self):
        positioning = read_skill("short-video-positioning")
        audience = read_skill("short-video-audience-insight")
        self.assertIn("先定位后受众", positioning)
        self.assertIn("定位给宝妈，但不知道她们具体担心什么", audience)


class MaterialTopicBoundaryTests(unittest.TestCase):
    def test_material_library_preserves_provenance_and_rights(self):
        text = read_skill("short-video-material-library")
        for phrase in ["素材分类", "source", "rights", "usageHistory", "直接复制", "跨行业"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `materials`", text)

    def test_topic_planning_scores_execution_and_risk(self):
        text = read_skill("short-video-topic-planning")
        for phrase in ["attention", "relevance", "evidenceAvailability", "shootability", "conversionDistance", "riskScore", "rankingReason"]:
            self.assertIn(phrase, text)
        self.assertIn("热点", text)
        self.assertIn("只写 `topics`", text)


class ScriptEvidenceBoundaryTests(unittest.TestCase):
    def test_script_strategy_has_four_functions_and_copy_route(self):
        text = read_skill("short-video-script-strategy")
        for phrase in ["观点", "过程", "知识", "故事", "hookA", "hookB", "coreIdea", "CTA", "content-voiceover-copywriter"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `scriptStrategy`", text)

    def test_evidence_planning_maps_or_removes_claims(self):
        text = read_skill("short-video-evidence-planning")
        for phrase in ["主张—证据", "事实", "可观察过程", "公平比较", "有限结果", "删除", "reviewItems", "production-ready"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `evidence`", text)


class ShotReviewBoundaryTests(unittest.TestCase):
    def test_shot_plan_prioritizes_information_and_routes_execution(self):
        text = read_skill("short-video-shot-planning")
        for phrase in ["cameraRelationship", "scenePurpose", "spokenTrack", "visualEvidence", "captions", "sound", "assets", "privacy", "信息和证据优先于装饰", "talking-head-video-production", "video-use"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `production`", text)

    def test_review_uses_severity_and_small_revision_set(self):
        text = read_skill("short-video-content-review")
        for phrase in ["severity", "一到两个变量", "虚构场景", "假顾客", "未经同意", "复杂效果"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `review`", text)


class PublishPaidBoundaryTests(unittest.TestCase):
    def test_publish_experiment_controls_causality_and_permission(self):
        text = read_skill("short-video-publish-experiment")
        for phrase in ["hypothesis", "primaryVariable", "comparableConditions", "metric", "stopRule", "单条", "pendingApproval"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `publishExperiment`", text)

    def test_paid_growth_uses_full_economics_and_never_authorizes_spend(self):
        text = read_skill("short-video-paid-growth")
        for phrase in ["budgetCeiling", "funnel", "leadQuality", "refunds", "fulfillment", "contributionMargin", "低播放成本", "不授权支出", "pendingApproval"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `paidGrowth`", text)


class LiveReviewBoundaryTests(unittest.TestCase):
    def test_live_conversion_connects_promise_to_fulfillment(self):
        text = read_skill("short-video-live-conversion")
        for phrase in ["短视频承诺", "productProof", "priceRights", "service", "fulfillment", "refunds", "虚假稀缺", "伪造销量", "假砍价", "pendingApproval"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `liveConversion`", text)

    def test_performance_review_uses_four_metric_layers_and_adoption_gate(self):
        text = read_skill("short-video-performance-review")
        for phrase in ["contentMetrics", "audienceMetrics", "conversionMetrics", "deliveryMetrics", "多个可比样本", "adoptionGate", "nextExperiment"]:
            self.assertIn(phrase, text)
        self.assertIn("只写 `metrics` 和 `nextActions`", text)


if __name__ == "__main__":
    unittest.main()
