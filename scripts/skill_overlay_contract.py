from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import skill_artifact_contract
import skill_catalog_contract


OVERLAY_STUBS_DIR = Path("tests") / "fixtures" / "overlay_stubs"
PROJECT_OVERLAY_FILE = "PROJECT_OVERLAY.md"
PROJECT_OVERLAY_SKILL_FILE = "PROJECT_OVERLAY_SKILL.md"
OVERLAY_DIR_PREFIXES = ("atm10-", "abyss-")
PROJECT_OVERLAY_HEADINGS = (
    "Overlay target",
    "Base skill surface",
    "Local authority and approvals",
    "Local paths and commands",
    "Local verification",
    "Non-goals and boundaries",
)
PROJECT_OVERLAY_SKILL_HEADINGS = (
    "Base skill",
    "Overlay triggers",
    "Local inputs",
    "Local outputs",
    "Local procedure notes",
    "Authority and safety notes",
    "Verification notes",
    "Stub-only notes",
)


@dataclass(frozen=True)
class OverlayContractIssue:
    location: str
    message: str


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def contains_phrase(text: str, phrases: Sequence[str]) -> bool:
    normalized = " ".join(text.lower().split())
    return any(" ".join(phrase.lower().split()) in normalized for phrase in phrases)


def collect_overlay_heading_issues(
    path: Path,
    repo_root: Path,
    *,
    artifact_label: str,
    expected_headings: Sequence[str],
) -> list[OverlayContractIssue]:
    section_pairs = skill_artifact_contract.extract_artifact_sections(
        path.read_text(encoding="utf-8")
    )
    issues: list[OverlayContractIssue] = []
    for issue in skill_artifact_contract.collect_heading_contract_issues(
        section_pairs,
        location=relative_location(path, repo_root),
        artifact_label=artifact_label,
        expected_headings=expected_headings,
    ):
        issues.append(OverlayContractIssue(issue.location, issue.message))
    return issues


def collect_overlay_stub_issues(repo_root: Path) -> list[OverlayContractIssue]:
    root = repo_root / OVERLAY_STUBS_DIR
    issues: list[OverlayContractIssue] = []
    if not root.is_dir():
        return issues

    for stub_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        if not any(stub_dir.name.startswith(prefix) for prefix in OVERLAY_DIR_PREFIXES):
            issues.append(
                OverlayContractIssue(
                    relative_location(stub_dir, repo_root),
                    "overlay stub directories must start with 'atm10-' or 'abyss-'",
                )
            )
        overlay_path = stub_dir / PROJECT_OVERLAY_FILE
        overlay_skill_path = stub_dir / PROJECT_OVERLAY_SKILL_FILE
        if not overlay_path.is_file():
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_path, repo_root),
                    "overlay stub is missing PROJECT_OVERLAY.md",
                )
            )
            continue
        if not overlay_skill_path.is_file():
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_skill_path, repo_root),
                    "overlay stub is missing PROJECT_OVERLAY_SKILL.md",
                )
            )
            continue

        issues.extend(
            collect_overlay_heading_issues(
                overlay_path,
                repo_root,
                artifact_label="project overlay",
                expected_headings=PROJECT_OVERLAY_HEADINGS,
            )
        )
        issues.extend(
            collect_overlay_heading_issues(
                overlay_skill_path,
                repo_root,
                artifact_label="project overlay skill",
                expected_headings=PROJECT_OVERLAY_SKILL_HEADINGS,
            )
        )

        overlay_text = overlay_path.read_text(encoding="utf-8")
        overlay_skill_text = overlay_skill_path.read_text(encoding="utf-8")
        if not contains_phrase(
            overlay_text,
            (
                "does not change the base skill boundary",
                "does not redefine the base skill",
            ),
        ):
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_path, repo_root),
                    "project overlay must explicitly say that it does not change the base skill boundary",
                )
            )
        if not contains_phrase(
            overlay_skill_text,
            (
                "stub",
                "future stub",
            ),
        ):
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_skill_path, repo_root),
                    "project overlay skill must explicitly describe itself as a stub or future stub",
                )
            )
        if not contains_phrase(
            overlay_skill_text,
            (
                "repository-relative",
                "repo-relative",
            ),
        ):
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_skill_path, repo_root),
                    "project overlay skill must explicitly keep paths or commands repository-relative",
                )
            )

    return issues


def overlay_readiness_rows(repo_root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        return rows

    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.is_file():
            continue
        text = skill_path.read_text(encoding="utf-8")
        has_adaptation_points = "## Adaptation points" in text
        has_overlay_policy = (skill_dir / "agents" / "openai.yaml").is_file()
        rows.append(
            {
                "name": skill_dir.name,
                "overlay_hooks": "yes" if has_adaptation_points else "no",
                "invocation_stub": "yes" if has_overlay_policy else "no",
            }
        )
    return rows


def render_overlay_readiness_markdown(repo_root: Path) -> str:
    rows = overlay_readiness_rows(repo_root)
    lines = [
        "# Overlay readiness",
        "",
        "This derived file summarizes whether the current skill surface already exposes the minimum hooks for thin project overlays.",
        "It does not add real project-family skills; it only reflects repo-local readiness.",
        "",
        "| name | adaptation points | invocation stub |",
        "|---|---|---|",
    ]
    if not rows:
        lines.append("| - | - | - |")
    else:
        for row in rows:
            lines.append(
                f"| {row['name']} | {row['overlay_hooks']} | {row['invocation_stub']} |"
            )
    lines.append("")
    return "\n".join(lines)
