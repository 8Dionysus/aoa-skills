from __future__ import annotations

import ast
import contextlib
import io
import inspect
import json
import re
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validation import validate_skills
from builders import build_catalog
from skill_model import skill_lineage_surface
from skill_model import skill_review_surface
from validation.validators import (
    generated_surface,
    questbook_contract,
    questbook_surface,
    skill_status_surface,
)


PRIMARY_PUBLISHED_TECHNIQUE = {
    "id": "AOA-T-0001",
    "repo": "8Dionysus/aoa-techniques",
    "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
    "source_ref": "0123456789abcdef0123456789abcdef01234567",
    "use_sections": [
        "Intent",
        "When to use",
        "Inputs",
        "Outputs",
        "Core procedure",
        "Contracts",
        "Risks",
        "Validation",
    ],
}
SECONDARY_PUBLISHED_TECHNIQUE = {
    "id": "AOA-T-0002",
    "repo": "8Dionysus/aoa-techniques",
    "path": "techniques/docs/source-of-truth-layout/TECHNIQUE.md",
    "source_ref": "0123456789abcdef0123456789abcdef01234567",
    "use_sections": ["summary"],
}
PENDING_TECHNIQUE = {
    "id": "AOA-T-PENDING-TEST",
    "repo": "8Dionysus/aoa-techniques",
    "path": "TBD",
    "source_ref": "TBD",
    "use_sections": ["Intent"],
}
PENDING_NOTE = "Replace AOA-T-PENDING-TEST, path TBD, and source_ref TBD after publish."


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_valid_questbook_surface(repo_root: Path) -> None:
    write_text(
        repo_root / "QUESTBOOK.md",
        (REPO_ROOT / "QUESTBOOK.md").read_text(encoding="utf-8"),
    )
    write_text(
        repo_root
        / "mechanics"
        / "questbook"
        / "docs"
        / "QUESTBOOK_SKILL_INTEGRATION.md",
        (
            REPO_ROOT
            / "mechanics"
            / "questbook"
            / "docs"
            / "QUESTBOOK_SKILL_INTEGRATION.md"
        ).read_text(encoding="utf-8"),
    )
    write_text(
        repo_root / "mechanics" / "questbook" / "schemas" / "quest.schema.json",
        (
            REPO_ROOT / "mechanics" / "questbook" / "schemas" / "quest.schema.json"
        ).read_text(encoding="utf-8"),
    )
    write_text(
        repo_root
        / "mechanics"
        / "questbook"
        / "schemas"
        / "quest_dispatch.schema.json",
        (
            REPO_ROOT
            / "mechanics"
            / "questbook"
            / "schemas"
            / "quest_dispatch.schema.json"
        ).read_text(encoding="utf-8"),
    )
    for quest_path in sorted((REPO_ROOT / "quests").glob("**/AOA-SK-Q-*.yaml")):
        write_text(
            repo_root / quest_path.relative_to(REPO_ROOT),
            quest_path.read_text(encoding="utf-8"),
        )
    write_text(
        repo_root / "generated" / "quest_catalog.min.json",
        (REPO_ROOT / "generated" / "quest_catalog.min.json").read_text(
            encoding="utf-8"
        ),
    )
    write_text(
        repo_root / "generated" / "quest_dispatch.min.json",
        (REPO_ROOT / "generated" / "quest_dispatch.min.json").read_text(
            encoding="utf-8"
        ),
    )
    write_text(
        repo_root / "generated" / "quest_catalog.min.example.json",
        (REPO_ROOT / "generated" / "quest_catalog.min.example.json").read_text(
            encoding="utf-8"
        ),
    )
    write_text(
        repo_root / "generated" / "quest_dispatch.min.example.json",
        (REPO_ROOT / "generated" / "quest_dispatch.min.example.json").read_text(
            encoding="utf-8"
        ),
    )


def quest_fixture_path(repo_root: Path, quest_id: str) -> Path:
    matches = sorted((repo_root / "quests").glob(f"**/{quest_id}.yaml"))
    if not matches:
        return repo_root / "quests" / f"{quest_id}.yaml"
    return matches[0]


