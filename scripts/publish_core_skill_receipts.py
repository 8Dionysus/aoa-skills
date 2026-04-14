#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
KERNEL_MANIFEST_PATH = REPO_ROOT / "config" / "project_core_skill_kernel.json"
DEFAULT_LOG_PATH = REPO_ROOT / ".aoa" / "live_receipts" / "core-skill-applications.jsonl"
ALLOWED_DETAIL_EVENT_KINDS = {
    "automation_candidate_receipt",
    "checkpoint_closeout_execution_report",
    "decision_fork_receipt",
    "diagnosis_packet_receipt",
    "harvest_packet_receipt",
    "progression_delta_receipt",
    "quest_promotion_receipt",
    "repair_cycle_receipt",
}
ALLOWED_OWNER_REPOS = {
    "aoa-techniques",
    "aoa-skills",
    "aoa-evals",
    "aoa-memo",
    "aoa-playbooks",
    "aoa-agents",
}
ALLOWED_HANDOFF_TARGETS = {
    "aoa-session-donor-harvest",
    "aoa-automation-opportunity-scan",
    "aoa-session-route-forks",
    "aoa-session-self-diagnose",
    "aoa-session-self-repair",
    "aoa-session-progression-lift",
    "aoa-quest-harvest",
}
ALLOWED_AUTHORITY_CONTRACT_FIELDS = {
    "contract",
    "bridge_output",
    "checkpoint_notes",
    "reviewed_artifact",
    "agent_skill_application",
}


class ReceiptPublishError(ValueError):
    pass


def load_kernel_manifest() -> tuple[str, dict[str, str]]:
    payload = json.loads(KERNEL_MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: kernel manifest must be an object")
    kernel_id = payload.get("kernel_id")
    skills = payload.get("skills")
    skill_contracts = payload.get("skill_contracts")
    if not isinstance(kernel_id, str) or not kernel_id:
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: kernel_id must be a non-empty string")
    if not isinstance(skills, list) or not skills:
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: skills must be a non-empty list")
    skill_names = {skill for skill in skills if isinstance(skill, str) and skill}
    if len(skill_names) != len(skills):
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: skills must be non-empty strings without duplicates")
    if not isinstance(skill_contracts, list) or not skill_contracts:
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: skill_contracts must be a non-empty list")

    detail_event_kind_by_skill: dict[str, str] = {}
    for index, entry in enumerate(skill_contracts):
        if not isinstance(entry, dict):
            raise ReceiptPublishError(
                f"{KERNEL_MANIFEST_PATH}: skill_contracts[{index}] must be an object"
            )
        skill_name = entry.get("skill_name")
        detail_event_kind = entry.get("detail_event_kind")
        if not isinstance(skill_name, str) or not skill_name:
            raise ReceiptPublishError(
                f"{KERNEL_MANIFEST_PATH}: skill_contracts[{index}].skill_name must be a non-empty string"
            )
        if skill_name not in skill_names:
            raise ReceiptPublishError(
                f"{KERNEL_MANIFEST_PATH}: skill_contracts[{index}].skill_name must be declared in skills"
            )
        if skill_name in detail_event_kind_by_skill:
            raise ReceiptPublishError(
                f"{KERNEL_MANIFEST_PATH}: duplicate skill_contract entry for {skill_name!r}"
            )
        if not isinstance(detail_event_kind, str) or not detail_event_kind:
            raise ReceiptPublishError(
                f"{KERNEL_MANIFEST_PATH}: skill_contracts[{index}].detail_event_kind must be a non-empty string"
            )
        if detail_event_kind not in ALLOWED_DETAIL_EVENT_KINDS:
            raise ReceiptPublishError(
                f"{KERNEL_MANIFEST_PATH}: skill_contracts[{index}].detail_event_kind must be one of "
                f"{sorted(ALLOWED_DETAIL_EVENT_KINDS)!r}"
            )
        detail_event_kind_by_skill[skill_name] = detail_event_kind
    if set(detail_event_kind_by_skill) != skill_names:
        raise ReceiptPublishError(
            f"{KERNEL_MANIFEST_PATH}: skill_contracts must cover every kernel skill exactly once"
        )
    return kernel_id, detail_event_kind_by_skill


KERNEL_ID, KERNEL_DETAIL_EVENT_KIND_BY_SKILL = load_kernel_manifest()
KERNEL_SKILLS = set(KERNEL_DETAIL_EVENT_KIND_BY_SKILL)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append bounded project-core kernel receipts to the owner-local live JSONL log."
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="Path to a JSON or JSONL file containing one receipt, an array of receipts, or one receipt per line.",
    )
    parser.add_argument(
        "--log-path",
        default=str(DEFAULT_LOG_PATH),
        help="Owner-local JSONL log that should receive newly published core skill receipts.",
    )
    return parser.parse_args(argv)


