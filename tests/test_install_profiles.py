import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class InstallProfilesTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
