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

import validate_skills
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
PENDING_NOTE = "Replace AOA-T-PENDING-TEST, path TBD, and source_ref TBD after publish."


class ValidateSkillsTests(unittest.TestCase):
    def add_skill_bundle(
        self,
        repo_root: Path,
        *,
        skill_name: str,
        traceability_heading: str = "Technique traceability",
        invocation_mode: str = "explicit-preferred",
        status: str = "scaffold",
        include_support_artifact: bool = True,
        include_techniques_manifest: bool = True,
        policy_allow_implicit: bool | None = None,
        techniques: list[dict] | None = None,
        notes: list[str] | None = None,
    ) -> None:
        skill_dir = repo_root / "skills" / skill_name
        skill_dir.mkdir()

        technique_ids = [entry["id"] for entry in (techniques or [PRIMARY_PUBLISHED_TECHNIQUE])]
        skill_md = textwrap.dedent(
            f"""\
            ---
            name: {skill_name}
            scope: core
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
                "# Example\n\nSupport artifact.\n",
                encoding="utf-8",
            )

        if include_techniques_manifest:
            manifest = {
                "skill_name": skill_name,
                "composition_mode": "bounded",
                "techniques": techniques or [PRIMARY_PUBLISHED_TECHNIQUE],
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

    def make_repo(
        self,
        *,
        skill_name: str = "aoa-test-skill",
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
    ) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-validator-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()

        if index_names is None:
            index_names = [skill_name]
        self.write_skill_index(repo_root, index_names)
        self.add_skill_bundle(
            repo_root,
            skill_name=skill_name,
            traceability_heading=traceability_heading,
            invocation_mode=invocation_mode,
            status=status,
            include_support_artifact=include_support_artifact,
            include_techniques_manifest=include_techniques_manifest,
            policy_allow_implicit=policy_allow_implicit,
            techniques=techniques,
            notes=notes,
        )
        if review_record_surface is not None:
            self.add_public_review_record(repo_root, skill_name, review_record_surface)
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

    def write_evaluation_fixtures_for_skill(
        self,
        repo_root: Path,
        *,
        skill_name: str = "aoa-test-skill",
        include_autonomy: bool = True,
        use_cases: int = 1,
        do_not_use_cases: int = 1,
    ) -> None:
        fixtures_dir = repo_root / "tests" / "fixtures"
        fixtures_dir.mkdir(parents=True, exist_ok=True)

        data: dict[str, list[dict]] = {
            "autonomy_checks": [],
            "trigger_cases": [],
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
        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)

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

    def test_clean_fixture_passes(self) -> None:
        repo_root = self.make_repo()
        issues = validate_skills.run_validation(repo_root)
        self.assertEqual([], issues)
        self.assertEqual(0, self.run_main(repo_root))
        self.assertEqual(0, self.run_main(repo_root, ["--skill", "aoa-test-skill"]))

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

    def test_future_traceability_heading_is_allowed(self) -> None:
        repo_root = self.make_repo(traceability_heading="Future traceability")
        self.assertEqual([], validate_skills.run_validation(repo_root))

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
        review_check.write_text("# Review\n\n- ok\n", encoding="utf-8")
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_reviewed_status_passes_with_status_promotion_review_record(self) -> None:
        repo_root = self.make_repo(
            status="reviewed",
            review_record_surface="status-promotions",
        )
        self.assertEqual([], validate_skills.run_validation(repo_root))

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
        self.assertIn("missing support artifact under examples/*.md or checks/*.md", messages)

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
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_canonical_status_passes_with_full_evaluation_coverage(self) -> None:
        repo_root = self.make_repo(
            status="canonical",
            review_record_surface="canonical-candidates",
        )
        self.write_evaluation_fixtures_for_skill(repo_root)
        self.assertEqual([], validate_skills.run_validation(repo_root))

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


if __name__ == "__main__":
    unittest.main()
