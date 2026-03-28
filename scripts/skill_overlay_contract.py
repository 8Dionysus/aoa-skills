from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import skill_artifact_contract
import skill_catalog_contract
import skill_evaluation_surface
import skill_source_model
import yaml


OVERLAY_STUBS_DIR = Path("tests") / "fixtures" / "overlay_stubs"
LIVE_OVERLAYS_DIR = Path("docs") / "overlays"
PROJECT_OVERLAY_FILE = "PROJECT_OVERLAY.md"
LIVE_OVERLAY_REVIEW_FILE = "REVIEW.md"
PROJECT_OVERLAY_SKILL_FILE = "PROJECT_OVERLAY_SKILL.md"
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
LIVE_OVERLAY_REVIEW_HEADINGS = (
    "Current status",
    "Evidence reviewed",
    "Findings",
    "Gaps and blockers",
    "Recommendation",
)
OVERLAY_READINESS_VERSION = 1
OVERLAY_READINESS_JSON_PATH = Path("generated") / "overlay_readiness.json"
OVERLAY_READINESS_MARKDOWN_PATH = Path("generated") / "overlay_readiness.md"
OVERLAY_READINESS_SOURCE_OF_TRUTH = {
    "skill_markdown": "skills/*/SKILL.md",
    "runtime_examples": "skills/*/examples/*.md",
    "review_checks": "skills/*/checks/review.md",
    "overlay_docs": "docs/overlays/*/PROJECT_OVERLAY.md",
    "overlay_reviews": "docs/overlays/*/REVIEW.md",
    "evaluation_fixtures": "tests/fixtures/skill_evaluation_cases.yaml",
}
OVERLAY_SKILL_BULLET_PATTERN = re.compile(r"^\s*-\s*`([a-z0-9-]+)`")
OVERLAY_STUB_DIR_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")


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


def skill_family_name(skill_name: str) -> str | None:
    family, separator, remainder = skill_name.partition("-")
    if not separator or not family or not remainder:
        return None
    return family


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


def project_skill_families(repo_root: Path) -> list[str]:
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        return []
    families = {
        family
        for path in skills_dir.iterdir()
        if path.is_dir()
        for family in [skill_family_name(path.name)]
        if family is not None and load_skill_scope(path / "SKILL.md") == "project"
    }
    return sorted(families)


def declared_live_overlay_dirs(repo_root: Path) -> list[Path]:
    root = repo_root / LIVE_OVERLAYS_DIR
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir())


def overlay_doc_families(repo_root: Path) -> list[str]:
    return sorted(
        overlay_dir.name
        for overlay_dir in declared_live_overlay_dirs(repo_root)
        if (overlay_dir / PROJECT_OVERLAY_FILE).is_file()
    )


