#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


MANAGED_MARKER = "<!-- managed-by: short-video-operations-pack -->"
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)


def load_manifest(pack_root: Path) -> dict:
    return json.loads((pack_root / "pack.json").read_text(encoding="utf-8"))


def canonical_description(skill_path: Path) -> str:
    text = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"invalid frontmatter: {skill_path}")
    for line in match.group(1).splitlines():
        if line.startswith("description: "):
            return line.removeprefix("description: ")
    raise ValueError(f"missing description: {skill_path}")


def wrapper_text(name: str, description: str) -> str:
    canonical = f"../short-video-operations-pack/skills/{name}/SKILL.md"
    return (
        f"---\nname: {name}\ndescription: {description}\n---\n\n"
        f"# {name}\n\n{MANAGED_MARKER}\n\n"
        f"Before acting, read and follow the canonical Skill at `{canonical}`. "
        "This file is only a flat runtime discovery entrypoint; the canonical "
        "Skill owns the workflow, references, templates, boundaries, and output contract.\n"
    )


def install_entrypoints(pack_root: Path, skill_root: Path) -> list[str]:
    manifest = load_manifest(pack_root)
    created = []
    for item in manifest["skills"]:
        name = item["name"]
        canonical = pack_root / item["path"] / "SKILL.md"
        target_dir = skill_root / name
        target = target_dir / "SKILL.md"
        if target.exists() and MANAGED_MARKER not in target.read_text(encoding="utf-8"):
            raise FileExistsError(f"refusing to overwrite unmanaged Skill: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)
        target.write_text(
            wrapper_text(name, canonical_description(canonical)),
            encoding="utf-8",
        )
        created.append(name)
    return created


def check_entrypoints(pack_root: Path, skill_root: Path) -> list[str]:
    missing = []
    for item in load_manifest(pack_root)["skills"]:
        target = skill_root / item["name"] / "SKILL.md"
        if not target.exists() or MANAGED_MARKER not in target.read_text(encoding="utf-8"):
            missing.append(item["name"])
    return missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack_root", type=Path)
    parser.add_argument("skill_root", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        missing = check_entrypoints(args.pack_root, args.skill_root)
        print(json.dumps({"missing": missing}, ensure_ascii=False))
        return 1 if missing else 0
    created = install_entrypoints(args.pack_root, args.skill_root)
    print(json.dumps({"installed": created}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
