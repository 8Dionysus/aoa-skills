from __future__ import annotations

import contextlib
import hashlib
import io
import json
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

from builders import build_catalog
from skill_model import skill_evaluation_contract


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


class BuildCatalogCase(unittest.TestCase):
    def make_repo(
        self,
        *,
        status: str = "scaffold",
        invocation_mode: str = "explicit-preferred",
        traceability_heading: str = "Technique traceability",
        techniques: list[dict] | None = None,
        review_surfaces: tuple[str, ...] = (),
        include_evaluation_fixtures: bool = False,
        policy_allow_implicit: bool | None = None,
        scope: str = "core",
    ) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-catalog-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        config_dir = repo_root / "config"
        config_dir.mkdir()
        skill_dir = repo_root / "skills" / "aoa-test-skill"
        skill_dir.mkdir()
        (skill_dir / "examples").mkdir()
        (skill_dir / "examples" / "example.md").write_text(
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

        techniques = techniques or [PRIMARY_PUBLISHED_TECHNIQUE]
        technique_ids = [entry["id"] for entry in techniques]

        (repo_root / "SKILL_INDEX.md").write_text(
            "# SKILL_INDEX\n\n| name | scope | status | summary |\n|---|---|---|---|\n"
            f"| aoa-test-skill | {scope} | {status} | Test summary. |\n",
            encoding="utf-8",
        )
        (config_dir / "skill_pack_profiles.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "profile": "codex-facing-wave-3",
                    "profiles": {
                        "repo-default": {
                            "description": "Test install profile.",
                            "scope": "repo",
                            "install_mode": "symlink-preferred",
                            "skills": ["aoa-test-skill"],
                        }
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (skill_dir / "SKILL.md").write_text(
            textwrap.dedent(
                f"""\
                ---
                name: aoa-test-skill
                scope: {scope}
                status: {status}
                summary: Test skill summary.
                invocation_mode: {invocation_mode}
                technique_dependencies:
                """
            )
            + "".join(f"  - {technique_id}\n" for technique_id in technique_ids)
            + textwrap.dedent(
                f"""\

                ---

                # aoa-test-skill

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
            ),
            encoding="utf-8",
        )
        (skill_dir / "techniques.yaml").write_text(
            yaml.safe_dump(
                {
                    "skill_name": "aoa-test-skill",
                    "composition_mode": "bounded",
                    "techniques": techniques,
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

        if policy_allow_implicit is not None:
            agents_dir = skill_dir / "agents"
            agents_dir.mkdir()
            (agents_dir / "openai.yaml").write_text(
                yaml.safe_dump(
                    {
                        "policy": {
                            "allow_implicit_invocation": policy_allow_implicit,
                        },
                        "notes": ["Test policy."],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

        for surface in review_surfaces:
            if surface == "status-promotions":
                review_dir = repo_root / "docs" / "reviews" / "status-promotions"
                title = "# aoa-test-skill status promotion review\n"
            elif surface == "canonical-candidates":
                review_dir = repo_root / "docs" / "reviews" / "canonical-candidates"
                title = "# aoa-test-skill canonical candidate review\n"
            else:
                raise ValueError(f"unknown review surface '{surface}'")
            review_dir.mkdir(parents=True, exist_ok=True)
            (review_dir / "aoa-test-skill.md").write_text(
                title + "\n## Findings\n\n- Evidence exists.\n",
                encoding="utf-8",
            )

        if include_evaluation_fixtures:
            fixtures_dir = repo_root / "tests" / "fixtures"
            fixtures_dir.mkdir(parents=True, exist_ok=True)
            snapshots_dir = (
                fixtures_dir / "skill_evaluation_snapshots" / "aoa-test-skill"
            )
            snapshots_dir.mkdir(parents=True, exist_ok=True)
            use_snapshot_path = snapshots_dir / "aoa_test_skill_use_snapshot_1.md"
            use_snapshot_path.write_text(
                textwrap.dedent(
                    """\
                    # Evaluation Snapshot

                    ## Prompt

                    use case

                    ## Expected selection

                    Decision: use `aoa-test-skill`.

                    ## Why

                    - the bounded trigger is needed

                    ## Expected object

                    - output

                    ## Boundary notes

                    - keep the scope bounded

                    ## Verification hooks

                    - verify the output
                    """
                ),
                encoding="utf-8",
            )
            do_not_use_snapshot_path = (
                snapshots_dir / "aoa_test_skill_do_not_use_snapshot_1.md"
            )
            do_not_use_snapshot_path.write_text(
                textwrap.dedent(
                    """\
                    # Evaluation Snapshot

                    ## Prompt

                    do not use case

                    ## Expected selection

                    Decision: do_not_use `aoa-test-skill`.

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
            (fixtures_dir / "skill_evaluation_cases.yaml").write_text(
                yaml.safe_dump(
                    {
                        "autonomy_checks": [
                            {
                                "skill": "aoa-test-skill",
                                "forbidden_runtime_terms": ["aoa-techniques"],
                            }
                        ],
                        "trigger_cases": [
                            {
                                "skill": "aoa-test-skill",
                                "case_id": "aoa_test_skill_use_1",
                                "prompt": "use case",
                                "expected": "use",
                                "required_phrases": ["needed"],
                            },
                            {
                                "skill": "aoa-test-skill",
                                "case_id": "aoa_test_skill_do_not_use_1",
                                "prompt": "do not use case",
                                "expected": "do_not_use",
                                "required_phrases": ["not needed"],
                            },
                        ],
                        "snapshot_cases": [
                            {
                                "skill": "aoa-test-skill",
                                "case_id": "aoa_test_skill_use_snapshot_1",
                                "prompt": "use case",
                                "expected": "use",
                                "snapshot_path": "tests/fixtures/skill_evaluation_snapshots/aoa-test-skill/aoa_test_skill_use_snapshot_1.md",
                                "required_output_phrases": [
                                    "Decision: use `aoa-test-skill`.",
                                    "output",
                                ],
                                "forbidden_output_phrases": [
                                    "Decision: do_not_use `aoa-test-skill`."
                                ],
                            },
                            {
                                "skill": "aoa-test-skill",
                                "case_id": "aoa_test_skill_do_not_use_snapshot_1",
                                "prompt": "do not use case",
                                "expected": "do_not_use",
                                "snapshot_path": "tests/fixtures/skill_evaluation_snapshots/aoa-test-skill/aoa_test_skill_do_not_use_snapshot_1.md",
                                "required_output_phrases": [
                                    "Decision: do_not_use `aoa-test-skill`.",
                                    "redirect",
                                ],
                                "forbidden_output_phrases": [
                                    "Decision: use `aoa-test-skill`."
                                ],
                            },
                        ],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

        return repo_root

    def run_main(self, repo_root: Path, argv: list[str] | None = None) -> int:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            return build_catalog.main(argv or [], repo_root=repo_root)

    def add_skill_bundle(
        self,
        repo_root: Path,
        *,
        skill_name: str,
        scope: str = "core",
        status: str = "scaffold",
        invocation_mode: str = "explicit-preferred",
        techniques: list[dict] | None = None,
        policy_allow_implicit: bool | None = None,
        include_review_check: bool = False,
    ) -> None:
        skill_dir = repo_root / "skills" / skill_name
        skill_dir.mkdir()
        (skill_dir / "examples").mkdir()
        (skill_dir / "examples" / "example.md").write_text(
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

        resolved_techniques = techniques or [PRIMARY_PUBLISHED_TECHNIQUE]
        technique_ids = [entry["id"] for entry in resolved_techniques]
        (skill_dir / "SKILL.md").write_text(
            textwrap.dedent(
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
            + "".join(f"  - {technique_id}\n" for technique_id in technique_ids)
            + textwrap.dedent(
                """\

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

                ## Technique traceability

                Traceability text.

                ## Adaptation points

                - adapt
                """.format(skill_name=skill_name)
            ),
            encoding="utf-8",
        )
        (skill_dir / "techniques.yaml").write_text(
            yaml.safe_dump(
                {
                    "skill_name": skill_name,
                    "composition_mode": "bounded",
                    "techniques": resolved_techniques,
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

        if policy_allow_implicit is not None:
            agents_dir = skill_dir / "agents"
            agents_dir.mkdir()
            (agents_dir / "openai.yaml").write_text(
                yaml.safe_dump(
                    {
                        "policy": {
                            "allow_implicit_invocation": policy_allow_implicit,
                        },
                        "notes": ["Test policy."],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

        if include_review_check:
            checks_dir = skill_dir / "checks"
            checks_dir.mkdir()
            (checks_dir / "review.md").write_text(
                textwrap.dedent(
                    f"""\
                    # Review Checklist

                    ## Purpose

                    Review checklist for `{skill_name}`.

                    ## When it applies

                    - when a repo-relative project overlay needs review evidence

                    ## Review checklist

                    - [ ] confirm the local overlay wording stays bounded
                    - [ ] confirm repo-relative files and commands stay explicit

                    ## Not a fit

                    - not for broad playbooks or scenario bundles
                    """
                ),
                encoding="utf-8",
            )

    def load_public_surface(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.PUBLIC_SURFACE_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_public_surface_markdown(self, repo_root: Path) -> str:
        path = repo_root / build_catalog.PUBLIC_SURFACE_MARKDOWN_PATH
        return path.read_text(encoding="utf-8")

    def load_walkthroughs(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.WALKTHROUGHS_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_walkthroughs_markdown(self, repo_root: Path) -> str:
        path = repo_root / build_catalog.WALKTHROUGHS_MARKDOWN_PATH
        return path.read_text(encoding="utf-8")

    def write_all_surfaces(self, repo_root: Path) -> None:
        for spec in build_catalog.generated_surface_specs(repo_root):
            build_catalog.write_generated_surface(repo_root, spec)

    def load_evaluation_matrix(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.EVALUATION_MATRIX_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_evaluation_matrix_markdown(self, repo_root: Path) -> str:
        path = repo_root / build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH
        return path.read_text(encoding="utf-8")

    def load_governance_backlog(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.GOVERNANCE_BACKLOG_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_governance_backlog_markdown(self, repo_root: Path) -> str:
        path = repo_root / build_catalog.GOVERNANCE_BACKLOG_MARKDOWN_PATH
        return path.read_text(encoding="utf-8")

    def load_overlay_readiness(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.OVERLAY_READINESS_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_overlay_readiness_markdown(self, repo_root: Path) -> str:
        path = repo_root / build_catalog.OVERLAY_READINESS_MARKDOWN_PATH
        return path.read_text(encoding="utf-8")

    def load_bundle_index(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.BUNDLE_INDEX_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_skill_graph(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.SKILL_GRAPH_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_skill_composition_audit(self, repo_root: Path) -> dict:
        path = repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_JSON_PATH
        return json.loads(path.read_text(encoding="utf-8"))

    def load_skill_composition_audit_markdown(self, repo_root: Path) -> str:
        path = repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_MARKDOWN_PATH
        return path.read_text(encoding="utf-8")

    def write_skill_composition_exception_review(
        self,
        repo_root: Path,
        *,
        skill_name: str = "aoa-test-skill",
        recommendation: str = "keep_exception",
    ) -> None:
        review_dir = repo_root / "docs" / "reviews" / "skill-composition-exceptions"
        review_dir.mkdir(parents=True, exist_ok=True)
        (review_dir / f"{skill_name}.md").write_text(
            textwrap.dedent(
                f"""\
                # {skill_name}

                ## Current shape

                - skill: `{skill_name}`
                - technique_count: `1`
                - technique_ids:
                  - `AOA-T-0001`
                - composition_class: `single_technique_exception`

                ## Package rationale

                This stays in the skill layer because it packages a bounded workflow.

                ## Why this is not just the technique

                The skill adds invocation and reporting boundaries around the technique.

                ## Adjacent skills considered

                - `aoa-other-skill`

                ## Recommendation

                - `{recommendation}`
                """
            ),
            encoding="utf-8",
        )

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

    def write_evaluation_fixtures_for_skills(
        self,
        repo_root: Path,
        skill_names: list[str],
    ) -> None:
        fixtures_dir = repo_root / "tests" / "fixtures"
        fixtures_dir.mkdir(parents=True, exist_ok=True)
        payload: dict[str, list[dict]] = {
            "autonomy_checks": [],
            "trigger_cases": [],
            "snapshot_cases": [],
            "adjacency_cases": [],
        }

        for skill_name in skill_names:
            snapshots_dir = fixtures_dir / "skill_evaluation_snapshots" / skill_name
            snapshots_dir.mkdir(parents=True, exist_ok=True)
            slug = skill_name.replace("-", "_")
            payload["autonomy_checks"].append(
                {
                    "skill": skill_name,
                    "forbidden_runtime_terms": ["aoa-techniques"],
                }
            )
            payload["trigger_cases"].extend(
                [
                    {
                        "skill": skill_name,
                        "case_id": f"{slug}_use_1",
                        "prompt": "use case",
                        "expected": "use",
                        "required_phrases": ["needed"],
                    },
                    {
                        "skill": skill_name,
                        "case_id": f"{slug}_do_not_use_1",
                        "prompt": "do not use case",
                        "expected": "do_not_use",
                        "required_phrases": ["not needed"],
                    },
                ]
            )

            use_snapshot_path = snapshots_dir / f"{slug}_use_1.md"
            use_snapshot_path.write_text(
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

                    - keep the scope bounded

                    ## Verification hooks

                    - verify the output
                    """
                ),
                encoding="utf-8",
            )
            do_not_use_snapshot_path = snapshots_dir / f"{slug}_do_not_use_1.md"
            do_not_use_snapshot_path.write_text(
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
            payload["snapshot_cases"].extend(
                [
                    {
                        "skill": skill_name,
                        "case_id": f"{slug}_use_1",
                        "prompt": "use case",
                        "expected": "use",
                        "snapshot_path": use_snapshot_path.relative_to(
                            repo_root
                        ).as_posix(),
                        "required_output_phrases": [
                            f"Decision: use `{skill_name}`.",
                            "output",
                        ],
                        "forbidden_output_phrases": [
                            f"Decision: do_not_use `{skill_name}`."
                        ],
                    },
                    {
                        "skill": skill_name,
                        "case_id": f"{slug}_do_not_use_1",
                        "prompt": "do not use case",
                        "expected": "do_not_use",
                        "snapshot_path": (
                            do_not_use_snapshot_path.relative_to(repo_root).as_posix()
                        ),
                        "required_output_phrases": [
                            f"Decision: do_not_use `{skill_name}`.",
                            "redirect",
                        ],
                        "forbidden_output_phrases": [f"Decision: use `{skill_name}`."],
                    },
                ]
            )

        (fixtures_dir / "skill_evaluation_cases.yaml").write_text(
            yaml.safe_dump(payload, sort_keys=False),
            encoding="utf-8",
        )

    def write_live_overlay_pack(
        self,
        repo_root: Path,
        *,
        family: str,
        skill_names: list[str],
        listed_skill_names: list[str] | None = None,
        include_authority_section: bool = True,
    ) -> None:
        overlay_dir = repo_root / "mechanics" / "boundary-bridge" / "overlays" / family
        overlay_dir.mkdir(parents=True, exist_ok=True)
        listed_skill_names = (
            skill_names if listed_skill_names is None else listed_skill_names
        )
        checklist_refs = ", ".join(
            f"`skills/{skill_name}/checks/review.md`" for skill_name in skill_names
        )
        overlay_lines = [
            f"# {family} overlay",
            "",
            "## Purpose",
            "",
            "This live exemplar overlay pack keeps repo-relative local adaptation explicit.",
            "It does not change the base skill boundary.",
            "",
            "## Local surface",
            "",
            "- repo-relative docs and commands remain explicit",
            f"- family review doc: `mechanics/boundary-bridge/overlays/{family}/REVIEW.md`",
            f"- bundle-local review checklists: {checklist_refs}",
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
            f"- confirm both `skills/{family}-*` bundles stay aligned",
            "",
        ]
        if include_authority_section:
            overlay_lines[7:7] = [
                "## Authority",
                "",
                f"- overlay family: `{family}`",
                "- local maintainers own repo-relative authority",
                "",
            ]
        (overlay_dir / "PROJECT_OVERLAY.md").write_text(
            "\n".join(overlay_lines),
            encoding="utf-8",
        )
        review_lines = [
            f"# {family} overlay family review",
            "",
            "## Current status",
            "",
            f"- overlay family: `{family}`",
            f"- reviewed skills: {', '.join(f'`{skill_name}`' for skill_name in skill_names)}",
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
                for skill_name in skill_names
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
