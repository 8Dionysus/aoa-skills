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
import inspect_skill


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


class InspectSkillTests(unittest.TestCase):
    def make_repo(self) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-inspect-"))
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

                A bounded change needs explicit scope and verification.

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
                invocation_mode: implicit-friendly
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
        promotion_dir = repo_root / "docs" / "reviews" / "canonical-candidates"
        promotion_dir.mkdir(parents=True, exist_ok=True)
        (promotion_dir / "aoa-change-protocol.md").write_text(
            "# aoa-change-protocol canonical candidate review\n\n## Findings\n\n- Evidence exists.\n",
            encoding="utf-8",
        )
        fixtures_dir = repo_root / "tests" / "fixtures"
        fixtures_dir.mkdir(parents=True, exist_ok=True)
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
        return repo_root

    def run_main(self, repo_root: Path, argv: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = inspect_skill.main(argv, repo_root=repo_root)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_walkthrough_text_view_succeeds(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            ["--skill", "aoa-change-protocol", "--view", "walkthrough"],
        )

        self.assertEqual(0, exit_code)
        self.assertEqual("", stderr)
        self.assertIn("# aoa-change-protocol", stdout)
        self.assertIn("pick summary: Bounded change workflow.", stdout)
        self.assertIn("Support artifacts", stdout)

    def test_walkthrough_json_view_is_deterministic(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            [
                "--skill",
                "aoa-change-protocol",
                "--view",
                "walkthrough",
                "--format",
                "json",
            ],
        )

        self.assertEqual(0, exit_code)
        self.assertEqual("", stderr)
        payload = json.loads(stdout)
        self.assertEqual("aoa-change-protocol", payload["name"])
        self.assertEqual(["declared scope", "verification summary"], payload["object_use_shape"])
        self.assertEqual(["capsule", "sections", "full", "evidence"], payload["inspection_order"])
        self.assertEqual(
            "skills/aoa-change-protocol/examples/runtime.md",
            payload["support_artifacts"][0]["path"],
        )

    def test_unknown_skill_returns_exit_2(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            ["--skill", "aoa-missing-skill", "--view", "walkthrough"],
        )

        self.assertEqual(2, exit_code)
        self.assertEqual("", stdout)
        self.assertIn("unknown skill 'aoa-missing-skill'", stderr)

    def test_unknown_view_returns_exit_2(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            ["--skill", "aoa-change-protocol", "--view", "unknown-view"],
        )

        self.assertEqual(2, exit_code)
        self.assertEqual("", stdout)
        self.assertIn("unknown view 'unknown-view'", stderr)


if __name__ == "__main__":
    unittest.main()
