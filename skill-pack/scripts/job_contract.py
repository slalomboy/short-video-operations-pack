#!/usr/bin/env python3
import copy
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "meta", "business", "audience", "materials", "topics",
    "scriptStrategy", "evidence", "production", "review",
    "publishExperiment", "paidGrowth", "liveConversion",
    "metrics", "nextActions", "governance",
}
JOB_STATES = {
    "intake", "positioning", "planning", "script-ready",
    "production-ready", "review-ready", "publish-ready",
    "measuring", "reviewed", "completed", "blocked",
    "paused", "superseded",
}
EXTERNAL_ACTIONS = {"publish", "paidSpend", "liveAction", "globalInstall", "externalWrite"}


def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def new_job(job_id: str, owner: str, now: str) -> dict:
    return {
        "meta": {
            "jobId": job_id,
            "version": 1,
            "status": "intake",
            "owner": owner,
            "createdAt": now,
            "updatedAt": now,
        },
        "business": {},
        "audience": {},
        "materials": {},
        "topics": {},
        "scriptStrategy": {},
        "evidence": {},
        "production": {},
        "review": {},
        "publishExperiment": {},
        "paidGrowth": {},
        "liveConversion": {},
        "metrics": {},
        "nextActions": [],
        "governance": {"approvals": [], "reviewItems": [], "conflicts": []},
    }


def validate_job(job: dict) -> list[str]:
    errors = []
    for field in sorted(REQUIRED_FIELDS - set(job)):
        errors.append(f"missing required field: {field}")
    meta = job.get("meta", {})
    for field in ("jobId", "version", "status", "owner", "createdAt", "updatedAt"):
        if field not in meta:
            errors.append(f"missing meta field: {field}")
    state = meta.get("status")
    if state is not None and state not in JOB_STATES:
        errors.append(f"invalid state: {state}")
    if not isinstance(meta.get("version"), int) or meta.get("version", 0) < 1:
        errors.append("meta.version must be a positive integer")
    governance = job.get("governance", {})
    for field in ("approvals", "reviewItems", "conflicts"):
        if field not in governance:
            errors.append(f"missing governance field: {field}")
    for section in ("publishExperiment", "paidGrowth", "liveConversion"):
        value = job.get(section, {})
        action = value.get("action") if isinstance(value, dict) else None
        if action in EXTERNAL_ACTIONS and value.get("authorized") is not True:
            errors.append(f"unauthorized external action: {action}")
    for request in governance.get("requestedActions", []):
        action = request.get("action")
        if action in EXTERNAL_ACTIONS and request.get("authorized") is not True:
            errors.append(f"unauthorized external action: {action}")
    return errors


def _pretty(value) -> str:
    if value in ({}, []):
        return "_未填写_"
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n```"


def render_markdown(job: dict) -> str:
    meta = job["meta"]
    sections = [
        f"# 短视频运营任务 {meta['jobId']}",
        "",
        f"- 状态：{meta['status']}",
        f"- 版本：{meta['version']}",
        f"- 负责人：{meta['owner']}",
        f"- 更新时间：{meta['updatedAt']}",
        "",
    ]
    labels = [
        ("业务定位", "business"), ("受众洞察", "audience"),
        ("素材库", "materials"), ("选题", "topics"),
        ("脚本策略", "scriptStrategy"), ("证据规划", "evidence"),
        ("制作规划", "production"), ("内容审查", "review"),
        ("发布实验", "publishExperiment"), ("付费增长", "paidGrowth"),
        ("直播转化", "liveConversion"), ("指标", "metrics"),
        ("下一步", "nextActions"), ("治理", "governance"),
    ]
    for label, field in labels:
        sections.extend([f"## {label}", "", _pretty(job[field]), ""])
    return "\n".join(sections).rstrip() + "\n"


def merge_owned_patch(job: dict, patch: dict, ownership: dict) -> dict:
    if patch.get("jobId") != job["meta"]["jobId"]:
        raise ValueError("job id mismatch")
    if patch.get("baseVersion") != job["meta"]["version"]:
        raise ValueError("stale task version")
    allowed = set(ownership.get(patch.get("skill"), []))
    requested = set(patch.get("writes", {}))
    if not requested <= allowed:
        raise ValueError("field ownership conflict")
    updated = copy.deepcopy(job)
    for field, value in patch.get("writes", {}).items():
        updated[field] = value
    updated["governance"]["reviewItems"].extend(patch.get("reviewItems", []))
    updated["meta"]["version"] += 1
    return updated
