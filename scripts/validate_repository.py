#!/usr/bin/env python3
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
manifest = json.loads((root / "skill-pack/pack.json").read_text(encoding="utf-8"))
names = [item["name"] for item in manifest["skills"]]
if len(names) != 13 or len(set(names)) != 13:
    errors.append("manifest must contain exactly 13 unique Skills")
if manifest.get("global_installed") is not False:
    errors.append("public manifest must not claim global installation")

required_sections = ["解决什么问题", "什么时候使用", "输入", "操作步骤", "输出", "验收标准", "常见错误", "示例调用"]
for name in names:
    tutorial = root / "docs/03-skills" / f"{name}.md"
    if not tutorial.exists():
        errors.append(f"missing tutorial: {name}")
        continue
    text = tutorial.read_text(encoding="utf-8")
    for section in required_sections:
        if f"## {section}" not in text:
            errors.append(f"{name}: missing section {section}")

svg_groups = {"illustrations": 5, "diagrams": 8, "skill-cards": 13, "workflow-flows": 7}
for group, minimum in svg_groups.items():
    files = list((root / "assets" / group).glob("*.svg"))
    if len(files) < minimum:
        errors.append(f"{group}: expected at least {minimum}, got {len(files)}")
    for file in files:
        try:
            ET.parse(file)
        except ET.ParseError as exc:
            errors.append(f"invalid SVG {file.relative_to(root)}: {exc}")

local_path = re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/")
secret = re.compile(r"(?:ghp_|github_pat_|sk-[A-Za-z0-9]{16,}|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY)")
link = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
scan_suffixes = {".md", ".json", ".py", ".yaml", ".yml"}
for file in root.rglob("*"):
    if not file.is_file() or ".git" in file.parts or file.suffix not in scan_suffixes:
        continue
    text = file.read_text(encoding="utf-8")
    if local_path.search(text):
        errors.append(f"local absolute path: {file.relative_to(root)}")
    if file.name != "validate_repository.py" and secret.search(text):
        errors.append(f"possible secret: {file.relative_to(root)}")
    if file.suffix == ".md":
        for target in link.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = (file.parent / target.split("#", 1)[0]).resolve()
            if not path.exists():
                errors.append(f"broken link in {file.relative_to(root)}: {target}")

summary = {"skills": len(names), "tutorials": len(list((root / "docs/03-skills").glob("short-video-*.md"))), "workflows": len(list((root / "docs/05-workflows").glob("[0-9][0-9]-*.md"))), "svgs": len(list((root / "assets").rglob("*.svg"))), "errors": errors}
print(json.dumps(summary, ensure_ascii=False, indent=2))
sys.exit(1 if errors else 0)
