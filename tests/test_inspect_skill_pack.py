import hashlib
import json
import pathlib
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


class InspectSkillPackTests(unittest.TestCase):
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

    def inspect_bundle(
        self,
        *,
        bundle_root: pathlib.Path | None = None,
        bundle_archive: pathlib.Path | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        command = [
            sys.executable,
            "scripts/inspect_skill_pack.py",
            "--format",
            "json",
        ]
        if bundle_root is not None:
            command.extend(["--bundle-root", str(bundle_root)])
        if bundle_archive is not None:
            command.extend(["--bundle-archive", str(bundle_archive)])
        completed = run_command(command)
        payload = json.loads(completed.stdout)
        return completed, payload

    def inspect_bundle_failure(
        self,
        *,
        bundle_root: pathlib.Path | None = None,
        bundle_archive: pathlib.Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            "scripts/inspect_skill_pack.py",
            "--format",
            "json",
        ]
        if bundle_root is not None:
            command.extend(["--bundle-root", str(bundle_root)])
        if bundle_archive is not None:
            command.extend(["--bundle-archive", str(bundle_archive)])
        return run_command(command)

    def test_inspect_staged_bundle_directory_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            self.stage_profile_bundle("repo-core-only", bundle_root)

            completed, payload = self.inspect_bundle(bundle_root=bundle_root)

            self.assertEqual(0, completed.returncode, msg=completed.stderr)
            self.assertTrue(payload["verified"])
            self.assertEqual("staged_bundle", payload["source_kind"])
            self.assertEqual(str(bundle_root.resolve()), payload["bundle_root"])
            self.assertIsNone(payload["bundle_archive"])
            self.assertTrue(payload["bundle_digest_matches_manifest"])

    def test_inspect_staged_archive_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            archive_path = pathlib.Path(tmpdir) / "repo-core-only.zip"
            self.stage_profile_bundle(
                "repo-core-only",
                bundle_root,
                archive_path=archive_path,
            )

            completed, payload = self.inspect_bundle(bundle_archive=archive_path)

            self.assertEqual(0, completed.returncode, msg=completed.stderr)
            self.assertTrue(payload["verified"])
            self.assertEqual("staged_archive", payload["source_kind"])
            self.assertIsNone(payload["bundle_root"])
            self.assertEqual(str(archive_path.resolve()), payload["bundle_archive"])
            self.assertRegex(payload["archive_sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(payload["archive_bytes"], 0)

    def test_deleted_staged_file_fails_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            (bundle_root / ".agents" / "skills" / "aoa-change-protocol" / "SKILL.md").unlink()

            completed, payload = self.inspect_bundle(bundle_root=bundle_root)

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn(".agents/skills/aoa-change-protocol/SKILL.md", payload["missing_files"])
            self.assertFalse(payload["bundle_digest_matches_manifest"])

    def test_extra_staged_file_fails_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            (bundle_root / "extra.txt").write_text("drift\n", encoding="utf-8")

            completed, payload = self.inspect_bundle(bundle_root=bundle_root)

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("extra.txt", payload["extra_files"])
            self.assertFalse(payload["bundle_digest_matches_manifest"])

    def test_mutated_staged_file_fails_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            skill_md_path = bundle_root / ".agents" / "skills" / "aoa-change-protocol" / "SKILL.md"
            skill_md_path.write_text(
                skill_md_path.read_text(encoding="utf-8") + "\n# drift\n",
                encoding="utf-8",
            )

            completed, payload = self.inspect_bundle(bundle_root=bundle_root)

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn(".agents/skills/aoa-change-protocol/SKILL.md", payload["mismatched_files"])
            self.assertFalse(payload["bundle_digest_matches_manifest"])

    def test_deleted_bundle_readme_fails_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            (bundle_root / "README.md").unlink()

            completed, payload = self.inspect_bundle(bundle_root=bundle_root)

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("README.md", payload["missing_files"])
            self.assertFalse(payload["bundle_digest_matches_manifest"])

    def test_mutated_bundle_readme_fails_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_root = pathlib.Path(tmpdir) / "bundle"
            self.stage_profile_bundle("repo-core-only", bundle_root)
            readme_path = bundle_root / "README.md"
            readme_path.write_text(
                readme_path.read_text(encoding="utf-8") + "\nDrift.\n",
                encoding="utf-8",
            )

            completed, payload = self.inspect_bundle(bundle_root=bundle_root)

            self.assertEqual(1, completed.returncode)
            self.assertFalse(payload["verified"])
            self.assertIn("README.md", payload["mismatched_files"])
            self.assertFalse(payload["bundle_digest_matches_manifest"])

    def test_archive_missing_bundle_manifest_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = pathlib.Path(tmpdir) / "missing-manifest.zip"
            with zipfile.ZipFile(archive_path, mode="w") as archive:
                archive.writestr(
                    "aoa-skills-repo-core-only/.agents/skills/aoa-change-protocol/SKILL.md",
                    "# placeholder\n",
                )

            completed = self.inspect_bundle_failure(bundle_archive=archive_path)

            self.assertNotEqual(0, completed.returncode)
            self.assertIn("missing bundle_manifest.json", completed.stderr)

    def test_corrupted_archive_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = pathlib.Path(tmpdir) / "corrupted.zip"
            archive_path.write_text("not a zip", encoding="utf-8")

            completed = self.inspect_bundle_failure(bundle_archive=archive_path)

            self.assertNotEqual(0, completed.returncode)
            self.assertIn("invalid bundle archive", completed.stderr)

    def test_archive_with_multiple_candidate_roots_fails_cleanly(self) -> None:
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

            completed = self.inspect_bundle_failure(bundle_archive=archive_path)

            self.assertNotEqual(0, completed.returncode)
            self.assertIn("exactly one top-level root", completed.stderr)

    def test_archive_with_wrong_top_level_root_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = pathlib.Path(tmpdir) / "wrong-root.zip"
            skill_payload = b"# placeholder\n"
            with zipfile.ZipFile(archive_path, mode="w") as archive:
                archive.writestr(
                    "wrong-root/bundle_manifest.json",
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
                                    "relative_dir": ".agents/skills/aoa-change-protocol",
                                    "skill_revision": "0" * 64,
                                    "content_hash": "0" * 64,
                                }
                            ],
                            "release_identity": {
                                "changelog": "CHANGELOG.md",
                                "releasing_doc": "docs/RELEASING.md",
                            },
                            "file_digests": [
                                {
                                    "path": ".agents/skills/aoa-change-protocol/SKILL.md",
                                    "sha256": hashlib.sha256(skill_payload).hexdigest(),
                                    "bytes": len(skill_payload),
                                }
                            ],
                            "bundle_digest": hashlib.sha256(
                                b".agents/skills/aoa-change-protocol/SKILL.md"
                                + b"\0"
                                + skill_payload
                                + b"\0"
                            ).hexdigest(),
                        }
                    )
                    + "\n",
                )
                archive.writestr(
                    "wrong-root/.agents/skills/aoa-change-protocol/SKILL.md",
                    skill_payload,
                )

            completed = self.inspect_bundle_failure(bundle_archive=archive_path)

            self.assertNotEqual(0, completed.returncode)
            self.assertIn("bundle archive root must be aoa-skills-repo-core-only", completed.stderr)


if __name__ == "__main__":
    unittest.main()
