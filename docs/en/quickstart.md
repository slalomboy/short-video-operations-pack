# Quick start

[中文主入口](../../README.md) · [English docs](README.md)

## Requirements

- Python 3.10 or newer.
- An Agent runtime that can load local Skills.

## Install the fixed version

```bash
git clone --branch v0.1.0-alpha.4 --depth 1 https://github.com/slalomboy/short-video-operations-pack.git
cd short-video-operations-pack
python3 skill-pack/scripts/validate_pack.py skill-pack
```

Install `skill-pack/` in your runtime. If the runtime only discovers flat Skill directories, run:

```bash
python3 skill-pack/scripts/install_runtime_entrypoints.py skill-pack <skill-root>
```

The installer refuses to overwrite an unmanaged same-name Skill.

## First request

Ask: “Use `short-video-operations` to define positioning and propose the first topic batch for this new account. Stop at planning; do not publish.”

Success means you receive a valid job record with evidence gaps, approval state, and next actions. It does not mean anything was published.
