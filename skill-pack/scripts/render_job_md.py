#!/usr/bin/env python3
import argparse
from pathlib import Path
from job_contract import load_json, render_markdown, validate_job


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    job = load_json(args.input)
    errors = validate_job(job)
    if errors:
        raise SystemExit("; ".join(errors))
    args.output.write_text(render_markdown(job), encoding="utf-8")


if __name__ == "__main__":
    main()
