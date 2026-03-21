from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_artifact_contract
import skill_catalog_contract
import skill_section_contract
import skill_source_model


SKILLS_DIR_NAME = "skills"
WALKTHROUGH_VERSION = 1
WALKTHROUGHS_JSON_PATH = Path("generated") / "skill_walkthroughs.json"
WALKTHROUGHS_MARKDOWN_PATH = Path("generated") / "skill_walkthroughs.md"
WALKTHROUGH_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "runtime_examples": "skills/*/examples/*.md",
    "review_checks": "skills/*/checks/review.md",
    "status_promotion_reviews": "docs/reviews/status-promotions/*.md",
    "canonical_candidate_reviews": "docs/reviews/canonical-candidates/*.md",
}
INSPECTION_ORDER = (
    "capsule",
    "sections",
    "full",
    "evidence",
)
EXPAND_SECTIONS = (
    "Procedure",
    "Contracts",
    "Risks and anti-patterns",
    "Verification",
)
LIST_ITEM_PATTERN = re.compile(r"^(?:[-*]|\d+\.)\s+(.*)$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\([^)]+\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
EMPHASIS_PATTERN = re.compile(r"(\*\*|\*|__|_)")
USE_HEADING = "Use this skill when:"
DO_NOT_USE_HEADING = "Do not use this skill when:"


@dataclass(frozen=True)
class RuntimeSurfaceIssue:
    location: str
    message: str


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def parse_skill_document(path: Path) -> tuple[dict[str, Any], str]:
    return skill_source_model.parse_skill_document(path)


def parse_skill_sections(body: str) -> dict[str, str]:
    return skill_source_model.parse_skill_sections(body)


def normalize_inline_markdown(text: str) -> str:
    normalized = MARKDOWN_LINK_PATTERN.sub(r"\1", text)
    normalized = INLINE_CODE_PATTERN.sub(r"\1", normalized)
    normalized = EMPHASIS_PATTERN.sub("", normalized)
    normalized = normalized.replace("\\", "")
    return " ".join(normalized.split())


def normalize_phrase(text: str) -> str:
    return normalize_inline_markdown(text).strip(" \t\r\n.;:")


def extract_markdown_items(section_text: str) -> list[str]:
    items: list[str] = []
    current_item: str | None = None

    for raw_line in section_text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue

        match = LIST_ITEM_PATTERN.match(stripped)
        if match:
            if current_item is not None:
                items.append(current_item)
            current_item = normalize_phrase(match.group(1))
            continue

        if current_item is not None and raw_line[:1].isspace():
            continuation = normalize_phrase(stripped)
            if continuation:
                current_item = f"{current_item} {continuation}".strip()
            continue

        if current_item is not None:
            items.append(current_item)
            current_item = None

        items.append(normalize_phrase(stripped))

    if current_item is not None:
        items.append(current_item)

    return [item for item in items if item]


def extract_trigger_boundary_items(section_text: str) -> tuple[list[str], list[str]]:
    use_items: list[str] = []
    do_not_use_items: list[str] = []
    current_bucket: list[str] | None = None
    current_item: str | None = None

    def flush_current_item() -> None:
        nonlocal current_item
        if current_item is None or current_bucket is None:
            current_item = None
            return
        current_bucket.append(current_item)
        current_item = None

    for raw_line in section_text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue

        normalized = normalize_inline_markdown(stripped)
        lowered = normalized.rstrip(":").lower()
        if lowered.startswith("use this skill when") or lowered.startswith("use when"):
            flush_current_item()
            current_bucket = use_items
            continue
        if lowered.startswith("do not use this skill when") or lowered.startswith("avoid when"):
            flush_current_item()
            current_bucket = do_not_use_items
            continue

        match = LIST_ITEM_PATTERN.match(stripped)
        if match:
            flush_current_item()
            current_item = normalize_phrase(match.group(1))
            continue

        if current_item is not None and raw_line[:1].isspace():
            continuation = normalize_phrase(stripped)
            if continuation:
                current_item = f"{current_item} {continuation}".strip()
            continue

        flush_current_item()
        if current_bucket is not None:
            current_bucket.append(normalize_phrase(normalized))

    flush_current_item()
    return [item for item in use_items if item], [item for item in do_not_use_items if item]


def count_markdown_list_items(section_text: str) -> int:
    return sum(
        1
        for raw_line in section_text.splitlines()
        if LIST_ITEM_PATTERN.match(raw_line.strip())
    )


def collect_runtime_surface_issues(
    *,
    location: str,
    trigger_boundary_text: str,
    outputs_text: str,
) -> list[RuntimeSurfaceIssue]:
    issues: list[RuntimeSurfaceIssue] = []
    if USE_HEADING not in trigger_boundary_text:
        issues.append(
            RuntimeSurfaceIssue(
                location,
                f"runtime trigger boundary must include exact heading '{USE_HEADING}'",
            )
        )
    if DO_NOT_USE_HEADING not in trigger_boundary_text:
        issues.append(
            RuntimeSurfaceIssue(
                location,
                f"runtime trigger boundary must include exact heading '{DO_NOT_USE_HEADING}'",
            )
        )

    use_when, do_not_use_when = extract_trigger_boundary_items(trigger_boundary_text)
    if not use_when:
        issues.append(
            RuntimeSurfaceIssue(
                location,
                "runtime trigger boundary must define at least one use bullet",
            )
        )
    if not do_not_use_when:
        issues.append(
            RuntimeSurfaceIssue(
                location,
                "runtime trigger boundary must define at least one do_not_use bullet",
            )
        )
    if count_markdown_list_items(outputs_text) < 1:
        issues.append(
            RuntimeSurfaceIssue(
                location,
                "runtime outputs must use at least one markdown bullet item",
            )
        )
    return issues


def enforce_runtime_surface_contract(
    *,
    location: str,
    trigger_boundary_text: str,
    outputs_text: str,
) -> None:
    issues = collect_runtime_surface_issues(
        location=location,
        trigger_boundary_text=trigger_boundary_text,
        outputs_text=outputs_text,
    )
    if issues:
        joined = "\n".join(f"- {issue.location}: {issue.message}" for issue in issues)
        raise ValueError(joined)


def build_skill_walkthrough_entry(repo_root: Path, skill_name: str) -> dict[str, Any]:
    skill_md_path = repo_root / SKILLS_DIR_NAME / skill_name / "SKILL.md"
    metadata, body = parse_skill_document(skill_md_path)
    sections = parse_skill_sections(body)

    if "Trigger boundary" not in sections:
        raise ValueError(f"{skill_md_path} is missing section 'Trigger boundary'")
    if "Outputs" not in sections:
        raise ValueError(f"{skill_md_path} is missing section 'Outputs'")

    enforce_runtime_surface_contract(
        location=relative_location(skill_md_path, repo_root),
        trigger_boundary_text=sections["Trigger boundary"],
        outputs_text=sections["Outputs"],
    )
    use_when, do_not_use_when = extract_trigger_boundary_items(sections["Trigger boundary"])
    object_use_shape = extract_markdown_items(sections["Outputs"])

    return {
        "name": skill_name,
        "scope": metadata.get("scope"),
        "status": metadata.get("status"),
        "invocation_mode": metadata.get("invocation_mode"),
        "skill_path": relative_location(skill_md_path, repo_root),
        "pick_summary": metadata.get("summary"),
        "use_when": use_when,
        "do_not_use_when": do_not_use_when,
        "inspection_order": list(INSPECTION_ORDER),
        "expand_sections": list(EXPAND_SECTIONS),
        "object_use_shape": object_use_shape,
        "support_artifacts": skill_artifact_contract.collect_support_artifacts(
            repo_root,
            skill_name,
        ),
    }


def build_walkthrough_payload(
    repo_root: Path,
    skill_names: Sequence[str],
) -> dict[str, Any]:
    return {
        "walkthrough_version": WALKTHROUGH_VERSION,
        "source_of_truth": WALKTHROUGH_SOURCE_OF_TRUTH,
        "skills": [
            build_skill_walkthrough_entry(repo_root, skill_name)
            for skill_name in skill_names
        ],
    }


def find_skill_walkthrough_entry(
    payload: Mapping[str, Any],
    skill_name: str,
) -> Mapping[str, Any]:
    skills = payload.get("skills", [])
    if not isinstance(skills, list):
        raise KeyError(skill_name)

    for entry in skills:
        if isinstance(entry, Mapping) and entry.get("name") == skill_name:
            return entry
    raise KeyError(skill_name)


def format_support_artifact_selection(artifact: Mapping[str, Any]) -> str:
    selected_suffix = ""
    if artifact.get("selected_for_runtime_inspection"):
        selected_suffix = " (selected)"
    return f"- `{artifact.get('type')}`{selected_suffix}: `{artifact.get('path')}`"


def render_walkthrough_markdown(payload: Mapping[str, Any]) -> str:
    skill_entries = payload.get("skills", [])
    if not isinstance(skill_entries, list):
        raise ValueError("walkthrough payload field 'skills' must be a list")

    lines = [
        "# Skill walkthroughs",
        "",
        "This derived file makes the runtime path concrete inside `aoa-skills`.",
        "`SKILL.md` remains the meaning-authoritative source; walkthroughs are inspect aids.",
        "",
        "## Shared inspection path",
        "",
        "1. Open the capsule view for a fast bounded summary.",
        "2. Open the sections view for source-owned expand-time reads.",
        "3. Open the full `SKILL.md` only when section detail still is not enough.",
        "4. Open the evidence view to inspect runtime examples and review surfaces.",
        "",
        "Common inspection order:",
        "",
    ]
    for view_name in INSPECTION_ORDER:
        lines.append(f"- `{view_name}`")
    lines.extend(
        [
            "",
            "Common expand sections:",
            "",
        ]
    )
    for section_name in EXPAND_SECTIONS:
        lines.append(f"- `{section_name}`")
    lines.append("")

    for entry in skill_entries:
        if not isinstance(entry, Mapping):
            continue
        lines.extend(
            [
                f"## {entry['name']}",
                "",
                f"- scope: `{entry['scope']}`",
                f"- status: `{entry['status']}`",
                f"- invocation mode: `{entry['invocation_mode']}`",
                f"- skill path: `{entry['skill_path']}`",
                f"- pick summary: {entry['pick_summary']}",
                "",
                "### Use when",
                "",
            ]
        )
        use_when = entry.get("use_when", [])
        if use_when:
            for item in use_when:
                lines.append(f"- {item}")
        else:
            lines.append("- No explicit use-when bullets were derived.")
        lines.extend(
            [
                "",
                "### Do not use when",
                "",
            ]
        )
        do_not_use_when = entry.get("do_not_use_when", [])
        if do_not_use_when:
            for item in do_not_use_when:
                lines.append(f"- {item}")
        else:
            lines.append("- No explicit do-not-use bullets were derived.")
        lines.extend(
            [
                "",
                "### Object use shape",
                "",
            ]
        )
        object_use_shape = entry.get("object_use_shape", [])
        if object_use_shape:
            for item in object_use_shape:
                lines.append(f"- {item}")
        else:
            lines.append("- No output bullets were derived.")
        lines.extend(
            [
                "",
                "### Support artifacts",
                "",
            ]
        )
        support_artifacts = entry.get("support_artifacts", [])
        if support_artifacts:
            for artifact in support_artifacts:
                if isinstance(artifact, Mapping):
                    lines.append(format_support_artifact_selection(artifact))
        else:
            lines.append("- No support artifacts were resolved.")
        lines.append("")

    return "\n".join(lines)
