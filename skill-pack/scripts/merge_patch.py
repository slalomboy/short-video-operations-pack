#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from job_contract import load_json, merge_owned_patch, validate_job


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=Path)
    parser.add_argument("patch", type=Path)
    parser.add_argument("ownership", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    updated = merge_owned_patch(load_json(args.job), load_json(args.patch), load_json(args.ownership))
    errors = validate_job(updated)
    if errors:
        raise SystemExit("; ".join(errors))
    args.output.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
