#!/usr/bin/env python3
import json
from pathlib import Path
from job_contract import merge_owned_patch, new_job, render_markdown, validate_job


ROUTES = {
    "new-account-first-plan": ["short-video-positioning", "short-video-audience-insight", "short-video-material-library", "short-video-topic-planning"],
    "comment-question-one-video": ["short-video-audience-insight", "short-video-topic-planning", "short-video-script-strategy", "short-video-evidence-planning", "short-video-shot-planning"],
    "script-to-production-review": ["short-video-evidence-planning", "short-video-shot-planning", "short-video-content-review"],
    "reach-good-conversion-weak": ["short-video-performance-review"],
    "organic-to-paid-eligibility": ["short-video-performance-review", "short-video-paid-growth"],
    "short-video-to-live-fulfillment": ["short-video-live-conversion"],
    "weekly-review-to-material-next-task": ["short-video-performance-review", "short-video-material-library"],
}


def run_scenario(scenario: dict, pack_root: Path) -> dict:
    request_type = scenario["requestType"]
    if request_type not in ROUTES:
        raise ValueError("unknown workflow request type")
    job = new_job(scenario["jobId"], scenario.get("owner", "operator"), scenario["now"])
    ownership = json.loads((Path(pack_root) / "shared" / "field-ownership.json").read_text(encoding="utf-8"))
    for patch in scenario.get("patches", []):
        job = merge_owned_patch(job, patch, ownership)
    errors = validate_job(job)
    action = scenario.get("requestedAction")
    gate = f"pendingApproval:{action}" if action and not scenario.get("authorized", False) else "none"
    next_actions = job.get("nextActions", [])
    next_action = next_actions[0] if next_actions else f"Complete {ROUTES[request_type][-1]}"
    return {
        "job": job,
        "markdown": render_markdown(job),
        "route": ROUTES[request_type],
        "errors": errors,
        "reviewItems": job["governance"]["reviewItems"],
        "gate": gate,
        "nextAction": next_action,
    }
