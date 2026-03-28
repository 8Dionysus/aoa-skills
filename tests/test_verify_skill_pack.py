import json
import pathlib
import shutil
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


class VerifySkillPackTests(unittest.TestCase):
    def install_profile_copy(self, profile: str, dest_root: pathlib.Path) -> None:
        completed = run_command(
            [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                profile,
                "--dest-root",
                str(dest_root),
                "--mode",
                "copy",
                "--execute",
            ]
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"install failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )

    def verify_profile(
        self,
        profile: str,
        *,
        install_root: pathlib.Path | None = None,
        strict_root: bool = False,
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        command = [
            sys.executable,
            "scripts/verify_skill_pack.py",
            "--repo-root",
            ".",
            "--profile",
            profile,
            "--format",
            "json",
        ]
        if install_root is not None:
            command.extend(["--install-root", str(install_root)])
        if strict_root:
            command.append("--strict-root")
        completed = run_command(command)
        payload = json.loads(completed.stdout)
        return completed, payload

    def test_repo_default_install_root_verifies_current_export(self) -> None:
        completed, payload = self.verify_profile("repo-default")

        self.assertEqual(
            completed.returncode,
            0,
            msg=f"verify failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        self.assertTrue(payload["verified"])
        self.assertEqual("repo-default", payload["profile"])
        self.assertEqual(
            payload["expected_skill_count"],
            payload["verified_skill_count"],
        )
        self.assertEqual([], payload["missing_skills"])
        self.assertEqual([], payload["mismatched_skills"])
        self.assertEqual([], payload["extra_skill_dirs"])
        self.assertEqual("0.1.0", payload["release_identity"]["latest_tagged_version"])

    def test_copy_installed_profile_verifies_successfully(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.install_profile_copy("repo-core-only", dest_root)

            completed, payload = self.verify_profile("repo-core-only", install_root=dest_root)

            self.assertEqual(
                completed.returncode,
                0,
                msg=f"verify failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            self.assertTrue(payload["verified"])
            self.assertEqual([], payload["extra_skill_dirs"])
            self.assertIn("aoa-change-protocol", [entry["name"] for entry in payload["skills"]])

    def test_missing_expected_skill_fails_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.install_profile_copy("repo-core-only", dest_root)
            shutil.rmtree(dest_root / "aoa-change-protocol")

            completed, payload = self.verify_profile("repo-core-only", install_root=dest_root)

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("aoa-change-protocol", payload["missing_skills"])

    def test_modified_skill_markdown_fails_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.install_profile_copy("repo-core-only", dest_root)
            skill_md_path = dest_root / "aoa-change-protocol" / "SKILL.md"
            skill_md_path.write_text(
                skill_md_path.read_text(encoding="utf-8") + "\n# drift\n",
                encoding="utf-8",
            )

            completed, payload = self.verify_profile("repo-core-only", install_root=dest_root)

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("aoa-change-protocol", payload["mismatched_skills"])

    def test_modified_support_artifact_fails_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.install_profile_copy("repo-risk-explicit", dest_root)
            artifact_path = (
                dest_root
                / "aoa-safe-infra-change"
                / "references"
                / "risk_surface_matrix.md"
            )
            artifact_path.write_text(
                artifact_path.read_text(encoding="utf-8") + "\nmanual drift\n",
                encoding="utf-8",
            )

            completed, payload = self.verify_profile("repo-risk-explicit", install_root=dest_root)

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("aoa-safe-infra-change", payload["mismatched_skills"])

    def test_extra_skill_dirs_are_reported_without_failing_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.install_profile_copy("repo-core-only", dest_root)
            (dest_root / "custom-skill").mkdir()

            completed, payload = self.verify_profile("repo-core-only", install_root=dest_root)

            self.assertEqual(0, completed.returncode)
            self.assertTrue(payload["verified"])
            self.assertIn("custom-skill", payload["extra_skill_dirs"])

    def test_extra_skill_dirs_fail_in_strict_root_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.install_profile_copy("repo-core-only", dest_root)
            (dest_root / "custom-skill").mkdir()

            completed, payload = self.verify_profile(
                "repo-core-only",
                install_root=dest_root,
                strict_root=True,
            )

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("custom-skill", payload["extra_skill_dirs"])


if __name__ == "__main__":
    unittest.main()