def validate_surface_detection_context(context: dict[str, Any], *, location: str) -> None:
    allowed_fields = {
        "activation_truth",
        "adjacent_owner_repos",
        "owner_layer_ambiguity",
        "shortlist_confidence",
        "detail_to_closeout_ref",
        "surface_detection_report_ref",
        "surface_closeout_handoff_ref",
        "family_entry_refs",
        "candidate_counts",
        "suggested_handoff_targets",
        "repeated_pattern_signal",
        "promotion_discussion_required",
    }
    extra = sorted(field for field in context if field not in allowed_fields)
    if extra:
        raise ReceiptPublishError(
            f"{location}: unsupported surface_detection_context fields {extra!r}"
        )

    activation_truth = context.get("activation_truth")
    if activation_truth is not None and (
        not isinstance(activation_truth, str)
        or activation_truth not in {"activated", "manual-equivalent-adjacent"}
    ):
        raise ReceiptPublishError(
            f"{location}.activation_truth: must be omitted or one of "
            f"{['activated', 'manual-equivalent-adjacent']!r}"
        )

    adjacent_owner_repos = context.get("adjacent_owner_repos")
    if adjacent_owner_repos is not None:
        if not isinstance(adjacent_owner_repos, list) or not adjacent_owner_repos:
            raise ReceiptPublishError(
                f"{location}.adjacent_owner_repos: must be omitted or a non-empty list"
            )
        if any(not isinstance(repo, str) or not repo for repo in adjacent_owner_repos):
            raise ReceiptPublishError(
                f"{location}.adjacent_owner_repos: must contain unique non-empty strings"
            )
        normalized_repos = set(adjacent_owner_repos)
        if len(normalized_repos) != len(adjacent_owner_repos):
            raise ReceiptPublishError(
                f"{location}.adjacent_owner_repos: must contain unique non-empty strings"
            )
        unsupported_repos = sorted(normalized_repos - ALLOWED_OWNER_REPOS)
        if unsupported_repos:
            raise ReceiptPublishError(
                f"{location}.adjacent_owner_repos: unsupported repos {unsupported_repos!r}"
            )

    owner_layer_ambiguity = context.get("owner_layer_ambiguity")
    if owner_layer_ambiguity is not None and not isinstance(owner_layer_ambiguity, bool):
        raise ReceiptPublishError(
            f"{location}.owner_layer_ambiguity: must be omitted or a boolean"
        )

    shortlist_confidence = context.get("shortlist_confidence")
    if shortlist_confidence is not None and shortlist_confidence not in {"low", "medium", "high"}:
        raise ReceiptPublishError(
            f"{location}.shortlist_confidence: must be omitted or one of {['low', 'medium', 'high']!r}"
        )

    for field in (
        "detail_to_closeout_ref",
        "surface_detection_report_ref",
        "surface_closeout_handoff_ref",
    ):
        value = context.get(field)
        if value is not None and (not isinstance(value, str) or not value):
            raise ReceiptPublishError(
                f"{location}.{field}: must be omitted or a non-empty string"
            )

    family_entry_refs = context.get("family_entry_refs")
    if family_entry_refs is not None:
        if not isinstance(family_entry_refs, list) or not family_entry_refs:
            raise ReceiptPublishError(
                f"{location}.family_entry_refs: must be omitted or a non-empty list"
            )
        if any(not isinstance(ref, str) or not ref for ref in family_entry_refs):
            raise ReceiptPublishError(
                f"{location}.family_entry_refs: must contain only non-empty strings"
            )
        if len(set(family_entry_refs)) != len(family_entry_refs):
            raise ReceiptPublishError(
                f"{location}.family_entry_refs: duplicate refs are not allowed"
            )

    candidate_counts = context.get("candidate_counts")
    if candidate_counts is not None:
        if not isinstance(candidate_counts, dict):
            raise ReceiptPublishError(
                f"{location}.candidate_counts: must be omitted or an object"
            )
        extra_candidate_fields = sorted(
            field for field in candidate_counts if field not in {"candidate_now", "candidate_later"}
        )
        if extra_candidate_fields:
            raise ReceiptPublishError(
                f"{location}.candidate_counts: unsupported fields {extra_candidate_fields!r}"
            )
        for field in ("candidate_now", "candidate_later"):
            value = candidate_counts.get(field)
            if value is not None and (type(value) is not int or value < 0):
                raise ReceiptPublishError(
                    f"{location}.candidate_counts.{field}: must be omitted or a non-negative integer"
                )

    suggested_handoff_targets = context.get("suggested_handoff_targets")
    if suggested_handoff_targets is not None:
        if not isinstance(suggested_handoff_targets, list) or not suggested_handoff_targets:
            raise ReceiptPublishError(
                f"{location}.suggested_handoff_targets: must be omitted or a non-empty list"
            )
        if any(not isinstance(skill_name, str) or not skill_name for skill_name in suggested_handoff_targets):
            raise ReceiptPublishError(
                f"{location}.suggested_handoff_targets: must contain unique non-empty strings"
            )
        normalized_targets = set(suggested_handoff_targets)
        if len(normalized_targets) != len(suggested_handoff_targets):
            raise ReceiptPublishError(
                f"{location}.suggested_handoff_targets: must contain unique non-empty strings"
            )
        unsupported_targets = sorted(normalized_targets - ALLOWED_HANDOFF_TARGETS)
        if unsupported_targets:
            raise ReceiptPublishError(
                f"{location}.suggested_handoff_targets: unsupported targets {unsupported_targets!r}"
            )

    for field in ("repeated_pattern_signal", "promotion_discussion_required"):
        value = context.get(field)
        if value is not None and not isinstance(value, bool):
            raise ReceiptPublishError(
                f"{location}.{field}: must be omitted or a boolean"
            )


