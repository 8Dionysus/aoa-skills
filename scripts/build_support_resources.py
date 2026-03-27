#!/usr/bin/env python3
"""Build wave-8 deterministic support-bundle manifests.

This builder records canonical support resources that live under
`skills/*/{scripts,references,assets}` for a targeted set of high-risk skills.
It does not mirror files into `.agents/skills/*`; the existing portable export
builder remains the only portable-copy authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


PROFILE = "codex-facing-wave-8-support-bundles"
JSON_INDENT = 2
STANDARD_DIRS = ("scripts", "references", "assets")
LEGACY_DIRS = ("agents", "checks", "examples")
TARGETED_SKILLS = {
    "aoa-safe-infra-change": "high-risk infra/config mutation",
    "aoa-local-stack-bringup": "bounded local runtime bring-up with explicit lifecycle",
    "aoa-dry-run-first": "preview-first mutation discipline",
}
EXPECTED_EXISTING_AOA_SUPPORT = {
    "aoa-safe-infra-change": {
        "agents": ["openai.yaml"],
        "checks": ["review.md"],
        "examples": ["runtime.md"],
    },
    "aoa-local-stack-bringup": {
        "agents": ["openai.yaml"],
        "checks": ["review.md"],
        "examples": ["runtime.md"],
    },
    "aoa-dry-run-first": {
        "agents": ["openai.yaml"],
        "checks": ["review.md"],
        "examples": ["runtime.md"],
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def collect_files(base: Path) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        rel = path.relative_to(base).as_posix()
        results.append(
            {
                "path": rel,
                "sha256": sha256(path),
                "bytes": str(path.stat().st_size),
            }
        )
    return results


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=JSON_INDENT, ensure_ascii=False) + "\n"


def dump_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)


def render_or_check(path: Path, text: str, check: bool, repo_root: Path) -> None:
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            raise SystemExit(f"{path.relative_to(repo_root).as_posix()} is out of date")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_documents(repo_root: Path) -> dict[Path, str]:
    generated_root = repo_root / "generated"

    manifest = {
        "schema_version": 1,
        "profile": PROFILE,
        "targeted_skills": TARGETED_SKILLS,
        "skills": [],
    }
    support_index = {
        "schema_version": 1,
        "profile": PROFILE,
        "skills": [],
    }
    schema_index = {
        "schema_version": 1,
        "profile": PROFILE,
        "schemas": [],
    }
    bridge_map = {
        "schema_version": 1,
        "profile": PROFILE,
        "skills": {},
    }
    expected_existing = {
        "schema_version": 1,
        "profile": PROFILE,
        "skills": EXPECTED_EXISTING_AOA_SUPPORT,
    }
    eval_cases: list[dict[str, Any]] = []

    for skill_name, intent in TARGETED_SKILLS.items():
        skill_dir = repo_root / "skills" / skill_name
        if not skill_dir.exists():
            raise SystemExit(f"missing targeted skill root: {skill_dir}")

        entry = {
            "name": skill_name,
            "targeted": True,
            "canonical_root": skill_dir.relative_to(repo_root).as_posix(),
            "standard_dirs": {},
            "legacy_dirs": {},
        }
        bridge_entry = {
            "canonical_root": skill_dir.relative_to(repo_root).as_posix(),
            "legacy_support_dirs": {},
            "standard_support_dirs": {},
        }

        for dirname in LEGACY_DIRS:
            source = skill_dir / dirname
            if source.exists():
                files = collect_files(source)
                entry["legacy_dirs"][dirname] = files
                bridge_entry["legacy_support_dirs"][dirname] = [item["path"] for item in files]

        for dirname in STANDARD_DIRS:
            source = skill_dir / dirname
            if not source.exists():
                raise SystemExit(f"{skill_name}: missing canonical {dirname}/")
            files = collect_files(source)
            if not files:
                raise SystemExit(f"{skill_name}: canonical {dirname}/ is empty")
            entry["standard_dirs"][dirname] = files
            bridge_entry["standard_support_dirs"][dirname] = [item["path"] for item in files]

            if dirname == "assets":
                for file_info in files:
                    if file_info["path"].endswith(".schema.json"):
                        schema_path = source / file_info["path"]
                        payload = json.loads(schema_path.read_text(encoding="utf-8"))
                        schema_index["schemas"].append(
                            {
                                "skill": skill_name,
                                "path": (skill_dir / dirname / file_info["path"]).relative_to(repo_root).as_posix(),
                                "title": payload.get("title", ""),
                                "required_count": len(payload.get("required", [])),
                            }
                        )

        manifest["skills"].append(entry)
        support_index["skills"].append(
            {
                "name": skill_name,
                "targeted": True,
                "standard_dir_counts": {
                    dirname: len(files) for dirname, files in entry["standard_dirs"].items()
                },
                "legacy_dir_counts": {
                    dirname: len(files) for dirname, files in entry["legacy_dirs"].items()
                },
            }
        )
        bridge_map["skills"][skill_name] = bridge_entry
        eval_cases.append(
            {
                "case_id": f"wave8-{skill_name}",
                "skill_name": skill_name,
                "prompt": f"Use {skill_name} with its deterministic helpers.",
                "intent": intent,
                "expected_standard_dirs": list(STANDARD_DIRS),
            }
        )

    return {
        generated_root / "deterministic_resource_manifest.json": dump_json(manifest),
        generated_root / "support_resource_index.json": dump_json(support_index),
        generated_root / "structured_output_schema_index.json": dump_json(schema_index),
        generated_root / "support_resource_bridge_map.json": dump_json(bridge_map),
        generated_root / "deterministic_resource_eval_cases.jsonl": dump_jsonl(eval_cases),
        generated_root / "expected_existing_aoa_support_dirs.json": dump_json(expected_existing),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic support-resource manifests.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--check", action="store_true", help="Check whether generated outputs are current.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    file_map = build_documents(repo_root)
    for path, text in file_map.items():
        render_or_check(path, text, args.check, repo_root)
    print(json.dumps({"status": "ok", "repo_root": str(repo_root), "check": args.check}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
