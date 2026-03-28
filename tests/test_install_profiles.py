import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class InstallProfilesTests(unittest.TestCase):
    def stage_profile_bundle(self, profile: str, bundle_root: pathlib.Path) -> None:
        command = [
            sys.executable,
            "scripts/stage_skill_pack.py",
            "--repo-root",
            ".",
            "--profile",
            profile,
            "--output-root",
            str(bundle_root),
            "--execute",
            "--overwrite",
            "--format",
            "json",
        ]
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )

    def stage_profile_archive(
        self,
        profile: str,
        bundle_root: pathlib.Path,
        archive_path: pathlib.Path,
    ) -> None:
        command = [
            sys.executable,
            "scripts/stage_skill_pack.py",
            "--repo-root",
            ".",
            "--profile",
            profile,
            "--output-root",
            str(bundle_root),
            "--archive-path",
            str(archive_path),
            "--execute",
            "--overwrite",
            "--format",
            "json",
        ]
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )

    def test_install_profile_copy_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            command = [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--dest-root",
                str(dest_root),
                "--mode",
                "copy",
                "--execute",
            ]
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            installed = sorted(path.name for path in dest_root.iterdir() if path.is_dir())
            self.assertIn("aoa-change-protocol", installed)
            self.assertNotIn("aoa-safe-infra-change", installed)

    def test_install_profile_json_plan_includes_revision_and_verify_command(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            command = [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--dest-root",
                str(dest_root),
                "--mode",
                "copy",
                "--format",
                "json",
            ]
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            payload = json.loads(completed.stdout)
            self.assertEqual("repo-core-only", payload["profile"])
            self.assertRegex(payload["profile_revision"], r"^[0-9a-f]{64}$")
            self.assertEqual("0.1.0", payload["release_identity"]["latest_tagged_version"])
            self.assertIn("scripts/verify_skill_pack.py", payload["recommended_verify_command"])
            self.assertIn("--profile repo-core-only", payload["recommended_verify_command"])

    def test_install_profile_can_use_staged_bundle_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            dest_root = pathlib.Path(tmpdir) / "installed"
            self.stage_profile_bundle("repo-core-only", bundle_root)

            command = [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--bundle-root",
                str(bundle_root),
                "--dest-root",
                str(dest_root),
                "--mode",
                "copy",
                "--execute",
                "--format",
                "json",
            ]
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            payload = json.loads(completed.stdout)
            self.assertEqual("staged_bundle", payload["source_kind"])
            self.assertEqual(str(bundle_root.resolve()), payload["bundle_root"])
            self.assertTrue((dest_root / "aoa-change-protocol" / "SKILL.md").exists())

    def test_install_profile_can_use_staged_archive_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            archive_path = pathlib.Path(tmpdir) / "repo-core-only.zip"
            dest_root = pathlib.Path(tmpdir) / "installed"
            self.stage_profile_archive("repo-core-only", bundle_root, archive_path)

            command = [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--bundle-archive",
                str(archive_path),
                "--dest-root",
                str(dest_root),
                "--mode",
                "copy",
                "--execute",
                "--format",
                "json",
            ]
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            payload = json.loads(completed.stdout)
            self.assertEqual("staged_archive", payload["source_kind"])
            self.assertIsNone(payload["bundle_root"])
            self.assertEqual(str(archive_path.resolve()), payload["bundle_archive"])
            self.assertTrue((dest_root / "aoa-change-protocol" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