def validate_authority_contract(contract: dict[str, Any], *, location: str) -> None:
    extra = sorted(field for field in contract if field not in ALLOWED_AUTHORITY_CONTRACT_FIELDS)
    if extra:
        raise ReceiptPublishError(f"{location}: unsupported authority_contract fields {extra!r}")
    for field in ALLOWED_AUTHORITY_CONTRACT_FIELDS:
        value = contract.get(field)
        if value is not None and (not isinstance(value, str) or not value):
            raise ReceiptPublishError(
                f"{location}.{field}: must be omitted or a non-empty string"
            )


def validate_receipt(receipt: dict[str, Any], *, location: str) -> None:
    required_fields = (
        "event_kind",
        "event_id",
        "observed_at",
        "run_ref",
        "session_ref",
        "actor_ref",
        "object_ref",
        "evidence_refs",
        "payload",
    )
    for field in required_fields:
        if field not in receipt:
            raise ReceiptPublishError(f"{location}: missing field {field!r}")
    if receipt["event_kind"] != "core_skill_application_receipt":
        raise ReceiptPublishError(
            f"{location}.event_kind: unsupported core receipt kind {receipt['event_kind']!r}"
        )
    if not isinstance(receipt["event_id"], str) or not receipt["event_id"]:
        raise ReceiptPublishError(f"{location}.event_id: must be a non-empty string")
    if not isinstance(receipt["object_ref"], dict):
        raise ReceiptPublishError(f"{location}.object_ref: must be an object")
    if receipt["object_ref"].get("repo") != "aoa-skills":
        raise ReceiptPublishError(f"{location}.object_ref.repo: must be 'aoa-skills'")
    if receipt["object_ref"].get("kind") != "skill":
        raise ReceiptPublishError(f"{location}.object_ref.kind: must be 'skill'")
    if not isinstance(receipt["evidence_refs"], list):
        raise ReceiptPublishError(f"{location}.evidence_refs: must be a list")
    payload = receipt["payload"]
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{location}.payload: must be an object")

    required_payload_fields = {
        "kernel_id",
        "skill_name",
        "application_stage",
        "detail_event_kind",
        "detail_receipt_ref",
    }
    allowed_payload_fields = {
        *required_payload_fields,
        "authority_contract",
        "route_ref",
        "surface_detection_context",
    }
    missing = sorted(field for field in required_payload_fields if field not in payload)
    if missing:
        raise ReceiptPublishError(f"{location}.payload: missing required fields {missing!r}")
    extra = sorted(field for field in payload if field not in allowed_payload_fields)
    if extra:
        raise ReceiptPublishError(f"{location}.payload: unsupported fields {extra!r}")
    if payload["kernel_id"] != KERNEL_ID:
        raise ReceiptPublishError(f"{location}.payload.kernel_id: must equal {KERNEL_ID!r}")
    skill_name = payload["skill_name"]
    if not isinstance(skill_name, str) or skill_name not in KERNEL_SKILLS:
        raise ReceiptPublishError(
            f"{location}.payload.skill_name: must be one of {sorted(KERNEL_SKILLS)!r}"
        )
    if receipt["object_ref"].get("id") != skill_name:
        raise ReceiptPublishError(f"{location}.object_ref.id: must match payload.skill_name")
    if payload["application_stage"] != "finish":
        raise ReceiptPublishError(f"{location}.payload.application_stage: must equal 'finish'")
    detail_event_kind = payload["detail_event_kind"]
    if detail_event_kind not in ALLOWED_DETAIL_EVENT_KINDS:
        raise ReceiptPublishError(
            f"{location}.payload.detail_event_kind: unsupported detail receipt kind {detail_event_kind!r}"
        )
    expected_detail_event_kind = KERNEL_DETAIL_EVENT_KIND_BY_SKILL[skill_name]
    if detail_event_kind != expected_detail_event_kind:
        raise ReceiptPublishError(
            f"{location}.payload.detail_event_kind: must equal {expected_detail_event_kind!r} "
            f"for skill {skill_name!r}"
        )
    detail_receipt_ref = payload["detail_receipt_ref"]
    if not isinstance(detail_receipt_ref, str) or not detail_receipt_ref:
        raise ReceiptPublishError(
            f"{location}.payload.detail_receipt_ref: must be a non-empty string"
        )
    route_ref = payload.get("route_ref")
    if route_ref is not None and (not isinstance(route_ref, str) or not route_ref):
        raise ReceiptPublishError(
            f"{location}.payload.route_ref: must be omitted or a non-empty string"
        )
    authority_contract = payload.get("authority_contract")
    if authority_contract is not None:
        if not isinstance(authority_contract, dict):
            raise ReceiptPublishError(
                f"{location}.payload.authority_contract: must be omitted or an object"
            )
        validate_authority_contract(
            authority_contract,
            location=f"{location}.payload.authority_contract",
        )
    surface_detection_context = payload.get("surface_detection_context")
    if surface_detection_context is not None:
        if not isinstance(surface_detection_context, dict):
            raise ReceiptPublishError(
                f"{location}.payload.surface_detection_context: must be omitted or an object"
            )
        validate_surface_detection_context(
            surface_detection_context,
            location=f"{location}.payload.surface_detection_context",
        )


