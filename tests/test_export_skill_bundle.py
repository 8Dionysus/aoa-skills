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
import export_skill_bundle


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


class ExportSkillBundleTests(unittest.TestCase):
    def make_repo(self) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-export-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        skill_dir = repo_root / "skills" / "aoa-change-protocol"
        skill_dir.mkdir(parents=True)

        (skill_dir / "examples").mkdir()
        (skill_dir / "examples" / "runtime.md").write_text(
            textwrap.dedent(
                """\
                # Runtime Example

                ## Scenario

                Bounded change preview.

                ## Why this skill fits

                - the work changes more than one touched surface

                ## Expected inputs

                - the intended change

                ## Expected outputs

                - a bounded change report

                ## Boundary notes

                - keep the work inside the named scope

                ## Verification notes

                - verify the declared checks ran
                """
            ),
            encoding="utf-8",
        )

        (repo_root / "SKILL_INDEX.md").write_text(
            "# SKILL_INDEX\n\n| name | scope | status | summary |\n|---|---|---|---|\n"
            "| aoa-change-protocol | core | canonical | Bounded change workflow. |\n",
            encoding="utf-8",
        )
        (skill_dir / "SKILL.md").write_text(
            textwrap.dedent(
                """\
                ---
                name: aoa-change-protocol
                scope: core
                status: canonical
                summary: Bounded change workflow.
                invocation_mode: explicit-preferred
                technique_dependencies:
                  - AOA-T-0001
                ---

                # aoa-change-protocol

                ## Intent

                Keep non-trivial change bounded and reviewable.

                ## Trigger boundary

                Use this skill when:
                - the change touches code, config, or docs in a meaningful way

                Do not use this skill when:
                - the task is a tiny wording tweak with no operational consequence

                ## Inputs

                - requested change

                ## Outputs

                - declared scope
                - verification summary

                ## Procedure

                1. name the change
                2. bound the scope
                3. verify the result

                ## Contracts

                - stay inside the stated surface

                ## Risks and anti-patterns

                - hidden scope widening

                ## Verification

                - confirm explicit verification

                ## Technique traceability

                Traceability text.

                ## Adaptation points

                - adapt the checklist to repo shape
                """
            ),
            encoding="utf-8",
        )
        (skill_dir / "techniques.yaml").write_text(
            yaml.safe_dump(
                {
                    "skill_name": "aoa-change-protocol",
                    "composition_mode": "bounded",
                    "techniques": [PRIMARY_PUBLISHED_TECHNIQUE],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        (skill_dir / "agents").mkdir()
        (skill_dir / "agents" / "openai.yaml").write_text(
            yaml.safe_dump(
                {
                    "policy": {"allow_implicit_invocation": True},
                    "notes": ["Test policy."],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

        promotion_dir = repo_root / "docs" / "reviews" / "status-promotions"
        candidate_dir = repo_root / "docs" / "reviews" / "canonical-candidates"
        promotion_dir.mkdir(parents=True, exist_ok=True)
        candidate_dir.mkdir(parents=True, exist_ok=True)
        (promotion_dir / "aoa-change-protocol.md").write_text(
            "# aoa-change-protocol status promotion review\n\n## Findings\n\n- Evidence exists.\n",
            encoding="utf-8",
        )
        (candidate_dir / "aoa-change-protocol.md").write_text(
            "# aoa-change-protocol canonical candidate review\n\n## Findings\n\n- Evidence exists.\n",
            encoding="utf-8",
        )

        fixtures_dir = repo_root / "tests" / "fixtures"
        fixtures_dir.mkdir(parents=True, exist_ok=True)
        snapshots_dir = fixtures_dir / "skill_evaluation_snapshots" / "aoa-change-protocol"
        snapshots_dir.mkdir(parents=True, exist_ok=True)
        (snapshots_dir / "aoa_change_protocol_use_snapshot_1.md").write_text(
            textwrap.dedent(
                """\
                # Evaluation Snapshot

                ## Prompt

                use case

                ## Expected selection

                Decision: use `aoa-change-protocol`.

                ## Why

                - the change is meaningful and bounded

                ## Expected object

                - declared scope

                ## Boundary notes

                - stay inside the named change

                ## Verification hooks

                - confirm explicit verification
                """
            ),
            encoding="utf-8",
        )
        (snapshots_dir / "aoa_change_protocol_do_not_use_snapshot_1.md").write_text(
            textwrap.dedent(
                """\
                # Evaluation Snapshot

                ## Prompt

                do not use case

                ## Expected selection

                Decision: do_not_use `aoa-change-protocol`.

                ## Why

                - the edit is tiny and has no operational consequence

                ## Expected object

                - keep the response local

                ## Boundary notes

                - do not widen the task

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
                            "skill": "aoa-change-protocol",
                            "forbidden_runtime_terms": ["aoa-techniques"],
                        }
                    ],
                    "trigger_cases": [
                        {
                            "skill": "aoa-change-protocol",
                            "case_id": "aoa_change_protocol_use_1",
                            "prompt": "use case",
                            "expected": "use",
                            "required_phrases": ["touches code"],
                        },
                        {
                            "skill": "aoa-change-protocol",
                            "case_id": "aoa_change_protocol_do_not_use_1",
                            "prompt": "do not use case",
                            "expected": "do_not_use",
                            "required_phrases": ["tiny wording tweak"],
                        },
                    ],
                    "snapshot_cases": [
                        {
                            "skill": "aoa-change-protocol",
                            "case_id": "aoa_change_protocol_use_snapshot_1",
                            "prompt": "use case",
                            "expected": "use",
                            "snapshot_path": "tests/fixtures/skill_evaluation_snapshots/aoa-change-protocol/aoa_change_protocol_use_snapshot_1.md",
                            "required_output_phrases": [
                                "Decision: use `aoa-change-protocol`.",
                                "declared scope",
                            ],
                            "forbidden_output_phrases": [
                                "Decision: do_not_use `aoa-change-protocol`."
                            ],
                        },
                        {
                            "skill": "aoa-change-protocol",
                            "case_id": "aoa_change_protocol_do_not_use_snapshot_1",
                            "prompt": "do not use case",
                            "expected": "do_not_use",
                            "snapshot_path": "tests/fixtures/skill_evaluation_snapshots/aoa-change-protocol/aoa_change_protocol_do_not_use_snapshot_1.md",
                            "required_output_phrases": [
                                "Decision: do_not_use `aoa-change-protocol`.",
                                "keep the response local",
                            ],
                            "forbidden_output_phrases": [
                                "Decision: use `aoa-change-protocol`."
                            ],
                        },
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

        build_catalog.write_catalogs(repo_root)
        build_catalog.write_capsules(repo_root)
        build_catalog.write_sections(repo_root)
        build_catalog.write_walkthroughs(repo_root)
        build_catalog.write_public_surface(repo_root)
        build_catalog.write_evaluation_matrix(repo_root)
        return repo_root

    def run_main(self, repo_root: Path, argv: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = export_skill_bundle.main(argv, repo_root=repo_root)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_json_export_includes_bundle_files_support_artifacts_and_generated_surfaces(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            ["--skill", "aoa-change-protocol"],
        )

        self.assertEqual(0, exit_code)
        self.assertEqual("", stderr)

        payload = json.loads(stdout)
        self.assertEqual(1, payload["export_version"])
        self.assertEqual("aoa-change-protocol", payload["skill"]["name"])
        self.assertEqual(
            "skills/aoa-change-protocol/SKILL.md",
            payload["skill"]["skill_path"],
        )
        self.assertEqual(
            ["AOA-T-0001"],
            payload["manifest_facts"]["technique_dependencies"],
        )
        bundle_paths = [entry["path"] for entry in payload["bundle_files"]]
        self.assertIn("skills/aoa-change-protocol/SKILL.md", bundle_paths)
        self.assertIn("skills/aoa-change-protocol/techniques.yaml", bundle_paths)
        self.assertIn("skills/aoa-change-protocol/agents/openai.yaml", bundle_paths)

        support_paths = [entry["path"] for entry in payload["support_artifacts"]]
        self.assertIn("skills/aoa-change-protocol/examples/runtime.md", support_paths)

        review_paths = [entry["path"] for entry in payload["review_surfaces"]]
        self.assertIn(
            "docs/reviews/status-promotions/aoa-change-protocol.md",
            review_paths,
        )
        self.assertIn(
            "docs/reviews/canonical-candidates/aoa-change-protocol.md",
            review_paths,
        )

        generated_by_name = {entry["name"]: entry for entry in payload["generated_surfaces"]}
        self.assertTrue(generated_by_name["skill_catalog"]["present"])
        self.assertTrue(generated_by_name["skill_walkthroughs"]["present"])
        self.assertTrue(generated_by_name["skill_evaluation_matrix"]["present"])
        self.assertTrue(generated_by_name["public_surface"]["present"])
        self.assertEqual(
            "aoa-change-protocol",
            generated_by_name["skill_walkthroughs"]["snippet"]["entry"]["name"],
        )
        self.assertEqual(
            "aoa-change-protocol",
            generated_by_name["public_surface"]["snippet"]["entry"]["name"],
        )

    def test_text_export_lists_key_paths(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            ["--skill", "aoa-change-protocol", "--format", "text"],
        )

        self.assertEqual(0, exit_code)
        self.assertEqual("", stderr)
        self.assertIn("# Skill bundle export preview", stdout)
        self.assertIn("skills/aoa-change-protocol/SKILL.md", stdout)
        self.assertIn("skills/aoa-change-protocol/techniques.yaml", stdout)
        self.assertIn("docs/reviews/canonical-candidates/aoa-change-protocol.md", stdout)
        self.assertIn("generated/skill_walkthroughs.json", stdout)

    def test_unknown_skill_returns_exit_2(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            ["--skill", "aoa-missing-skill"],
        )

        self.assertEqual(2, exit_code)
        self.assertEqual("", stdout)
        self.assertIn("unknown skill 'aoa-missing-skill'", stderr)

    def test_invalid_format_returns_exit_2(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            ["--skill", "aoa-change-protocol", "--format", "yaml"],
        )

        self.assertEqual(2, exit_code)
        self.assertEqual("", stdout)
        self.assertIn("unknown format 'yaml'", stderr)


if __name__ == "__main__":
    unittest.main()
