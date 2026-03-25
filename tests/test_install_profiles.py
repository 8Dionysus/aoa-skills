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


if __name__ == "__main__":
    unittest.main()
