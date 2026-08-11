#!/usr/bin/env python3
"""Validate a local, platform-neutral publishing handoff contract."""

from __future__ import annotations


STATES = {
    "draft",
    "ready_for_operator",
    "uploaded",
    "submitted",
    "scheduled",
    "published_verified",
    "blocked",
}


def validate_publish_job(job: dict) -> list[str]:
    errors: list[str] = []
    for field in ("job_id", "asset_package_id", "asset_owner", "account_asset_package", "authorization", "status"):
        if field not in job:
            errors.append(f"missing required field: {field}")
    package = job.get("account_asset_package") or {}
    for field in ("account_key", "platform", "video_ref", "cover_ref", "caption"):
        if not package.get(field):
            errors.append(f"account_asset_package missing field: {field}")
    account_key = str(package.get("account_key", ""))
    platform = str(package.get("platform", ""))
    if account_key and platform and account_key.split(":", 1)[0] != platform:
        errors.append("account_asset_package platform mismatch")
    if job.get("status") not in STATES:
        errors.append(f"invalid status: {job.get('status')}")
    if job.get("status") == "published_verified":
        result = job.get("platform_result") or {}
        if not result.get("public_url") or not result.get("platform_content_id"):
            errors.append("published_verified requires public_url and platform_content_id")
    return errors


def highest_proven_state(job: dict) -> str:
    """Return only the state directly present in evidence; never promote upload to publication."""
    return str(job.get("status", "draft"))
