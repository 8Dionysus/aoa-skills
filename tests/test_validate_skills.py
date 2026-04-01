from __future__ import annotations

import contextlib
import io
import json
import re
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

import validate_skills
import build_catalog
import skill_lineage_surface
import skill_review_surface


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


class ValidateSkillsTests(unittest.TestCase):
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
            snapshot_path = (
                snapshots_dir / f"{case_id}.md"
            )
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
        config_path = repo_root / "config" / "skill_pack_profiles.json"
        if not config_path.exists():
            (repo_root / "config").mkdir(exist_ok=True)
            skill_names = sorted(path.name for path in (repo_root / "skills").iterdir() if path.is_dir())
            self.write_skill_pack_profiles(repo_root, skill_names)
        for spec in build_catalog.generated_surface_specs():
            build_catalog.write_generated_surface(repo_root, spec)

    def write_skill_pack_profiles(self, repo_root: Path, skill_names: list[str]) -> None:
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

        technique_lines = "\n".join(f"  - `{technique_id}`" for technique_id in technique_ids)
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
        overlay_dir = repo_root / "docs" / "overlays" / family
        overlay_dir.mkdir(parents=True, exist_ok=True)
        listed_skill_names = skill_names if listed_skill_names is None else listed_skill_names
        review_check_skill_names = (
            skill_names if review_check_skill_names is None else review_check_skill_names
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
            f"- family review doc: `docs/overlays/{family}/REVIEW.md`",
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
                f"- `docs/overlays/{family}/PROJECT_OVERLAY.md`",
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
                include_review_doc=bool(
                    overlay_spec.get("include_review_doc", True)
                ),
                review_check_skill_names=overlay_spec.get("review_check_skill_names"),
                review_mentions_skill_names=overlay_spec.get(
                    "review_mentions_skill_names"
                ),
            )

        self.write_catalogs(repo_root)
        return repo_root

    def load_skill_frontmatter(self, repo_root: Path, skill_name: str = "aoa-test-skill") -> dict:
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

    def load_manifest(self, repo_root: Path, skill_name: str = "aoa-test-skill") -> dict:
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

    def test_clean_fixture_passes(self) -> None:
        repo_root = self.make_repo()
        issues = validate_skills.run_validation(repo_root)
        self.assertEqual([], issues)
        self.assertEqual(0, self.run_main(repo_root))
        self.assertEqual(0, self.run_main(repo_root, ["--skill", "aoa-test-skill"]))

    def test_single_technique_skill_without_exception_review_fails(self) -> None:
        repo_root = self.make_repo(include_composition_exception_review=False)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "single-technique skill requires a valid docs/reviews/skill-composition-exceptions/aoa-test-skill.md review record",
            messages,
        )

    def test_malformed_skill_composition_exception_review_fails(self) -> None:
        repo_root = self.make_repo(include_composition_exception_review=False)
        self.write_skill_composition_exception_review(
            repo_root,
            malformed=True,
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill composition exception review missing required section 'Package rationale'",
            messages,
        )
        self.assertIn(
            "skill composition exception review top-level sections must match the canonical order exactly",
            messages,
        )

    def test_governance_lane_unknown_skill_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
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
                            "name": "aoa-ghost-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane references unknown skill 'aoa-ghost-skill'",
            messages,
        )

    def test_governance_lane_overlay_skill_fails(self) -> None:
        repo_root = self.make_repo()
        self.write_skill_index(repo_root, ["aoa-test-skill", "atm10-test-skill"])
        self.add_skill_bundle(
            repo_root,
            skill_name="atm10-test-skill",
            scope="project",
            status="scaffold",
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
                            "name": "atm10-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lanes may only reference aoa-* public skills, not 'atm10-test-skill'",
            messages,
        )

    def test_governance_lane_missing_review_path_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
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
                    "review_path": "docs/governance/missing.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane review_path 'docs/governance/missing.md#test_lane' must reference an existing file",
            messages,
        )

    def test_governance_lane_absolute_review_path_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
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
                    "review_path": "/tmp/test_lane.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane review_path '/tmp/test_lane.md#test_lane' must be repo-relative",
            messages,
        )

    def test_governance_lane_missing_adjacency_case_id_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
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
                    "evidence_case_ids": ["missing_case"],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane evidence_case_id 'missing_case' must reference an existing adjacency case",
            messages,
        )

    def test_governance_lane_conflicting_decisions_fail(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "lane_one",
                    "title": "Lane one",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#lane_one",
                    "evidence_case_ids": [],
                },
                {
                    "id": "lane_two",
                    "title": "Lane two",
                    "scope": "core",
                    "state": "stable_defaults",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "default_reference",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#lane_two",
                    "evidence_case_ids": [],
                },
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' has conflicting governance decisions ('stay_evaluated' vs 'default_reference') across lanes",
            messages,
        )

    def test_governance_lane_duplicate_ids_fail(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "shared_lane",
                    "title": "Lane one",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#shared_lane",
                    "evidence_case_ids": [],
                },
                {
                    "id": "shared_lane",
                    "title": "Lane two",
                    "scope": "core",
                    "state": "comparative_pending",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "stay_evaluated",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#shared_lane_two",
                    "evidence_case_ids": [],
                },
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "governance lane id 'shared_lane' must be unique",
            messages,
        )

    def test_governance_lane_decision_status_mismatch_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_governance_lanes(
            repo_root,
            [
                {
                    "id": "test_lane",
                    "title": "Test lane",
                    "scope": "core",
                    "state": "stable_defaults",
                    "skills": [
                        {
                            "name": "aoa-test-skill",
                            "decision": "default_reference",
                        }
                    ],
                    "review_path": "docs/governance/lanes.md#test_lane",
                    "evidence_case_ids": [],
                }
            ],
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' uses decision 'default_reference' but is not currently 'canonical'",
            messages,
        )

    def test_governance_lane_missing_coverage_for_evaluated_skill_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_governance_lanes(repo_root, [])

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' with status 'evaluated' requires governance lane coverage",
            messages,
        )

    def test_pending_technique_count_deduplicates_manifest_and_frontmatter_ids(self) -> None:
        published_count, pending_count, tbd_ref_count = skill_lineage_surface.technique_counts(
            ["AOA-T-PENDING-TEST"],
            [
                {"id": "AOA-T-PENDING-TEST", "path": "TBD", "source_ref": "TBD"},
                PRIMARY_PUBLISHED_TECHNIQUE,
            ],
        )

        self.assertEqual(1, published_count)
        self.assertEqual(1, pending_count)
        self.assertEqual(1, tbd_ref_count)

    def test_build_catalog_projects_routing_surface(self) -> None:
        repo_root = self.make_repo(
            techniques=[PRIMARY_PUBLISHED_TECHNIQUE, SECONDARY_PUBLISHED_TECHNIQUE],
        )

        full_catalog = build_catalog.build_full_catalog(repo_root)
        min_catalog = build_catalog.project_min_catalog(full_catalog)

        self.assertEqual(1, full_catalog["catalog_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/*/SKILL.md",
                "technique_manifest": "skills/*/techniques.yaml",
            },
            full_catalog["source_of_truth"],
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "scope": "core",
                "status": "scaffold",
                "summary": "Test skill summary.",
                "invocation_mode": "explicit-preferred",
                "technique_dependencies": ["AOA-T-0001", "AOA-T-0002"],
                "skill_path": "skills/aoa-test-skill/SKILL.md",
                "composition_mode": "bounded",
                "technique_refs": [
                    {
                        "id": "AOA-T-0001",
                        "repo": "aoa-techniques",
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
                    },
                    {
                        "id": "AOA-T-0002",
                        "repo": "aoa-techniques",
                        "path": "techniques/docs/source-of-truth-layout/TECHNIQUE.md",
                        "source_ref": "0123456789abcdef0123456789abcdef01234567",
                        "use_sections": ["summary"],
                    },
                ],
            },
            full_catalog["skills"][0],
        )
        self.assertEqual(
            {
                "catalog_version": 1,
                "source_of_truth": {
                    "skill_markdown": "skills/*/SKILL.md",
                    "technique_manifest": "skills/*/techniques.yaml",
                },
                "skills": [
                    {
                        "name": "aoa-test-skill",
                        "scope": "core",
                        "status": "scaffold",
                        "summary": "Test skill summary.",
                        "invocation_mode": "explicit-preferred",
                        "technique_dependencies": ["AOA-T-0001", "AOA-T-0002"],
                        "skill_path": "skills/aoa-test-skill/SKILL.md",
                    }
                ],
            },
            min_catalog,
        )

        capsules = build_catalog.build_capsules_payload(repo_root)
        self.assertEqual(1, capsules["capsule_version"])
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
                "technique_dependencies": ["AOA-T-0001", "AOA-T-0002"],
                "skill_path": "skills/aoa-test-skill/SKILL.md",
            },
            capsules["skills"][0],
        )

    def test_future_traceability_heading_is_rejected(self) -> None:
        repo_root = self.make_repo(traceability_heading="Future traceability")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("missing required section 'Technique traceability'", messages)
        self.assertIn("unexpected top-level section 'Future traceability'", messages)

    def test_linked_status_is_allowed(self) -> None:
        repo_root = self.make_repo(status="linked")
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_linked_status_with_unpinned_source_ref_fails(self) -> None:
        repo_root = self.make_repo(
            status="linked",
            techniques=[
                {
                    "id": "AOA-T-0009",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "techniques/test/TECHNIQUE.md",
                    "source_ref": "TBD",
                    "use_sections": ["Intent"],
                }
            ],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'linked' requires published techniques to use concrete source_ref values",
            messages,
        )

    def test_reviewed_status_requires_review_evidence(self) -> None:
        repo_root = self.make_repo(status="reviewed")
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'reviewed' requires review evidence via checks/review.md or a public review record",
            messages,
        )

    def test_reviewed_status_passes_with_in_bundle_review_check(self) -> None:
        repo_root = self.make_repo(status="reviewed")
        review_check = repo_root / "skills" / "aoa-test-skill" / "checks" / "review.md"
        review_check.parent.mkdir(parents=True, exist_ok=True)
        review_check.write_text(
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
        self.write_catalogs(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_reviewed_status_passes_with_status_promotion_review_record(self) -> None:
        repo_root = self.make_repo(
            status="reviewed",
            review_record_surface="status-promotions",
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_review_truth_sync_can_be_strictly_validated(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)
        review_path = repo_root / "docs" / "reviews" / "status-promotions" / "aoa-test-skill.md"
        review_path.write_text(
            textwrap.dedent(
                f"""\
                ---
                name: aoa-test-skill
                ---

                # aoa-test-skill status promotion review

                ## Current status

                - current maturity status: evaluated
                - current machine-checkable floor: pass
                - current governance lane decision: stay_evaluated
                - scope: core
                - current lineage: published
                - reviewed revision: placeholder

                ## Target status

                - target maturity status: evaluated
                - machine-checkable floor result: pass
                - recorded governance outcome: stay_evaluated

                ## Evidence reviewed

                - `skills/aoa-test-skill/SKILL.md`

                ## Findings

                - runtime skill.md meaning changed: no

                ## Gaps and blockers

                - blockers for this target status: none
                - blockers for the next status step: none

                ## Recommendation

                Stay evaluated.
                """
            ),
            encoding="utf-8",
        )

        first_pass = validate_skills.run_validation(
            repo_root,
            fail_on_review_truth_sync=True,
        )
        mismatch_issue = next(
            issue
            for issue in first_pass
            if issue.message.startswith("reviewed_revision_mismatch(expected=")
        )
        expected_revision = re.search(
            r"expected=([^,]+), recorded=",
            mismatch_issue.message,
        ).group(1)
        review_path.write_text(
            review_path.read_text(encoding="utf-8").replace(
                "- reviewed revision: placeholder",
                f"- reviewed revision: {expected_revision}",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        self.assertEqual(
            [],
            validate_skills.run_validation(
                repo_root,
                fail_on_review_truth_sync=True,
            ),
        )

    def test_project_overlay_review_truth_sync_accepts_not_applicable_governance(self) -> None:
        repo_root = self.make_repo(
            skill_name="abyss-test-skill",
            scope="project",
            status="evaluated",
            review_record_surface="status-promotions",
            policy_allow_implicit=True,
        )
        self.write_live_overlay_pack(
            repo_root,
            family="abyss",
            skill_names=["abyss-test-skill"],
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            skill_name="abyss-test-skill",
        )
        self.write_catalogs(repo_root)
        review_path = (
            repo_root / "docs" / "reviews" / "status-promotions" / "abyss-test-skill.md"
        )
        review_path.write_text(
            textwrap.dedent(
                """\
                ---
                name: abyss-test-skill
                ---

                # abyss-test-skill status promotion review

                ## Current status

                - current maturity status: evaluated
                - current machine-checkable floor: pass
                - current governance lane decision: not applicable
                - scope: project
                - current lineage: published
                - reviewed revision: placeholder

                ## Target status

                - target maturity status: evaluated
                - machine-checkable floor result: pass
                - recorded governance outcome: not applicable

                ## Evidence reviewed

                - `skills/abyss-test-skill/SKILL.md`

                ## Findings

                - runtime skill.md meaning changed: no

                ## Gaps and blockers

                - blockers for this target status: none
                - blockers for the next status step: overlay-model follow-up

                ## Recommendation

                Keep the overlay evaluated.
                """
            ),
            encoding="utf-8",
        )

        first_pass = validate_skills.run_validation(
            repo_root,
            fail_on_review_truth_sync=True,
        )
        mismatch_issue = next(
            issue
            for issue in first_pass
            if issue.message.startswith("reviewed_revision_mismatch(expected=")
        )
        expected_revision = re.search(
            r"expected=([^,]+), recorded=",
            mismatch_issue.message,
        ).group(1)
        review_path.write_text(
            review_path.read_text(encoding="utf-8").replace(
                "- reviewed revision: placeholder",
                f"- reviewed revision: {expected_revision}",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        self.assertEqual(
            [],
            validate_skills.run_validation(
                repo_root,
                fail_on_review_truth_sync=True,
            ),
        )

    def test_project_overlay_evaluated_status_does_not_require_candidate_adjacency_without_lane(self) -> None:
        repo_root = self.make_repo(
            skill_name="abyss-test-skill",
            scope="project",
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_live_overlay_pack(
            repo_root,
            family="abyss",
            skill_names=["abyss-test-skill"],
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            skill_name="abyss-test-skill",
        )
        self.write_catalogs(repo_root)

        self.assertEqual([], validate_skills.validate_required_adjacency_coverage(repo_root, ["abyss-test-skill"]))

    def test_review_truth_sync_reports_malformed_review_doc_as_issue(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)
        review_path = repo_root / "docs" / "reviews" / "status-promotions" / "aoa-test-skill.md"
        review_path.write_text(
            textwrap.dedent(
                """\
                ---
                name: aoa-test-skill
                """
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(
            repo_root,
            fail_on_review_truth_sync=True,
        )
        malformed_issue = next(
            issue
            for issue in issues
            if issue.location == "docs/reviews/status-promotions/aoa-test-skill.md"
        )
        self.assertIn("missing a closing frontmatter delimiter", malformed_issue.message)

    def test_review_truth_sync_revision_excludes_review_surface_files(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        review_path = (
            repo_root / "docs" / "reviews" / "status-promotions" / "aoa-test-skill.md"
        )
        revision_before = skill_review_surface.current_bundle_revision(
            repo_root,
            "aoa-test-skill",
        )
        review_path.write_text(
            "# aoa-test-skill status promotion review\n\n## Findings\n\n- changed.\n",
            encoding="utf-8",
        )
        revision_after = skill_review_surface.current_bundle_revision(
            repo_root,
            "aoa-test-skill",
        )
        self.assertEqual(revision_before, revision_after)

    def test_reviewed_status_passes_with_canonical_candidate_review_record(self) -> None:
        repo_root = self.make_repo(
            status="reviewed",
            review_record_surface="canonical-candidates",
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_atm10_skill_passes(self) -> None:
        repo_root = self.make_repo(skill_name="atm10-perception-tests")
        self.assertEqual([], validate_skills.run_validation(repo_root))
        self.assertEqual(0, self.run_main(repo_root, ["--skill", "atm10-perception-tests"]))

    def test_abyss_skill_passes(self) -> None:
        repo_root = self.make_repo(skill_name="abyss-port-exposure-guard")
        self.assertEqual([], validate_skills.run_validation(repo_root))
        self.assertEqual(
            0,
            self.run_main(repo_root, ["--skill", "abyss-port-exposure-guard"]),
        )

    def test_mixed_family_index_passes(self) -> None:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-validator-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        skill_names = [
            "aoa-test-skill",
            "atm10-perception-tests",
            "abyss-port-exposure-guard",
        ]
        self.write_skill_index(repo_root, skill_names)
        for skill_name in skill_names:
            self.add_skill_bundle(repo_root, skill_name=skill_name)
        self.write_catalogs(repo_root)

        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_live_overlay_pack_passes_for_allowed_family(self) -> None:
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": "atm10",
                    "skill_names": [
                        "atm10-change-protocol",
                        "atm10-source-of-truth-check",
                    ],
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": "atm10-source-of-truth-check",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PENDING_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                            "notes": [PENDING_NOTE],
                        },
                    ],
                }
            ]
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_live_overlay_contract_parity_passes_for_multiple_families(self) -> None:
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": "atm10",
                    "skill_names": [
                        "atm10-change-protocol",
                        "atm10-source-of-truth-check",
                    ],
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": "atm10-source-of-truth-check",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                    ],
                },
                {
                    "family": "abyss",
                    "skill_names": [
                        "abyss-safe-infra-change",
                        "abyss-sanitized-share",
                    ],
                    "skill_specs": [
                        {
                            "skill_name": "abyss-safe-infra-change",
                            "scope": "project",
                            "invocation_mode": "explicit-only",
                            "status": "scaffold",
                            "policy_allow_implicit": False,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": "abyss-sanitized-share",
                            "scope": "project",
                            "invocation_mode": "explicit-only",
                            "status": "scaffold",
                            "policy_allow_implicit": False,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                    ],
                },
            ]
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_live_project_overlay_requires_repo_relative_language(self) -> None:
        family = "atm10"
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": family,
                    "skill_names": ["atm10-change-protocol"],
                    "repo_relative_language": False,
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        }
                    ],
                }
            ]
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "live project overlay must explicitly keep paths or commands repository-relative",
            messages,
        )

    def test_live_project_overlay_requires_family_review_doc(self) -> None:
        family = "atm10"
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": family,
                    "skill_names": ["atm10-change-protocol"],
                    "include_review_doc": False,
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        }
                    ],
                }
            ]
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            f"live overlay family '{family}' is missing docs/overlays/{family}/REVIEW.md",
            messages,
        )

    def test_live_project_overlay_requires_bundle_review_checklist(self) -> None:
        family = "atm10"
        missing_skill = "atm10-source-of-truth-check"
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": family,
                    "skill_names": [
                        "atm10-change-protocol",
                        missing_skill,
                    ],
                    "review_check_skill_names": ["atm10-change-protocol"],
                    "skill_specs": [
                        {
                            "skill_name": "atm10-change-protocol",
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": missing_skill,
                            "scope": "project",
                            "policy_allow_implicit": True,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                    ],
                }
            ]
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            f"live overlay family '{family}' requires skills/{missing_skill}/checks/review.md",
            messages,
        )

    def test_live_project_overlay_requires_listed_skill_parity(self) -> None:
        family = "abyss"
        missing_skill = "abyss-sanitized-share"
        repo_root = self.make_live_overlay_repo(
            overlay_specs=[
                {
                    "family": family,
                    "skill_names": [
                        "abyss-safe-infra-change",
                        missing_skill,
                    ],
                    "listed_skill_names": ["abyss-safe-infra-change"],
                    "skill_specs": [
                        {
                            "skill_name": "abyss-safe-infra-change",
                            "scope": "project",
                            "invocation_mode": "explicit-only",
                            "status": "scaffold",
                            "policy_allow_implicit": False,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                        {
                            "skill_name": missing_skill,
                            "scope": "project",
                            "invocation_mode": "explicit-only",
                            "status": "scaffold",
                            "policy_allow_implicit": False,
                            "techniques": [
                                PRIMARY_PUBLISHED_TECHNIQUE,
                                SECONDARY_PUBLISHED_TECHNIQUE,
                            ],
                        },
                    ],
                }
            ]
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            f"live project overlay '{family}' must list matching skill bundle(s): {missing_skill}",
            messages,
        )

    def test_single_skill_validation_checks_additional_generated_surfaces(self) -> None:
        repo_root = self.make_repo()
        self.write_catalogs(repo_root)

        lineage_path = repo_root / "generated" / "skill_lineage_surface.json"
        payload = json.loads(lineage_path.read_text(encoding="utf-8"))
        payload["skills"][0]["pending_technique_count"] = 99
        lineage_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root, skill_name="aoa-test-skill")
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated lineage surface artifact is out of date; run python scripts/build_catalog.py",
            messages,
        )
        self.assertEqual(1, self.run_main(repo_root, ["--skill", "aoa-test-skill"]))

    def test_stale_skill_composition_audit_surface_fails(self) -> None:
        repo_root = self.make_repo()
        self.write_catalogs(repo_root)

        audit = self.load_skill_composition_audit(repo_root)
        audit["summary"]["approved_exception_count"] = 99
        self.write_skill_composition_audit(repo_root, audit)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated skill composition audit artifact is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_mixed_family_index_duplicate_fails(self) -> None:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-validator-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        skill_names = [
            "aoa-test-skill",
            "atm10-perception-tests",
            "abyss-port-exposure-guard",
            "atm10-perception-tests",
        ]
        self.write_skill_index(repo_root, skill_names)
        for skill_name in {
            "aoa-test-skill",
            "atm10-perception-tests",
            "abyss-port-exposure-guard",
        }:
            self.add_skill_bundle(repo_root, skill_name=skill_name)
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("skill 'atm10-perception-tests' appears 2 times in the index", messages)

    def test_frontmatter_schema_violation_fails(self) -> None:
        repo_root = self.make_repo()
        frontmatter = self.load_skill_frontmatter(repo_root)
        frontmatter["summary"] = ["not", "a", "string"]
        self.write_skill_frontmatter(repo_root, frontmatter)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertTrue(any("schema violation" in message for message in messages))

    def test_manifest_schema_violation_fails(self) -> None:
        repo_root = self.make_repo()
        manifest = self.load_manifest(repo_root)
        manifest["unexpected"] = True
        self.write_manifest(repo_root, manifest)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertTrue(any("schema violation" in message for message in messages))

    def test_policy_schema_violation_fails(self) -> None:
        repo_root = self.make_repo(policy_allow_implicit=False)
        self.write_policy(
            repo_root,
            {
                "policy": {"allow_implicit_invocation": "sometimes"},
                "notes": ["Invalid policy fixture."],
            },
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertTrue(any("schema violation" in message for message in messages))

    def test_missing_techniques_yaml_fails(self) -> None:
        repo_root = self.make_repo(include_techniques_manifest=False)
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("file is missing", messages)
        self.assertEqual(1, self.run_main(repo_root))

    def test_missing_support_artifact_fails(self) -> None:
        repo_root = self.make_repo(include_support_artifact=False)
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "missing support artifact under examples/*.md, checks/review.md, or docs/reviews/*",
            messages,
        )

    def test_empty_capsule_source_section_fails(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "## Verification\n\n",
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("capsule source section 'Verification' must not be empty", messages)

    def test_explicit_only_without_policy_fails(self) -> None:
        repo_root = self.make_repo(invocation_mode="explicit-only")
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("explicit-only skills require agents/openai.yaml", messages)

    def test_explicit_only_with_implicit_policy_fails(self) -> None:
        repo_root = self.make_repo(
            invocation_mode="explicit-only",
            policy_allow_implicit=True,
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "explicit-only skills must set 'policy.allow_implicit_invocation' to false",
            messages,
        )

    def test_pending_technique_with_non_tbd_path_fails(self) -> None:
        repo_root = self.make_repo(
            techniques=[
                {
                    **PENDING_TECHNIQUE,
                    "path": "techniques/test/TECHNIQUE.md",
                }
            ],
            notes=[PENDING_NOTE],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("pending techniques must use path 'TBD'", messages)

    def test_published_technique_with_tbd_path_fails(self) -> None:
        repo_root = self.make_repo(
            techniques=[
                {
                    "id": "AOA-T-0009",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "TBD",
                    "source_ref": "0123456789abcdef0123456789abcdef01234567",
                    "use_sections": ["Intent"],
                }
            ]
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("published techniques cannot use path 'TBD'", messages)

    def test_pending_technique_with_non_tbd_source_ref_fails(self) -> None:
        repo_root = self.make_repo(
            techniques=[
                {
                    **PENDING_TECHNIQUE,
                    "source_ref": "0123456789abcdef0123456789abcdef01234567",
                }
            ],
            notes=[PENDING_NOTE],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("pending techniques must use source_ref 'TBD'", messages)

    def test_published_technique_with_tbd_source_ref_fails(self) -> None:
        repo_root = self.make_repo(
            techniques=[
                {
                    "id": "AOA-T-0009",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "techniques/test/TECHNIQUE.md",
                    "source_ref": "TBD",
                    "use_sections": ["Intent"],
                }
            ]
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("published techniques cannot use source_ref 'TBD'", messages)

    def test_canonical_status_rejects_pending_lineage(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
            techniques=[PENDING_TECHNIQUE],
            notes=[PENDING_NOTE],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("status 'canonical' cannot use pending technique_dependencies", messages)
        self.assertIn("status 'canonical' cannot use pending techniques in techniques.yaml", messages)

    def test_canonical_status_rejects_legacy_future_traceability(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            traceability_heading="Future traceability",
            review_record_surface="canonical-candidates",
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'canonical' requires 'Technique traceability' and forbids legacy 'Future traceability'",
            messages,
        )

    def test_canonical_status_rejects_tbd_traceability_values(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
            techniques=[
                {
                    "id": "AOA-T-0009",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "techniques/test/TECHNIQUE.md",
                    "source_ref": "TBD",
                    "use_sections": ["Intent"],
                }
            ],
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'canonical' requires concrete path and source_ref for every technique",
            messages,
        )

    def test_evaluated_status_requires_evaluation_fixture_file(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("file is missing", messages)

    def test_evaluated_status_with_only_autonomy_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            include_autonomy=True,
            use_cases=0,
            do_not_use_cases=0,
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' with status 'evaluated' requires at least one 'use' trigger case",
            messages,
        )
        self.assertIn(
            "skill 'aoa-test-skill' with status 'evaluated' requires at least one 'do_not_use' trigger case",
            messages,
        )

    def test_evaluated_status_with_one_trigger_side_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            include_autonomy=True,
            use_cases=1,
            do_not_use_cases=0,
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "skill 'aoa-test-skill' with status 'evaluated' requires at least one 'do_not_use' trigger case",
            messages,
        )

    def test_canonical_status_requires_evaluation_fixture_file(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("file is missing", messages)

    def test_evaluated_status_passes_with_full_evaluation_coverage(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_canonical_status_passes_with_full_evaluation_coverage(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_evaluated_status_allows_reportable_snapshot_gaps(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            use_snapshots=0,
            do_not_use_snapshots=0,
        )
        self.write_catalogs(repo_root)

        self.assertEqual([], validate_skills.run_validation(repo_root))
        matrix = self.load_evaluation_matrix(repo_root)
        self.assertEqual(
            [
                "missing_use_snapshot",
                "missing_do_not_use_snapshot",
            ],
            matrix["skills"][0]["canonical_eval_blockers"],
        )

    def test_canonical_status_requires_use_snapshot(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            use_snapshots=0,
            do_not_use_snapshots=1,
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'canonical' requires at least one 'use' snapshot case",
            messages,
        )

    def test_canonical_status_requires_do_not_use_snapshot(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(
            repo_root,
            use_snapshots=1,
            do_not_use_snapshots=0,
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "status 'canonical' requires at least one 'do_not_use' snapshot case",
            messages,
        )

    def test_skill_index_mismatch_fails(self) -> None:
        repo_root = self.make_repo(index_names=["aoa-other-skill"])
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("skill 'aoa-test-skill' is missing from the index", messages)
        self.assertIn(
            "index lists 'aoa-other-skill' but no matching skill directory exists",
            messages,
        )

    def test_pending_technique_with_tbd_refs_passes_for_scaffold_skill(self) -> None:
        repo_root = self.make_repo(
            techniques=[PENDING_TECHNIQUE],
            notes=[PENDING_NOTE],
        )
        self.write_catalogs(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_invalid_runtime_example_headings_fail(self) -> None:
        repo_root = self.make_repo()
        example_path = repo_root / "skills" / "aoa-test-skill" / "examples" / "example.md"
        example_path.write_text(
            textwrap.dedent(
                """\
                # Example

                ## Scenario

                Example scenario.

                ## Inputs

                - input
                """
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "runtime example missing required section 'Why this skill fits'",
            messages,
        )
        self.assertIn(
            "runtime example top-level sections must match the canonical order exactly",
            messages,
        )

    def test_invalid_review_checklist_headings_fail(self) -> None:
        repo_root = self.make_repo(include_support_artifact=False)
        review_path = repo_root / "skills" / "aoa-test-skill" / "checks" / "review.md"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text(
            textwrap.dedent(
                """\
                # Review Checklist

                ## Purpose

                Review purpose.

                ## Checklist

                - [ ] confirm scope
                """
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "review checklist missing required section 'When it applies'",
            messages,
        )
        self.assertIn(
            "review checklist top-level sections must match the canonical order exactly",
            messages,
        )

    def test_invalid_snapshot_headings_fail(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        snapshot_path = (
            repo_root
            / "tests"
            / "fixtures"
            / "skill_evaluation_snapshots"
            / "aoa-test-skill"
            / "aoa_test_skill_use_1.md"
        )
        snapshot_path.write_text(
            snapshot_path.read_text(encoding="utf-8").replace(
                "## Expected object\n\n- output\n\n",
                "",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "evaluation snapshot missing required section 'Expected object'",
            messages,
        )
        self.assertIn(
            "evaluation snapshot top-level sections must match the canonical order exactly",
            messages,
        )

    def test_snapshot_missing_required_phrase_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        snapshot_path = (
            repo_root
            / "tests"
            / "fixtures"
            / "skill_evaluation_snapshots"
            / "aoa-test-skill"
            / "aoa_test_skill_use_1.md"
        )
        snapshot_path.write_text(
            snapshot_path.read_text(encoding="utf-8").replace(
                "Decision: use `aoa-test-skill`.",
                "Decision: inspect `aoa-test-skill`.",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "evaluation snapshot is missing required output phrase 'Decision: use `aoa-test-skill`.'",
            messages,
        )

    def test_snapshot_forbidden_phrase_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        snapshot_path = (
            repo_root
            / "tests"
            / "fixtures"
            / "skill_evaluation_snapshots"
            / "aoa-test-skill"
            / "aoa_test_skill_do_not_use_1.md"
        )
        snapshot_path.write_text(
            snapshot_path.read_text(encoding="utf-8").replace(
                "- confirm the deflection is explicit",
                "- confirm the deflection is explicit\n- Decision: use `aoa-test-skill`.",
            ),
            encoding="utf-8",
        )
        self.write_catalogs(repo_root)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "evaluation snapshot contains forbidden output phrase 'Decision: use `aoa-test-skill`.'",
            messages,
        )

    def test_technique_dependencies_must_match_manifest_order(self) -> None:
        repo_root = self.make_repo(
            techniques=[PRIMARY_PUBLISHED_TECHNIQUE, SECONDARY_PUBLISHED_TECHNIQUE],
        )
        frontmatter = self.load_skill_frontmatter(repo_root)
        frontmatter["technique_dependencies"] = [
            SECONDARY_PUBLISHED_TECHNIQUE["id"],
            PRIMARY_PUBLISHED_TECHNIQUE["id"],
        ]
        self.write_skill_frontmatter(repo_root, frontmatter)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "frontmatter 'technique_dependencies' must exactly match techniques.yaml technique IDs in order",
            messages,
        )

    def test_manifest_repo_mismatch_fails_directly(self) -> None:
        repo_root = self.make_repo()
        manifest = self.load_manifest(repo_root)
        manifest["techniques"][0]["repo"] = "example/other-repo"
        self.write_manifest(repo_root, manifest)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("repo must resolve to 'aoa-techniques'", messages)

    def test_malformed_manifest_techniques_list_reports_issue_without_crashing(self) -> None:
        repo_root = self.make_repo()
        manifest = self.load_manifest(repo_root)
        manifest["techniques"] = "broken"
        self.write_manifest(repo_root, manifest)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("techniques.yaml must contain a techniques list", messages)

    def test_published_technique_requires_repo_relative_path(self) -> None:
        repo_root = self.make_repo()
        manifest = self.load_manifest(repo_root)
        manifest["techniques"][0]["path"] = "../techniques/test/TECHNIQUE.md"
        self.write_manifest(repo_root, manifest)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "published techniques must use concrete repo-relative paths",
            messages,
        )

    def test_missing_generated_catalogs_fail(self) -> None:
        repo_root = self.make_repo()
        shutil.rmtree(repo_root / "generated")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("generated catalog is missing", messages)
        self.assertIn("generated capsules are missing", messages)
        self.assertIn("generated sections are missing", messages)
        self.assertIn("generated walkthrough surface is missing", messages)
        self.assertIn("generated walkthrough markdown is missing", messages)
        self.assertIn("generated public surface is missing", messages)
        self.assertIn("generated public surface markdown is missing", messages)
        self.assertIn("generated evaluation matrix is missing", messages)
        self.assertIn("generated evaluation matrix markdown is missing", messages)

    def test_stale_generated_catalogs_fail(self) -> None:
        repo_root = self.make_repo()
        frontmatter = self.load_skill_frontmatter(repo_root)
        frontmatter["summary"] = "Changed without rebuilding catalog."
        self.write_skill_frontmatter(repo_root, frontmatter)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated catalog is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_targeted_validation_catches_stale_generated_catalog_for_selected_skill(self) -> None:
        repo_root = self.make_repo()
        frontmatter = self.load_skill_frontmatter(repo_root)
        frontmatter["summary"] = "Changed without rebuilding catalog."
        self.write_skill_frontmatter(repo_root, frontmatter)

        issues = validate_skills.run_validation(repo_root, skill_name="aoa-test-skill")
        messages = [issue.message for issue in issues]

        self.assertIn(
            "generated catalog entry for 'aoa-test-skill' is out of date; run python scripts/build_catalog.py",
            messages,
        )
        self.assertIn(
            "generated min catalog entry for 'aoa-test-skill' is out of date; run python scripts/build_catalog.py",
            messages,
        )
        self.assertIn(
            "generated capsule entry for 'aoa-test-skill' is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_min_catalog_must_match_full_projection(self) -> None:
        repo_root = self.make_repo()
        min_path = repo_root / "generated" / "skill_catalog.min.json"
        min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
        min_catalog["skills"][0]["summary"] = "tampered"
        min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "min catalog must be an exact projection of the full catalog",
            messages,
        )

    def test_malformed_full_catalog_reports_projection_issue_without_crashing(self) -> None:
        repo_root = self.make_repo()
        full_path = repo_root / "generated" / "skill_catalog.json"
        full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
        del full_catalog["skills"]
        full_path.write_text(json.dumps(full_catalog), encoding="utf-8")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated catalog is malformed; min projection could not be computed",
            messages,
        )

    def test_targeted_validation_reports_malformed_catalog_entry_projection(self) -> None:
        repo_root = self.make_repo()
        full_path = repo_root / "generated" / "skill_catalog.json"
        full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
        del full_catalog["skills"][0]["summary"]
        full_path.write_text(json.dumps(full_catalog), encoding="utf-8")

        issues = validate_skills.run_validation(repo_root, skill_name="aoa-test-skill")
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated catalog entry for 'aoa-test-skill' is malformed; min projection could not be computed",
            messages,
        )

    def test_stale_generated_capsules_fail(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "- verify",
                "- verify harder",
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated capsules are out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_generated_capsules_must_align_with_full_catalog(self) -> None:
        repo_root = self.make_repo()
        capsules = self.load_capsules(repo_root)
        capsules["skills"][0]["scope"] = "risk"
        self.write_capsules(repo_root, capsules)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated capsule entry for 'aoa-test-skill' must align with full catalog field 'scope'",
            messages,
        )

    def test_stale_generated_sections_fail(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Adaptation points\n\n- adapt\n",
                "## Adaptation points\n\n- adapt\n- adapt more\n",
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated sections are out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_generated_sections_must_align_with_full_catalog(self) -> None:
        repo_root = self.make_repo()
        sections = self.load_sections(repo_root)
        sections["skills"][0]["status"] = "promoted"
        self.write_sections(repo_root, sections)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated section entry for 'aoa-test-skill' must align with full catalog field 'status'",
            messages,
        )

    def test_targeted_validation_catches_stale_generated_section_for_selected_skill(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Adaptation points\n\n- adapt\n",
                "## Adaptation points\n\n- adapt\n- adapt more\n",
            ),
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root, skill_name="aoa-test-skill")
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated section entry for 'aoa-test-skill' is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_stale_generated_public_surface_json_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)

        public_surface = self.load_public_surface(repo_root)
        public_surface["skills"][0]["summary"] = "tampered"
        self.write_public_surface(repo_root, public_surface)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated public surface is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_stale_generated_public_surface_markdown_fails(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_record_surface="status-promotions",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)

        public_surface_markdown_path = repo_root / "generated" / "public_surface.md"
        public_surface_markdown_path.write_text(
            "stale markdown\n",
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated public surface markdown is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_stale_generated_walkthrough_surface_fails(self) -> None:
        repo_root = self.make_repo()
        walkthroughs = self.load_walkthroughs(repo_root)
        walkthroughs["skills"][0]["pick_summary"] = "tampered"
        self.write_walkthroughs(repo_root, walkthroughs)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated walkthrough surface is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_stale_generated_walkthrough_markdown_fails(self) -> None:
        repo_root = self.make_repo()
        walkthrough_markdown_path = repo_root / "generated" / "skill_walkthroughs.md"
        walkthrough_markdown_path.write_text(
            "stale walkthrough markdown\n",
            encoding="utf-8",
        )

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated walkthrough markdown is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_stale_generated_evaluation_matrix_json_fails(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)

        matrix = self.load_evaluation_matrix(repo_root)
        matrix["skills"][0]["use_snapshot_count"] = 0
        self.write_evaluation_matrix(repo_root, matrix)

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated evaluation matrix is out of date; run python scripts/build_catalog.py",
            messages,
        )

    def test_stale_generated_evaluation_matrix_markdown_fails(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.write_catalogs(repo_root)

        matrix_markdown_path = repo_root / "generated" / "skill_evaluation_matrix.md"
        matrix_markdown_path.write_text("stale evaluation matrix markdown\n", encoding="utf-8")

        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn(
            "generated evaluation matrix markdown is out of date; run python scripts/build_catalog.py",
            messages,
        )


class ValidateQuestbookSurfaceTests(unittest.TestCase):
    def write_valid_surface(self, repo_root: Path) -> None:
        write_text(
            repo_root / "QUESTBOOK.md",
            (REPO_ROOT / "QUESTBOOK.md").read_text(encoding="utf-8"),
        )
        write_text(
            repo_root / "docs" / "QUESTBOOK_SKILL_INTEGRATION.md",
            (REPO_ROOT / "docs" / "QUESTBOOK_SKILL_INTEGRATION.md").read_text(
                encoding="utf-8"
            ),
        )
        write_text(
            repo_root / "schemas" / "quest.schema.json",
            (REPO_ROOT / "schemas" / "quest.schema.json").read_text(encoding="utf-8"),
        )
        write_text(
            repo_root / "schemas" / "quest_dispatch.schema.json",
            (REPO_ROOT / "schemas" / "quest_dispatch.schema.json").read_text(
                encoding="utf-8"
            ),
        )
        for quest_id in validate_skills.QUEST_IDS:
            write_text(
                repo_root / "quests" / f"{quest_id}.yaml",
                (REPO_ROOT / "quests" / f"{quest_id}.yaml").read_text(encoding="utf-8"),
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

    def test_valid_questbook_surface_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "aoa-skills"
            self.write_valid_surface(repo_root)

            self.assertEqual([], validate_skills.validate_questbook_surface(repo_root))

    def test_missing_questbook_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "aoa-skills"
            self.write_valid_surface(repo_root)
            (repo_root / "QUESTBOOK.md").unlink()

            issues = validate_skills.validate_questbook_surface(repo_root)
            self.assertTrue(
                any(
                    issue.location.endswith("QUESTBOOK.md")
                    and issue.message == "file is missing"
                    for issue in issues
                )
            )

    def test_atm10_specific_anchor_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "aoa-skills"
            self.write_valid_surface(repo_root)
            write_text(
                repo_root / "quests" / "AOA-SK-Q-0004.yaml",
                (repo_root / "quests" / "AOA-SK-Q-0004.yaml")
                .read_text(encoding="utf-8")
                .replace("docs/OVERLAY_SPEC.md", "docs/overlays/atm10/PROJECT_OVERLAY.md", 1),
            )

            issues = validate_skills.validate_questbook_surface(repo_root)
            messages = [issue.message for issue in issues]
            self.assertIn(
                "AOA-SK-Q-0004 must keep activation.ref 'docs/OVERLAY_SPEC.md'",
                messages,
            )

    def test_wrong_repo_value_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "aoa-skills"
            self.write_valid_surface(repo_root)
            write_text(
                repo_root / "quests" / "AOA-SK-Q-0002.yaml",
                (repo_root / "quests" / "AOA-SK-Q-0002.yaml")
                .read_text(encoding="utf-8")
                .replace("repo: aoa-skills", "repo: aoa-evals"),
            )

            issues = validate_skills.validate_questbook_surface(repo_root)
            self.assertTrue(
                any(issue.message == "repo must be 'aoa-skills'" for issue in issues)
            )

    def test_example_projection_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir) / "aoa-skills"
            self.write_valid_surface(repo_root)
            write_text(
                repo_root / "generated" / "quest_catalog.min.example.json",
                (repo_root / "generated" / "quest_catalog.min.example.json")
                .read_text(encoding="utf-8")
                .replace(
                    '"source_path": "quests/AOA-SK-Q-0004.yaml"',
                    '"source_path": "quests/AOA-SK-Q-9999.yaml"',
                ),
            )

            issues = validate_skills.validate_questbook_surface(repo_root)
            self.assertTrue(
                any(
                    issue.message == "example catalog must stay aligned with quests/*.yaml"
                    for issue in issues
                )
            )


if __name__ == "__main__":
    unittest.main()
