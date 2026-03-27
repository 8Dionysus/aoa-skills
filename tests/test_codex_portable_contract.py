import json
import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


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

    def test_validation_scripts_pass(self):
        commands = [
            [sys.executable, "scripts/build_runtime_seam.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/build_runtime_guardrails.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/build_description_trigger_evals.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/build_support_resources.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/validate_agent_skills.py", "--repo-root", "."],
            [sys.executable, "scripts/validate_support_resources.py", "--repo-root", ".", "--check-portable"],
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
