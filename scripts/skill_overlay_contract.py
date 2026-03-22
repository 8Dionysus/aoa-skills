from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import skill_artifact_contract
import skill_catalog_contract
import yaml


OVERLAY_STUBS_DIR = Path("tests") / "fixtures" / "overlay_stubs"
LIVE_OVERLAYS_DIR = Path("docs") / "overlays"
PROJECT_OVERLAY_FILE = "PROJECT_OVERLAY.md"
PROJECT_OVERLAY_SKILL_FILE = "PROJECT_OVERLAY_SKILL.md"
LIVE_OVERLAY_FAMILIES = ("atm10", "abyss")
OVERLAY_DIR_PREFIXES = tuple(f"{family}-" for family in LIVE_OVERLAY_FAMILIES)
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
LIVE_PROJECT_OVERLAY_HEADINGS = (
    "Purpose",
    "Authority",
    "Local surface",
    "Overlayed skills",
    "Risks and anti-patterns",
    "Validation",
)
OVERLAY_SKILL_BULLET_PATTERN = re.compile(r"^\s*-\s*`([a-z0-9-]+)`")


@dataclass(frozen=True)
class OverlayContractIssue:
    location: str
    message: str


def relative_location(path: Path, repo_root: Path) -> str:
    return skill_catalog_contract.relative_location(path, repo_root)


def contains_phrase(text: str, phrases: Sequence[str]) -> bool:
    normalized = " ".join(text.lower().split())
    return any(" ".join(phrase.lower().split()) in normalized for phrase in phrases)


def load_skill_scope(skill_path: Path) -> str | None:
    try:
        text = skill_path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        return None
    try:
        metadata = yaml.safe_load(frontmatter)
    except yaml.YAMLError:
        return None
    if not isinstance(metadata, dict):
        return None
    scope = metadata.get("scope")
    return scope if isinstance(scope, str) else None


def family_skill_names(repo_root: Path, family: str) -> list[str]:
    prefix = f"{family}-"
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(
        path.name
        for path in skills_dir.iterdir()
        if path.is_dir()
        and path.name.startswith(prefix)
        and load_skill_scope(path / "SKILL.md") == "project"
    )


def extract_overlay_skill_names(section_text: str) -> list[str]:
    skill_names: list[str] = []
    for raw_line in section_text.splitlines():
        match = OVERLAY_SKILL_BULLET_PATTERN.match(raw_line)
        if match is not None:
            skill_names.append(match.group(1))
    return skill_names


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


def collect_live_overlay_issues(repo_root: Path) -> list[OverlayContractIssue]:
    root = repo_root / LIVE_OVERLAYS_DIR
    issues: list[OverlayContractIssue] = []

    if root.is_dir():
        for overlay_dir in sorted(path for path in root.iterdir() if path.is_dir()):
            if overlay_dir.name not in LIVE_OVERLAY_FAMILIES:
                issues.append(
                    OverlayContractIssue(
                        relative_location(overlay_dir, repo_root),
                        "live overlay directories must be named 'atm10' or 'abyss'",
                    )
                )

    for family in LIVE_OVERLAY_FAMILIES:
        skill_names = family_skill_names(repo_root, family)
        overlay_path = root / family / PROJECT_OVERLAY_FILE

        if not skill_names:
            if overlay_path.is_file():
                issues.append(
                    OverlayContractIssue(
                        relative_location(overlay_path, repo_root),
                        f"live overlay '{family}' requires at least one matching skills/{family}-* bundle",
                    )
                )
            continue

        if not overlay_path.is_file():
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_path, repo_root),
                    f"live overlay family '{family}' is missing docs/overlays/{family}/PROJECT_OVERLAY.md",
                )
            )
            continue

        issues.extend(
            collect_overlay_heading_issues(
                overlay_path,
                repo_root,
                artifact_label="live project overlay",
                expected_headings=LIVE_PROJECT_OVERLAY_HEADINGS,
            )
        )

        overlay_text = overlay_path.read_text(encoding="utf-8")
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
                    "live project overlay must explicitly say that it does not change the base skill boundary",
                )
            )
        if not contains_phrase(
            overlay_text,
            (
                "repository-relative",
                "repo-relative",
            ),
        ):
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_path, repo_root),
                    "live project overlay must explicitly keep paths or commands repository-relative",
                )
            )

        sections = {
            heading: content
            for heading, content in skill_artifact_contract.extract_artifact_sections(overlay_text)
        }
        overlayed_skills = extract_overlay_skill_names(sections.get("Overlayed skills", ""))
        if not overlayed_skills:
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_path, repo_root),
                    f"live project overlay '{family}' must list matching skills/{family}-* bundles under 'Overlayed skills'",
                )
            )
            continue

        for skill_name in overlayed_skills:
            if not skill_name.startswith(f"{family}-"):
                issues.append(
                    OverlayContractIssue(
                        relative_location(overlay_path, repo_root),
                        f"live project overlay '{family}' may only list skills/{family}-* bundles under 'Overlayed skills'",
                    )
                )
                break

        listed = sorted(set(overlayed_skills))
        actual = sorted(skill_names)
        if listed != actual:
            missing = [name for name in actual if name not in listed]
            extra = [name for name in listed if name not in actual]
            if missing:
                issues.append(
                    OverlayContractIssue(
                        relative_location(overlay_path, repo_root),
                        f"live project overlay '{family}' must list matching skill bundle(s): {', '.join(missing)}",
                    )
                )
            if extra:
                issues.append(
                    OverlayContractIssue(
                        relative_location(overlay_path, repo_root),
                        f"live project overlay '{family}' lists unknown skill bundle(s): {', '.join(extra)}",
                    )
                )

    return issues


def live_overlay_families(repo_root: Path) -> list[str]:
    root = repo_root / LIVE_OVERLAYS_DIR
    return [
        family
        for family in LIVE_OVERLAY_FAMILIES
        if (root / family / PROJECT_OVERLAY_FILE).is_file()
    ]


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
    families = live_overlay_families(repo_root)
    lines = [
        "# Overlay readiness",
        "",
        "This derived file summarizes whether the current skill surface already exposes the minimum hooks for thin project overlays",
        "and which live exemplar overlay packs are committed in this repository.",
        "",
        f"- live exemplar overlay packs: {', '.join(families) if families else '-'}",
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
