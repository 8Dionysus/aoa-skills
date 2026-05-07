#!/usr/bin/env python3
"""Audit authored skill bodies against evaluation, runtime, and lineage evidence."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

import skill_layout
import technique_bridge_tools


EXPECTED_HEADINGS = [
    "Intent",
    "Trigger boundary",
    "Inputs",
    "Outputs",
    "Procedure",
    "Contracts",
    "Risks and anti-patterns",
    "Verification",
    "Technique traceability",
    "Adaptation points",
]
RUNTIME_HEADINGS = EXPECTED_HEADINGS[:8]
PENDING_PATTERN = re.compile(r"\b(?:TODO|TBD|AOA-T-PENDING-[A-Z0-9-]+|placeholder)\b")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def section_text(skill_text: str, heading: str) -> str:
    lines = skill_text.splitlines()
    target = f"## {heading}"
    start: int | None = None
    end = len(lines)
    for index, line in enumerate(lines):
        if line.strip() == target:
            start = index + 1
            for next_index in range(index + 1, len(lines)):
                if lines[next_index].startswith("## "):
                    end = next_index
                    break
            break
    if start is None:
        return ""
    return "\n".join(lines[start:end]).strip()


def bullet_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip().startswith("- "))


def procedure_numbers(text: str) -> list[int]:
    numbers: list[int] = []
    for line in text.splitlines():
        match = re.match(r"\s*(\d+)\.\s+", line)
        if match:
            numbers.append(int(match.group(1)))
    return numbers


def duplicate_numbers(numbers: Sequence[int]) -> list[int]:
    counts = Counter(numbers)
    return sorted(number for number, count in counts.items() if count > 1)


def trigger_group_counts(trigger_text: str) -> dict[str, int]:
    groups = {"use": 0, "do_not_use": 0}
    current: str | None = None
    for raw_line in trigger_text.splitlines():
        line = raw_line.strip()
        if line == "Use this skill when:":
            current = "use"
            continue
        if line == "Do not use this skill when:":
            current = "do_not_use"
            continue
        if current and line.startswith("- "):
            groups[current] += 1
    return groups


def generated_by_name(repo_root: Path, relative_path: str) -> dict[str, Mapping[str, Any]]:
    data = load_json(repo_root / relative_path)
    rows = data.get("skills", [])
    if not isinstance(rows, list):
        return {}
    return {str(row["name"]): row for row in rows if isinstance(row, Mapping) and "name" in row}


def technique_dependency_ids(techniques_payload: Mapping[str, Any]) -> list[str]:
    deps: list[str] = []
    for entry in techniques_payload.get("techniques", []):
        if isinstance(entry, Mapping) and isinstance(entry.get("id"), str):
            deps.append(entry["id"])
    return deps


def body_metrics(skill_text: str) -> dict[str, Any]:
    headings = [line[3:].strip() for line in skill_text.splitlines() if line.startswith("## ")]
    missing_headings = [heading for heading in EXPECTED_HEADINGS if heading not in headings]
    extra_headings = [heading for heading in headings if heading not in EXPECTED_HEADINGS]
    sections = {heading: section_text(skill_text, heading) for heading in EXPECTED_HEADINGS}
    trigger_counts = trigger_group_counts(sections["Trigger boundary"])
    procedure_nums = procedure_numbers(sections["Procedure"])
    low_count_findings: list[str] = []
    count_specs = {
        "outputs": bullet_count(sections["Outputs"]),
        "contracts": bullet_count(sections["Contracts"]),
        "risks": bullet_count(sections["Risks and anti-patterns"]),
        "verification": bullet_count(sections["Verification"]),
    }
    for key, count in count_specs.items():
        if count < 4:
            low_count_findings.append(f"{key}_below_4")
    if trigger_counts["use"] == 0:
        low_count_findings.append("missing_use_trigger_bullets")
    if trigger_counts["do_not_use"] == 0:
        low_count_findings.append("missing_do_not_use_trigger_bullets")
    if len(procedure_nums) < 4:
        low_count_findings.append("procedure_below_4_steps")

    runtime_text = "\n".join(sections[heading] for heading in RUNTIME_HEADINGS)
    pending_markers = sorted(set(PENDING_PATTERN.findall(runtime_text)))
    return {
        "heading_count": len(headings),
        "missing_headings": missing_headings,
        "extra_headings": extra_headings,
        "trigger_bullets": trigger_counts,
        "inputs_count": bullet_count(sections["Inputs"]),
        "outputs_count": count_specs["outputs"],
        "procedure_step_count": len(procedure_nums),
        "procedure_duplicate_numbers": duplicate_numbers(procedure_nums),
        "contracts_count": count_specs["contracts"],
        "risks_count": count_specs["risks"],
        "verification_count": count_specs["verification"],
        "pending_markers": pending_markers,
        "runtime_line_count": len(runtime_text.splitlines()),
        "low_count_findings": low_count_findings,
    }


def support_artifact_kinds(bundle_entry: Mapping[str, Any]) -> list[str]:
    kinds: list[str] = []
    for artifact in bundle_entry.get("support_artifacts", []):
        if isinstance(artifact, Mapping):
            kind = artifact.get("kind") or artifact.get("type") or artifact.get("artifact_type")
            if isinstance(kind, str):
                kinds.append(kind)
    return kinds


def drift_record_payload(record: technique_bridge_tools.TechniqueDriftRecord) -> dict[str, str]:
    return {
        "technique_id": record.technique_id,
        "path": record.path,
        "pinned_ref": record.pinned_ref,
        "target_ref": record.target_ref,
        "state": record.state,
    }


def technique_drift_by_skill(
    *,
    repo_root: Path,
    techniques_repo: Path | None,
    target_ref: str,
) -> tuple[dict[str, list[dict[str, str]]], dict[str, Any]]:
    if techniques_repo is None:
        return {}, {"available": False, "reason": "skipped"}

    candidate = techniques_repo.expanduser()
    if not candidate.exists():
        return {}, {"available": False, "reason": f"missing techniques repo: {candidate}"}

    resolved_repo = technique_bridge_tools.resolve_techniques_repo(candidate)
    resolved_ref = technique_bridge_tools.resolve_git_ref(resolved_repo, target_ref)
    by_skill: dict[str, list[dict[str, str]]] = {}
    state_counts: Counter[str] = Counter()
    for bundle in technique_bridge_tools.resolve_skill_bundles(repo_root):
        records = technique_bridge_tools.collect_drift_records(
            resolved_repo,
            resolved_ref,
            bundle,
        )
        payloads = [drift_record_payload(record) for record in records]
        by_skill[bundle.skill_name] = payloads
        state_counts.update(record["state"] for record in payloads)
    return by_skill, {
        "available": True,
        "techniques_repo": str(resolved_repo),
        "target_ref": resolved_ref,
        "state_counts": dict(sorted(state_counts.items())),
    }


def build_skill_report(
    *,
    repo_root: Path,
    skill_name: str,
    bundle_entry: Mapping[str, Any],
    eval_entry: Mapping[str, Any],
    public_entry: Mapping[str, Any],
    governance_entry: Mapping[str, Any],
    runtime_entry: Mapping[str, Any],
    technique_drift_records: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    bundle_path = skill_layout.skill_bundle_path(repo_root, skill_name)
    if bundle_path is None:
        raise ValueError(f"unknown skill: {skill_name}")
    skill_text = bundle_path.skill_md_path.read_text(encoding="utf-8")
    techniques_payload = load_yaml(bundle_path.techniques_path)
    metrics = body_metrics(skill_text)
    technique_ids = technique_dependency_ids(techniques_payload)

    findings: list[str] = []
    findings.extend(metrics["low_count_findings"])
    if metrics["missing_headings"]:
        findings.append("missing_required_headings")
    if metrics["extra_headings"]:
        findings.append("unexpected_extra_headings")
    if metrics["procedure_duplicate_numbers"]:
        findings.append("duplicate_procedure_numbering")
    if metrics["pending_markers"]:
        findings.append("pending_markers_in_skill_body")
    if bundle_entry.get("lineage_state") == "pending":
        findings.append("pending_technique_lineage")
    if any(record.get("state") == "drifted" for record in technique_drift_records):
        findings.append("technique_source_drift")
    if int(eval_entry.get("autonomy_check_count", 0)) == 0:
        findings.append("missing_autonomy_check")
    if int(eval_entry.get("use_case_count", 0)) == 0:
        findings.append("missing_use_case")
    if int(eval_entry.get("do_not_use_case_count", 0)) == 0:
        findings.append("missing_do_not_use_case")
    if int(eval_entry.get("use_snapshot_count", 0)) == 0:
        findings.append("missing_use_snapshot")
    if int(eval_entry.get("do_not_use_snapshot_count", 0)) == 0:
        findings.append("missing_do_not_use_snapshot")
    if bundle_entry.get("status") == "evaluated" and not bundle_entry.get("promotion_review_path"):
        findings.append("missing_promotion_review")
    if bundle_entry.get("status") == "canonical" and not bundle_entry.get("candidate_review_path"):
        findings.append("missing_candidate_review")

    blocker_count = sum(
        1
        for finding in findings
        if finding
        in {
            "missing_required_headings",
            "missing_use_case",
            "missing_do_not_use_case",
            "missing_use_snapshot",
            "missing_do_not_use_snapshot",
            "missing_candidate_review",
        }
    )
    maintenance_count = len(findings) - blocker_count

    if blocker_count:
        verdict = "blocked"
    elif bundle_entry.get("status") == "scaffold":
        verdict = "working_scaffold_needs_promotion_review"
    elif maintenance_count:
        verdict = "working_with_maintenance_findings"
    else:
        verdict = "healthy"

    return {
        "name": skill_name,
        "skill_path": bundle_entry.get("skill_path"),
        "scope": bundle_entry.get("scope"),
        "status": bundle_entry.get("status"),
        "invocation_mode": bundle_entry.get("invocation_mode"),
        "lineage_state": bundle_entry.get("lineage_state"),
        "technique_dependencies": technique_ids,
        "technique_drift": {
            "records": list(technique_drift_records),
            "state_counts": dict(
                sorted(Counter(record.get("state", "unknown") for record in technique_drift_records).items())
            ),
        },
        "governance_decision": public_entry.get("governance_decision"),
        "readiness_reconciliation": governance_entry.get("readiness_reconciliation"),
        "runtime": {
            "allow_implicit_invocation": runtime_entry.get("allow_implicit_invocation"),
            "trust_posture": runtime_entry.get("trust_posture"),
            "mutation_surface": runtime_entry.get("mutation_surface"),
        },
        "evidence": {
            "autonomy_check_count": eval_entry.get("autonomy_check_count", 0),
            "use_case_count": eval_entry.get("use_case_count", 0),
            "do_not_use_case_count": eval_entry.get("do_not_use_case_count", 0),
            "use_snapshot_count": eval_entry.get("use_snapshot_count", 0),
            "do_not_use_snapshot_count": eval_entry.get("do_not_use_snapshot_count", 0),
            "selected_runtime_artifact_path": eval_entry.get("selected_runtime_artifact_path"),
            "promotion_review_path": bundle_entry.get("promotion_review_path"),
            "candidate_review_path": bundle_entry.get("candidate_review_path"),
            "support_artifact_kinds": support_artifact_kinds(bundle_entry),
        },
        "body": metrics,
        "findings": sorted(set(findings)),
        "verdict": verdict,
    }


def build_report(
    repo_root: Path,
    *,
    techniques_repo: Path | None = None,
    target_ref: str = "HEAD",
) -> dict[str, Any]:
    bundle = generated_by_name(repo_root, "generated/skill_bundle_index.json")
    evaluation = generated_by_name(repo_root, "generated/skill_evaluation_matrix.json")
    public = generated_by_name(repo_root, "generated/public_surface.json")
    governance = generated_by_name(repo_root, "generated/governance_backlog.json")
    runtime = generated_by_name(repo_root, "generated/runtime_discovery_index.json")
    names = skill_layout.discover_skill_names(repo_root)
    drift_by_skill, drift_summary = technique_drift_by_skill(
        repo_root=repo_root,
        techniques_repo=techniques_repo,
        target_ref=target_ref,
    )

    skills = [
        build_skill_report(
            repo_root=repo_root,
            skill_name=name,
            bundle_entry=bundle.get(name, {}),
            eval_entry=evaluation.get(name, {}),
            public_entry=public.get(name, {}),
            governance_entry=governance.get(name, {}),
            runtime_entry=runtime.get(name, {}),
            technique_drift_records=drift_by_skill.get(name, []),
        )
        for name in names
    ]
    verdicts = Counter(skill["verdict"] for skill in skills)
    findings = Counter(finding for skill in skills for finding in skill["findings"])
    return {
        "schema_version": 1,
        "report_kind": "skill_quality_audit",
        "source_of_truth": [
            "skills/**/SKILL.md",
            "skills/**/techniques.yaml",
            "tests/fixtures/skill_evaluation_cases.yaml",
            "generated/skill_bundle_index.json",
            "generated/skill_evaluation_matrix.json",
            "generated/runtime_discovery_index.json",
            "generated/public_surface.json",
            "generated/governance_backlog.json",
            "local aoa-techniques drift check",
        ],
        "skill_count": len(skills),
        "summary": {
            "verdicts": dict(sorted(verdicts.items())),
            "findings": dict(sorted(findings.items())),
            "technique_drift": drift_summary,
        },
        "upgrade_targets": [
            {
                "name": skill["name"],
                "status": skill["status"],
                "scope": skill["scope"],
                "verdict": skill["verdict"],
                "findings": skill["findings"],
            }
            for skill in skills
            if skill["findings"] or skill["verdict"] != "healthy"
        ],
        "skills": skills,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Skill Quality Audit",
        "",
        "This report audits authored skill bodies against evaluation fixtures,",
        "runtime discovery, support artifacts, governance status, and technique",
        "lineage. Generated surfaces are evidence; `skills/**/SKILL.md` and",
        "`techniques.yaml` remain the meaning source.",
        "",
        f"- skill count: {report['skill_count']}",
        "",
        "## Verdicts",
        "",
    ]
    for verdict, count in report["summary"]["verdicts"].items():
        lines.append(f"- `{verdict}`: {count}")
    drift_summary = report["summary"].get("technique_drift", {})
    if drift_summary.get("available"):
        drift_counts = drift_summary.get("state_counts", {})
        drift_bits = ", ".join(
            f"{state}={count}" for state, count in sorted(drift_counts.items())
        )
        lines.extend(
            [
                "",
                "## Technique Drift",
                "",
                f"- repo: `{drift_summary['techniques_repo']}`",
                f"- target ref: `{drift_summary['target_ref']}`",
                f"- states: {drift_bits or 'none'}",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## Technique Drift",
                "",
                f"- unavailable: {drift_summary.get('reason', 'not checked')}",
            ]
        )
    lines.extend(["", "## Findings", ""])
    if report["summary"]["findings"]:
        for finding, count in report["summary"]["findings"].items():
            lines.append(f"- `{finding}`: {count}")
    else:
        lines.append("- no findings")

    lines.extend(
        [
            "",
            "## Upgrade Targets",
            "",
            "| skill | status | scope | verdict | findings |",
            "|---|---|---|---|---|",
        ]
    )
    for target in report["upgrade_targets"]:
        findings = ", ".join(f"`{item}`" for item in target["findings"]) or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{target['name']}`",
                    f"`{target['status']}`",
                    f"`{target['scope']}`",
                    f"`{target['verdict']}`",
                    findings,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Skill Matrix",
            "",
            "| skill | status | lineage | technique drift | eval | body | runtime | verdict |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for skill in report["skills"]:
        evidence = skill["evidence"]
        body = skill["body"]
        drift_counts = skill["technique_drift"]["state_counts"]
        drift_bits = (
            "/".join(f"{state}{count}" for state, count in sorted(drift_counts.items()))
            or "-"
        )
        eval_bits = (
            f"a{evidence['autonomy_check_count']}/"
            f"u{evidence['use_case_count']}/"
            f"d{evidence['do_not_use_case_count']}/"
            f"su{evidence['use_snapshot_count']}/"
            f"sd{evidence['do_not_use_snapshot_count']}"
        )
        body_bits = (
            f"out{body['outputs_count']}/"
            f"c{body['contracts_count']}/"
            f"r{body['risks_count']}/"
            f"v{body['verification_count']}/"
            f"p{body['procedure_step_count']}"
        )
        runtime_bits = (
            f"{skill['runtime']['trust_posture']}, "
            f"{skill['runtime']['mutation_surface']}, "
            f"implicit={str(skill['runtime']['allow_implicit_invocation']).lower()}"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{skill['name']}`",
                    f"`{skill['status']}`",
                    f"`{skill['lineage_state']}`",
                    f"`{drift_bits}`",
                    f"`{eval_bits}`",
                    f"`{body_bits}`",
                    f"`{runtime_bits}`",
                    f"`{skill['verdict']}`",
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
    parser.add_argument("--repo-root", default=".", help="aoa-skills repository root")
    parser.add_argument(
        "--techniques-repo",
        default=None,
        help="Optional aoa-techniques checkout for technique drift evidence. Defaults to ../aoa-techniques when present.",
    )
    parser.add_argument("--target-ref", default="HEAD", help="aoa-techniques ref for drift evidence")
    parser.add_argument(
        "--skip-technique-drift",
        action="store_true",
        help="Skip local aoa-techniques drift evidence.",
    )
    parser.add_argument("--write-json", default=None, help="Optional JSON report path")
    parser.add_argument("--write-markdown", default=None, help="Optional Markdown report path")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument(
        "--fail-on-blocked",
        action="store_true",
        help="Return non-zero when any skill has a blocked verdict",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    techniques_repo = None
    if not args.skip_technique_drift:
        techniques_repo = (
            Path(args.techniques_repo).expanduser().resolve()
            if args.techniques_repo
            else repo_root.parent / "aoa-techniques"
        )
    report = build_report(
        repo_root,
        techniques_repo=techniques_repo,
        target_ref=args.target_ref,
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

    if args.fail_on_blocked and report["summary"]["verdicts"].get("blocked", 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
