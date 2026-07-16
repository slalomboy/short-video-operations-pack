#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from job_contract import load_json, validate_job


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    errors = validate_job(load_json(args.input))
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
