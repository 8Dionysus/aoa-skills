#!/usr/bin/env python3
"""Run the upstream skills-ref validator across the portable export."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
from typing import Any


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def resolve_validator(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    env_value = os.environ.get("SKILLS_REF_BIN")
    if env_value:
        return env_value
    return shutil.which("skills-ref")


def validator_command(validator_bin: str) -> list[str]:
    validator_path = pathlib.Path(validator_bin)
    if validator_path.suffix.lower() == ".py":
        return [sys.executable, str(validator_path)]
    return [validator_bin]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--skills-ref-bin", help="Explicit path to the skills-ref executable")
    parser.add_argument("--require-skills-ref", action="store_true", help="Fail when the validator is unavailable")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--summary-file", help="Optional path to write the summary JSON")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    manifest = load_json(repo_root / "generated" / "skills_ref_validation_manifest.json")
    validator_bin = resolve_validator(args.skills_ref_bin)

    if not validator_bin:
        payload = {
            "status": "skipped",
            "reason": "skills-ref executable not found",
            "required": bool(args.require_skills_ref),
            "targets": len(manifest.get("targets", [])),
        }
        if args.summary_file:
            summary_path = pathlib.Path(args.summary_file)
            summary_path.parent.mkdir(parents=True, exist_ok=True)
            summary_path.write_text(dump_json(payload), encoding="utf-8", newline="\n")
        if args.format == "json":
            print(dump_json(payload), end="")
        else:
            print("skills-ref executable not found; skipping portable export conformance lane")
        return 1 if args.require_skills_ref else 0

    results: list[dict[str, Any]] = []
    failed = False
    for target in manifest.get("targets", []):
        skill_path = repo_root / target["path"]
        command = [*validator_command(validator_bin), "validate", str(skill_path)]
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        result = {
            "skill_name": target["skill_name"],
            "path": target["path"],
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "passed": completed.returncode == 0,
        }
        results.append(result)
        if completed.returncode != 0:
            failed = True

    payload = {
        "status": "failed" if failed else "passed",
        "validator": validator_bin,
        "target_count": len(results),
        "passed_count": sum(1 for result in results if result["passed"]),
        "failed_count": sum(1 for result in results if not result["passed"]),
        "results": results,
    }

    if args.summary_file:
        summary_path = pathlib.Path(args.summary_file)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(dump_json(payload), encoding="utf-8", newline="\n")

    if args.format == "json":
        print(dump_json(payload), end="")
    else:
        print(f"skills-ref {payload['status']}: {payload['passed_count']}/{payload['target_count']} skills")
        if failed:
            for result in results:
                if not result["passed"]:
                    print(f"- {result['skill_name']}: validator failed")
                    if result["stderr"].strip():
                        print(result["stderr"].rstrip())
                    elif result["stdout"].strip():
                        print(result["stdout"].rstrip())

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
