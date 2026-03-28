from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
import sys

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import release_manifest_contract


class ReleaseManifestContractTests(unittest.TestCase):
    def make_tempdir(self) -> Path:
        tempdir = Path(tempfile.mkdtemp(prefix="aoa-release-manifest-"))
        self.addCleanup(shutil.rmtree, tempdir, True)
        return tempdir

    def test_parse_changelog_release_identity_reads_latest_tag_and_unreleased_state(self) -> None:
        changelog = """# Changelog

## [Unreleased]

### Added

- pending change

## [0.1.0] - 2026-03-23

### Summary

- first release
"""
        identity = release_manifest_contract.parse_changelog_release_identity(changelog)
        self.assertEqual(identity["latest_tagged_version"], "0.1.0")
        self.assertEqual(identity["latest_tagged_date"], "2026-03-23")
        self.assertTrue(identity["has_unreleased_changes"])

    def test_parse_changelog_release_identity_ignores_heading_only_unreleased(self) -> None:
        changelog = """# Changelog

## [Unreleased]

### Added

### Changed

## [0.1.0] - 2026-03-23

### Summary

- first release
"""
        identity = release_manifest_contract.parse_changelog_release_identity(changelog)
        self.assertFalse(identity["has_unreleased_changes"])

    def test_text_file_digest_normalization_is_newline_stable(self) -> None:
        repo_root = self.make_tempdir()
        rel_path = "sample.txt"
        path = repo_root / rel_path
        path.write_text("line1\r\nline2\r\n", encoding="utf-8", newline="")
        first = release_manifest_contract.file_digest_record(repo_root, rel_path, {})
        path.write_text("line1\nline2\n", encoding="utf-8", newline="\n")
        second = release_manifest_contract.file_digest_record(repo_root, rel_path, {})
        self.assertEqual(first["sha256"], second["sha256"])
        self.assertEqual(first["bytes"], second["bytes"])

    def test_profile_revision_changes_when_member_set_changes(self) -> None:
        resolved_profiles = {
            "profiles": {
                "repo-default": {
                    "skills": [
                        {"name": "aoa-a"},
                        {"name": "aoa-b"},
                    ]
                }
            }
        }
        bundle_revisions = [
            {"name": "aoa-a", "skill_revision": "aaaaaaaaaaaa", "content_hash": "a" * 64},
            {"name": "aoa-b", "skill_revision": "bbbbbbbbbbbb", "content_hash": "b" * 64},
            {"name": "aoa-c", "skill_revision": "cccccccccccc", "content_hash": "c" * 64},
        ]
        first = release_manifest_contract.build_install_profile_revisions(
            resolved_profiles,
            bundle_revisions,
        )[0]["profile_revision"]
        resolved_profiles["profiles"]["repo-default"]["skills"].append({"name": "aoa-c"})
        second = release_manifest_contract.build_install_profile_revisions(
            resolved_profiles,
            bundle_revisions,
        )[0]["profile_revision"]
        self.assertNotEqual(first, second)

    def test_profile_revision_changes_when_member_skill_revision_changes(self) -> None:
        resolved_profiles = {
            "profiles": {
                "repo-default": {
                    "skills": [
                        {"name": "aoa-a"},
                        {"name": "aoa-b"},
                    ]
                }
            }
        }
        first = release_manifest_contract.build_install_profile_revisions(
            resolved_profiles,
            [
                {"name": "aoa-a", "skill_revision": "aaaaaaaaaaaa", "content_hash": "a" * 64},
                {"name": "aoa-b", "skill_revision": "bbbbbbbbbbbb", "content_hash": "b" * 64},
            ],
        )[0]["profile_revision"]
        second = release_manifest_contract.build_install_profile_revisions(
            resolved_profiles,
            [
                {"name": "aoa-a", "skill_revision": "aaaaaaaaaaab", "content_hash": "a" * 64},
                {"name": "aoa-b", "skill_revision": "bbbbbbbbbbbb", "content_hash": "b" * 64},
            ],
        )[0]["profile_revision"]
        self.assertNotEqual(first, second)

    def test_profile_revision_is_stable_when_profile_skill_order_changes(self) -> None:
        resolved_profiles = {
            "profiles": {
                "repo-default": {
                    "skills": [
                        {"name": "aoa-b"},
                        {"name": "aoa-a"},
                    ]
                }
            }
        }
        bundle_revisions = [
            {"name": "aoa-a", "skill_revision": "aaaaaaaaaaaa", "content_hash": "a" * 64},
            {"name": "aoa-b", "skill_revision": "bbbbbbbbbbbb", "content_hash": "b" * 64},
        ]
        first = release_manifest_contract.build_install_profile_revisions(
            resolved_profiles,
            bundle_revisions,
        )[0]
        resolved_profiles["profiles"]["repo-default"]["skills"] = [
            {"name": "aoa-a"},
            {"name": "aoa-b"},
        ]
        second = release_manifest_contract.build_install_profile_revisions(
            resolved_profiles,
            bundle_revisions,
        )[0]
        self.assertEqual(first["profile_revision"], second["profile_revision"])
        self.assertEqual(["aoa-a", "aoa-b"], first["skill_names"])
        self.assertEqual(["aoa-a", "aoa-b"], second["skill_names"])


if __name__ == "__main__":
    unittest.main()
