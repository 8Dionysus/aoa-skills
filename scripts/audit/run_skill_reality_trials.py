#!/usr/bin/env python3
"""Run real repository skill-dispatch trials and report activation evidence."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class TrialCase:
    case_id: str
    repo: str
    intent: str
    expected: Mapping[str, Sequence[str]]
    purpose: str


TRIAL_CASES = [
    TrialCase(
        case_id="atm10_operator_dry_run_gate",
        repo="ATM10-Agent",
        intent=(
            "Before running an automation that may move the mouse or press keys, "
            "preview the operator action with a dry run and require explicit confirmation."
        ),
        expected={"must_confirm": ["aoa-dry-run-first", "aoa-approval-gate-check"]},
        purpose="Operator automation should route into explicit risk-ring gates before action.",
    ),
    TrialCase(
        case_id="aoa_skills_quality_audit",
        repo="aoa-skills",
        intent=(
            "Audit whether current skill evaluation cases actually constrain trigger boundaries, "
            "autonomy checks, and runtime activation quality for the authored skills."
        ),
        expected={"activate_now": ["aoa-invariant-coverage-audit"]},
        purpose="Skill-quality work should activate coverage-audit behavior inside aoa-skills.",
    ),
    TrialCase(
        case_id="aoa_downstream_source_truth",
        repo="Agents-of-Abyss",
        intent=(
            "Repository source-of-truth and workspace skill adoption posture check for "
            "downstream skill installation guidance."
        ),
        expected={"suggest_next": ["aoa-source-of-truth-check"]},
        purpose="Constitutional repo should keep downstream guidance tied to source-of-truth checks.",
    ),
    TrialCase(
        case_id="atm10_bounded_change",
        repo="ATM10-Agent",
        intent=(
            "Apply a bounded non-trivial ATM10 repository change with local verification, "
            "without touching unrelated user work."
        ),
        expected={"activate_now": ["aoa-change-protocol"]},
        purpose="Ordinary bounded repo mutation should activate the change protocol.",
    ),
]


def bucket_names(report: Mapping[str, Any], bucket: str) -> list[str]:
    values = report.get(bucket, [])
    if not isinstance(values, list):
        return []
    names: list[str] = []
    for item in values:
        if isinstance(item, Mapping) and isinstance(item.get("skill_name"), str):
            names.append(item["skill_name"])
    return names


def run_trial(workspace_root: Path, case: TrialCase) -> dict[str, Any]:
    repo_root = workspace_root / case.repo
    completed = subprocess.run(
        [
            "aoa",
            "skills",
            "enter",
            str(repo_root),
            "--root",
            str(workspace_root),
            "--intent-text",
            case.intent,
            "--json",
        ],
        cwd=workspace_root,
        text=True,
        capture_output=True,
        check=False,
    )
    parsed: dict[str, Any] | None = None
    if completed.stdout:
        try:
            parsed = json.loads(completed.stdout)
        except json.JSONDecodeError:
            parsed = None

    report = parsed.get("report", {}) if isinstance(parsed, Mapping) else {}
    actual = {
        "activate_now": bucket_names(report, "activate_now"),
        "must_confirm": bucket_names(report, "must_confirm"),
        "suggest_next": bucket_names(report, "suggest_next"),
        "blocked_actions": bucket_names(report, "blocked_actions"),
    }
    missing = {
        bucket: [name for name in expected_names if name not in actual.get(bucket, [])]
        for bucket, expected_names in case.expected.items()
    }
    missing = {bucket: names for bucket, names in missing.items() if names}
    return {
        "case_id": case.case_id,
        "purpose": case.purpose,
        "repo": case.repo,
        "intent": case.intent,
        "command_returncode": completed.returncode,
        "report_path": parsed.get("report_path") if isinstance(parsed, Mapping) else None,
        "expected": {bucket: list(names) for bucket, names in case.expected.items()},
        "actual": actual,
        "reasoning": report.get("reasoning", []) if isinstance(report, Mapping) else [],
        "host_inventory_provided": report.get("host_inventory_provided") if isinstance(report, Mapping) else None,
        "actionability_gaps": report.get("actionability_gaps", []) if isinstance(report, Mapping) else [],
        "missing_expected": missing,
        "stderr": completed.stderr.strip(),
        "verdict": "pass" if completed.returncode == 0 and not missing else "fail",
    }


def build_report(workspace_root: Path) -> dict[str, Any]:
    trials = [run_trial(workspace_root, case) for case in TRIAL_CASES]
    verdicts = {
        "pass": sum(1 for trial in trials if trial["verdict"] == "pass"),
        "fail": sum(1 for trial in trials if trial["verdict"] == "fail"),
    }
    return {
        "schema_version": 1,
        "report_kind": "skill_reality_trials",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace_root": str(workspace_root),
        "trial_count": len(trials),
        "summary": {"verdicts": verdicts},
        "trials": trials,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Skill Reality Trials",
        "",
        "This report is execution evidence for real repository skill dispatch.",
        "It checks that authored skills are not only present, but selectable in",
        "the repository contexts where future agents are expected to use them.",
        "Generated dispatch reports are evidence, not source authority.",
        "",
        f"- trial count: {report['trial_count']}",
        f"- pass: {report['summary']['verdicts']['pass']}",
        f"- fail: {report['summary']['verdicts']['fail']}",
        "",
        "## Trials",
        "",
        "| case | repo | expected | actual | verdict |",
        "|---|---|---|---|---|",
    ]
    for trial in report["trials"]:
        expected = "; ".join(
            f"{bucket}={','.join(names)}" for bucket, names in trial["expected"].items()
        )
        actual_parts = []
        for bucket in ("activate_now", "must_confirm", "suggest_next", "blocked_actions"):
            names = trial["actual"].get(bucket, [])
            if names:
                actual_parts.append(f"{bucket}={','.join(names)}")
        actual = "; ".join(actual_parts) or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{trial['case_id']}`",
                    f"`{trial['repo']}`",
                    f"`{expected}`",
                    f"`{actual}`",
                    f"`{trial['verdict']}`",
                ]
            )
            + " |"
        )

    lines.extend(["", "## Reading", ""])
    for trial in report["trials"]:
        lines.append(f"### {trial['case_id']}")
        lines.append("")
        lines.append(trial["purpose"])
        lines.append("")
        lines.append(f"- report path: `{trial['report_path']}`")
        lines.append(f"- host inventory: `{trial['host_inventory_provided']}`")
        if trial["actionability_gaps"]:
            gaps = ", ".join(f"`{gap}`" for gap in trial["actionability_gaps"])
            lines.append(f"- actionability gaps: {gaps}")
        else:
            lines.append("- actionability gaps: none")
        for reason in trial["reasoning"]:
            lines.append(f"- {reason}")
        lines.append("")
    return "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", default="/srv/AbyssOS")
    parser.add_argument("--write-json", default=None)
    parser.add_argument("--write-markdown", default=None)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--fail-on-failed-trial", action="store_true")
    args = parser.parse_args()

    workspace_root = Path(args.workspace_root).expanduser().resolve()
    report = build_report(workspace_root)
    json_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    markdown_text = render_markdown(report) + "\n"
    if args.write_json:
        write_text(Path(args.write_json), json_text)
    if args.write_markdown:
        write_text(Path(args.write_markdown), markdown_text)
    if args.format == "json":
        print(json_text, end="")
    else:
        print(markdown_text, end="")
    if args.fail_on_failed_trial and report["summary"]["verdicts"]["fail"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