def load_receipts(paths: list[Path]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for path in paths:
        if path.suffix == ".jsonl":
            for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                line = raw_line.strip()
                if not line:
                    continue
                item = json.loads(line)
                if not isinstance(item, dict):
                    raise ReceiptPublishError(f"{path}:{line_number}: receipt must be an object")
                validate_receipt(item, location=f"{path}:{line_number}")
                receipts.append(item)
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            validate_receipt(payload, location=str(path))
            receipts.append(payload)
            continue
        if not isinstance(payload, list):
            raise ReceiptPublishError(f"{path}: receipt payload must be an object or list")
        for index, item in enumerate(payload):
            if not isinstance(item, dict):
                raise ReceiptPublishError(f"{path}[{index}]: receipt must be an object")
            validate_receipt(item, location=f"{path}[{index}]")
            receipts.append(item)
    return receipts


def load_existing_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    event_ids: set[str] = set()
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}:{line_number}: existing log line must be an object")
        event_id = item.get("event_id")
        if isinstance(event_id, str) and event_id:
            event_ids.add(event_id)
    return event_ids


def append_new_receipts(*, log_path: Path, receipts: list[dict[str, Any]]) -> tuple[int, int]:
    existing_ids = load_existing_ids(log_path)
    appended = 0
    skipped = 0
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        for receipt in receipts:
            event_id = receipt["event_id"]
            if event_id in existing_ids:
                skipped += 1
                continue
            handle.write(json.dumps(receipt, sort_keys=True, ensure_ascii=False) + "\n")
            existing_ids.add(event_id)
            appended += 1
    return appended, skipped


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_paths = [Path(path).expanduser().resolve() for path in args.input]
    if not input_paths:
        raise SystemExit("no receipt input files were provided")
    log_path = Path(args.log_path).expanduser().resolve()
    receipts = load_receipts(input_paths)
    appended, skipped = append_new_receipts(log_path=log_path, receipts=receipts)
    print(f"[ok] appended {appended} core skill receipts to {log_path}")
    print(f"[skip] duplicate event ids skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
