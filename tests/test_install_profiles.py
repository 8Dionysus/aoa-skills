import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class InstallProfilesTests(unittest.TestCase):
    def test_install_script_imports_without_site_packages(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-S",
                "-c",
                (
                    "import pathlib, sys; "
                    f"sys.path.insert(0, r'{(REPO_ROOT / 'scripts').as_posix()}'); "
                    "import install_skill_pack; "
                    "print('ok')"
                ),
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, msg=completed.stderr)
        self.assertEqual("ok", completed.stdout.strip())

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

    def test_foundation_profile_copy_mode_includes_risk_ring_without_overlays(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            command = [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                "repo-project-foundation",
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
            self.assertIn("aoa-safe-infra-change", installed)
            self.assertNotIn("abyss-safe-infra-change", installed)

    def test_install_profile_symlink_reinstall_is_idempotent_when_target_matches_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest_root = pathlib.Path(tmpdir) / "skills"
            command = [
                sys.executable,
                "scripts/install_skill_pack.py",
                "--repo-root",
                ".",
                "--profile",
                "repo-project-core-kernel",
                "--dest-root",
                str(dest_root),
                "--mode",
                "symlink",
                "--execute",
                "--overwrite",
                "--format",
                "json",
            ]
            first = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            second = subprocess.run(
                command,
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, first.returncode, msg=first.stderr or first.stdout)
            self.assertEqual(0, second.returncode, msg=second.stderr or second.stdout)

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
            self.assertEqual("0.2.0", payload["release_identity"]["latest_tagged_version"])
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

    def test_install_profile_rejects_symlink_mode_for_staged_archive(self):
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
                "symlink",
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
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn(
                "symlink mode is not supported with --bundle-archive",
                completed.stderr,
            )

    def test_install_profile_rejects_bundle_paths_outside_root(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            dest_root = pathlib.Path(tmpdir) / "installed"
            (bundle_root / ".agents" / "skills").mkdir(parents=True, exist_ok=True)
            (bundle_root / "bundle_manifest.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "profile": "repo-core-only",
                        "profile_revision": "0" * 64,
                        "scope": "repo",
                        "install_mode": "copy",
                        "install_root": ".agents/skills",
                        "skill_root": ".agents/skills",
                        "skill_count": 1,
                        "skills": [
                            {
                                "name": "aoa-change-protocol",
                                "relative_dir": "../escape",
                                "skill_revision": "0" * 64,
                                "content_hash": "0" * 64,
                            }
                        ],
                        "release_identity": {
                            "latest_tagged_version": "0.1.0",
                            "latest_tagged_date": "2026-03-23",
                            "has_unreleased_changes": True,
                        },
                        "file_digests": [],
                        "bundle_digest": "0" * 64,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
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
                    str(dest_root),
                    "--mode",
                    "copy",
                    "--format",
                    "json",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(0, completed.returncode)
            self.assertIn("bundle skill path escapes bundle root", completed.stderr)


if __name__ == "__main__":
    unittest.main()
