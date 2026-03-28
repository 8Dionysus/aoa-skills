from __future__ import annotations

import contextlib
import io
import json
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_catalog


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


class BuildCatalogTests(unittest.TestCase):
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
            snapshots_dir = fixtures_dir / "skill_evaluation_snapshots" / "aoa-test-skill"
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
        for spec in build_catalog.generated_surface_specs():
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
        headings = "\n\n".join(
            f"## {lane['id']}\n\nLane notes.\n" for lane in lanes
        )
        if not headings:
            headings = "## governance\n\nLane notes.\n"
        (governance_dir / "lanes.md").write_text(
            "# Governance lanes\n\n"
            "Candidate-ready is a gate-pass signal only.\n\n"
            + headings,
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
                        "snapshot_path": use_snapshot_path.relative_to(repo_root).as_posix(),
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
                        "forbidden_output_phrases": [
                            f"Decision: use `{skill_name}`."
                        ],
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
        overlay_dir = repo_root / "docs" / "overlays" / family
        overlay_dir.mkdir(parents=True, exist_ok=True)
        listed_skill_names = skill_names if listed_skill_names is None else listed_skill_names
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
            f"- family review doc: `docs/overlays/{family}/REVIEW.md`",
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
            f"- `docs/overlays/{family}/PROJECT_OVERLAY.md`",
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

    def test_write_catalogs_generates_full_and_min_projection(self) -> None:
        repo_root = self.make_repo()

        full_path, min_path = build_catalog.write_catalogs(repo_root)

        full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
        min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
        self.assertEqual(1, full_catalog["catalog_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/*/SKILL.md",
                "technique_manifest": "skills/*/techniques.yaml",
            },
            full_catalog["source_of_truth"],
        )
        self.assertEqual(
            build_catalog.project_min_catalog(full_catalog),
            min_catalog,
        )
        self.assertEqual(
            "skills/aoa-test-skill/SKILL.md",
            min_catalog["skills"][0]["skill_path"],
        )
        self.assertEqual(
            "aoa-techniques",
            full_catalog["skills"][0]["technique_refs"][0]["repo"],
        )

    def test_write_capsules_generates_runtime_cards(self) -> None:
        repo_root = self.make_repo()

        capsule_path = build_catalog.write_capsules(repo_root)

        capsules = json.loads(capsule_path.read_text(encoding="utf-8"))
        self.assertEqual(1, capsules["capsule_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/*/SKILL.md",
                "frontmatter_fields": [
                    "name",
                    "scope",
                    "status",
                    "summary",
                    "invocation_mode",
                    "technique_dependencies",
                ],
                "sections": [
                    "Intent",
                    "Trigger boundary",
                    "Inputs",
                    "Outputs",
                    "Procedure",
                    "Risks and anti-patterns",
                    "Verification",
                ],
            },
            capsules["source_of_truth"],
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "scope": "core",
                "status": "scaffold",
                "summary": "Test skill summary.",
                "trigger_boundary_short": "Use when needed; Avoid when not needed.",
                "inputs_short": "Needs: input.",
                "outputs_short": "Produces: output.",
                "workflow_short": "Purpose: Intent text. Flow: step.",
                "main_anti_patterns_short": "Avoid: risk.",
                "verification_short": "Checks: verify.",
                "invocation_mode": "explicit-preferred",
                "technique_dependencies": ["AOA-T-0001"],
                "skill_path": "skills/aoa-test-skill/SKILL.md",
            },
            capsules["skills"][0],
        )

    def test_write_sections_generates_source_owned_section_surface(self) -> None:
        repo_root = self.make_repo()

        sections_path = build_catalog.write_sections(repo_root)

        sections_payload = json.loads(sections_path.read_text(encoding="utf-8"))
        assert_entry = sections_payload["skills"][0]
        self.assertEqual(1, sections_payload["section_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/*/SKILL.md",
                "sections": [
                    "Intent",
                    "Trigger boundary",
                    "Inputs",
                    "Outputs",
                    "Procedure",
                    "Contracts",
                    "Risks and anti-patterns",
                    "Verification",
                    "Technique traceability",
                    "Adaptation points",
                ],
            },
            sections_payload["source_of_truth"],
        )
        self.assertEqual("aoa-test-skill", assert_entry["name"])
        self.assertEqual("skills/aoa-test-skill/SKILL.md", assert_entry["skill_path"])
        self.assertEqual(
            [
                "intent",
                "trigger_boundary",
                "inputs",
                "outputs",
                "procedure",
                "contracts",
                "risks_and_anti_patterns",
                "verification",
                "technique_traceability",
                "adaptation_points",
            ],
            [section["key"] for section in assert_entry["sections"]],
        )
        self.assertEqual("Intent text.", assert_entry["sections"][0]["content_markdown"])
        self.assertIn("1. step", assert_entry["sections"][4]["content_markdown"])

    def test_write_walkthroughs_generates_runtime_inspect_surface(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        walkthrough_json_path, walkthrough_markdown_path = build_catalog.write_walkthroughs(
            repo_root
        )

        payload = self.load_walkthroughs(repo_root)
        markdown = self.load_walkthroughs_markdown(repo_root)
        self.assertEqual(build_catalog.WALKTHROUGH_VERSION, payload["walkthrough_version"])
        self.assertEqual(
            build_catalog.WALKTHROUGH_SOURCE_OF_TRUTH,
            payload["source_of_truth"],
        )
        self.assertEqual(walkthrough_json_path, repo_root / build_catalog.WALKTHROUGHS_JSON_PATH)
        self.assertEqual(
            walkthrough_markdown_path,
            repo_root / build_catalog.WALKTHROUGHS_MARKDOWN_PATH,
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "scope": "core",
                "status": "evaluated",
                "invocation_mode": "explicit-preferred",
                "skill_path": "skills/aoa-test-skill/SKILL.md",
                "pick_summary": "Test skill summary.",
                "use_when": ["needed"],
                "do_not_use_when": ["not needed"],
                "inspection_order": ["capsule", "sections", "full", "evidence"],
                "expand_sections": [
                    "Procedure",
                    "Contracts",
                    "Risks and anti-patterns",
                    "Verification",
                ],
                "object_use_shape": ["output"],
                "support_artifacts": [
                    {
                        "type": "runtime_example",
                        "path": "skills/aoa-test-skill/examples/example.md",
                        "selected_for_runtime_inspection": True,
                    },
                    {
                        "type": "promotion_review",
                        "path": "docs/reviews/status-promotions/aoa-test-skill.md",
                        "selected_for_runtime_inspection": False,
                    },
                ],
            },
            payload["skills"][0],
        )
        self.assertIn("## Shared inspection path", markdown)
        self.assertIn("## aoa-test-skill", markdown)
        self.assertIn("`runtime_example` (selected)", markdown)

    def test_walkthrough_support_artifact_precedence_prefers_runtime_example_then_review(self) -> None:
        repo_root = self.make_repo()
        skill_dir = repo_root / "skills" / "aoa-test-skill"
        checks_dir = skill_dir / "checks"
        checks_dir.mkdir()
        (checks_dir / "review.md").write_text(
            textwrap.dedent(
                """\
                # Review Checklist

                ## Purpose

                Review purpose.

                ## When it applies

                - when bounded review is needed

                ## Review checklist

                - [ ] confirm scope

                ## Not a fit

                - not for unrelated rewrites
                """
            ),
            encoding="utf-8",
        )
        (skill_dir / "examples" / "runtime.md").write_text(
            textwrap.dedent(
                """\
                # Runtime Example

                ## Scenario

                Runtime scenario.

                ## Why this skill fits

                - explicit runtime example

                ## Expected inputs

                - input

                ## Expected outputs

                - output

                ## Boundary notes

                - keep scope bounded

                ## Verification notes

                - verify the outcome
                """
            ),
            encoding="utf-8",
        )

        payload = build_catalog.build_walkthrough_payload(repo_root)
        support_artifacts = payload["skills"][0]["support_artifacts"]
        selected_paths = [
            artifact["path"]
            for artifact in support_artifacts
            if artifact["selected_for_runtime_inspection"]
        ]
        self.assertEqual(
            ["skills/aoa-test-skill/examples/runtime.md"],
            selected_paths,
        )

        (skill_dir / "examples" / "runtime.md").unlink()
        payload = build_catalog.build_walkthrough_payload(repo_root)
        support_artifacts = payload["skills"][0]["support_artifacts"]
        selected_paths = [
            artifact["path"]
            for artifact in support_artifacts
            if artifact["selected_for_runtime_inspection"]
        ]
        self.assertEqual(
            ["skills/aoa-test-skill/examples/example.md"],
            selected_paths,
        )

        shutil.rmtree(skill_dir / "examples")
        payload = build_catalog.build_walkthrough_payload(repo_root)
        support_artifacts = payload["skills"][0]["support_artifacts"]
        selected_paths = [
            artifact["path"]
            for artifact in support_artifacts
            if artifact["selected_for_runtime_inspection"]
        ]
        self.assertEqual(
            ["skills/aoa-test-skill/checks/review.md"],
            selected_paths,
        )

    def test_write_public_surface_marks_canonical_skill_as_default_reference(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_surfaces=("canonical-candidates",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertTrue(skill_entry["is_default_reference"])
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual([], skill_entry["canonical_candidate_blockers"])
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["default_references"],
        )

    def test_write_public_surface_marks_published_evaluated_skill_as_candidate_ready(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertEqual("published", skill_entry["lineage_state"])
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["candidate_ready"],
        )

    def test_write_public_surface_preserves_candidate_ready_while_recording_stay_evaluated(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "test_lane",
                    "title": "Test lane",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertTrue(skill_entry["canonical_candidate_ready"])
        self.assertEqual("stay_evaluated", skill_entry["governance_decision"])
        self.assertEqual(["test_lane"], skill_entry["governance_lane_ids"])
        self.assertEqual([], skill_entry["governance_evidence_case_ids"])
        self.assertFalse(skill_entry["is_default_reference"])
        self.assertEqual(["aoa-test-skill"], payload["cohorts"]["candidate_ready"])

    def test_project_overlay_stays_out_of_candidate_ready_without_governance_lane(self) -> None:
        repo_root = self.make_repo(
            scope="project",
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)
        build_catalog.write_governance_backlog(repo_root)
        build_catalog.write_bundle_index(repo_root)

        public_payload = self.load_public_surface(repo_root)
        backlog_payload = self.load_governance_backlog(repo_root)
        bundle_payload = self.load_bundle_index(repo_root)

        public_entry = public_payload["skills"][0]
        backlog_entry = backlog_payload["skills"][0]
        bundle_entry = bundle_payload["skills"][0]

        self.assertFalse(public_entry["canonical_candidate_ready"])
        self.assertEqual([], public_entry["canonical_candidate_blockers"])
        self.assertEqual([], public_payload["cohorts"]["candidate_ready"])
        self.assertEqual([], backlog_payload["cohorts"]["candidate_ready_without_review"])
        self.assertFalse(backlog_entry["canonical_candidate_ready"])
        self.assertFalse(bundle_entry["canonical_candidate_ready"])

    def test_project_overlay_backlog_marks_eval_ready_without_governance_lane(self) -> None:
        repo_root = self.make_repo(
            scope="project",
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_governance_backlog(repo_root)

        payload = self.load_governance_backlog(repo_root)
        markdown = self.load_governance_backlog_markdown(repo_root)
        skill_entry = payload["skills"][0]

        self.assertFalse(skill_entry["canonical_candidate_ready"])
        self.assertTrue(skill_entry["canonical_eval_ready"])
        self.assertEqual(
            "project_overlay_eval_ready",
            skill_entry["readiness_reconciliation"],
        )
        self.assertIn("project_overlay_eval_ready", markdown)

    def test_project_overlay_backlog_marks_eval_blocked_as_needs_evidence(self) -> None:
        repo_root = self.make_repo(
            scope="project",
            status="evaluated",
            review_surfaces=("status-promotions",),
        )

        build_catalog.write_governance_backlog(repo_root)

        payload = self.load_governance_backlog(repo_root)
        markdown = self.load_governance_backlog_markdown(repo_root)
        skill_entry = payload["skills"][0]

        self.assertFalse(skill_entry["canonical_candidate_ready"])
        self.assertFalse(skill_entry["canonical_eval_ready"])
        self.assertEqual(
            "project_overlay_needs_evidence",
            skill_entry["readiness_reconciliation"],
        )
        self.assertIn("project_overlay_needs_evidence", markdown)

    def test_bundle_index_includes_relationship_fields(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_bundle_index(repo_root)

        payload = self.load_bundle_index(repo_root)
        entry = payload["skills"][0]
        self.assertEqual(["repo-default"], entry["install_profiles"])
        self.assertEqual(
            [
                "portable_export",
                "runtime_seam",
                "runtime_guardrails",
                "description_trigger",
                "tiny_router",
            ],
            entry["artifact_group_coverage"],
        )
        self.assertEqual(
            [
                {
                    "id": "AOA-T-0001",
                    "repo": "aoa-techniques",
                    "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
                    "source_ref": "0123456789abcdef0123456789abcdef01234567",
                    "lineage_state": "published",
                }
            ],
            entry["technique_lineage"],
        )

    def test_bundle_index_support_resource_coverage_stays_targeted(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        skill_name = "aoa-safe-infra-change"
        skill_dir = repo_root / "skills" / "aoa-test-skill"
        renamed_dir = repo_root / "skills" / skill_name
        skill_dir.rename(renamed_dir)
        skill_md = (renamed_dir / "SKILL.md").read_text(encoding="utf-8")
        (renamed_dir / "SKILL.md").write_text(
            skill_md.replace("aoa-test-skill", skill_name),
            encoding="utf-8",
        )
        manifest = yaml.safe_load((renamed_dir / "techniques.yaml").read_text(encoding="utf-8"))
        manifest["skill_name"] = skill_name
        (renamed_dir / "techniques.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )
        (repo_root / "SKILL_INDEX.md").write_text(
            "# SKILL_INDEX\n\n| name | scope | status | summary |\n|---|---|---|---|\n"
            f"| {skill_name} | core | evaluated | Test summary. |\n",
            encoding="utf-8",
        )
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
                            "skills": [skill_name],
                        }
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        build_catalog.write_bundle_index(repo_root)

        payload = self.load_bundle_index(repo_root)
        entry = payload["skills"][0]
        self.assertIn("support_resources", entry["artifact_group_coverage"])

    def test_skill_graph_includes_profile_and_artifact_group_edges(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_skill_graph(repo_root)

        payload = self.load_skill_graph(repo_root)
        node_types = {entry["type"] for entry in payload["nodes"]}
        edge_kinds = {entry["kind"] for entry in payload["edges"]}
        self.assertIn("profile", node_types)
        self.assertIn("artifact_group", node_types)
        self.assertIn("included_in_profile", edge_kinds)
        self.assertIn("available_in_artifact_group", edge_kinds)

    def test_write_public_surface_marks_pending_lineage_and_resolves_both_review_paths(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            techniques=[PENDING_TECHNIQUE],
            review_surfaces=("status-promotions", "canonical-candidates"),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertEqual("pending", skill_entry["lineage_state"])
        self.assertFalse(skill_entry["canonical_candidate_ready"])
        self.assertIn(
            "pending_technique_dependencies",
            skill_entry["canonical_candidate_blockers"],
        )
        self.assertIn(
            "pending_technique_entries",
            skill_entry["canonical_candidate_blockers"],
        )
        self.assertIn(
            "tbd_technique_refs",
            skill_entry["canonical_candidate_blockers"],
        )
        self.assertEqual(
            "docs/reviews/status-promotions/aoa-test-skill.md",
            skill_entry["promotion_review_path"],
        )
        self.assertEqual(
            "docs/reviews/canonical-candidates/aoa-test-skill.md",
            skill_entry["candidate_review_path"],
        )
        self.assertEqual(
            ["aoa-test-skill"],
            payload["cohorts"]["blocked_by_pending_lineage"],
        )

    def test_write_public_surface_does_not_flag_valid_explicit_only_policy(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            invocation_mode="explicit-only",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
            policy_allow_implicit=False,
            scope="risk",
        )

        build_catalog.write_public_surface(repo_root)

        payload = self.load_public_surface(repo_root)
        skill_entry = payload["skills"][0]
        self.assertNotIn(
            "explicit_only_policy_violation",
            skill_entry["canonical_candidate_blockers"],
        )
        self.assertEqual(["aoa-test-skill"], payload["cohorts"]["risk_surfaces"])

    def test_public_surface_markdown_reflects_candidate_ready_cohort(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_public_surface(repo_root)

        markdown = self.load_public_surface_markdown(repo_root)
        self.assertIn("## Candidate-ready cohort", markdown)
        self.assertIn(
            "| aoa-test-skill | evaluated | core | explicit-preferred | published | - | - | - | `docs/reviews/status-promotions/aoa-test-skill.md` | - |",
            markdown,
        )

    def test_governance_backlog_renders_comparative_pending_cohort(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "test_lane",
                    "title": "Test lane",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        build_catalog.write_governance_backlog(repo_root)

        payload = self.load_governance_backlog(repo_root)
        markdown = self.load_governance_backlog_markdown(repo_root)
        self.assertEqual(["aoa-test-skill"], payload["cohorts"]["comparative_pending"])
        self.assertEqual(["aoa-test-skill"], payload["cohorts"]["review_truth_sync"])
        self.assertFalse(payload["review_truth_sync"][0]["truth_synced"])
        self.assertEqual("stay_evaluated", payload["skills"][0]["governance_decision"])
        self.assertEqual(["test_lane"], payload["skills"][0]["governance_lane_ids"])
        self.assertIn("comparative pending cohort: 1", markdown)
        self.assertIn("## Review truth sync", markdown)
        self.assertIn("`comparative_pending`: aoa-test-skill", markdown)

    def test_write_overlay_readiness_generates_reviewable_family_surface(self) -> None:
        repo_root = self.make_repo()
        skill_names = [
            "cinder-change-protocol",
            "cinder-source-of-truth-check",
        ]
        family = "cinder"
        for skill_name in skill_names:
            self.add_skill_bundle(
                repo_root,
                skill_name=skill_name,
                scope="project",
                techniques=[PRIMARY_PUBLISHED_TECHNIQUE],
                policy_allow_implicit=True,
                include_review_check=True,
            )
        self.write_evaluation_fixtures_for_skills(repo_root, skill_names)
        self.write_live_overlay_pack(
            repo_root,
            family=family,
            skill_names=skill_names,
        )

        overlay_json_path, overlay_markdown_path = build_catalog.write_overlay_readiness(
            repo_root
        )

        payload = self.load_overlay_readiness(repo_root)
        markdown = self.load_overlay_readiness_markdown(repo_root)
        self.assertEqual(
            build_catalog.OVERLAY_READINESS_VERSION,
            payload["overlay_readiness_version"],
        )
        self.assertEqual(
            build_catalog.skill_overlay_contract.OVERLAY_READINESS_SOURCE_OF_TRUTH,
            payload["source_of_truth"],
        )
        self.assertEqual(
            repo_root / build_catalog.OVERLAY_READINESS_JSON_PATH,
            overlay_json_path,
        )
        self.assertEqual(
            repo_root / build_catalog.OVERLAY_READINESS_MARKDOWN_PATH,
            overlay_markdown_path,
        )
        self.assertEqual(
            {
                "live_overlay_family_count": 1,
                "reviewable_family_count": 1,
                "project_skill_count": 2,
                "project_skill_review_check_count": 2,
                "eval_ready_project_skill_count": 2,
            },
            payload["summary"],
        )
        self.assertEqual(1, len(payload["families"]))
        self.assertEqual(
            {
                "family": family,
                "project_overlay_path": f"docs/overlays/{family}/PROJECT_OVERLAY.md",
                "review_path": f"docs/overlays/{family}/REVIEW.md",
                "project_skill_names": skill_names,
                "listed_skill_names": skill_names,
                "listed_matches_actual": True,
                "project_skill_count": 2,
                "bundle_review_check_count": 2,
                "eval_ready_skill_count": 2,
                "boundary_statement_present": True,
                "repo_relative_statement_present": True,
                "authority_section_present": True,
                "review_mentions_all_skills": True,
                "readiness_state": "reviewable",
            },
            payload["families"][0],
        )
        self.assertEqual(
            skill_names,
            [entry["name"] for entry in payload["skills"]],
        )
        self.assertTrue(all(entry["eval_ready"] for entry in payload["skills"]))
        self.assertIn("# Overlay readiness", markdown)
        self.assertIn(
            "`reviewable` is the current mature exemplar target for a live project-overlay family in this repo.",
            markdown,
        )
        self.assertIn(
            "Use this surface for family maturity and `generated/governance_backlog.md` for per-skill maintenance readout.",
            markdown,
        )
        self.assertIn(
            f"| {family} | 2 | true | docs/overlays/{family}/REVIEW.md | 2 | 2 | true | true | reviewable |",
            markdown,
        )
        self.assertIn(
            "skills/cinder-change-protocol/checks/review.md",
            markdown,
        )

    def test_write_overlay_readiness_requires_authority_section_for_reviewable_family(self) -> None:
        repo_root = self.make_repo()
        skill_names = [
            "cinder-change-protocol",
            "cinder-source-of-truth-check",
        ]
        family = "cinder"
        for skill_name in skill_names:
            self.add_skill_bundle(
                repo_root,
                skill_name=skill_name,
                scope="project",
                techniques=[PRIMARY_PUBLISHED_TECHNIQUE],
                policy_allow_implicit=True,
                include_review_check=True,
            )
        self.write_evaluation_fixtures_for_skills(repo_root, skill_names)
        self.write_live_overlay_pack(
            repo_root,
            family=family,
            skill_names=skill_names,
            include_authority_section=False,
        )

        build_catalog.write_overlay_readiness(repo_root)

        payload = self.load_overlay_readiness(repo_root)
        self.assertEqual(0, payload["summary"]["reviewable_family_count"])
        self.assertFalse(payload["families"][0]["authority_section_present"])
        self.assertEqual("baseline", payload["families"][0]["readiness_state"])

    def test_write_overlay_readiness_discovers_synthetic_live_families_from_repo_state(self) -> None:
        repo_root = self.make_repo()
        families = {
            "cinder": [
                "cinder-change-protocol",
                "cinder-source-of-truth-check",
            ],
            "harbor": [
                "harbor-safe-infra-change",
                "harbor-sanitized-share",
            ],
        }
        all_skill_names = [
            skill_name
            for skill_names in families.values()
            for skill_name in skill_names
        ]
        for skill_name in all_skill_names:
            self.add_skill_bundle(
                repo_root,
                skill_name=skill_name,
                scope="project",
                techniques=[PRIMARY_PUBLISHED_TECHNIQUE],
                policy_allow_implicit=False,
                include_review_check=True,
            )
        self.write_evaluation_fixtures_for_skills(repo_root, all_skill_names)
        for family, skill_names in families.items():
            self.write_live_overlay_pack(
                repo_root,
                family=family,
                skill_names=skill_names,
            )

        build_catalog.write_overlay_readiness(repo_root)

        payload = self.load_overlay_readiness(repo_root)
        markdown = self.load_overlay_readiness_markdown(repo_root)
        self.assertEqual(
            {
                "live_overlay_family_count": 2,
                "reviewable_family_count": 2,
                "project_skill_count": 4,
                "project_skill_review_check_count": 4,
                "eval_ready_project_skill_count": 4,
            },
            payload["summary"],
        )
        readiness_by_family = {
            entry["family"]: entry["readiness_state"] for entry in payload["families"]
        }
        self.assertEqual(
            {
                "cinder": "reviewable",
                "harbor": "reviewable",
            },
            readiness_by_family,
        )
        self.assertCountEqual(
            all_skill_names,
            [entry["name"] for entry in payload["skills"]],
        )
        self.assertTrue(all(entry["eval_ready"] for entry in payload["skills"]))
        self.assertIn(
            "| cinder | 2 | true | docs/overlays/cinder/REVIEW.md | 2 | 2 | true | true | reviewable |",
            markdown,
        )
        self.assertIn(
            "| harbor | 2 | true | docs/overlays/harbor/REVIEW.md | 2 | 2 | true | true | reviewable |",
            markdown,
        )

    def test_write_skill_composition_audit_marks_multi_technique_skill(self) -> None:
        repo_root = self.make_repo(
            techniques=[PRIMARY_PUBLISHED_TECHNIQUE, SECONDARY_PUBLISHED_TECHNIQUE],
        )

        audit_json_path, audit_markdown_path = build_catalog.write_skill_composition_audit(
            repo_root
        )

        payload = self.load_skill_composition_audit(repo_root)
        markdown = self.load_skill_composition_audit_markdown(repo_root)
        self.assertEqual(
            build_catalog.SKILL_COMPOSITION_AUDIT_VERSION,
            payload["skill_composition_version"],
        )
        self.assertEqual(
            build_catalog.skill_composition_audit.SKILL_COMPOSITION_SOURCE_OF_TRUTH,
            payload["source_of_truth"],
        )
        self.assertEqual(
            repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_JSON_PATH,
            audit_json_path,
        )
        self.assertEqual(
            repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_MARKDOWN_PATH,
            audit_markdown_path,
        )
        self.assertEqual(
            {
                "total_skill_count": 1,
                "multi_technique_skill_count": 1,
                "single_technique_skill_count": 0,
                "approved_exception_count": 0,
                "needs_reframe_count": 0,
            },
            payload["summary"],
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "technique_count": 2,
                "technique_ids": ["AOA-T-0001", "AOA-T-0002"],
                "composition_class": "multi_technique",
                "exception_review_path": None,
                "recommended_action": "keep_multi_technique",
            },
            payload["skills"][0],
        )
        self.assertIn("# Skill composition audit", markdown)
        self.assertIn("| aoa-test-skill | 2 | multi_technique | keep_multi_technique | - |", markdown)

    def test_write_skill_composition_audit_marks_reviewed_exception(self) -> None:
        repo_root = self.make_repo()
        self.write_skill_composition_exception_review(repo_root)

        build_catalog.write_skill_composition_audit(repo_root)

        payload = self.load_skill_composition_audit(repo_root)
        self.assertEqual(
            {
                "total_skill_count": 1,
                "multi_technique_skill_count": 0,
                "single_technique_skill_count": 1,
                "approved_exception_count": 1,
                "needs_reframe_count": 0,
            },
            payload["summary"],
        )
        self.assertEqual(
            "single_technique_exception",
            payload["skills"][0]["composition_class"],
        )
        self.assertEqual(
            "docs/reviews/skill-composition-exceptions/aoa-test-skill.md",
            payload["skills"][0]["exception_review_path"],
        )
        self.assertEqual(
            "keep_exception",
            payload["skills"][0]["recommended_action"],
        )

    def test_write_evaluation_matrix_generates_snapshot_backed_surface(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_surfaces=("canonical-candidates",),
            include_evaluation_fixtures=True,
        )

        matrix_json_path, matrix_markdown_path = build_catalog.write_evaluation_matrix(repo_root)

        payload = self.load_evaluation_matrix(repo_root)
        markdown = self.load_evaluation_matrix_markdown(repo_root)
        self.assertEqual(
            build_catalog.EVALUATION_MATRIX_VERSION,
            payload["evaluation_matrix_version"],
        )
        self.assertEqual(
            build_catalog.EVALUATION_MATRIX_SOURCE_OF_TRUTH,
            payload["source_of_truth"],
        )
        self.assertEqual(
            matrix_json_path,
            repo_root / build_catalog.EVALUATION_MATRIX_JSON_PATH,
        )
        self.assertEqual(
            matrix_markdown_path,
            repo_root / build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH,
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "status": "canonical",
                "scope": "core",
                "invocation_mode": "explicit-preferred",
                "skill_path": "skills/aoa-test-skill/SKILL.md",
                "autonomy_check_count": 1,
                "use_case_count": 1,
                "do_not_use_case_count": 1,
                "use_snapshot_count": 1,
                "do_not_use_snapshot_count": 1,
                "selected_runtime_artifact_path": "skills/aoa-test-skill/examples/example.md",
                "promotion_review_path": None,
                "candidate_review_path": "docs/reviews/canonical-candidates/aoa-test-skill.md",
                "canonical_eval_ready": True,
                "canonical_eval_blockers": [],
            },
            payload["skills"][0],
        )
        self.assertIn("# Skill evaluation matrix", markdown)
        self.assertIn("| aoa-test-skill | canonical | core | explicit-preferred |", markdown)

    def test_check_mode_passes_after_write(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)

        self.assertEqual(0, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_catalog_is_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "Test skill summary.",
                "Changed summary.",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_capsules_are_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "- verify",
                "- verify harder",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_sections_are_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Adaptation points\n\n- adapt\n",
                "## Adaptation points\n\n- adapt\n- adapt more\n",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_public_surface_is_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)

        public_surface_markdown_path = repo_root / build_catalog.PUBLIC_SURFACE_MARKDOWN_PATH
        public_surface_markdown_path.write_text(
            public_surface_markdown_path.read_text(encoding="utf-8").replace(
                "candidate-ready skills: 1",
                "candidate-ready skills: 0",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_walkthroughs_are_stale(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "- output",
                "- output\n- output detail",
            ),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_walkthroughs_are_missing(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)

        (repo_root / build_catalog.WALKTHROUGHS_JSON_PATH).unlink()
        (repo_root / build_catalog.WALKTHROUGHS_MARKDOWN_PATH).unlink()

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_evaluation_matrix_is_stale(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_surfaces=("canonical-candidates",),
            include_evaluation_fixtures=True,
        )
        self.write_all_surfaces(repo_root)

        matrix_markdown_path = repo_root / build_catalog.EVALUATION_MATRIX_MARKDOWN_PATH
        matrix_markdown_path.write_text("stale matrix markdown\n", encoding="utf-8")

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_check_mode_fails_when_skill_composition_audit_is_stale(self) -> None:
        repo_root = self.make_repo()
        self.write_skill_composition_exception_review(repo_root)
        self.write_all_surfaces(repo_root)

        audit_markdown_path = repo_root / build_catalog.SKILL_COMPOSITION_AUDIT_MARKDOWN_PATH
        audit_markdown_path.write_text("stale composition audit\n", encoding="utf-8")

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_write_catalogs_rejects_invalid_routing_contract(self) -> None:
        repo_root = self.make_repo()
        manifest_path = repo_root / "skills" / "aoa-test-skill" / "techniques.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["techniques"][0]["repo"] = "aoa-evals"
        manifest["techniques"][0]["path"] = "../bad/path.md"
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "repo must resolve to 'aoa-techniques'",
        ):
            build_catalog.write_catalogs(repo_root)

    def test_check_mode_reports_invalid_routing_contract(self) -> None:
        repo_root = self.make_repo()
        manifest_path = repo_root / "skills" / "aoa-test-skill" / "techniques.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["techniques"][0]["repo"] = "aoa-evals"
        manifest["techniques"][0]["path"] = "../bad/path.md"
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )

        self.assertEqual(1, self.run_main(repo_root, ["--check"]))

    def test_write_capsules_rejects_missing_required_source_section(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "capsule source section 'Verification' is missing",
        ):
            build_catalog.write_capsules(repo_root)

    def test_write_capsules_ignores_indented_fake_heading(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "## Procedure\n\n1. step\n\n    ## Verification\n\n    - example only\n\n",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "capsule source section 'Verification' is missing",
        ):
            build_catalog.write_capsules(repo_root)

    def test_write_sections_rejects_reordered_top_level_sections(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Outputs\n\n- output\n\n## Procedure\n\n1. step\n",
                "## Procedure\n\n1. step\n\n## Outputs\n\n- output\n",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "top-level sections must match the canonical order exactly",
        ):
            build_catalog.write_sections(repo_root)


if __name__ == "__main__":
    unittest.main()
