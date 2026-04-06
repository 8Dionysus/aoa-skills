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
    "decision_fork_receipt",
    "harvest_packet_receipt",
    "progression_delta_receipt",
    "quest_promotion_receipt",
    "repair_cycle_receipt",
    "skill_run_receipt",
}


class ReceiptPublishError(ValueError):
    pass


def load_kernel_manifest() -> tuple[str, set[str]]:
    payload = json.loads(KERNEL_MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: kernel manifest must be an object")
    kernel_id = payload.get("kernel_id")
    skills = payload.get("skills")
    if not isinstance(kernel_id, str) or not kernel_id:
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: kernel_id must be a non-empty string")
    if not isinstance(skills, list) or not skills:
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: skills must be a non-empty list")
    skill_names = {skill for skill in skills if isinstance(skill, str) and skill}
    if len(skill_names) != len(skills):
        raise ReceiptPublishError(f"{KERNEL_MANIFEST_PATH}: skills must be non-empty strings without duplicates")
    return kernel_id, skill_names


KERNEL_ID, KERNEL_SKILLS = load_kernel_manifest()


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
    allowed_payload_fields = {*required_payload_fields, "route_ref"}
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
