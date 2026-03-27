#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


TARGETED_SKILLS = (
    "aoa-safe-infra-change",
    "aoa-local-stack-bringup",
    "aoa-dry-run-first",
)


def lint(repo_root: Path) -> dict[str, object]:
    errors: list[str] = []
    notes: list[str] = []

    for skill in TARGETED_SKILLS:
        assets_dir = repo_root / "skills" / skill / "assets"
        scripts_dir = repo_root / "skills" / skill / "scripts"
        references_dir = repo_root / "skills" / skill / "references"

        template_files = sorted(assets_dir.glob("*.template.json"))
        schema_files = sorted(assets_dir.glob("*.schema.json"))
        if len(template_files) != 1:
            errors.append(f"{skill}: expected exactly one *.template.json file")
        if len(schema_files) != 1:
            errors.append(f"{skill}: expected exactly one *.schema.json file")

        if len(list(scripts_dir.glob("*.py"))) < 2:
            notes.append(f"{skill}: fewer than two python helpers")
        if len(list(references_dir.glob("*.md"))) < 2:
            notes.append(f"{skill}: fewer than two markdown references")

    return {"status": "ok" if not errors else "fail", "errors": errors, "notes": notes}


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint support-resource naming and file-count conventions.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    args = parser.parse_args()

    result = lint(Path(args.repo_root).resolve())
    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))
    return 0 if result["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
