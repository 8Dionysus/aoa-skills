from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_bundle_surface
import skill_catalog_contract
import skill_governance_lane_contract
import skill_governance_surface
import skill_source_model


REVIEW_KIND_STATUS_PROMOTION = "status_promotion"
STATUS_PROMOTION_SECTION_ORDER = (
    "Current status",
    "Target status",
    "Evidence reviewed",
    "Findings",
    "Gaps and blockers",
    "Recommendation",
)
LABEL_PATTERN = re.compile(r"^\s*[-*]\s+([^:]+?):\s*(.*)$")
LIST_SPLIT_PATTERN = re.compile(r"\s*[;,]\s*")
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")


@dataclass(frozen=True)
class ReviewSection:
    labels: dict[str, str]
    items: tuple[str, ...]


@dataclass(frozen=True)
class StatusPromotionReviewRecord:
    skill_name: str
    review_path: str
    sections: dict[str, ReviewSection]
    current_maturity_status: str | None
    current_machine_checkable_floor: str | None
    current_governance_lane_decision: str | None
    scope: str | None
    current_lineage: str | None
    reviewed_revision: str | None
    target_maturity_status: str | None
    machine_checkable_floor_result: str | None
    recorded_governance_outcome: str | None
    runtime_skill_md_meaning_changed: bool | None
    blockers_for_target_status: tuple[str, ...]
    blockers_for_next_status_step: tuple[str, ...]


@dataclass(frozen=True)
class StatusPromotionReviewTruthSync:
    skill_name: str
    status: str | None
    lineage_state: str | None
    governance_decision: str | None
    reviewed_revision: str | None
    current_revision: str | None
    runtime_skill_md_meaning_changed: bool | None
    review_path: str | None
    issues: tuple[str, ...]


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def review_record_path(repo_root: Path, skill_name: str) -> str | None:
    review_path = repo_root / "docs" / "reviews" / "status-promotions" / f"{skill_name}.md"
    if review_path.is_file():
        return relative_location(review_path, repo_root)
    return None


def _normalize_label(label: str) -> str:
    normalized = INLINE_CODE_PATTERN.sub(r"\1", label)
    return " ".join(normalized.lower().split())


def _normalize_value(value: str) -> str | None:
    normalized = INLINE_CODE_PATTERN.sub(r"\1", value)
    normalized = " ".join(normalized.split())
    for separator in (" with ", " because ", " while "):
        if separator in normalized:
            normalized = normalized.split(separator, 1)[0]
            break
    return normalized or None


def _parse_bullets(section_text: str) -> ReviewSection:
    labels: dict[str, str] = {}
    items: list[str] = []
    current_label: str | None = None
    current_value: list[str] = []

    def flush() -> None:
        nonlocal current_label, current_value
        if current_label is None:
            return
        labels[current_label] = _normalize_value(" ".join(current_value)) or ""
        current_label = None
        current_value = []

    for raw_line in section_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if current_label is not None and current_value:
                current_value.append("")
            continue
        match = LABEL_PATTERN.match(line)
        if match:
            flush()
            current_label = _normalize_label(match.group(1))
            current_value = [match.group(2).strip()] if match.group(2).strip() else []
            continue
        if current_label is not None and raw_line[:1].isspace():
            current_value.append(line.strip())
            continue
        items.append(line.strip())

    flush()
    return ReviewSection(
        labels=labels,
        items=tuple(item for item in items if item),
    )


def _parse_sections(review_body: str) -> dict[str, ReviewSection]:
    parsed_sections = skill_source_model.parse_skill_sections(review_body)
    return {
        heading: _parse_bullets(section_text)
        for heading, section_text in parsed_sections.items()
    }


def _split_frontmatter_and_body(review_text: str) -> tuple[str, str]:
    lines = review_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", review_text

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        raise ValueError("missing a closing frontmatter delimiter")

    frontmatter = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])
    return frontmatter, body


def _find_label(sections: Mapping[str, ReviewSection], *labels: str) -> str | None:
    normalized_labels = {_normalize_label(label) for label in labels}
    for section in sections.values():
        for label, value in section.labels.items():
            if label in normalized_labels:
                return value or None
    return None


