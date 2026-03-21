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

import report_skill_boundaries


PRIMARY_TECHNIQUE = {
    "id": "AOA-T-0001",
    "repo": "8Dionysus/aoa-techniques",
    "path": "techniques/adjacency/primary/TECHNIQUE.md",
    "source_ref": "0123456789abcdef0123456789abcdef01234567",
}


class ReportSkillBoundariesTests(unittest.TestCase):
    def make_repo(self, *, include_candidate_adjacency: bool = True) -> Path:
        repo_root = Path(tempfile.mkdtemp(prefix="aoa-skills-boundary-report-"))
        self.addCleanup(shutil.rmtree, repo_root, True)
        (repo_root / "skills").mkdir()
        (repo_root / "docs" / "reviews" / "status-promotions").mkdir(parents=True, exist_ok=True)
        (repo_root / "docs" / "reviews" / "canonical-candidates").mkdir(parents=True, exist_ok=True)
        (repo_root / "tests" / "fixtures" / "skill_evaluation_snapshots").mkdir(
            parents=True,
            exist_ok=True,
        )

        self.write_skill(
            repo_root,
            "aoa-change-protocol",
            status="canonical",
            summary="Bounded change workflow.",
        )
        self.write_skill(
            repo_root,
            "aoa-bounded-context-map",
            status="evaluated",
            summary="Boundary clarification workflow.",
        )

        if include_candidate_adjacency:
            adjacency_cases = [
                self.write_adjacency_case(
                    repo_root,
                    skill="aoa-change-protocol",
                    case_id="change_protocol_vs_bounded_context_map_boundary",
                    adjacent_skills=["aoa-bounded-context-map"],
                    expected="use",
                    prompt="Compare a bounded change workflow with a boundary mapping workflow.",
                    required_output_phrases=[
                        "This is an aoa-change-protocol case, not an aoa-bounded-context-map case.",
                        "A scoped change plan with a stated risk, bounded edit, and named verification step.",
                    ],
                ),
                self.write_adjacency_case(
                    repo_root,
                    skill="aoa-bounded-context-map",
                    case_id="bounded_context_map_vs_change_protocol_boundary",
                    adjacent_skills=["aoa-change-protocol"],
                    expected="use",
                    prompt="Compare a boundary mapping workflow with a bounded change workflow.",
                    required_output_phrases=[
                        "This is an aoa-bounded-context-map case, not an aoa-change-protocol case.",
                        "A boundary clarification that separates overlapping concepts before implementation continues.",
                    ],
                ),
            ]
        else:
            adjacency_cases = [
                self.write_adjacency_case(
                    repo_root,
                    skill="aoa-change-protocol",
                    case_id="change_protocol_vs_bounded_context_map_boundary",
                    adjacent_skills=["aoa-bounded-context-map"],
                    expected="use",
                    prompt="Compare a bounded change workflow with a boundary mapping workflow.",
                    required_output_phrases=[
                        "This is an aoa-change-protocol case, not an aoa-bounded-context-map case.",
                        "A scoped change plan with a stated risk, bounded edit, and named verification step.",
                    ],
                )
            ]

        self.write_fixtures(repo_root, adjacency_cases)
        return repo_root

    def write_skill(self, repo_root: Path, skill_name: str, *, status: str, summary: str) -> None:
        skill_dir = repo_root / "skills" / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            textwrap.dedent(
                f"""\
                ---
                name: {skill_name}
                scope: core
                status: {status}
                summary: {summary}
                invocation_mode: implicit-friendly
                technique_dependencies:
                  - {PRIMARY_TECHNIQUE["id"]}
                ---

                # {skill_name}

                ## Intent

                Explain the workflow.

                ## Trigger boundary

                Use this skill when:
                - the task is meaningfully bounded and needs a clear choice between nearby workflows

                Do not use this skill when:
                - the task is a tiny local edit or a different adjacent skill is a clearer fit

                ## Inputs

                - user request

                ## Outputs

                - bounded recommendation
                - next step

                ## Procedure

                1. inspect the request
                2. name the fit
                3. state the next step

                ## Contracts

                - stay inside the named boundary

                ## Risks and anti-patterns

                - scope widening

                ## Verification

                - confirm the recommendation stays bounded

                ## Technique traceability

                Traceability notes.
                """
            ),
            encoding="utf-8",
        )
        (skill_dir / "techniques.yaml").write_text(
            yaml.safe_dump(
                {
                    "skill_name": skill_name,
                    "composition_mode": "bounded",
                    "techniques": [PRIMARY_TECHNIQUE],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def write_adjacency_case(
        self,
        repo_root: Path,
        *,
        skill: str,
        case_id: str,
        adjacent_skills: list[str],
        expected: str,
        prompt: str,
        required_output_phrases: list[str],
    ) -> dict[str, object]:
        snapshot_dir = repo_root / "tests" / "fixtures" / "skill_evaluation_snapshots" / skill
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        snapshot_path = snapshot_dir / f"{case_id}.md"
        snapshot_path.write_text(
            textwrap.dedent(
                f"""\
                # Evaluation Snapshot

                ## Prompt

                {prompt}

                ## Expected selection

                Decision: {expected} `{skill}`.

                ## Why

                - {required_output_phrases[0]}

                ## Expected object

                - {required_output_phrases[1]}

                ## Boundary notes

                - stay inside the named boundary

                ## Verification hooks

                - confirm the recommendation stays bounded
                """
            ),
            encoding="utf-8",
        )
        return {
            "skill": skill,
            "case_id": case_id,
            "prompt": prompt,
            "expected": expected,
            "adjacent_skill": adjacent_skills[0] if len(adjacent_skills) == 1 else None,
            "snapshot_path": str(snapshot_path.relative_to(repo_root).as_posix()),
            "required_output_phrases": required_output_phrases,
            "forbidden_output_phrases": [],
        }

    def write_fixtures(self, repo_root: Path, adjacency_cases: list[dict[str, object]]) -> None:
        (repo_root / "tests" / "fixtures").mkdir(parents=True, exist_ok=True)
        (repo_root / "tests" / "fixtures" / "skill_evaluation_cases.yaml").write_text(
            yaml.safe_dump(
                {
                    "autonomy_checks": [
                        {
                            "skill": "aoa-change-protocol",
                            "forbidden_runtime_terms": ["aoa-techniques"],
                        },
                        {
                            "skill": "aoa-bounded-context-map",
                            "forbidden_runtime_terms": ["aoa-techniques"],
                        },
                    ],
                    "trigger_cases": [
                        {
                            "skill": "aoa-change-protocol",
                            "case_id": "change_protocol_use",
                            "prompt": "Use the bounded change workflow.",
                            "expected": "use",
                            "required_phrases": ["meaningfully bounded"],
                        },
                        {
                            "skill": "aoa-change-protocol",
                            "case_id": "change_protocol_do_not_use",
                            "prompt": "This is a tiny local fix.",
                            "expected": "do_not_use",
                            "required_phrases": ["tiny local edit"],
                        },
                        {
                            "skill": "aoa-bounded-context-map",
                            "case_id": "bounded_context_map_use",
                            "prompt": "Clarify the boundary before coding.",
                            "expected": "use",
                            "required_phrases": ["meaningfully bounded"],
                        },
                        {
                            "skill": "aoa-bounded-context-map",
                            "case_id": "bounded_context_map_do_not_use",
                            "prompt": "The boundary is already obvious.",
                            "expected": "do_not_use",
                            "required_phrases": ["tiny local edit"],
                        },
                    ],
                    "snapshot_cases": [],
                    "adjacency_cases": adjacency_cases,
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def run_main(self, repo_root: Path, argv: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = report_skill_boundaries.main(argv, repo_root=repo_root)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_text_report_succeeds(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(repo_root, ["--format", "text"])

        self.assertEqual(0, exit_code)
        self.assertEqual("", stderr)
        self.assertIn("# Skill boundary report", stdout)
        self.assertIn("required adjacency gaps: 0", stdout)
        self.assertIn("aoa-change-protocol", stdout)
        self.assertIn("aoa-bounded-context-map", stdout)

    def test_json_report_is_deterministic(self) -> None:
        repo_root = self.make_repo()

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            [
                "--skill",
                "aoa-bounded-context-map",
                "--skill",
                "aoa-change-protocol",
                "--format",
                "json",
            ],
        )

        self.assertEqual(0, exit_code)
        self.assertEqual("", stderr)
        payload = json.loads(stdout)
        self.assertEqual(["aoa-bounded-context-map", "aoa-change-protocol"], payload["selected_skills"])
        self.assertEqual(2, len(payload["skills"]))
        self.assertEqual(2, len(payload["cases"]))
        self.assertEqual(0, payload["summary"]["required_gap_count"])

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
            ["--format", "yaml"],
        )

        self.assertEqual(2, exit_code)
        self.assertEqual("", stdout)
        self.assertIn("unknown format 'yaml'", stderr)

    def test_fail_on_required_gaps_returns_exit_1(self) -> None:
        repo_root = self.make_repo(include_candidate_adjacency=False)

        exit_code, stdout, stderr = self.run_main(
            repo_root,
            ["--fail-on-required-gaps"],
        )

        self.assertEqual(1, exit_code)
        self.assertEqual("", stderr)
        self.assertIn("required adjacency gaps: 1", stdout)
        self.assertIn("aoa-bounded-context-map", stdout)


if __name__ == "__main__":
    unittest.main()
