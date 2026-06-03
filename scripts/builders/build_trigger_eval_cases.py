#!/usr/bin/env python3
"""Normalize trigger-eval seed rows against activation policy."""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
from typing import Any

from activation.skill_activation_policy import (
    allow_implicit_invocation,
    resolve_implicit_activation_policy,
)


JSONL_PATH = Path("generated") / "skill_trigger_eval_cases.jsonl"
CSV_PATH = Path("generated") / "skill_trigger_eval_cases.csv"
CSV_FIELDS = [
    "case_id",
    "skill_name",
    "mode",
    "expected_behavior",
    "expected_skill",
    "invocation_mode",
    "prompt",
    "note",
]

PROMPT_REPLACEMENTS = {
    "local-first Codex execution defaults": "local coding-agent execution defaults",
    "local Codex execution": "local coding-agent execution",
    "without executing Codex": "without starting hidden agent execution",
    "no Codex process was started": "no hidden agent process was started",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dump_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)


def dump_csv(rows: list[dict[str, Any]]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field) for field in CSV_FIELDS})
    return buffer.getvalue()


def normalize_rows(rows: list[dict[str, Any]], policy_doc: dict[str, Any]) -> list[dict[str, Any]]:
    policy_by_name = policy_doc.get("skills", {})
    normalized: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        prompt = item.get("prompt")
        if isinstance(prompt, str):
            for old, new in PROMPT_REPLACEMENTS.items():
                prompt = prompt.replace(old, new)
            item["prompt"] = prompt
        skill_name = str(item["skill_name"])
        policy_entry = policy_by_name.get(skill_name)
        activation_policy = resolve_implicit_activation_policy(policy_entry, skill_name)
        allow_implicit = allow_implicit_invocation(policy_entry, skill_name)
        mode = item.get("mode")
        if mode in {"implicit", "collision"} and item.get("expected_behavior") == "invoke-skill" and not allow_implicit:
            item["expected_behavior"] = "manual-invocation-required"
            item["expected_skill"] = None
            if activation_policy == "suggest":
                item["note"] = (
                    "Implicit semantic matches may surface this skill as a candidate, "
                    "but reviewed activation remains explicit."
                )
            elif mode == "collision":
                item["note"] = (
                    "Strong collision-family matches must not activate this manual skill; "
                    "use an explicit handle or deliberate manual decision before execution."
                )
            else:
                item["note"] = (
                    "Implicit semantic matches must not activate this skill; use an explicit handle "
                    "or manual decision before execution."
                )
        normalized.append(item)
    return normalized


def render_or_check(path: Path, text: str, check: bool) -> None:
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            raise SystemExit(f"trigger eval drift: {path}")
        return
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--check", action="store_true", help="Check generated outputs instead of writing")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    rows = load_jsonl(repo_root / JSONL_PATH)
    policy_doc = json.loads((repo_root / "config" / "skill_policy_matrix.json").read_text(encoding="utf-8"))
    normalized = normalize_rows(rows, policy_doc)
    render_or_check(repo_root / JSONL_PATH, dump_jsonl(normalized), args.check)
    render_or_check(repo_root / CSV_PATH, dump_csv(normalized), args.check)
    print(json.dumps({"status": "ok", "case_count": len(normalized), "check": args.check}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