def _split_list_value(value: str | None) -> tuple[str, ...]:
    if value is None:
        return ()
    parts = [part.strip(" -") for part in LIST_SPLIT_PATTERN.split(value)]
    return tuple(part for part in parts if part)


def _parse_bool_token(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"yes", "true", "y"}:
        return True
    if normalized in {"no", "false", "n"}:
        return False
    return None


def parse_status_promotion_review_text(
    *,
    skill_name: str,
    review_path: str,
    review_text: str,
) -> StatusPromotionReviewRecord:
    _metadata, body = _split_frontmatter_and_body(review_text)
    sections = _parse_sections(body)
    return StatusPromotionReviewRecord(
        skill_name=skill_name,
        review_path=review_path,
        sections=sections,
        current_maturity_status=_find_label(
            sections,
            "current maturity status",
        ),
        current_machine_checkable_floor=_find_label(
            sections,
            "current machine-checkable floor",
            "current machine-checkable floor (`candidate_ready` gate only when applicable)",
        ),
        current_governance_lane_decision=_find_label(
            sections,
            "current governance lane decision",
        ),
        scope=_find_label(sections, "scope"),
        current_lineage=_find_label(sections, "current lineage"),
        reviewed_revision=_find_label(sections, "reviewed revision"),
        target_maturity_status=_find_label(sections, "target maturity status"),
        machine_checkable_floor_result=_find_label(
            sections,
            "machine-checkable floor result",
        ),
        recorded_governance_outcome=_find_label(
            sections,
            "recorded governance outcome",
        ),
        runtime_skill_md_meaning_changed=_parse_bool_token(
            _find_label(sections, "runtime skill.md meaning changed")
            or _find_label(sections, "runtime skill md meaning changed")
        ),
        blockers_for_target_status=_split_list_value(
            _find_label(sections, "blockers for this target status")
            or _find_label(sections, "blockers for target status")
        ),
        blockers_for_next_status_step=_split_list_value(
            _find_label(sections, "blockers for the next status step")
            or _find_label(sections, "blockers for next status step")
        ),
    )


def load_status_promotion_review_record(
    repo_root: Path,
    skill_name: str,
) -> StatusPromotionReviewRecord | None:
    review_path = repo_root / "docs" / "reviews" / "status-promotions" / f"{skill_name}.md"
    if not review_path.is_file():
        return None

    review_text = review_path.read_text(encoding="utf-8")
    return parse_status_promotion_review_text(
        skill_name=skill_name,
        review_path=relative_location(review_path, repo_root),
        review_text=review_text,
    )


def current_bundle_revision(repo_root: Path, skill_name: str) -> str:
    source = skill_source_model.load_skill_source(repo_root, skill_name)
    file_paths = [
        path
        for path in skill_bundle_surface.bundle_file_paths(source)
        if not _is_review_surface(path, repo_root)
    ]
    return skill_bundle_surface.hash_files(repo_root, file_paths)[:12]


def _is_review_surface(path: Path, repo_root: Path) -> bool:
    relative_path = relative_location(path, repo_root)
    return relative_path.startswith("docs/reviews/")


def _lineage_state_from_source(source: skill_source_model.SkillSource) -> str:
    techniques = skill_catalog_contract.normalize_technique_refs(source.manifest)
    return skill_governance_surface.derive_lineage_state(
        list(source.metadata.get("technique_dependencies", [])),
        techniques,
    )