def live_overlay_families(repo_root: Path) -> list[str]:
    return sorted(
        set(project_skill_families(repo_root)) | set(overlay_doc_families(repo_root))
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
        if OVERLAY_STUB_DIR_PATTERN.match(stub_dir.name) is None:
            issues.append(
                OverlayContractIssue(
                    relative_location(stub_dir, repo_root),
                    "overlay stub directories must follow '<family>-<stub-name>' naming",
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

    for overlay_dir in declared_live_overlay_dirs(repo_root):
        overlay_path = overlay_dir / PROJECT_OVERLAY_FILE
        if not overlay_path.is_file():
            issues.append(
                OverlayContractIssue(
                    relative_location(overlay_dir, repo_root),
                    f"live overlay directory '{overlay_dir.name}' must include {PROJECT_OVERLAY_FILE}",
                )
            )

    for family in live_overlay_families(repo_root):
        skill_names = family_skill_names(repo_root, family)
        overlay_path = root / family / PROJECT_OVERLAY_FILE
        review_path = root / family / LIVE_OVERLAY_REVIEW_FILE

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

        if not review_path.is_file():
            issues.append(
                OverlayContractIssue(
                    relative_location(review_path, repo_root),
                    f"live overlay family '{family}' is missing docs/overlays/{family}/REVIEW.md",
                )
            )
        else:
            issues.extend(
                collect_overlay_heading_issues(
                    review_path,
                    repo_root,
                    artifact_label="live overlay family review",
                    expected_headings=LIVE_OVERLAY_REVIEW_HEADINGS,
                )
            )
            review_text = review_path.read_text(encoding="utf-8")
            if not _review_mentions_all_skills(review_text, skill_names):
                issues.append(
                    OverlayContractIssue(
                        relative_location(review_path, repo_root),
                        f"live overlay family review '{family}' must mention every matching skills/{family}-* bundle",
                    )
                )

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

        for skill_name in actual:
            review_check_path = (
                repo_root / "skills" / skill_name / "checks" / "review.md"
            )
            if not review_check_path.is_file():
                issues.append(
                    OverlayContractIssue(
                        relative_location(review_check_path, repo_root),
                        f"live overlay family '{family}' requires skills/{skill_name}/checks/review.md",
                    )
                )

    return issues


def _overlay_path(repo_root: Path, family: str) -> Path:
    return repo_root / LIVE_OVERLAYS_DIR / family / PROJECT_OVERLAY_FILE


def _overlay_review_path(repo_root: Path, family: str) -> Path:
    return repo_root / LIVE_OVERLAYS_DIR / family / LIVE_OVERLAY_REVIEW_FILE


def _overlay_sections(path: Path) -> dict[str, str]:
    return {
        heading: content
        for heading, content in skill_artifact_contract.extract_artifact_sections(
            path.read_text(encoding="utf-8")
        )
    }


def _review_mentions_all_skills(review_text: str, skill_names: Sequence[str]) -> bool:
    normalized = " ".join(review_text.lower().split())
    return all(skill_name.lower() in normalized for skill_name in skill_names)


def _evaluation_entry_by_name(
    payload: Mapping[str, Any],
    skill_name: str,
) -> Mapping[str, Any]:
    for entry in payload.get("skills", []):
        if isinstance(entry, Mapping) and entry.get("name") == skill_name:
            return entry
    raise KeyError(skill_name)


def _project_skill_sources(repo_root: Path) -> list[skill_source_model.SkillSource]:
    return [
        source
        for source in skill_source_model.load_skill_sources(repo_root)
        if source.metadata.get("scope") == "project"
    ]


def _project_skill_entry(
    repo_root: Path,
    source: skill_source_model.SkillSource,
    evaluation_entry: Mapping[str, Any],
) -> dict[str, Any]:
    review_check_path = source.skill_dir / "checks" / "review.md"
    runtime_examples = [
        artifact
        for artifact in source.support_artifacts
        if artifact.get("type") == skill_artifact_contract.RUNTIME_EXAMPLE_TYPE
    ]
    return {
        "name": source.name,
        "family": source.name.split("-", 1)[0],
        "status": source.metadata.get("status"),
        "skill_path": relative_location(source.skill_md_path, repo_root),
        "review_check_path": (
            relative_location(review_check_path, repo_root)
            if review_check_path.is_file()
            else None
        ),
        "runtime_example_count": len(runtime_examples),
        "has_adaptation_points": "Adaptation points" in source.sections,
        "has_policy_file": source.policy_exists,
        "eval_ready": bool(evaluation_entry.get("canonical_eval_ready")),
        "eval_blockers": list(evaluation_entry.get("canonical_eval_blockers", [])),
    }


def build_overlay_readiness_payload(repo_root: Path) -> dict[str, Any]:
    project_sources = _project_skill_sources(repo_root)
    evaluation_payload = skill_evaluation_surface.build_evaluation_matrix_payload(
        repo_root,
        [source.name for source in project_sources],
    )
    skills = [
        _project_skill_entry(
            repo_root,
            source,
            _evaluation_entry_by_name(evaluation_payload, source.name),
        )
        for source in project_sources
    ]

    families: list[dict[str, Any]] = []
    for family in live_overlay_families(repo_root):
        overlay_path = _overlay_path(repo_root, family)
        review_path = _overlay_review_path(repo_root, family)
        project_skill_names = sorted(
            entry["name"] for entry in skills if entry["family"] == family
        )

        listed_skill_names: list[str] = []
        boundary_statement_present = False
        repo_relative_statement_present = False
        authority_section_present = False
        if overlay_path.is_file():
            overlay_text = overlay_path.read_text(encoding="utf-8")
            sections = _overlay_sections(overlay_path)
            listed_skill_names = extract_overlay_skill_names(
                sections.get("Overlayed skills", "")
            )
            boundary_statement_present = contains_phrase(
                overlay_text,
                (
                    "does not change the base skill boundary",
                    "does not redefine the base skill",
                ),
            )
            repo_relative_statement_present = contains_phrase(
                overlay_text,
                (
                    "repository-relative",
                    "repo-relative",
                ),
            )
            authority_section_present = "Authority" in sections

        review_mentions_all_skills = False
        if review_path.is_file():
            review_mentions_all_skills = _review_mentions_all_skills(
                review_path.read_text(encoding="utf-8"),
                project_skill_names,
            )

        bundle_review_check_count = sum(
            1
            for entry in skills
            if entry["family"] == family and entry["review_check_path"] is not None
        )
        eval_ready_skill_count = sum(
            1
            for entry in skills
            if entry["family"] == family and entry["eval_ready"]
        )
        listed_matches_actual = sorted(set(listed_skill_names)) == project_skill_names
        readiness_state = (
            "reviewable"
            if review_path.is_file()
            and listed_matches_actual
            and bundle_review_check_count == len(project_skill_names)
            and eval_ready_skill_count == len(project_skill_names)
            and boundary_statement_present
            and repo_relative_statement_present
            and authority_section_present
            and review_mentions_all_skills
            else "baseline"
        )

        families.append(
            {
                "family": family,
                "project_overlay_path": (
                    relative_location(overlay_path, repo_root)
                    if overlay_path.is_file()
                    else None
                ),
                "review_path": (
                    relative_location(review_path, repo_root)
                    if review_path.is_file()
                    else None
                ),
                "project_skill_names": project_skill_names,
                "listed_skill_names": sorted(set(listed_skill_names)),
                "listed_matches_actual": listed_matches_actual,
                "project_skill_count": len(project_skill_names),
                "bundle_review_check_count": bundle_review_check_count,
                "eval_ready_skill_count": eval_ready_skill_count,
                "boundary_statement_present": boundary_statement_present,
                "repo_relative_statement_present": repo_relative_statement_present,
                "authority_section_present": authority_section_present,
                "review_mentions_all_skills": review_mentions_all_skills,
                "readiness_state": readiness_state,
            }
        )

    reviewable_families = [
        entry for entry in families if entry.get("readiness_state") == "reviewable"
    ]
    skills_with_review_checks = [
        entry for entry in skills if entry.get("review_check_path") is not None
    ]
    eval_ready_skills = [entry for entry in skills if entry.get("eval_ready")]

    return {
        "overlay_readiness_version": OVERLAY_READINESS_VERSION,
        "source_of_truth": OVERLAY_READINESS_SOURCE_OF_TRUTH,
        "summary": {
            "live_overlay_family_count": len(families),
            "reviewable_family_count": len(reviewable_families),
            "project_skill_count": len(skills),
            "project_skill_review_check_count": len(skills_with_review_checks),
            "eval_ready_project_skill_count": len(eval_ready_skills),
        },
        "families": families,
        "skills": skills,
    }


def render_overlay_readiness_markdown(payload: Mapping[str, Any]) -> str:
    families = payload.get("families", [])
    skills = payload.get("skills", [])
    summary = payload.get("summary", {})
    lines = [
        "# Overlay readiness",
        "",
        "This derived file summarizes live overlay-family maturity and project-skill readiness",
        "for the thin overlay layer in `aoa-skills`.",
        "`reviewable` is the current mature exemplar target for a live project-overlay family in this repo.",
        "Use this surface for family maturity and `generated/governance_backlog.md` for per-skill maintenance readout.",
        "",
        "## Summary",
        "",
        f"- live overlay families: {summary.get('live_overlay_family_count', 0)}",
        f"- reviewable families: {summary.get('reviewable_family_count', 0)}",
        f"- project overlay skills: {summary.get('project_skill_count', 0)}",
        f"- project skills with review checklists: {summary.get('project_skill_review_check_count', 0)}",
        f"- eval-ready project skills: {summary.get('eval_ready_project_skill_count', 0)}",
        "",
        "## Families",
        "",
        "| family | skills | listed parity | family review | bundle review checks | eval-ready skills | repo-relative evidence | boundary evidence | readiness |",
        "|---|---:|---|---|---:|---:|---|---|---|",
    ]
    if not families:
        lines.append("| - | - | - | - | - | - | - | - | - |")
    else:
        for row in families:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["family"]),
                        str(row["project_skill_count"]),
                        "true" if row["listed_matches_actual"] else "false",
                        str(row["review_path"] or "-"),
                        str(row["bundle_review_check_count"]),
                        str(row["eval_ready_skill_count"]),
                        "true" if row["repo_relative_statement_present"] else "false",
                        "true" if row["boundary_statement_present"] else "false",
                        str(row["readiness_state"]),
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Project skills",
            "",
            "| name | family | status | review checklist | runtime examples | adaptation points | policy file | eval ready | blockers |",
            "|---|---|---|---|---:|---|---|---|---|",
        ]
    )
    if not skills:
        lines.append("| - | - | - | - | - | - | - | - | - |")
    else:
        for entry in skills:
            blockers = ", ".join(entry.get("eval_blockers", [])) or "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(entry["name"]),
                        str(entry["family"]),
                        str(entry["status"]),
                        str(entry["review_check_path"] or "-"),
                        str(entry["runtime_example_count"]),
                        "true" if entry["has_adaptation_points"] else "false",
                        "true" if entry["has_policy_file"] else "false",
                        "true" if entry["eval_ready"] else "false",
                        blockers,
                    ]
                )
                + " |"
            )
    lines.append("")
    return "\n".join(lines)
