from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validation.validators import skill_evidence_readout_surface


VALIDATOR_COMMAND = (
    "python",
    "scripts/validation/validate_skill_evidence_readouts.py",
    "--repo-root",
    ".",
)


class SkillEvidenceReadoutFreshnessTests(unittest.TestCase):
    def make_repo(
        self,
        *,
        matrix_skills: list[dict[str, str]],
        quality_skills: list[dict[str, str]],
        promotion_skills: list[dict[str, str]],
        quality_count: int | None = None,
        promotion_count: int | None = None,
    ) -> Path:
        tempdir = tempfile.TemporaryDirectory(prefix="aoa-evidence-readouts-")
        self.addCleanup(tempdir.cleanup)
        repo_root = Path(tempdir.name)
        generated = repo_root / "generated"
        generated.mkdir(parents=True)

        payloads = {
            "skill_evaluation_matrix.json": {
                "evaluation_matrix_version": "test",
                "source_of_truth": "test",
                "skills": matrix_skills,
            },
            "skill_quality_audit.json": {
                "report_kind": "skill_quality_audit",
                "skill_count": len(quality_skills) if quality_count is None else quality_count,
                "skills": quality_skills,
            },
            "skill_promotion_pressure.json": {
                "report_kind": "skill_promotion_pressure",
                "skill_count": len(promotion_skills)
                if promotion_count is None
                else promotion_count,
                "skills": promotion_skills,
            },
        }
        for filename, payload in payloads.items():
            (generated / filename).write_text(
                json.dumps(payload, indent=2) + "\n",
                encoding="utf-8",
            )
        for filename, skills in (
            ("skill_quality_audit.md", quality_skills),
            ("skill_promotion_pressure.md", promotion_skills),
        ):
            lines = [
                "# Test Readout",
                "",
                f"- skill count: {len(skills)}",
                "",
                "## Skill Matrix",
                "",
                "| skill | status |",
                "|---|---|",
                *[f"| `{skill['name']}` | `{skill['status']}` |" for skill in skills],
            ]
            (generated / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")
        return repo_root

    @staticmethod
    def skill(name: str, *, status: str = "scaffold", scope: str = "core") -> dict[str, str]:
        return {"name": name, "status": status, "scope": scope}

    def messages(self, repo_root: Path) -> list[str]:
        return [
            f"{issue.location}: {issue.message}"
            for issue in skill_evidence_readout_surface.validate(repo_root)
        ]

    def test_reports_must_cover_the_exact_evaluation_matrix_skill_set(self) -> None:
        matrix = [self.skill("aoa-alpha"), self.skill("aoa-beta")]
        repo_root = self.make_repo(
            matrix_skills=matrix,
            quality_skills=[self.skill("aoa-alpha")],
            promotion_skills=[self.skill("aoa-alpha"), self.skill("aoa-extra")],
            quality_count=45,
        )

        messages = self.messages(repo_root)

        self.assertTrue(
            any("skill_count must equal evaluation matrix count 2; got 45" in item for item in messages)
        )
        self.assertTrue(any("missing skills: aoa-beta" in item for item in messages))
        self.assertTrue(any("unexpected skills: aoa-extra" in item for item in messages))

    def test_reports_reject_duplicate_names_and_status_scope_drift(self) -> None:
        matrix = [self.skill("aoa-alpha", status="evaluated", scope="project")]
        repo_root = self.make_repo(
            matrix_skills=matrix,
            quality_skills=[
                self.skill("aoa-alpha", status="scaffold", scope="core"),
                self.skill("aoa-alpha", status="scaffold", scope="core"),
            ],
            promotion_skills=[self.skill("aoa-alpha", status="canonical", scope="risk")],
        )

        messages = self.messages(repo_root)

        self.assertTrue(any("duplicate skill names: aoa-alpha" in item for item in messages))
        self.assertTrue(
            any("aoa-alpha status must be 'evaluated'; got 'scaffold'" in item for item in messages)
        )
        self.assertTrue(
            any("aoa-alpha scope must be 'project'; got 'core'" in item for item in messages)
        )
        self.assertTrue(
            any("aoa-alpha status must be 'evaluated'; got 'canonical'" in item for item in messages)
        )

    def test_complete_reports_pass_while_live_metrics_remain_out_of_claim(self) -> None:
        matrix = [
            self.skill("aoa-alpha", status="evaluated", scope="project"),
            self.skill("aoa-beta", status="scaffold", scope="core"),
        ]
        quality = [dict(skill, evidence={"session_mention_count": 999}) for skill in matrix]
        promotion = [dict(skill, usage_evidence={"dispatch_event_count": 999}) for skill in matrix]
        repo_root = self.make_repo(
            matrix_skills=matrix,
            quality_skills=quality,
            promotion_skills=promotion,
        )

        self.assertEqual([], skill_evidence_readout_surface.validate(repo_root))
        self.assertIn("does not validate live usage", skill_evidence_readout_surface.CLAIM_LIMIT)

    def test_markdown_skill_matrix_must_match_its_json_readout(self) -> None:
        matrix = [self.skill("aoa-alpha"), self.skill("aoa-beta", status="evaluated")]
        repo_root = self.make_repo(
            matrix_skills=matrix,
            quality_skills=matrix,
            promotion_skills=matrix,
        )
        (repo_root / "generated" / "skill_quality_audit.md").write_text(
            "# Stale\n\n- skill count: 1\n\n## Skill Matrix\n\n"
            "| skill | status |\n|---|---|\n| `aoa-alpha` | `scaffold` |\n",
            encoding="utf-8",
        )

        messages = self.messages(repo_root)

        self.assertTrue(any("skill count must equal JSON skill_count 2; got 1" in item for item in messages))
        self.assertTrue(any("missing skills: aoa-beta" in item for item in messages))

    def test_json_cli_is_machine_readable_and_fails_closed(self) -> None:
        matrix = [self.skill("aoa-alpha"), self.skill("aoa-beta")]
        repo_root = self.make_repo(
            matrix_skills=matrix,
            quality_skills=[self.skill("aoa-alpha")],
            promotion_skills=matrix,
        )
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = skill_evidence_readout_surface.main_validate(
                ["--repo-root", str(repo_root), "--json"]
            )

        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, exit_code)
        self.assertEqual("fail", payload["status"])
        self.assertEqual(2, payload["expected_skill_count"])
        self.assertGreater(payload["issue_count"], 0)
        self.assertEqual(skill_evidence_readout_surface.CLAIM_LIMIT, payload["claim_limit"])

    def test_blocking_lanes_include_the_freshness_validator(self) -> None:
        manifest = json.loads(
            (REPO_ROOT / "config" / "validation_lanes.json").read_text(encoding="utf-8")
        )

        for sequence_name in ("export_generated_check", "export_full", "release_check"):
            commands = [tuple(command) for command in manifest["command_sequences"][sequence_name]]
            with self.subTest(sequence=sequence_name):
                self.assertIn(VALIDATOR_COMMAND, commands)


if __name__ == "__main__":
    unittest.main()