def status_promotion_review_truth_sync(
    repo_root: Path,
    skill_name: str,
) -> StatusPromotionReviewTruthSync:
    source = skill_source_model.load_skill_source(repo_root, skill_name)
    record = load_status_promotion_review_record(repo_root, skill_name)
    lineage_state = _lineage_state_from_source(source)
    signals = skill_governance_lane_contract.governance_signals_for_skill(
        skill_governance_lane_contract.governance_skill_signals(
            skill_governance_lane_contract.load_governance_lanes(repo_root)
        ),
        skill_name,
    )
    current_revision = current_bundle_revision(repo_root, skill_name)
    issues: list[str] = []

    if record is None:
        issues.append("missing_status_promotion_review_record")
        return StatusPromotionReviewTruthSync(
            skill_name=skill_name,
            status=source.metadata.get("status"),
            lineage_state=lineage_state,
            governance_decision=signals.governance_decision,
            reviewed_revision=None,
            current_revision=current_revision,
            runtime_skill_md_meaning_changed=None,
            review_path=None,
            issues=tuple(issues),
        )

    if record.current_maturity_status is None:
        issues.append("missing_current_maturity_status")
    elif record.current_maturity_status != str(source.metadata.get("status")):
        issues.append(
            f"current_status_mismatch(expected={source.metadata.get('status')}, recorded={record.current_maturity_status})"
        )

    if record.current_lineage is None:
        issues.append("missing_current_lineage")
    elif record.current_lineage != lineage_state:
        issues.append(
            f"current_lineage_mismatch(expected={lineage_state}, recorded={record.current_lineage})"
        )

    if record.current_governance_lane_decision is None:
        issues.append("missing_current_governance_lane_decision")
    elif record.current_governance_lane_decision != signals.governance_decision:
        issues.append(
            "current_governance_decision_mismatch("
            f"expected={signals.governance_decision}, recorded={record.current_governance_lane_decision})"
        )

    if record.scope is None:
        issues.append("missing_scope")
    elif record.scope != str(source.metadata.get("scope")):
        issues.append(
            f"scope_mismatch(expected={source.metadata.get('scope')}, recorded={record.scope})"
        )

    if record.current_machine_checkable_floor is None:
        issues.append("missing_current_machine_checkable_floor")

    if record.reviewed_revision is None:
        issues.append("missing_reviewed_revision")
    elif record.reviewed_revision != current_revision:
        issues.append(
            f"reviewed_revision_mismatch(expected={current_revision}, recorded={record.reviewed_revision})"
        )

    if record.runtime_skill_md_meaning_changed is None:
        issues.append("missing_runtime_skill_md_meaning_changed_field")

    if record.target_maturity_status is None:
        issues.append("missing_target_maturity_status")
    if record.machine_checkable_floor_result is None:
        issues.append("missing_machine_checkable_floor_result")
    if record.recorded_governance_outcome is None:
        issues.append("missing_recorded_governance_outcome")
    elif record.recorded_governance_outcome != signals.governance_decision:
        issues.append(
            "recorded_governance_outcome_mismatch("
            f"expected={signals.governance_decision}, recorded={record.recorded_governance_outcome})"
        )
    if not record.blockers_for_target_status:
        issues.append("missing_blockers_for_target_status")
    if not record.blockers_for_next_status_step:
        issues.append("missing_blockers_for_next_status_step")

    return StatusPromotionReviewTruthSync(
        skill_name=skill_name,
        status=source.metadata.get("status"),
        lineage_state=lineage_state,
        governance_decision=signals.governance_decision,
        reviewed_revision=record.reviewed_revision,
        current_revision=current_revision,
        runtime_skill_md_meaning_changed=record.runtime_skill_md_meaning_changed,
        review_path=record.review_path,
        issues=tuple(issues),
    )


def build_status_promotion_review_truth_sync_entries(
    repo_root: Path,
    skill_names: Sequence[str],
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for skill_name in skill_names:
        if review_record_path(repo_root, skill_name) is None:
            continue
        truth_sync = status_promotion_review_truth_sync(repo_root, skill_name)
        entries.append(
            {
                "name": truth_sync.skill_name,
                "status": truth_sync.status,
                "lineage_state": truth_sync.lineage_state,
                "governance_decision": truth_sync.governance_decision,
                "review_path": truth_sync.review_path,
                "reviewed_revision": truth_sync.reviewed_revision,
                "current_revision": truth_sync.current_revision,
                "runtime_skill_md_meaning_changed": truth_sync.runtime_skill_md_meaning_changed,
                "issues": list(truth_sync.issues),
                "truth_synced": not truth_sync.issues,
            }
        )
    return entries
