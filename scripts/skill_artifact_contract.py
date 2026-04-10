from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import skill_catalog_contract


SKILLS_DIR_NAME = "skills"
RUNTIME_EXAMPLE_HEADINGS = (
    "Scenario",
    "Why this skill fits",
    "Expected inputs",
    "Expected outputs",
    "Boundary notes",
    "Verification notes",
)
REVIEW_CHECKLIST_HEADINGS = (
    "Purpose",
    "When it applies",
    "Review checklist",
    "Not a fit",
)
RUNTIME_EXAMPLE_TYPE = "runtime_example"
REVIEW_CHECKLIST_TYPE = "review_checklist"
PROMOTION_REVIEW_TYPE = "promotion_review"
CANDIDATE_REVIEW_TYPE = "candidate_review"
SECTION_HEADING_PATTERN = re.compile(r"^[ ]{0,3}##\s+(.+?)\s*$")
STATUS_PROMOTION_REVIEWS_DIR = Path("docs") / "reviews" / "status-promotions"
CANONICAL_CANDIDATES_DIR = Path("docs") / "reviews" / "canonical-candidates"


@dataclass(frozen=True)
class ArtifactContractIssue:
    location: str
    message: str


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def trim_boundary_blank_lines(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def extract_artifact_sections(body: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    current_lines: list[str] = []
    normalized_body = body.replace("\r\n", "\n").replace("\r", "\n")

    def flush_current() -> None:
        nonlocal current_heading, current_lines
        if current_heading is None:
            return
        sections.append((current_heading, trim_boundary_blank_lines("\n".join(current_lines))))
        current_heading = None
        current_lines = []

    for line in normalized_body.split("\n"):
        heading_match = SECTION_HEADING_PATTERN.match(line)
        if heading_match:
            flush_current()
            current_heading = heading_match.group(1).strip()
            continue
        if current_heading is not None:
            current_lines.append(line)

    flush_current()
    return sections


def collect_heading_contract_issues(
    section_pairs: Sequence[tuple[str, str]],
    *,
    location: str,
    artifact_label: str,
    expected_headings: Sequence[str],
) -> list[ArtifactContractIssue]:
    issues: list[ArtifactContractIssue] = []
    headings = [heading for heading, _content in section_pairs]
    heading_counts = Counter(headings)

    for heading in expected_headings:
        if heading_counts[heading] == 0:
            issues.append(
                ArtifactContractIssue(
                    location,
                    f"{artifact_label} missing required section '{heading}'",
                )
            )
        elif heading_counts[heading] > 1:
            issues.append(
                ArtifactContractIssue(
                    location,
                    f"{artifact_label} has duplicate top-level section '{heading}'",
                )
            )

    for heading in headings:
        if heading not in expected_headings:
            issues.append(
                ArtifactContractIssue(
                    location,
                    f"{artifact_label} has unexpected top-level section '{heading}'",
                )
            )

    if headings != list(expected_headings):
        issues.append(
            ArtifactContractIssue(
                location,
                f"{artifact_label} top-level sections must match the canonical order exactly",
            )
        )

    for heading, content_markdown in section_pairs:
        if heading in expected_headings and not content_markdown.strip():
            issues.append(
                ArtifactContractIssue(
                    location,
                    f"{artifact_label} section '{heading}' must not be empty",
                )
            )

    return issues


def collect_runtime_example_issues(
    path: Path,
    repo_root: Path,
) -> list[ArtifactContractIssue]:
    section_pairs = extract_artifact_sections(path.read_text(encoding="utf-8"))
    return collect_heading_contract_issues(
        section_pairs,
        location=relative_location(path, repo_root),
        artifact_label="runtime example",
        expected_headings=RUNTIME_EXAMPLE_HEADINGS,
    )


def collect_review_checklist_issues(
    path: Path,
    repo_root: Path,
) -> list[ArtifactContractIssue]:
    section_pairs = extract_artifact_sections(path.read_text(encoding="utf-8"))
    return collect_heading_contract_issues(
        section_pairs,
        location=relative_location(path, repo_root),
        artifact_label="review checklist",
        expected_headings=REVIEW_CHECKLIST_HEADINGS,
    )


def collect_skill_artifact_issues(
    repo_root: Path,
    skill_name: str,
) -> list[ArtifactContractIssue]:
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    issues: list[ArtifactContractIssue] = []
    examples_dir = skill_dir / "examples"
    if examples_dir.is_dir():
        for example_path in sorted(examples_dir.glob("*.md")):
            issues.extend(collect_runtime_example_issues(example_path, repo_root))

    review_path = skill_dir / "checks" / "review.md"
    if review_path.is_file():
        issues.extend(collect_review_checklist_issues(review_path, repo_root))

    return issues


def preferred_runtime_artifact(skill_dir: Path) -> Path | None:
    runtime_example = skill_dir / "examples" / "runtime.md"
    if runtime_example.is_file():
        return runtime_example

    examples_dir = skill_dir / "examples"
    if examples_dir.is_dir():
        example_paths = sorted(examples_dir.glob("*.md"))
        if example_paths:
            return example_paths[0]

    review_path = skill_dir / "checks" / "review.md"
    if review_path.is_file():
        return review_path
    return None


def collect_support_artifacts(
    repo_root: Path,
    skill_name: str,
) -> list[dict[str, Any]]:
    skill_dir = repo_root / SKILLS_DIR_NAME / skill_name
    selected_runtime_artifact = preferred_runtime_artifact(skill_dir)
    artifacts: list[dict[str, Any]] = []

    examples_dir = skill_dir / "examples"
    if examples_dir.is_dir():
        for example_path in sorted(examples_dir.glob("*.md")):
            artifacts.append(
                {
                    "type": RUNTIME_EXAMPLE_TYPE,
                    "path": relative_location(example_path, repo_root),
                    "selected_for_runtime_inspection": example_path == selected_runtime_artifact,
                }
            )

    review_check_path = skill_dir / "checks" / "review.md"
    if review_check_path.is_file():
        artifacts.append(
            {
                "type": REVIEW_CHECKLIST_TYPE,
                "path": relative_location(review_check_path, repo_root),
                "selected_for_runtime_inspection": review_check_path == selected_runtime_artifact,
            }
        )

    promotion_review_path = repo_root / STATUS_PROMOTION_REVIEWS_DIR / f"{skill_name}.md"
    if promotion_review_path.is_file():
        artifacts.append(
            {
                "type": PROMOTION_REVIEW_TYPE,
                "path": relative_location(promotion_review_path, repo_root),
                "selected_for_runtime_inspection": False,
            }
        )

    candidate_review_path = repo_root / CANONICAL_CANDIDATES_DIR / f"{skill_name}.md"
    if candidate_review_path.is_file():
        artifacts.append(
            {
                "type": CANDIDATE_REVIEW_TYPE,
                "path": relative_location(candidate_review_path, repo_root),
                "selected_for_runtime_inspection": False,
            }
        )

    return artifacts
