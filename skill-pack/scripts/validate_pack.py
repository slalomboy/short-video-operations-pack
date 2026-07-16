#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
QUOTED_FIELD = lambda name: re.compile(rf'^\s+{name}: "([^"]+)"$', re.M)


def load_json(path, errors):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid json {path}: {error}")
        return {}


def validate_relative_references(root, errors):
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for reference in re.findall(r"`(\.\./[^`]+)`", text):
            target = (path.parent / reference).resolve()
            if not target.exists():
                errors.append(f"broken reference {path.relative_to(root)} -> {reference}")
    for path in root.rglob("*.json"):
        data = load_json(path, errors)
        stack = [data]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
            elif isinstance(value, str) and value.startswith("../"):
                if not (path.parent / value).resolve().exists():
                    errors.append(f"broken reference {path.relative_to(root)} -> {value}")


def validate_pack(root):
    errors = []
    warnings = []
    manifest = load_json(root / "pack.json", errors)
    skills = manifest.get("skills", [])
    scenarios = load_json(root / "tests" / "scenarios.json", errors)
    skill_passed = 0
    seen = set()

    if len(skills) != 13:
        errors.append(f"expected 13 skills, found {len(skills)}")
    for item in skills:
        name = item.get("name", "")
        local_errors = []
        if name in seen:
            local_errors.append(f"duplicate skill name: {name}")
        seen.add(name)
        skill_root = root / item.get("path", "")
        if skill_root.name != name:
            local_errors.append(f"folder/name mismatch: {name}")
        skill_path = skill_root / "SKILL.md"
        metadata_path = skill_root / "agents" / "openai.yaml"
        if not skill_path.exists():
            local_errors.append(f"missing SKILL.md: {name}")
        else:
            text = skill_path.read_text(encoding="utf-8")
            match = FRONTMATTER.match(text)
            if not match:
                local_errors.append(f"invalid frontmatter: {name}")
            else:
                lines = [line for line in match.group(1).splitlines() if line.strip()]
                if len(lines) != 2 or lines[0] != f"name: {name}" or not lines[1].startswith("description: Use when "):
                    local_errors.append(f"frontmatter must contain exact name and trigger-only description: {name}")
                if len(match.group(1)) > 1024:
                    local_errors.append(f"frontmatter too long: {name}")
        if not metadata_path.exists():
            local_errors.append(f"missing agents/openai.yaml: {name}")
        else:
            metadata = metadata_path.read_text(encoding="utf-8")
            fields = {field: QUOTED_FIELD(field).search(metadata) for field in ("display_name", "short_description", "default_prompt")}
            for field, match in fields.items():
                if not match:
                    local_errors.append(f"missing quoted {field}: {name}")
            if fields["short_description"]:
                length = len(fields["short_description"].group(1))
                if not 25 <= length <= 64:
                    local_errors.append(f"short_description length {length} outside 25-64: {name}")
            if fields["default_prompt"] and not fields["default_prompt"].group(1).startswith(f"Use ${name}"):
                local_errors.append(f"default_prompt must start with Use ${name}: {name}")
        groups = scenarios.get(name, {})
        if len(groups.get("positive", [])) != 3 or len(groups.get("negative", [])) != 2 or len(groups.get("boundary", [])) != 1:
            local_errors.append(f"scenario counts must be 3/2/1: {name}")
        if local_errors:
            errors.extend(local_errors)
        else:
            skill_passed += 1

    if set(scenarios) != seen:
        errors.append("scenario skill inventory does not match manifest")
    if manifest.get("global_installed") is True:
        installation = manifest.get("installation", {})
        if installation.get("status") != "installed" or not installation.get("target"):
            errors.append("global installation requires an installed status and target path")
    entrypoints = manifest.get("runtime_entrypoints", {})
    if entrypoints.get("mode") != "flat-wrappers" or entrypoints.get("skills") != 13:
        errors.append("runtime entrypoints must declare 13 flat wrappers")
    installer = root / entrypoints.get("installer", "")
    if not installer.is_file():
        errors.append("runtime entrypoint installer is missing")
    validate_relative_references(root, errors)
    official_record = manifest.get("validation", {}).get("official_skills_ref", {})
    official = official_record.get("status", "pending")
    if official != "passed":
        warnings.append("official skills-ref validation is pending; global installation remains blocked")
    return {
        "skills_total": len(skills),
        "skills_passed": skill_passed,
        "errors": errors,
        "warnings": warnings,
        "official_validation_status": official,
        "global_installed": manifest.get("global_installed"),
    }


def main(argv):
    if len(argv) != 2:
        print("Usage: validate_pack.py PACK_ROOT", file=sys.stderr)
        return 2
    summary = validate_pack(Path(argv[1]).resolve())
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if not summary["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
