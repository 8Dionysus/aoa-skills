import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class StageSkillPackTests(unittest.TestCase):
    def stage_profile(
        self,
        profile: str,
        bundle_root: pathlib.Path,
        *,
        execute: bool,
        overwrite: bool = False,
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        command = [
            sys.executable,
            "scripts/stage_skill_pack.py",
            "--repo-root",
            ".",
            "--profile",
            profile,
            "--output-root",
            str(bundle_root),
            "--format",
            "json",
        ]
        if execute:
            command.append("--execute")
        if overwrite:
            command.append("--overwrite")
        completed = run_command(command)
        payload = json.loads(completed.stdout)
        return completed, payload

    def test_stage_dry_run_reports_bundle_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            completed, payload = self.stage_profile(
                "repo-core-only",
                bundle_root,
                execute=False,
            )

            self.assertEqual(
                completed.returncode,
                0,
                msg=f"stage failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            self.assertEqual("repo-core-only", payload["profile"])
            self.assertRegex(payload["profile_revision"], r"^[0-9a-f]{64}$")
            self.assertEqual("0.1.0", payload["release_identity"]["latest_tagged_version"])
            self.assertRegex(payload["bundle_digest"], r"^[0-9a-f]{64}$")
            self.assertIn("scripts/install_skill_pack.py", payload["recommended_install_command"])
            self.assertIn("--bundle-root", payload["recommended_install_command"])
            self.assertIn("scripts/verify_skill_pack.py", payload["recommended_verify_command"])
            self.assertIn("--bundle-root", payload["recommended_verify_command"])

    def test_execute_stage_creates_deterministic_bundle_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root_a = pathlib.Path(tmpdir) / "bundle-a"
            bundle_root_b = pathlib.Path(tmpdir) / "bundle-b"

            completed_a, payload_a = self.stage_profile(
                "repo-core-only",
                bundle_root_a,
                execute=True,
                overwrite=True,
            )
            completed_b, payload_b = self.stage_profile(
                "repo-core-only",
                bundle_root_b,
                execute=True,
                overwrite=True,
            )

            self.assertEqual(0, completed_a.returncode, msg=completed_a.stderr)
            self.assertEqual(0, completed_b.returncode, msg=completed_b.stderr)
            self.assertTrue((bundle_root_a / "bundle_manifest.json").exists())
            self.assertTrue((bundle_root_a / ".agents" / "skills" / "aoa-change-protocol" / "SKILL.md").exists())

            manifest_a = json.loads((bundle_root_a / "bundle_manifest.json").read_text(encoding="utf-8"))
            manifest_b = json.loads((bundle_root_b / "bundle_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest_a, manifest_b)
            self.assertEqual(manifest_a["bundle_digest"], payload_a["bundle_digest"])
            self.assertEqual(manifest_b["bundle_digest"], payload_b["bundle_digest"])

    def test_staged_bundle_round_trip_install_and_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            install_root = pathlib.Path(tmpdir) / "installed"
            stage_completed, _ = self.stage_profile(
                "repo-core-only",
                bundle_root,
                execute=True,
                overwrite=True,
            )
            self.assertEqual(0, stage_completed.returncode, msg=stage_completed.stderr)

            install_completed = run_command(
                [
                    sys.executable,
                    "scripts/install_skill_pack.py",
                    "--repo-root",
                    ".",
                    "--profile",
                    "repo-core-only",
                    "--bundle-root",
                    str(bundle_root),
                    "--dest-root",
                    str(install_root),
                    "--mode",
                    "copy",
                    "--execute",
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(0, install_completed.returncode, msg=install_completed.stderr)

            verify_completed = run_command(
                [
                    sys.executable,
                    "scripts/verify_skill_pack.py",
                    "--repo-root",
                    ".",
                    "--profile",
                    "repo-core-only",
                    "--bundle-root",
                    str(bundle_root),
                    "--install-root",
                    str(install_root),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(0, verify_completed.returncode, msg=verify_completed.stderr)
            verify_payload = json.loads(verify_completed.stdout)
            self.assertTrue(verify_payload["verified"])
            self.assertEqual("staged_bundle", verify_payload["source_kind"])


if __name__ == "__main__":
    unittest.main()
