import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


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
    def test_verify_script_imports_without_site_packages(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-S",
                "-c",
                (
                    "import pathlib, sys; "
                    f"sys.path.insert(0, r'{(REPO_ROOT / 'scripts').as_posix()}'); "
                    "import verify_skill_pack; "
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

    def stage_profile_bundle(
        self,
        profile: str,
        bundle_root: pathlib.Path,
        *,
        archive_path: pathlib.Path | None = None,
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
            "--execute",
            "--overwrite",
            "--format",
            "json",
        ]
        if archive_path is not None:
            command.extend(["--archive-path", str(archive_path)])
        completed = run_command(command)
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"stage failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )

    def install_profile_copy(
        self,
        profile: str,
        dest_root: pathlib.Path,
        *,
        bundle_root: pathlib.Path | None = None,
        bundle_archive: pathlib.Path | None = None,
    ) -> None:
        command = [
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
        if bundle_root is not None:
            command.extend(["--bundle-root", str(bundle_root)])
        if bundle_archive is not None:
            command.extend(["--bundle-archive", str(bundle_archive)])
        completed = run_command(command)
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
        bundle_root: pathlib.Path | None = None,
        bundle_archive: pathlib.Path | None = None,
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
        if bundle_root is not None:
            command.extend(["--bundle-root", str(bundle_root)])
        if bundle_archive is not None:
            command.extend(["--bundle-archive", str(bundle_archive)])
        if strict_root:
            command.append("--strict-root")
        completed = run_command(command)
        payload = json.loads(completed.stdout)
        return completed, payload

    def verify_profile_failure(
        self,
        profile: str,
        *,
        install_root: pathlib.Path | None = None,
        bundle_root: pathlib.Path | None = None,
        bundle_archive: pathlib.Path | None = None,
        strict_root: bool = False,
    ) -> subprocess.CompletedProcess[str]:
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
        if bundle_root is not None:
            command.extend(["--bundle-root", str(bundle_root)])
        if bundle_archive is not None:
            command.extend(["--bundle-archive", str(bundle_archive)])
        if strict_root:
            command.append("--strict-root")
        return run_command(command)

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

    def test_staged_bundle_verifies_offline(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            self.install_profile_copy("repo-core-only", dest_root)

            completed, payload = self.verify_profile(
                "repo-core-only",
                install_root=dest_root,
                bundle_root=bundle_root,
            )

            self.assertEqual(
                completed.returncode,
                0,
                msg=f"verify failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            self.assertTrue(payload["verified"])
            self.assertEqual("staged_bundle", payload["source_kind"])
            self.assertEqual(str(bundle_root.resolve()), payload["bundle_root"])

    def test_staged_archive_verifies_offline(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            archive_path = pathlib.Path(tmpdir) / "repo-core-only.zip"
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.stage_profile_bundle(
                "repo-core-only",
                bundle_root,
                archive_path=archive_path,
            )
            self.install_profile_copy(
                "repo-core-only",
                dest_root,
                bundle_archive=archive_path,
            )

            completed, payload = self.verify_profile(
                "repo-core-only",
                install_root=dest_root,
                bundle_archive=archive_path,
            )

            self.assertEqual(
                completed.returncode,
                0,
                msg=f"verify failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            self.assertTrue(payload["verified"])
            self.assertEqual("staged_archive", payload["source_kind"])
            self.assertIsNone(payload["bundle_root"])
            self.assertEqual(str(archive_path.resolve()), payload["bundle_archive"])

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

    def test_deleted_staged_bundle_file_fails_bundle_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            self.install_profile_copy("repo-core-only", dest_root)
            (bundle_root / ".agents" / "skills" / "aoa-change-protocol" / "SKILL.md").unlink()

            completed, payload = self.verify_profile(
                "repo-core-only",
                install_root=dest_root,
                bundle_root=bundle_root,
            )

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("aoa-change-protocol", payload["mismatched_skills"])

    def test_modified_installed_file_fails_staged_bundle_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            dest_root = pathlib.Path(tmpdir) / "skills"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            self.install_profile_copy("repo-core-only", dest_root)
            skill_md_path = dest_root / "aoa-change-protocol" / "SKILL.md"
            skill_md_path.write_text(
                skill_md_path.read_text(encoding="utf-8") + "\n# drift\n",
                encoding="utf-8",
            )

            completed, payload = self.verify_profile(
                "repo-core-only",
                install_root=dest_root,
                bundle_root=bundle_root,
            )

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("aoa-change-protocol", payload["mismatched_skills"])

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

    def test_corrupted_archive_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = pathlib.Path(tmpdir) / "corrupted.zip"
            archive_path.write_text("not a zip", encoding="utf-8")

            completed = self.verify_profile_failure(
                "repo-core-only",
                bundle_archive=archive_path,
            )

            self.assertNotEqual(0, completed.returncode)
            self.assertIn("invalid bundle archive", completed.stderr)

    def test_archive_missing_bundle_manifest_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = pathlib.Path(tmpdir) / "missing-manifest.zip"
            with zipfile.ZipFile(archive_path, mode="w") as archive:
                archive.writestr(
                    "aoa-skills-repo-core-only/.agents/skills/aoa-change-protocol/SKILL.md",
                    "# placeholder\n",
                )

            completed = self.verify_profile_failure(
                "repo-core-only",
                bundle_archive=archive_path,
            )

            self.assertNotEqual(0, completed.returncode)
            self.assertIn("missing bundle_manifest.json", completed.stderr)

    def test_archive_with_multiple_bundle_roots_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = pathlib.Path(tmpdir) / "multiple-roots.zip"
            with zipfile.ZipFile(archive_path, mode="w") as archive:
                archive.writestr(
                    "aoa-skills-repo-core-only-a/bundle_manifest.json",
                    "{}\n",
                )
                archive.writestr(
                    "aoa-skills-repo-core-only-b/bundle_manifest.json",
                    "{}\n",
                )

            completed = self.verify_profile_failure(
                "repo-core-only",
                bundle_archive=archive_path,
            )

            self.assertNotEqual(0, completed.returncode)
            self.assertIn("exactly one top-level root", completed.stderr)


if __name__ == "__main__":
    unittest.main()
