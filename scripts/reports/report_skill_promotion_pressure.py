#!/usr/bin/env python3
"""Report promotion pressure from quality, governance, adoption, and runtime evidence."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from skill_model import skill_layout


DEFAULT_WORKSPACE_ROOT = Path("/srv/AbyssOS")
DEFAULT_SESSIONS_ROOT = Path.home() / ".codex" / "sessions"
DEFAULT_HOOKS_ROOT = DEFAULT_WORKSPACE_ROOT / ".codex" / "generated" / "codex" / "hooks"
DEFAULT_DISPATCH_ROOT = DEFAULT_WORKSPACE_ROOT / "aoa-sdk" / ".aoa" / "skill-dispatch"

GENERATED_DIR = Path("generated")
PUBLIC_SURFACE_PATH = GENERATED_DIR / "public_surface.json"
GOVERNANCE_BACKLOG_PATH = GENERATED_DIR / "governance_backlog.json"
QUALITY_AUDIT_PATH = GENERATED_DIR / "skill_quality_audit.json"
ADOPTION_AUDIT_PATH = GENERATED_DIR / "workspace_skill_adoption_audit.json"
REALITY_TRIALS_PATH = GENERATED_DIR / "skill_reality_trials.json"
PROMOTION_PRESSURE_JSON_PATH = GENERATED_DIR / "skill_promotion_pressure.json"
PROMOTION_PRESSURE_MARKDOWN_PATH = GENERATED_DIR / "skill_promotion_pressure.md"

HARD_PROMOTION_FINDINGS = {
    "implicit_policy_collapse",
    "missing_portable_checks_examples",
    "missing_runtime_card",
    "missing_candidate_review",
    "missing_do_not_use_case",
    "missing_do_not_use_snapshot",
    "missing_required_headings",
    "missing_use_case",
    "missing_use_snapshot",
    "pending_markers_in_skill_body",
    "unapproved_codex_source_wording",
    "unsupported_canonical_promotion",
}
SESSION_EVENT_TYPES = {"event_msg", "response_item"}
PROMOTION_BUCKETS = (
    "activate_now",
    "must_confirm",
    "suggest_next",
    "blocked_actions",
)


@dataclass(frozen=True)
class ScanResult:
    counts: dict[str, int]
    files_scanned: int


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: Path) -> Any | None:
    try:
        return load_json(path)
    except FileNotFoundError:
        return None


def rows_by_name(payload: Mapping[str, Any] | None) -> dict[str, Mapping[str, Any]]:
    if not isinstance(payload, Mapping):
        return {}
    rows = payload.get("skills", [])
    if not isinstance(rows, list):
        return {}
    return {
        str(row["name"]): row
        for row in rows
        if isinstance(row, Mapping) and isinstance(row.get("name"), str)
    }


def compile_skill_patterns(skill_names: Sequence[str]) -> dict[str, re.Pattern[str]]:
    return {
        name: re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])")
        for name in skill_names
    }


def count_mentions(text: str, patterns: Mapping[str, re.Pattern[str]]) -> dict[str, int]:
    return {
        name: len(pattern.findall(text))
        for name, pattern in patterns.items()
        if pattern.search(text)
    }


def add_counts(target: dict[str, int], source: Mapping[str, int]) -> None:
    for name, count in source.items():
        target[name] = target.get(name, 0) + int(count)


def iter_message_texts(event: Mapping[str, Any]) -> Iterable[str]:
    event_type = event.get("type")
    payload = event.get("payload")
    if not isinstance(payload, Mapping) or event_type not in SESSION_EVENT_TYPES:
        return

    if event_type == "event_msg" and payload.get("type") == "user_message":
        message = payload.get("message")
        if isinstance(message, str):
            yield message
        return

    if event_type != "response_item":
        return
    if payload.get("role") != "assistant" or payload.get("type") != "message":
        return
    content = payload.get("content")
    if not isinstance(content, list):
        return
    for item in content:
        if not isinstance(item, Mapping):
            continue
        text = item.get("text")
        if isinstance(text, str):
            yield text


def scan_session_mentions(
    sessions_root: Path,
    patterns: Mapping[str, re.Pattern[str]],
) -> ScanResult:
    counts: dict[str, int] = {}
    files_scanned = 0
    if not sessions_root.is_dir():
        return ScanResult(counts, files_scanned)
    for path in sorted(sessions_root.rglob("*.jsonl")):
        files_scanned += 1
        try:
            handle = path.open(encoding="utf-8")
        except OSError:
            continue
        with handle:
            for raw_line in handle:
                try:
                    event = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(event, Mapping):
                    continue
                for text in iter_message_texts(event):
                    add_counts(counts, count_mentions(text, patterns))
    return ScanResult(counts, files_scanned)


def scan_hook_prompt_mentions(
    hooks_root: Path,
    patterns: Mapping[str, re.Pattern[str]],
) -> ScanResult:
    counts: dict[str, int] = {}
    files_scanned = 0
    if not hooks_root.is_dir():
        return ScanResult(counts, files_scanned)
    for path in sorted(hooks_root.glob("*.json")):
        files_scanned += 1
        try:
            payload = load_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, Mapping):
            continue
        event = payload.get("event")
        if not isinstance(event, Mapping):
            continue
        prompt = event.get("prompt")
        if isinstance(prompt, str):
            add_counts(counts, count_mentions(prompt, patterns))
    return ScanResult(counts, files_scanned)


def collect_dispatch_counts(dispatch_root: Path) -> tuple[dict[str, Counter[str]], int]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    files_scanned = 0
    if not dispatch_root.is_dir():
        return counts, files_scanned
    for path in sorted(dispatch_root.glob("*.json")):
        files_scanned += 1
        try:
            payload = load_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, Mapping):
            continue
        report = payload.get("report")
        if not isinstance(report, Mapping):
            continue
        for bucket in PROMOTION_BUCKETS:
            rows = report.get(bucket, [])
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, Mapping):
                    continue
                skill_name = row.get("skill_name")
                if isinstance(skill_name, str):
                    counts[skill_name][bucket] += 1
    return counts, files_scanned


def collect_reality_trial_counts(payload: Mapping[str, Any] | None) -> dict[str, Counter[str]]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    if not isinstance(payload, Mapping):
        return counts
    trials = payload.get("trials", [])
    if not isinstance(trials, list):
        return counts
    for trial in trials:
        if not isinstance(trial, Mapping):
            continue
        actual = trial.get("actual", {})
        if not isinstance(actual, Mapping):
            continue
        for bucket in PROMOTION_BUCKETS:
            names = actual.get(bucket, [])
            if not isinstance(names, list):
                continue
            for name in names:
                if isinstance(name, str):
                    counts[name][bucket] += 1
    return counts


def collect_installed_target_counts(
    adoption_payload: Mapping[str, Any] | None,
    skill_names: Sequence[str],
) -> tuple[dict[str, int], int]:
    counts: dict[str, int] = {name: 0 for name in skill_names}
    if not isinstance(adoption_payload, Mapping):
        return counts, 0
    skill_name_set = set(skill_names)
    targets = adoption_payload.get("targets", [])
    if not isinstance(targets, list):
        return counts, 0
    scanned = 0
    for target in targets:
        if not isinstance(target, Mapping):
            continue
        install_root_raw = target.get("install_root")
        if not isinstance(install_root_raw, str):
            continue
        install_root = Path(install_root_raw)
        if not install_root.is_dir():
            continue
        scanned += 1
        for child in install_root.iterdir():
            if child.is_dir() and child.name in skill_name_set:
                counts[child.name] += 1
    return counts, scanned


def counter_total(counter: Mapping[str, int]) -> int:
    return sum(int(value) for value in counter.values())


def usage_score(
    *,
    installed_targets: int,
    dispatch_total: int,
    reality_total: int,
    session_mentions: int,
    hook_mentions: int,
) -> int:
    return (
        installed_targets
        + (dispatch_total * 3)
        + (reality_total * 4)
        + min(session_mentions, 25)
        + min(hook_mentions, 10)
    )


def has_repeated_usage_signal(entry: Mapping[str, Any]) -> bool:
    evidence = entry["usage_evidence"]
    channels = 0
    for key in (
        "installed_target_count",
        "dispatch_event_count",
        "reality_trial_event_count",
        "session_mention_count",
        "hook_prompt_mention_count",
    ):
        if int(evidence.get(key, 0)) > 0:
            channels += 1
    return channels >= 2 or int(evidence["usage_score"]) >= 5


def pressure_classification(
    *,
    status: str,
    scope: str,
    quality_verdict: str,
    quality_findings: Sequence[str],
    default_reference_readiness: str | None,
    governance_decision: str | None,
    repeated_usage: bool,
) -> tuple[str, str]:
    hard_findings = sorted(set(quality_findings) & HARD_PROMOTION_FINDINGS)
    if status == "canonical":
        return "canonical_monitor", "already canonical; keep maintenance and drift visible"
    if scope == "project":
        if repeated_usage and quality_verdict != "blocked":
            return "overlay_adoption_review", "project overlay use should route to owner adoption review"
        return "overlay_watch", "project overlay is not a core canonical-reference candidate by default"
    if quality_verdict == "blocked" or hard_findings:
        if repeated_usage:
            return "blockers_first", "usage exists, but promotion review must clear hard blockers first"
        return "blocked_no_pressure", "hard blockers remain before promotion pressure matters"
    if default_reference_readiness == "ready":
        if governance_decision == "stay_evaluated" and repeated_usage:
            return "revisit_stay_evaluated", "usage pressure justifies revisiting the stay_evaluated decision"
        if repeated_usage:
            return "canonical_review_now", "machine gates and usage pressure justify canonical review"
        return "candidate_ready_watch", "machine gates pass, but usage pressure is still weak"
    if repeated_usage:
        return "promotion_review_now", "usage pressure should open the next status/promotion review"
    return "watch", "no repeated usage pressure yet"


def build_report(
    *,
    repo_root: Path,
    workspace_root: Path,
    sessions_root: Path | None,
    hooks_root: Path | None,
    dispatch_root: Path | None,
) -> dict[str, Any]:
    skill_names = skill_layout.discover_skill_names(repo_root)
    patterns = compile_skill_patterns(skill_names)
    public_by_name = rows_by_name(load_json(repo_root / PUBLIC_SURFACE_PATH))
    governance_by_name = rows_by_name(load_json(repo_root / GOVERNANCE_BACKLOG_PATH))
    quality_by_name = rows_by_name(load_json(repo_root / QUALITY_AUDIT_PATH))
    adoption_payload = load_optional_json(repo_root / ADOPTION_AUDIT_PATH)
    reality_payload = load_optional_json(repo_root / REALITY_TRIALS_PATH)

    session_scan = (
        scan_session_mentions(sessions_root, patterns)
        if sessions_root is not None
        else ScanResult({}, 0)
    )
    hook_scan = (
        scan_hook_prompt_mentions(hooks_root, patterns)
        if hooks_root is not None
        else ScanResult({}, 0)
    )
    dispatch_counts, dispatch_files = (
        collect_dispatch_counts(dispatch_root)
        if dispatch_root is not None
        else ({}, 0)
    )
    reality_counts = collect_reality_trial_counts(reality_payload)
    installed_counts, adoption_targets_scanned = collect_installed_target_counts(
        adoption_payload,
        skill_names,
    )

    skills: list[dict[str, Any]] = []
    for name in skill_names:
        public_entry = public_by_name.get(name, {})
        governance_entry = governance_by_name.get(name, {})
        quality_entry = quality_by_name.get(name, {})
        dispatch_counter = dispatch_counts.get(name, Counter())
        reality_counter = reality_counts.get(name, Counter())
        dispatch_total = counter_total(dispatch_counter)
        reality_total = counter_total(reality_counter)
        session_mentions = session_scan.counts.get(name, 0)
        hook_mentions = hook_scan.counts.get(name, 0)
        installed_targets = installed_counts.get(name, 0)
        score = usage_score(
            installed_targets=installed_targets,
            dispatch_total=dispatch_total,
            reality_total=reality_total,
            session_mentions=session_mentions,
            hook_mentions=hook_mentions,
        )
        usage = {
            "installed_target_count": installed_targets,
            "dispatch_event_count": dispatch_total,
            "dispatch_buckets": dict(sorted(dispatch_counter.items())),
            "reality_trial_event_count": reality_total,
            "reality_trial_buckets": dict(sorted(reality_counter.items())),
            "session_mention_count": session_mentions,
            "hook_prompt_mention_count": hook_mentions,
            "usage_score": score,
        }
        status = str(public_entry.get("status") or governance_entry.get("status") or "")
        scope = str(public_entry.get("scope") or governance_entry.get("scope") or "")
        quality_verdict = str(quality_entry.get("verdict") or "unknown")
        quality_findings = [
            str(finding)
            for finding in quality_entry.get("findings", [])
            if isinstance(finding, str)
        ]
        repeated_usage = has_repeated_usage_signal({"usage_evidence": usage})
        pressure, reason = pressure_classification(
            status=status,
            scope=scope,
            quality_verdict=quality_verdict,
            quality_findings=quality_findings,
            default_reference_readiness=public_entry.get("default_reference_readiness"),
            governance_decision=public_entry.get("governance_decision"),
            repeated_usage=repeated_usage,
        )
        skills.append(
            {
                "name": name,
                "status": status,
                "scope": scope,
                "skill_path": public_entry.get("skill_path") or quality_entry.get("skill_path"),
                "lineage_state": public_entry.get("lineage_state"),
                "technique_bridge_findings": list(
                    public_entry.get("technique_bridge_findings", [])
                ),
                "default_reference_readiness": public_entry.get(
                    "default_reference_readiness"
                ),
                "default_reference_readiness_blockers": list(
                    public_entry.get("default_reference_readiness_blockers", [])
                ),
                "governance_decision": public_entry.get("governance_decision"),
                "readiness_reconciliation": governance_entry.get(
                    "readiness_reconciliation"
                ),
                "quality_verdict": quality_verdict,
                "quality_findings": quality_findings,
                "usage_evidence": usage,
                "repeated_usage_signal": repeated_usage,
                "promotion_pressure": pressure,
                "pressure_reason": reason,
            }
        )

    pressure_counts = Counter(skill["promotion_pressure"] for skill in skills)
    return {
        "schema_version": 1,
        "report_kind": "skill_promotion_pressure",
        "source_of_truth": {
            "status_and_governance": PUBLIC_SURFACE_PATH.as_posix(),
            "governance_backlog": GOVERNANCE_BACKLOG_PATH.as_posix(),
            "skill_quality": QUALITY_AUDIT_PATH.as_posix(),
            "workspace_adoption": ADOPTION_AUDIT_PATH.as_posix(),
            "reality_trials": REALITY_TRIALS_PATH.as_posix(),
            "sessions_root": str(sessions_root) if sessions_root else None,
            "hooks_root": str(hooks_root) if hooks_root else None,
            "dispatch_root": str(dispatch_root) if dispatch_root else None,
        },
        "workspace_root": str(workspace_root),
        "skill_count": len(skills),
        "scan_summary": {
            "session_files_scanned": session_scan.files_scanned,
            "hook_files_scanned": hook_scan.files_scanned,
            "dispatch_files_scanned": dispatch_files,
            "adoption_targets_scanned": adoption_targets_scanned,
        },
        "summary": {
            "pressure_counts": dict(sorted(pressure_counts.items())),
            "review_pressure": sorted(
                skill["name"]
                for skill in skills
                if skill["promotion_pressure"]
                in {
                    "canonical_review_now",
                    "promotion_review_now",
                    "revisit_stay_evaluated",
                    "overlay_adoption_review",
                }
            ),
            "blockers_first": sorted(
                skill["name"]
                for skill in skills
                if skill["promotion_pressure"] == "blockers_first"
            ),
        },
        "skills": sorted(
            skills,
            key=lambda item: (
                str(item["promotion_pressure"]),
                -int(item["usage_evidence"]["usage_score"]),
                str(item["name"]),
            ),
        ),
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Skill Promotion Pressure",
        "",
        "This derived report connects lived usage evidence to the formal",
        "promotion path. It does not promote skills automatically. It makes",
        "review pressure visible so scaffold/evaluated skills that are already",
        "used across the workspace do not depend on manual memory.",
        "",
        "## Summary",
        "",
        f"- skill count: {report['skill_count']}",
        f"- session files scanned: {report['scan_summary']['session_files_scanned']}",
        f"- hook files scanned: {report['scan_summary']['hook_files_scanned']}",
        f"- dispatch files scanned: {report['scan_summary']['dispatch_files_scanned']}",
        f"- adoption targets scanned: {report['scan_summary']['adoption_targets_scanned']}",
        "",
        "## Pressure Counts",
        "",
    ]
    for pressure, count in report["summary"]["pressure_counts"].items():
        lines.append(f"- `{pressure}`: {count}")
    lines.extend(
        [
            "",
            "## Review Pressure",
            "",
            ", ".join(f"`{name}`" for name in report["summary"]["review_pressure"])
            or "-",
            "",
            "## Blockers First",
            "",
            ", ".join(f"`{name}`" for name in report["summary"]["blockers_first"])
            or "-",
            "",
            "## Skill Matrix",
            "",
            "| skill | status | pressure | use score | installed | dispatch | trials | sessions | hooks | quality | blockers/findings |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---|---|",
        ]
    )
    for skill in report["skills"]:
        usage = skill["usage_evidence"]
        blockers = skill.get("default_reference_readiness_blockers", [])
        findings = skill.get("quality_findings", [])
        notes = (
            ", ".join(
                f"`{item}`" for item in sorted(set([*blockers, *findings]))
            )
            or "-"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{skill['name']}`",
                    f"`{skill['status']}`",
                    f"`{skill['promotion_pressure']}`",
                    str(usage["usage_score"]),
                    str(usage["installed_target_count"]),
                    str(usage["dispatch_event_count"]),
                    str(usage["reality_trial_event_count"]),
                    str(usage["session_mention_count"]),
                    str(usage["hook_prompt_mention_count"]),
                    f"`{skill['quality_verdict']}`",
                    notes,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--sessions-root", default=str(DEFAULT_SESSIONS_ROOT))
    parser.add_argument("--hooks-root", default=None)
    parser.add_argument("--dispatch-root", default=None)
    parser.add_argument("--skip-session-scan", action="store_true")
    parser.add_argument("--skip-hooks-scan", action="store_true")
    parser.add_argument("--skip-dispatch-scan", action="store_true")
    parser.add_argument("--write-json", default=None)
    parser.add_argument("--write-markdown", default=None)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    hooks_root = (
        Path(args.hooks_root).expanduser().resolve()
        if args.hooks_root
        else workspace_root / ".codex" / "generated" / "codex" / "hooks"
    )
    dispatch_root = (
        Path(args.dispatch_root).expanduser().resolve()
        if args.dispatch_root
        else workspace_root / "aoa-sdk" / ".aoa" / "skill-dispatch"
    )
    report = build_report(
        repo_root=repo_root,
        workspace_root=workspace_root,
        sessions_root=None
        if args.skip_session_scan
        else Path(args.sessions_root).expanduser().resolve(),
        hooks_root=None if args.skip_hooks_scan else hooks_root,
        dispatch_root=None if args.skip_dispatch_scan else dispatch_root,
    )
    json_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    markdown_text = render_markdown(report)
    if args.write_json:
        write_text(Path(args.write_json), json_text)
    if args.write_markdown:
        write_text(Path(args.write_markdown), markdown_text)
    if args.format == "json":
        print(json_text, end="")
    else:
        print(markdown_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
