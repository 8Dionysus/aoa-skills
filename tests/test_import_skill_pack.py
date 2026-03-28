import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class ImportSkillPackTests(unittest.TestCase):
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

    def run_import(self, *args: str) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, "scripts/import_skill_pack.py", *args]
        return subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_import_from_bundle_root_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            dest_root = pathlib.Path(tmpdir) / "installed"
            self.stage_profile_bundle("repo-core-only", bundle_root)

            completed = self.run_import(
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--bundle-root",
                str(bundle_root),
                "--dest-root",
                str(dest_root),
                "--format",
                "json",
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            payload = json.loads(completed.stdout)
            self.assertEqual("staged_bundle", payload["source_kind"])
            self.assertTrue(payload["inspection"]["verified"])
            self.assertFalse(payload["execute"])
            self.assertIsNone(payload["verification"])
            self.assertTrue(payload["verified"])

    def test_dry_run_import_from_bundle_archive_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            archive_path = pathlib.Path(tmpdir) / "repo-core-only.zip"
            dest_root = pathlib.Path(tmpdir) / "installed"
            self.stage_profile_archive("repo-core-only", bundle_root, archive_path)

            completed = self.run_import(
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--bundle-archive",
                str(archive_path),
                "--dest-root",
                str(dest_root),
                "--format",
                "json",
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
            self.assertTrue(payload["inspection"]["verified"])
            self.assertTrue(payload["verified"])

    def test_execute_import_from_bundle_root_copy_mode_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            dest_root = pathlib.Path(tmpdir) / "installed"
            self.stage_profile_bundle("repo-core-only", bundle_root)

            completed = self.run_import(
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
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            payload = json.loads(completed.stdout)
            self.assertTrue(payload["verified"])
            self.assertTrue(payload["verification"]["verified"])
            self.assertTrue((dest_root / "aoa-change-protocol" / "SKILL.md").exists())

    def test_execute_import_from_bundle_archive_copy_mode_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            archive_path = pathlib.Path(tmpdir) / "repo-core-only.zip"
            dest_root = pathlib.Path(tmpdir) / "installed"
            self.stage_profile_archive("repo-core-only", bundle_root, archive_path)

            completed = self.run_import(
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
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"command failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            payload = json.loads(completed.stdout)
            self.assertEqual("staged_archive", payload["source_kind"])
            self.assertTrue(payload["verification"]["verified"])
            self.assertTrue((dest_root / "aoa-change-protocol" / "SKILL.md").exists())

    def test_corrupted_bundle_archive_fails_before_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = pathlib.Path(tmpdir) / "broken.zip"
            dest_root = pathlib.Path(tmpdir) / "installed"
            archive_path.write_text("not-a-zip\n", encoding="utf-8")

            completed = self.run_import(
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--bundle-archive",
                str(archive_path),
                "--dest-root",
                str(dest_root),
                "--execute",
                "--format",
                "json",
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("invalid bundle archive", completed.stderr)
            self.assertFalse(dest_root.exists())

    def test_strict_root_propagates_to_final_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            dest_root = pathlib.Path(tmpdir) / "installed"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            (dest_root / "extra-skill").mkdir(parents=True, exist_ok=True)

            completed = self.run_import(
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--bundle-root",
                str(bundle_root),
                "--dest-root",
                str(dest_root),
                "--strict-root",
                "--execute",
                "--format",
                "json",
            )
            self.assertEqual(
                completed.returncode,
                1,
                msg=f"command failed unexpectedly\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            payload = json.loads(completed.stdout)
            self.assertFalse(payload["verified"])
            self.assertFalse(payload["verification"]["verified"])
            self.assertEqual(["extra-skill"], payload["verification"]["extra_skill_dirs"])

    def test_archive_source_rejects_symlink_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            archive_path = pathlib.Path(tmpdir) / "repo-core-only.zip"
            self.stage_profile_archive("repo-core-only", bundle_root, archive_path)

            completed = self.run_import(
                "--repo-root",
                ".",
                "--profile",
                "repo-core-only",
                "--bundle-archive",
                str(archive_path),
                "--mode",
                "symlink",
                "--format",
                "json",
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("symlink mode is not supported with --bundle-archive", completed.stderr)


if __name__ == "__main__":
    unittest.main()
