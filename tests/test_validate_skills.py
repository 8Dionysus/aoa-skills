from __future__ import annotations

import contextlib
import io
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


class ValidateSkillsTests(unittest.TestCase):
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
    ) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-validator-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()

        if index_names is None:
            index_names = [skill_name]
        self.write_skill_index(repo_root, index_names)

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

        return repo_root

    def write_skill_index(self, repo_root: Path, index_names: list[str]) -> None:
        rows = "\n".join(
            f"| {name} | core | scaffold | Test summary. |" for name in index_names
        )
        content = textwrap.dedent(
            f"""\
            # SKILL_INDEX

            | name | scope | status | summary |
            |---|---|---|---|
            {rows}
            """
        )
        (repo_root / "SKILL_INDEX.md").write_text(content, encoding="utf-8")

    def run_main(self, repo_root: Path, argv: list[str] | None = None) -> int:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            return validate_skills.main(argv or [], repo_root=repo_root)

    def load_skill_frontmatter(self, repo_root: Path) -> dict:
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        text = skill_md_path.read_text(encoding="utf-8")
        _, frontmatter, _ = text.split("---", 2)
        return yaml.safe_load(frontmatter)

    def write_skill_frontmatter(self, repo_root: Path, frontmatter: dict) -> None:
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        text = skill_md_path.read_text(encoding="utf-8")
        _, _, body = text.split("---", 2)
        updated = (
            "---\n"
            + yaml.safe_dump(frontmatter, sort_keys=False).strip()
            + "\n---"
            + body
        )
        skill_md_path.write_text(updated, encoding="utf-8")

    def load_manifest(self, repo_root: Path) -> dict:
        manifest_path = repo_root / "skills" / "aoa-test-skill" / "techniques.yaml"
        return yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, repo_root: Path, manifest: dict) -> None:
        manifest_path = repo_root / "skills" / "aoa-test-skill" / "techniques.yaml"
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

    def test_clean_fixture_passes(self) -> None:
        repo_root = self.make_repo()
        issues = validate_skills.run_validation(repo_root)
        self.assertEqual([], issues)
        self.assertEqual(0, self.run_main(repo_root))
        self.assertEqual(0, self.run_main(repo_root, ["--skill", "aoa-test-skill"]))

    def test_future_traceability_heading_is_allowed(self) -> None:
        repo_root = self.make_repo(traceability_heading="Future traceability")
        self.assertEqual([], validate_skills.run_validation(repo_root))

    def test_linked_status_is_allowed(self) -> None:
        repo_root = self.make_repo(status="linked")
        self.assertEqual([], validate_skills.run_validation(repo_root))

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
                    "id": "AOA-T-PENDING-TEST",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "techniques/test/TECHNIQUE.md",
                    "source_ref": "TBD",
                    "use_sections": ["Intent"],
                }
            ],
            notes=["Replace AOA-T-PENDING-TEST, path TBD, and source_ref TBD after publication."],
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
                    "id": "AOA-T-PENDING-TEST",
                    "repo": "8Dionysus/aoa-techniques",
                    "path": "TBD",
                    "source_ref": "0123456789abcdef0123456789abcdef01234567",
                    "use_sections": ["Intent"],
                }
            ],
            notes=["Replace AOA-T-PENDING-TEST, path TBD, and source_ref TBD after publication."],
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

    def test_skill_index_mismatch_fails(self) -> None:
        repo_root = self.make_repo(index_names=["aoa-other-skill"])
        issues = validate_skills.run_validation(repo_root)
        messages = [issue.message for issue in issues]
        self.assertIn("skill 'aoa-test-skill' is missing from the index", messages)
        self.assertIn(
            "index lists 'aoa-other-skill' but no matching skill directory exists",
            messages,
        )


if __name__ == "__main__":
    unittest.main()
