from __future__ import annotations

from tests.support.build_catalog_case import *


class BuildCatalogCoreTests(BuildCatalogCase):
    def test_write_catalogs_generates_full_and_min_projection(self) -> None:
        repo_root = self.make_repo()

        full_path, min_path = build_catalog.write_catalogs(repo_root)

        full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
        min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
        self.assertEqual(1, full_catalog["catalog_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/**/SKILL.md",
                "technique_manifest": "skills/**/techniques.yaml",
            },
            full_catalog["source_of_truth"],
        )
        self.assertEqual(
            build_catalog.project_min_catalog(full_catalog),
            min_catalog,
        )
        self.assertEqual(
            "skills/aoa-test-skill/SKILL.md",
            min_catalog["skills"][0]["skill_path"],
        )
        self.assertEqual(
            "aoa-techniques",
            full_catalog["skills"][0]["technique_refs"][0]["repo"],
        )

    def test_write_capsules_generates_runtime_cards(self) -> None:
        repo_root = self.make_repo()

        capsule_path = build_catalog.write_capsules(repo_root)

        capsules = json.loads(capsule_path.read_text(encoding="utf-8"))
        self.assertEqual(1, capsules["capsule_version"])
        self.assertEqual(
            {
                "skill_markdown": "skills/**/SKILL.md",
                "frontmatter_fields": [
                    "name",
                    "scope",
                    "status",
                    "summary",
                    "invocation_mode",
                    "technique_dependencies",
                ],
                "sections": [
                    "Intent",
                    "Trigger boundary",
                    "Inputs",
                    "Outputs",
                    "Procedure",
                    "Risks and anti-patterns",
                    "Verification",
                ],
            },
            capsules["source_of_truth"],
        )
        self.assertEqual(
            {
                "name": "aoa-test-skill",
                "scope": "core",
                "status": "scaffold",
                "summary": "Test skill summary.",
                "trigger_boundary_short": "Use when needed; Avoid when not needed.",
                "inputs_short": "Needs: input.",
                "outputs_short": "Produces: output.",
                "workflow_short": "Purpose: Intent text. Flow: step.",
                "main_anti_patterns_short": "Avoid: risk.",
                "verification_short": "Checks: verify.",
                "invocation_mode": "explicit-preferred",
                "technique_dependencies": ["AOA-T-0001"],
                "skill_path": "skills/aoa-test-skill/SKILL.md",
            },
            capsules["skills"][0],
        )

    def test_bundle_index_includes_relationship_fields(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )

        build_catalog.write_bundle_index(repo_root)

        payload = self.load_bundle_index(repo_root)
        entry = payload["skills"][0]
        self.assertEqual(["repo-default"], entry["install_profiles"])
        self.assertEqual(
            [
                "portable_export",
                "runtime_seam",
                "runtime_guardrails",
                "description_trigger",
                "tiny_router",
            ],
            entry["artifact_group_coverage"],
        )
        self.assertEqual(
            [
                {
                    "id": "AOA-T-0001",
                    "repo": "aoa-techniques",
                    "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
                    "source_ref": "0123456789abcdef0123456789abcdef01234567",
                    "lineage_state": "published",
                }
            ],
            entry["technique_lineage"],
        )

    def test_bundle_index_hash_uses_repo_relative_file_order(self) -> None:
        repo_root = self.make_repo(policy_allow_implicit=False)
        skill_dir = repo_root / "skills" / "aoa-test-skill"
        file_paths = [
            skill_dir / "SKILL.md",
            skill_dir / "techniques.yaml",
            skill_dir / "agents" / "openai.yaml",
        ]

        digest = build_catalog.skill_bundle_surface.hash_files(repo_root, file_paths)
        file_by_relative_path = {
            build_catalog.skill_bundle_surface.relative_location(path, repo_root): path
            for path in file_paths
        }
        expected = hashlib.sha256()
        for relative_path in sorted(file_by_relative_path):
            path = file_by_relative_path[relative_path]
            normalized_text = (
                path.read_text(encoding="utf-8")
                .replace("\r\n", "\n")
                .replace("\r", "\n")
            )
            expected.update(relative_path.encode("utf-8"))
            expected.update(b"\0")
            expected.update(normalized_text.encode("utf-8"))
            expected.update(b"\0")

        self.assertEqual(expected.hexdigest(), digest)

    def test_bundle_index_support_resource_coverage_stays_targeted(self) -> None:
        repo_root = self.make_repo(
            status="evaluated",
            review_surfaces=("status-promotions",),
            include_evaluation_fixtures=True,
        )
        skill_name = "aoa-safe-infra-change"
        skill_dir = repo_root / "skills" / "aoa-test-skill"
        renamed_dir = repo_root / "skills" / skill_name
        skill_dir.rename(renamed_dir)
        skill_md = (renamed_dir / "SKILL.md").read_text(encoding="utf-8")
        (renamed_dir / "SKILL.md").write_text(
            skill_md.replace("aoa-test-skill", skill_name),
            encoding="utf-8",
        )
        manifest = yaml.safe_load(
            (renamed_dir / "techniques.yaml").read_text(encoding="utf-8")
        )
        manifest["skill_name"] = skill_name
        (renamed_dir / "techniques.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )
        (repo_root / "SKILL_INDEX.md").write_text(
            "# SKILL_INDEX\n\n| name | scope | status | summary |\n|---|---|---|---|\n"
            f"| {skill_name} | core | evaluated | Test summary. |\n",
            encoding="utf-8",
        )
        (repo_root / "config" / "skill_pack_profiles.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "profile": "codex-facing-wave-3",
                    "profiles": {
                        "repo-default": {
                            "description": "Test install profile.",
                            "scope": "repo",
                            "install_mode": "symlink-preferred",
                            "skills": [skill_name],
                        }
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        build_catalog.write_bundle_index(repo_root)

        payload = self.load_bundle_index(repo_root)
        entry = payload["skills"][0]
        self.assertIn("support_resources", entry["artifact_group_coverage"])

    def test_write_catalogs_rejects_invalid_routing_contract(self) -> None:
        repo_root = self.make_repo()
        manifest_path = repo_root / "skills" / "aoa-test-skill" / "techniques.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["techniques"][0]["repo"] = "aoa-evals"
        manifest["techniques"][0]["path"] = "../bad/path.md"
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "repo must resolve to 'aoa-techniques'",
        ):
            build_catalog.write_catalogs(repo_root)

    def test_write_capsules_rejects_missing_required_source_section(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "capsule source section 'Verification' is missing",
        ):
            build_catalog.write_capsules(repo_root)

    def test_write_capsules_ignores_indented_fake_heading(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "## Procedure\n\n1. step\n\n    ## Verification\n\n    - example only\n\n",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "capsule source section 'Verification' is missing",
        ):
            build_catalog.write_capsules(repo_root)

    def test_write_capsules_ignores_fenced_fake_heading(self) -> None:
        repo_root = self.make_repo()
        skill_md_path = repo_root / "skills" / "aoa-test-skill" / "SKILL.md"
        skill_md_path.write_text(
            skill_md_path.read_text(encoding="utf-8").replace(
                "## Verification\n\n- verify\n\n",
                "## Procedure\n\n1. step\n\n```md\n## Verification\n\n- example only\n```\n\n",
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ValueError,
            "capsule source section 'Verification' is missing",
        ):
            build_catalog.write_capsules(repo_root)


if __name__ == "__main__":
    unittest.main()
