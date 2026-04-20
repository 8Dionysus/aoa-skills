import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import release_manifest_contract


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: pathlib.Path):
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            items.append(json.loads(line))
    return items


class CodexPortableContractTests(unittest.TestCase):
    def test_local_adapter_manifest_matches_catalog(self):
        manifest = load_json(REPO_ROOT / "generated" / "local_adapter_manifest.json")
        catalog = load_json(REPO_ROOT / "generated" / "agent_skill_catalog.json")
        manifest_names = {entry["name"] for entry in manifest["skills"]}
        catalog_names = {entry["name"] for entry in catalog["skills"]}
        self.assertEqual(manifest_names, catalog_names)

    def test_runtime_contracts_match_catalog(self):
        handoff_doc = load_json(REPO_ROOT / "generated" / "skill_handoff_contracts.json")
        runtime_doc = load_json(REPO_ROOT / "generated" / "skill_runtime_contracts.json")
        trust_doc = load_json(REPO_ROOT / "generated" / "trust_policy_matrix.json")
        context_doc = load_json(REPO_ROOT / "generated" / "context_retention_manifest.json")
        guardrail_trust = load_json(REPO_ROOT / "generated" / "repo_trust_gate_manifest.json")
        guardrail_allowlist = load_json(REPO_ROOT / "generated" / "permission_allowlist_manifest.json")
        guardrail_context = load_json(REPO_ROOT / "generated" / "skill_context_guard_manifest.json")
        description_signals = load_json(REPO_ROOT / "generated" / "skill_description_signals.json")
        description_manifest = load_json(REPO_ROOT / "generated" / "description_trigger_eval_manifest.json")
        skills_ref_manifest = load_json(REPO_ROOT / "generated" / "skills_ref_validation_manifest.json")
        support_manifest = load_json(REPO_ROOT / "generated" / "deterministic_resource_manifest.json")
        support_index = load_json(REPO_ROOT / "generated" / "support_resource_index.json")
        support_bridge = load_json(REPO_ROOT / "generated" / "support_resource_bridge_map.json")
        expected_support = load_json(REPO_ROOT / "generated" / "expected_existing_aoa_support_dirs.json")
        tiny_router_signals = load_json(REPO_ROOT / "generated" / "tiny_router_skill_signals.json")
        tiny_router_capsules = load_json(REPO_ROOT / "generated" / "tiny_router_capsules.min.json")
        tiny_router_manifest = load_json(REPO_ROOT / "generated" / "tiny_router_overlay_manifest.json")
        catalog = load_json(REPO_ROOT / "generated" / "agent_skill_catalog.json")
        catalog_names = {entry["name"] for entry in catalog["skills"]}
        support_names = {"aoa-dry-run-first", "aoa-safe-infra-change", "aoa-local-stack-bringup"}
        self.assertEqual({entry["name"] for entry in handoff_doc["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in runtime_doc["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in trust_doc["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in context_doc["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in guardrail_trust["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in guardrail_allowlist["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in guardrail_context["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in description_signals["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in description_manifest["skills"]}, catalog_names)
        self.assertEqual({entry["skill_name"] for entry in skills_ref_manifest["targets"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in support_manifest["skills"]}, support_names)
        self.assertEqual({entry["name"] for entry in support_index["skills"]}, support_names)
        self.assertEqual(set(support_bridge["skills"]), support_names)
        self.assertEqual(set(expected_support["skills"]), support_names)
        self.assertEqual({entry["name"] for entry in tiny_router_signals["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in tiny_router_capsules["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in tiny_router_manifest["skills"]}, catalog_names)

    def test_support_resource_manifests_match_exported_resources(self):
        support_manifest = load_json(REPO_ROOT / "generated" / "deterministic_resource_manifest.json")
        support_bridge = load_json(REPO_ROOT / "generated" / "support_resource_bridge_map.json")
        support_index = load_json(REPO_ROOT / "generated" / "support_resource_index.json")
        catalog = load_json(REPO_ROOT / "generated" / "agent_skill_catalog.json")
        catalog_by_name = {entry["name"]: entry for entry in catalog["skills"]}

        for entry in support_manifest["skills"]:
            name = entry["name"]
            catalog_entry = catalog_by_name[name]
            bridge_entry = support_bridge["skills"][name]
            index_entry = next(item for item in support_index["skills"] if item["name"] == name)
            inventory = catalog_entry["resource_inventory"]

            for dirname in ("scripts", "references", "assets"):
                manifest_paths = [item["path"] for item in entry["standard_dirs"][dirname]]
                inventory_paths = [
                    path.removeprefix(f"{dirname}/")
                    for path in inventory.get(dirname, [])
                    if not path.endswith("small-logo.svg") and not path.endswith("large-logo.svg")
                ]
                self.assertTrue(set(manifest_paths).issubset(set(inventory_paths)))
                self.assertEqual(bridge_entry["standard_support_dirs"][dirname], manifest_paths)
                self.assertEqual(index_entry["standard_dir_counts"][dirname], len(manifest_paths))

    def test_handoff_contracts_expose_compact_packet_templates(self):
        handoff_doc = load_json(REPO_ROOT / "generated" / "skill_handoff_contracts.json")
        for entry in handoff_doc["skills"]:
            packet = entry["handoff_packet_template"]
            self.assertEqual(packet["from_skill"], entry["name"])
            self.assertIsInstance(packet["produced_artifacts"], list)
            self.assertIsInstance(packet["verification_notes"], list)
            self.assertIsInstance(packet["contract_notes"], list)

    def test_runtime_seam_indexes_match_catalog(self):
        catalog = load_json(REPO_ROOT / "generated" / "agent_skill_catalog.json")
        discovery = load_json(REPO_ROOT / "generated" / "runtime_discovery_index.json")
        discovery_min = load_json(REPO_ROOT / "generated" / "runtime_discovery_index.min.json")
        disclosure = load_json(REPO_ROOT / "generated" / "runtime_disclosure_index.json")
        router = load_json(REPO_ROOT / "generated" / "runtime_router_hints.json")
        aliases = load_json(REPO_ROOT / "generated" / "runtime_activation_aliases.json")
        catalog_names = {entry["name"] for entry in catalog["skills"]}

        self.assertEqual({entry["name"] for entry in discovery["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in discovery_min["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in disclosure["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in router["skills"]}, catalog_names)
        self.assertEqual({entry["name"] for entry in aliases["aliases"]}, catalog_names)

    def test_runtime_router_hints_keep_prompt_buckets_disjoint(self):
        router = load_json(REPO_ROOT / "generated" / "runtime_router_hints.json")
        for entry in router["skills"]:
            should_trigger = set(entry.get("should_trigger", []))
            manual_required = set(entry.get("manual_invocation_required", []))
            negative_controls = set(entry.get("negative_controls", []))
            self.assertFalse(should_trigger & manual_required, entry["name"])
            self.assertFalse(should_trigger & negative_controls, entry["name"])
            self.assertFalse(manual_required & negative_controls, entry["name"])

    def test_discovery_and_disclosure_do_not_expose_full_instructions(self):
        discovery = load_json(REPO_ROOT / "generated" / "runtime_discovery_index.json")
        disclosure = load_json(REPO_ROOT / "generated" / "runtime_disclosure_index.json")

        for entry in discovery["skills"]:
            self.assertNotIn("instructions_markdown", entry)
        for entry in disclosure["skills"]:
            self.assertNotIn("instructions_markdown", entry)

    def test_resolved_profiles_and_snippets_match(self):
        profiles = load_json(REPO_ROOT / "generated" / "skill_pack_profiles.resolved.json")
        snippets = load_json(REPO_ROOT / "generated" / "codex_config_snippets.json")
        self.assertEqual(set(profiles["profiles"]), set(snippets["snippets"]))

    def test_project_core_outer_ring_profiles_and_surfaces_stay_aligned(self):
        kernel = load_json(REPO_ROOT / "generated" / "project_core_skill_kernel.min.json")
        outer_ring = load_json(REPO_ROOT / "generated" / "project_core_outer_ring.min.json")
        readiness = load_json(REPO_ROOT / "generated" / "project_core_outer_ring_readiness.min.json")
        profiles = load_json(REPO_ROOT / "config" / "skill_pack_profiles.json")["profiles"]

        self.assertEqual("project-core-engineering-ring-v1", outer_ring["ring_id"])
        self.assertEqual("repo-project-core-outer-ring", outer_ring["canonical_install_profile"])
        self.assertEqual(kernel["kernel_id"], outer_ring["adjacent_kernel_id"])
        self.assertEqual(
            profiles["repo-project-core-outer-ring"]["skills"],
            outer_ring["skills"],
        )
        self.assertEqual(
            profiles["repo-core-only"]["skills"],
            [*kernel["skills"], *outer_ring["skills"]],
        )
        self.assertEqual(
            [entry["skill_name"] for entry in readiness["skills"]],
            outer_ring["skills"],
        )
        self.assertTrue(all(entry["readiness_passed"] for entry in readiness["skills"]))

    def test_project_foundation_profile_stays_aligned(self):
        kernel = load_json(REPO_ROOT / "generated" / "project_core_skill_kernel.min.json")
        outer_ring = load_json(REPO_ROOT / "generated" / "project_core_outer_ring.min.json")
        risk_ring = load_json(REPO_ROOT / "generated" / "project_risk_guard_ring.min.json")
        foundation = load_json(REPO_ROOT / "generated" / "project_foundation_profile.min.json")
        profiles = load_json(REPO_ROOT / "config" / "skill_pack_profiles.json")["profiles"]

        expected_skills = [*kernel["skills"], *outer_ring["skills"], *risk_ring["skills"]]
        self.assertEqual(foundation["foundation_id"], "project-foundation-v1")
        self.assertEqual(foundation["canonical_install_profile"], "repo-project-foundation")
        self.assertEqual(foundation["skills"], expected_skills)
        self.assertEqual(foundation["kernel_skills"], kernel["skills"])
        self.assertEqual(foundation["outer_ring_skills"], outer_ring["skills"])
        self.assertEqual(foundation["risk_ring_skills"], risk_ring["skills"])
        self.assertEqual(profiles["repo-project-foundation"]["skills"], expected_skills)

    def test_release_manifest_matches_current_packaging_contract(self):
        release_manifest = load_json(REPO_ROOT / "generated" / "release_manifest.json")
        expected_manifest = release_manifest_contract.build_release_manifest(REPO_ROOT)
        source_catalog = load_json(REPO_ROOT / "generated" / "skill_catalog.min.json")
        self.assertEqual(release_manifest, expected_manifest)

        for rel_path in release_manifest["generated_files"]:
            self.assertTrue((REPO_ROOT / rel_path).exists(), msg=rel_path)
        for rel_path in release_manifest["authoring_inputs"]:
            self.assertTrue((REPO_ROOT / rel_path).exists(), msg=rel_path)

        self.assertEqual(release_manifest["skill_count"], len(source_catalog["skills"]))
        self.assertEqual(
            release_manifest["explicit_only_count"],
            sum(1 for entry in source_catalog["skills"] if entry["invocation_mode"] == "explicit-only"),
        )
        self.assertEqual(
            release_manifest["profile_count"],
            len(release_manifest["install_profile_revisions"]),
        )
        self.assertEqual(release_manifest["release_identity"]["latest_tagged_version"], "0.3.2")
        self.assertTrue(release_manifest["release_identity"]["has_unreleased_changes"])
        self.assertEqual(
            release_manifest["relationship_views"],
            [
                "generated/skill_bundle_index.json",
                "generated/skill_bundle_index.md",
                "generated/skill_graph.json",
                "generated/skill_graph.md",
            ],
        )

        bundle_index = load_json(REPO_ROOT / "generated" / "skill_bundle_index.json")
        expected_bundle_revisions = [
            {
                "name": entry["name"],
                "skill_revision": entry["skill_revision"],
                "content_hash": entry["content_hash"],
            }
            for entry in sorted(bundle_index["skills"], key=lambda item: item["name"])
        ]
        self.assertEqual(release_manifest["skill_bundle_revisions"], expected_bundle_revisions)

        resolved_profiles = load_json(REPO_ROOT / "generated" / "skill_pack_profiles.resolved.json")
        expected_profile_revisions = release_manifest_contract.build_install_profile_revisions(
            resolved_profiles,
            expected_bundle_revisions,
        )
        self.assertEqual(
            release_manifest["install_profile_revisions"],
            expected_profile_revisions,
        )
        generated_digests = {
            entry["path"]: entry for entry in release_manifest["generated_file_digests"]
        }
        for rel_path in release_manifest["relationship_views"]:
            self.assertIn(rel_path, release_manifest["generated_files"])
            self.assertIn(rel_path, generated_digests)
            self.assertEqual(
                generated_digests[rel_path],
                release_manifest_contract.file_digest_record(REPO_ROOT, rel_path, {}),
            )

    def test_bundle_index_tracks_overlay_profiles_and_targeted_support_coverage(self):
        bundle_index = load_json(REPO_ROOT / "generated" / "skill_bundle_index.json")
        entries = {entry["name"]: entry for entry in bundle_index["skills"]}
        self.assertEqual(
            entries["atm10-change-protocol"]["install_profiles"],
            ["repo-atm10-overlay", "repo-default"],
        )
        self.assertEqual(
            entries["abyss-safe-infra-change"]["install_profiles"],
            ["repo-abyss-overlay", "repo-default"],
        )
        self.assertIn(
            "support_resources",
            entries["aoa-dry-run-first"]["artifact_group_coverage"],
        )
        self.assertNotIn(
            "support_resources",
            entries["aoa-adr-write"]["artifact_group_coverage"],
        )
        self.assertTrue(
            all(
                technique["lineage_state"] == "published"
                for technique in entries["aoa-safe-infra-change"]["technique_lineage"]
            )
        )

    def test_stage_skill_pack_dry_run_succeeds(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = pathlib.Path(tmpdir) / "repo-core-only.zip"
            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/stage_skill_pack.py",
                    "--repo-root",
                    ".",
                    "--profile",
                    "repo-core-only",
                    "--output-root",
                    str(pathlib.Path(tmpdir) / "bundle"),
                    "--archive-path",
                    str(archive_path),
                    "--format",
                    "json",
                ],
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
            self.assertEqual(str(archive_path.resolve()), payload["archive_path"])
            self.assertEqual("zip", payload["archive_format"])
            self.assertIn("--bundle-archive", payload["recommended_inspect_command"])
            self.assertIn("--bundle-archive", payload["recommended_install_command"])

    def test_build_agent_skills_refuses_to_delete_nonempty_external_output_root(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = pathlib.Path(tmpdir) / "portable-skills"
            output_root.mkdir()
            (output_root / "keep.txt").write_text("do not delete\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_agent_skills.py",
                    "--repo-root",
                    ".",
                    "--output-root",
                    str(output_root),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("refusing to delete existing external contents", completed.stderr)
            self.assertTrue((output_root / "keep.txt").exists())

    def test_explicit_only_skills_have_no_implicit_positive_cases(self):
        source_catalog = load_json(REPO_ROOT / "generated" / "skill_catalog.min.json")
        cases = load_jsonl(REPO_ROOT / "generated" / "skill_trigger_eval_cases.jsonl")
        explicit_only = {
            entry["name"] for entry in source_catalog["skills"] if entry["invocation_mode"] == "explicit-only"
        }
        offenders = []
        for case in cases:
            if (
                case["skill_name"] in explicit_only
                and case["mode"] == "implicit"
                and case["expected_behavior"] == "invoke-skill"
            ):
                offenders.append(case["case_id"])
        self.assertEqual(offenders, [])

    def test_description_trigger_suite_respects_explicit_only_policy(self):
        source_catalog = load_json(REPO_ROOT / "generated" / "skill_catalog.min.json")
        cases = load_jsonl(REPO_ROOT / "generated" / "description_trigger_eval_cases.jsonl")
        explicit_only = {
            entry["name"] for entry in source_catalog["skills"] if entry["invocation_mode"] == "explicit-only"
        }
        offenders = []
        for case in cases:
            if case["skill_name"] in explicit_only and case["case_class"] == "should-trigger":
                offenders.append(case["case_id"])
        self.assertEqual(offenders, [])

    def test_tiny_router_surfaces_respect_invocation_mode_and_overlay_scope(self):
        source_catalog = load_json(REPO_ROOT / "generated" / "skill_catalog.min.json")
        tiny_router_signals = load_json(REPO_ROOT / "generated" / "tiny_router_skill_signals.json")
        tiny_router_bands = load_json(REPO_ROOT / "generated" / "tiny_router_candidate_bands.json")
        source_by_name = {entry["name"]: entry for entry in source_catalog["skills"]}
        signal_by_name = {entry["name"]: entry for entry in tiny_router_signals["skills"]}

        for name, source in source_by_name.items():
            signal = signal_by_name[name]
            self.assertEqual(signal["manual_invocation_required"], source["invocation_mode"] == "explicit-only")
            self.assertEqual(signal["project_overlay"], source["scope"] == "project")

        band_skill_names = set()
        for band in tiny_router_bands["bands"]:
            band_skill_names.update(band["skills"])
        self.assertEqual(band_skill_names, set(source_by_name))

    def test_validation_scripts_pass(self):
        commands = [
            [sys.executable, "scripts/build_runtime_seam.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/build_runtime_guardrails.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/build_description_trigger_evals.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/build_support_resources.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/build_tiny_router_inputs.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/validate_agent_skills.py", "--repo-root", "."],
            [sys.executable, "scripts/verify_skill_pack.py", "--repo-root", ".", "--profile", "repo-default", "--format", "json"],
            [sys.executable, "scripts/validate_support_resources.py", "--repo-root", ".", "--check-portable"],
            [sys.executable, "scripts/validate_tiny_router_inputs.py", "--repo-root", "."],
            [sys.executable, "scripts/lint_trigger_evals.py", "--repo-root", "."],
            [sys.executable, "scripts/lint_description_trigger_evals.py", "--repo-root", "."],
            [sys.executable, "scripts/lint_pack_profiles.py", "--repo-root", "."],
            [sys.executable, "scripts/lint_support_resources.py", "--repo-root", "."],
            [sys.executable, "scripts/run_skills_ref_validation.py", "--repo-root", "."],
        ]
        for command in commands:
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
                msg=f"command failed: {' '.join(command)}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )


if __name__ == "__main__":
    unittest.main()