class ValidateSkillsCase(unittest.TestCase):
    def add_skill_bundle(
        self,
        repo_root: Path,
        *,
        skill_name: str,
        scope: str = "core",
        traceability_heading: str = "Technique traceability",
        invocation_mode: str = "explicit-preferred",
        status: str = "scaffold",
        include_support_artifact: bool = True,
        include_techniques_manifest: bool = True,
        policy_allow_implicit: bool | None = None,
        techniques: list[dict] | None = None,
        notes: list[str] | None = None,
        include_composition_exception_review: bool | None = None,
    ) -> None:
        skill_dir = repo_root / "skills" / skill_name
        skill_dir.mkdir()

        resolved_techniques = techniques or [PRIMARY_PUBLISHED_TECHNIQUE]
        technique_ids = [entry["id"] for entry in resolved_techniques]
        skill_md = textwrap.dedent(
            f"""\
            ---
            name: {skill_name}
            scope: {scope}
            status: {status}
            summary: Test skill summary.
            invocation_mode: {invocation_mode}
            technique_dependencies:
            """
        )
        for technique_id in technique_ids:
            skill_md += f"  - {technique_id}\n"
        skill_md += textwrap.dedent(
            f"""\

            ---

            # {skill_name}

            ## Intent

            Intent text.

            ## Trigger boundary

            Use this skill when:
            - needed

            Do not use this skill when:
            - not needed

            ## Inputs

            - input

            ## Outputs

            - output

            ## Procedure

            1. step

            ## Contracts

            - contract

            ## Risks and anti-patterns

            - risk

            ## Verification

            - verify

            ## {traceability_heading}

            Traceability text.

            ## Adaptation points

            - adapt
            """
        )
        (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

        if include_support_artifact:
            examples_dir = skill_dir / "examples"
            examples_dir.mkdir()
            (examples_dir / "example.md").write_text(
                textwrap.dedent(
                    """\
                    # Example

                    ## Scenario

                    Example scenario.

                    ## Why this skill fits

                    - the workflow is bounded

                    ## Expected inputs

                    - input

                    ## Expected outputs

                    - output

                    ## Boundary notes

                    - keep the task bounded

                    ## Verification notes

                    - verify the result
                    """
                ),
                encoding="utf-8",
            )

        if include_techniques_manifest:
            manifest = {
                "skill_name": skill_name,
                "composition_mode": "bounded",
                "techniques": resolved_techniques,
            }
            if notes is not None:
                manifest["notes"] = notes
            (skill_dir / "techniques.yaml").write_text(
                yaml.safe_dump(manifest, sort_keys=False),
                encoding="utf-8",
            )

        if policy_allow_implicit is not None:
            agents_dir = skill_dir / "agents"
            agents_dir.mkdir()
            policy = {
                "policy": {"allow_implicit_invocation": policy_allow_implicit},
                "notes": ["Test policy."],
            }
            (agents_dir / "openai.yaml").write_text(
                yaml.safe_dump(policy, sort_keys=False),
                encoding="utf-8",
            )

        if include_composition_exception_review is None:
            include_composition_exception_review = len(technique_ids) == 1
        if include_composition_exception_review:
            self.write_skill_composition_exception_review(
                repo_root,
                skill_name=skill_name,
                technique_ids=technique_ids,
            )

    def make_repo(
        self,
        *,
        skill_name: str = "aoa-test-skill",
        scope: str = "core",
        traceability_heading: str = "Technique traceability",
        invocation_mode: str = "explicit-preferred",
        status: str = "scaffold",
        include_support_artifact: bool = True,
        include_techniques_manifest: bool = True,
        policy_allow_implicit: bool | None = None,
        techniques: list[dict] | None = None,
        notes: list[str] | None = None,
        index_names: list[str] | None = None,
        review_record_surface: str | None = None,
        include_composition_exception_review: bool | None = None,
    ) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-validator-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        (repo_root / "config").mkdir()
        write_valid_questbook_surface(repo_root)

        if index_names is None:
            index_names = [skill_name]
        self.write_skill_index(repo_root, index_names)
        self.write_skill_pack_profiles(repo_root, index_names)
        self.add_skill_bundle(
            repo_root,
            skill_name=skill_name,
            scope=scope,
            traceability_heading=traceability_heading,
            invocation_mode=invocation_mode,
            status=status,
            include_support_artifact=include_support_artifact,
            include_techniques_manifest=include_techniques_manifest,
            policy_allow_implicit=policy_allow_implicit,
            techniques=techniques,
            notes=notes,
            include_composition_exception_review=include_composition_exception_review,
        )
        if review_record_surface is not None:
            self.add_public_review_record(repo_root, skill_name, review_record_surface)
        self.write_governance_lanes(
            repo_root,
            self.default_governance_lanes(
                skill_name=skill_name,
                scope=scope,
                status=status,
            ),
        )
        if include_techniques_manifest:
            try:
                self.write_catalogs(repo_root)
            except ValueError:
                pass

        return repo_root

    def add_public_review_record(
        self,
        repo_root: Path,
        skill_name: str,
        surface: str,
    ) -> None:
        if surface == "status-promotions":
            review_dir = repo_root / "docs" / "reviews" / "status-promotions"
            title = f"# {skill_name} status promotion review\n"
        elif surface == "canonical-candidates":
            review_dir = repo_root / "docs" / "reviews" / "canonical-candidates"
            title = f"# {skill_name} candidate review\n"
        else:
            raise ValueError(f"unknown review surface '{surface}'")

        review_dir.mkdir(parents=True, exist_ok=True)
        (review_dir / f"{skill_name}.md").write_text(
            title + "\n## Findings\n\n- Evidence exists.\n",
            encoding="utf-8",
        )

    def default_governance_lanes(
        self,
        *,
        skill_name: str,
        scope: str,
        status: str,
    ) -> list[dict]:
        if not skill_name.startswith("aoa-"):
            return []
        if scope == "project":
            return []
        if status not in {"evaluated", "canonical"}:
            return []
        lane_id = f"{skill_name.replace('-', '_')}_lane"
        return [
            {
                "id": lane_id,
                "title": f"{skill_name} governance lane",
                "scope": "risk" if scope == "risk" else "core",
                "state": (
                    "stable_defaults"
                    if status == "canonical"
                    else "comparative_pending"
                ),
                "skills": [
                    {
                        "name": skill_name,
                        "decision": (
                            "default_reference"
                            if status == "canonical"
                            else "stay_evaluated"
                        ),
                    }
                ],
                "review_path": f"docs/governance/lanes.md#{lane_id}",
                "evidence_case_ids": [],
            }
        ]

    def write_governance_lanes(self, repo_root: Path, lanes: list[dict]) -> None:
        governance_dir = repo_root / "docs" / "governance"
        governance_dir.mkdir(parents=True, exist_ok=True)
        headings = "\n\n".join(f"## {lane['id']}\n\nLane notes.\n" for lane in lanes)
        if not headings:
            headings = "## governance\n\nLane notes.\n"
        (governance_dir / "lanes.md").write_text(
            "# Governance lanes\n\n"
            "Candidate-ready is a gate-pass signal only.\n\n" + headings,
            encoding="utf-8",
        )
        (governance_dir / "lanes.yaml").write_text(
            yaml.safe_dump(
                {
                    "governance_lanes_version": 1,
                    "lanes": lanes,
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def write_evaluation_fixtures_for_skill(
        self,
        repo_root: Path,
        *,
        skill_name: str = "aoa-test-skill",
        include_autonomy: bool = True,
        use_cases: int = 1,
        do_not_use_cases: int = 1,
        use_snapshots: int = 1,
        do_not_use_snapshots: int = 1,
    ) -> None:
        fixtures_dir = repo_root / "tests" / "fixtures"
        fixtures_dir.mkdir(parents=True, exist_ok=True)
        snapshots_dir = fixtures_dir / "skill_evaluation_snapshots" / skill_name
        snapshots_dir.mkdir(parents=True, exist_ok=True)

        data: dict[str, list[dict]] = {
            "autonomy_checks": [],
            "trigger_cases": [],
            "snapshot_cases": [],
            "adjacency_cases": [],
        }
        if include_autonomy:
            data["autonomy_checks"].append(
                {
                    "skill": skill_name,
                    "forbidden_runtime_terms": ["aoa-techniques"],
                }
            )

        for index in range(use_cases):
            data["trigger_cases"].append(
                {
                    "skill": skill_name,
                    "case_id": f"{skill_name.replace('-', '_')}_use_{index + 1}",
                    "prompt": "use case",
                    "expected": "use",
                    "required_phrases": ["needed"],
                }
            )
        for index in range(do_not_use_cases):
            data["trigger_cases"].append(
                {
                    "skill": skill_name,
                    "case_id": f"{skill_name.replace('-', '_')}_do_not_use_{index + 1}",
                    "prompt": "do not use case",
                    "expected": "do_not_use",
                    "required_phrases": ["not needed"],
                }
            )

        for index in range(use_snapshots):
            case_id = f"{skill_name.replace('-', '_')}_use_{index + 1}"
            snapshot_path = snapshots_dir / f"{case_id}.md"
            snapshot_path.write_text(
                textwrap.dedent(
                    f"""\
                    # Evaluation Snapshot

                    ## Prompt

                    use case

                    ## Expected selection

                    Decision: use `{skill_name}`.

                    ## Why

                    - the bounded trigger is needed

                    ## Expected object

                    - output

                    ## Boundary notes

                    - stay inside the bounded surface

                    ## Verification hooks

                    - verify the output
                    """
                ),
                encoding="utf-8",
            )
            data["snapshot_cases"].append(
                {
                    "skill": skill_name,
                    "case_id": case_id,
                    "prompt": "use case",
                    "expected": "use",
                    "snapshot_path": snapshot_path.relative_to(repo_root).as_posix(),
                    "required_output_phrases": [
                        f"Decision: use `{skill_name}`.",
                        "output",
                    ],
                    "forbidden_output_phrases": [
                        f"Decision: do_not_use `{skill_name}`."
                    ],
                }
            )

        for index in range(do_not_use_snapshots):
            case_id = f"{skill_name.replace('-', '_')}_do_not_use_{index + 1}"
            snapshot_path = snapshots_dir / f"{case_id}.md"
            snapshot_path.write_text(
                textwrap.dedent(
                    f"""\
                    # Evaluation Snapshot

                    ## Prompt

                    do not use case

                    ## Expected selection

                    Decision: do_not_use `{skill_name}`.

                    ## Why

                    - the task is not needed here

                    ## Expected object

                    - redirect to a better fit

                    ## Boundary notes

                    - keep the decision bounded

                    ## Verification hooks

                    - confirm the deflection is explicit
                    """
                ),
                encoding="utf-8",
            )
            data["snapshot_cases"].append(
                {
                    "skill": skill_name,
                    "case_id": case_id,
                    "prompt": "do not use case",
                    "expected": "do_not_use",
                    "snapshot_path": snapshot_path.relative_to(repo_root).as_posix(),
                    "required_output_phrases": [
                        f"Decision: do_not_use `{skill_name}`.",
                        "redirect",
                    ],
                    "forbidden_output_phrases": [f"Decision: use `{skill_name}`."],
                }
            )

        (fixtures_dir / "skill_evaluation_cases.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False),
            encoding="utf-8",
        )

    def write_skill_index(self, repo_root: Path, index_names: list[str]) -> None:
        rows = "\n".join(
            f"| {name} | core | scaffold | Test summary. |" for name in index_names
        )
        content = (
            "# SKILL_INDEX\n\n"
            "| name | scope | status | summary |\n"
            "|---|---|---|---|\n"
            f"{rows}\n"
        )
        (repo_root / "SKILL_INDEX.md").write_text(content, encoding="utf-8")

    def run_main(self, repo_root: Path, argv: list[str] | None = None) -> int:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            return validate_skills.main(argv or [], repo_root=repo_root)

    def write_catalogs(self, repo_root: Path) -> None:
        if not (repo_root / "QUESTBOOK.md").is_file():
            write_valid_questbook_surface(repo_root)
        config_path = repo_root / "config" / "skill_pack_profiles.json"
        if not config_path.exists():
            (repo_root / "config").mkdir(exist_ok=True)
            skill_names = sorted(
                path.name for path in (repo_root / "skills").iterdir() if path.is_dir()
            )
            self.write_skill_pack_profiles(repo_root, skill_names)
        for spec in build_catalog.generated_surface_specs(repo_root):
            build_catalog.write_generated_surface(repo_root, spec)

    def write_skill_pack_profiles(
        self, repo_root: Path, skill_names: list[str]
    ) -> None:
        (repo_root / "config" / "skill_pack_profiles.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "profile": "codex-facing-wave-3",
                    "profiles": {
                        "repo-default": {
                            "description": "Test install profile.",
                            "scope": "repo",
                            "install_mode": "symlink-preferred",
                            "skills": skill_names,
                        }
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def write_skill_composition_exception_review(
        self,
        repo_root: Path,
        *,
        skill_name: str = "aoa-test-skill",
        technique_ids: list[str] | None = None,
        recommendation: str = "keep_exception",
        malformed: bool = False,
    ) -> None:
        review_path = (
            repo_root
            / "docs"
            / "reviews"
            / "skill-composition-exceptions"
            / f"{skill_name}.md"
        )
        review_path.parent.mkdir(parents=True, exist_ok=True)
        technique_ids = technique_ids or ["AOA-T-0001"]
        if malformed:
            review_path.write_text(
                textwrap.dedent(
                    f"""\
                    # {skill_name}

                    ## Current shape

                    - skill: `{skill_name}`

                    ## Recommendation

                    - `{recommendation}`
                    """
                ),
                encoding="utf-8",
            )
            return

        technique_lines = "\n".join(
            f"  - `{technique_id}`" for technique_id in technique_ids
        )
        review_path.write_text(
            textwrap.dedent(
                f"""\
                # {skill_name}

                ## Current shape

                - skill: `{skill_name}`
                - technique_count: `{len(technique_ids)}`
                - technique_ids:
                {technique_lines}
                - composition_class: `single_technique_exception`

                ## Package rationale

                This stays in the skill layer because it packages a bounded workflow.

                ## Why this is not just the technique

                The skill adds invocation, output, and review boundaries around the technique.

                ## Adjacent skills considered

                - `aoa-other-skill`

                ## Recommendation

                - `{recommendation}`
                """
            ),
            encoding="utf-8",
        )

    def write_review_checklist(self, repo_root: Path, skill_name: str) -> None:
        review_path = repo_root / "skills" / skill_name / "checks" / "review.md"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text(
            textwrap.dedent(
                f"""\
                # Review Checklist

                ## Purpose

                Review checklist for `{skill_name}`.

                ## When it applies

                - when a live overlay family needs review evidence

                ## Review checklist

                - [ ] confirm the local overlay wording stays bounded
                - [ ] confirm repo-relative files and commands stay explicit

                ## Not a fit

                - not for broad playbooks or scenario bundles
                """
            ),
            encoding="utf-8",
        )

    def write_live_overlay_pack(
        self,
        repo_root: Path,
        *,
        family: str,
        skill_names: list[str],
        listed_skill_names: list[str] | None = None,
        repo_relative_language: bool = True,
        include_review_doc: bool = True,
        review_check_skill_names: list[str] | None = None,
        review_mentions_skill_names: list[str] | None = None,
    ) -> None:
        overlay_dir = repo_root / "mechanics" / "boundary-bridge" / "overlays" / family
        overlay_dir.mkdir(parents=True, exist_ok=True)
        listed_skill_names = (
            skill_names if listed_skill_names is None else listed_skill_names
        )
        review_check_skill_names = (
            skill_names
            if review_check_skill_names is None
            else review_check_skill_names
        )
        review_mentions_skill_names = (
            skill_names
            if review_mentions_skill_names is None
            else review_mentions_skill_names
        )
        local_surface_line = (
            "- repo-relative docs and commands remain explicit"
            if repo_relative_language
            else "- keep commands and paths explicit"
        )
        authority_line = (
            "- local maintainers own repo-relative authority"
            if repo_relative_language
            else "- local maintainers own authority"
        )
        review_refs = ", ".join(
            f"`skills/{skill_name}/checks/review.md`"
            for skill_name in review_check_skill_names
        )
        if not review_refs:
            review_refs = "- no bundle-local review checklists authored"
        else:
            review_refs = f"- bundle-local review checklists: {review_refs}"
        overlay_lines = [
            f"# {family} overlay",
            "",
            "## Purpose",
            "",
            (
                "This exemplar overlay pack keeps repo-relative local adaptation explicit."
                if repo_relative_language
                else "This exemplar overlay pack keeps local adaptation explicit."
            ),
            "It does not change the base skill boundary.",
            "",
            "## Authority",
            "",
            f"- overlay family: `{family}`",
            authority_line,
            "",
            "## Local surface",
            "",
            local_surface_line,
            f"- family review doc: `mechanics/boundary-bridge/overlays/{family}/REVIEW.md`",
            review_refs,
            "",
            "## Overlayed skills",
            "",
            *[f"- `{skill_name}`" for skill_name in listed_skill_names],
            "",
            "## Risks and anti-patterns",
            "",
            "- do not widen the pack into a playbook",
            "",
            "## Validation",
            "",
            f"- confirm `skills/{family}-*` bundles stay aligned",
            "",
        ]
        (overlay_dir / "PROJECT_OVERLAY.md").write_text(
            "\n".join(overlay_lines),
            encoding="utf-8",
        )

        if include_review_doc:
            review_lines = [
                f"# {family} overlay family review",
                "",
                "## Current status",
                "",
                f"- overlay family: `{family}`",
                f"- reviewed skills: {', '.join(f'`{skill_name}`' for skill_name in review_mentions_skill_names)}",
                "",
                "## Evidence reviewed",
                "",
                f"- `mechanics/boundary-bridge/overlays/{family}/PROJECT_OVERLAY.md`",
                f"- bundle-local review checklists under `skills/{family}-*/checks/review.md`",
                "",
                "## Findings",
                "",
                *[
                    f"- reviewed `{skill_name}` against the family overlay contract"
                    for skill_name in review_mentions_skill_names
                ],
                "",
                "## Gaps and blockers",
                "",
                "- no blocker identified in this bounded test fixture",
                "",
                "## Recommendation",
                "",
                f"Keep `{family}` as a thin reviewable overlay family.",
                "",
            ]
            (overlay_dir / "REVIEW.md").write_text(
                "\n".join(review_lines),
                encoding="utf-8",
            )

        for skill_name in review_check_skill_names:
            self.write_review_checklist(repo_root, skill_name)

    def make_live_overlay_repo(
        self,
        *,
        overlay_specs: list[dict[str, Any]],
    ) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-validator-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        write_valid_questbook_surface(repo_root)

        skill_specs = [
            skill_spec
            for overlay_spec in overlay_specs
            for skill_spec in overlay_spec["skill_specs"]
        ]
        self.write_skill_index(
            repo_root,
            [str(skill_spec["skill_name"]) for skill_spec in skill_specs],
        )
        for skill_spec in skill_specs:
            self.add_skill_bundle(repo_root, **skill_spec)

        for overlay_spec in overlay_specs:
            self.write_live_overlay_pack(
                repo_root,
                family=str(overlay_spec["family"]),
                skill_names=list(overlay_spec["skill_names"]),
                listed_skill_names=overlay_spec.get("listed_skill_names"),
                repo_relative_language=bool(
                    overlay_spec.get("repo_relative_language", True)
                ),
                include_review_doc=bool(overlay_spec.get("include_review_doc", True)),
                review_check_skill_names=overlay_spec.get("review_check_skill_names"),
                review_mentions_skill_names=overlay_spec.get(
                    "review_mentions_skill_names"
                ),
            )

        self.write_catalogs(repo_root)
        return repo_root

    def load_skill_frontmatter(
        self, repo_root: Path, skill_name: str = "aoa-test-skill"
    ) -> dict:
        skill_md_path = repo_root / "skills" / skill_name / "SKILL.md"
        text = skill_md_path.read_text(encoding="utf-8")
        _, frontmatter, _ = text.split("---", 2)
        return yaml.safe_load(frontmatter)

    def write_skill_frontmatter(
        self,
        repo_root: Path,
        frontmatter: dict,
        skill_name: str = "aoa-test-skill",
    ) -> None:
        skill_md_path = repo_root / "skills" / skill_name / "SKILL.md"
        text = skill_md_path.read_text(encoding="utf-8")
        _, _, body = text.split("---", 2)
        updated = (
            "---\n"
            + yaml.safe_dump(frontmatter, sort_keys=False).strip()
            + "\n---"
            + body
        )
        skill_md_path.write_text(updated, encoding="utf-8")

    def load_manifest(
        self, repo_root: Path, skill_name: str = "aoa-test-skill"
    ) -> dict:
        manifest_path = repo_root / "skills" / skill_name / "techniques.yaml"
        return yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    def write_manifest(
        self,
        repo_root: Path,
        manifest: dict,
        skill_name: str = "aoa-test-skill",
    ) -> None:
        manifest_path = repo_root / "skills" / skill_name / "techniques.yaml"
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )

    def write_policy(self, repo_root: Path, policy: dict) -> None:
        policy_path = repo_root / "skills" / "aoa-test-skill" / "agents" / "openai.yaml"
        policy_path.parent.mkdir(parents=True, exist_ok=True)
        policy_path.write_text(
            yaml.safe_dump(policy, sort_keys=False),
            encoding="utf-8",
        )

    def load_capsules(self, repo_root: Path) -> dict:
        capsule_path = repo_root / "generated" / "skill_capsules.json"
        return json.loads(capsule_path.read_text(encoding="utf-8"))

    def write_capsules(self, repo_root: Path, payload: dict) -> None:
        capsule_path = repo_root / "generated" / "skill_capsules.json"
        capsule_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

    def load_sections(self, repo_root: Path) -> dict:
        sections_path = repo_root / "generated" / "skill_sections.full.json"
        return json.loads(sections_path.read_text(encoding="utf-8"))

    def write_sections(self, repo_root: Path, payload: dict) -> None:
        sections_path = repo_root / "generated" / "skill_sections.full.json"
        sections_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

    def load_public_surface(self, repo_root: Path) -> dict:
        public_surface_path = repo_root / "generated" / "public_surface.json"
        return json.loads(public_surface_path.read_text(encoding="utf-8"))

    def write_public_surface(self, repo_root: Path, payload: dict) -> None:
        public_surface_path = repo_root / "generated" / "public_surface.json"
        public_surface_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

    def load_walkthroughs(self, repo_root: Path) -> dict:
        walkthrough_path = repo_root / "generated" / "skill_walkthroughs.json"
        return json.loads(walkthrough_path.read_text(encoding="utf-8"))

    def write_walkthroughs(self, repo_root: Path, payload: dict) -> None:
        walkthrough_path = repo_root / "generated" / "skill_walkthroughs.json"
        walkthrough_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

    def load_evaluation_matrix(self, repo_root: Path) -> dict:
        matrix_path = repo_root / "generated" / "skill_evaluation_matrix.json"
        return json.loads(matrix_path.read_text(encoding="utf-8"))

    def write_evaluation_matrix(self, repo_root: Path, payload: dict) -> None:
        matrix_path = repo_root / "generated" / "skill_evaluation_matrix.json"
        matrix_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

    def load_skill_composition_audit(self, repo_root: Path) -> dict:
        audit_path = repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_JSON_PATH
        return json.loads(audit_path.read_text(encoding="utf-8"))

    def write_skill_composition_audit(self, repo_root: Path, payload: dict) -> None:
        audit_path = repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_JSON_PATH
        audit_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
