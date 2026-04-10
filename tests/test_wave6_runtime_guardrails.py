import json
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Wave6RuntimeGuardrailsTests(unittest.TestCase):
    def test_trust_gate_allowlist_and_rehydration_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = pathlib.Path(tmpdir)
            trust_store = tmpdir_path / "repo-trust-store.json"
            session_file = tmpdir_path / "skill-runtime-session.json"

            discover_blocked = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_guardrails.py",
                    "discover",
                    "--repo-root",
                    ".",
                    "--trust-store",
                    str(trust_store),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(discover_blocked.returncode, 0, msg=discover_blocked.stderr)
            discover_blocked_payload = json.loads(discover_blocked.stdout)
            self.assertEqual(discover_blocked_payload["stage"], "discover")
            self.assertEqual(discover_blocked_payload["count"], 0)
            self.assertGreaterEqual(discover_blocked_payload["blocked_count"], 17)
            self.assertFalse(discover_blocked_payload["trust_status"]["repo_trusted"])

            blocked_activate = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_guardrails.py",
                    "activate",
                    "--repo-root",
                    ".",
                    "--skill-name",
                    "aoa-change-protocol",
                    "--session-file",
                    str(session_file),
                    "--trust-store",
                    str(trust_store),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(blocked_activate.returncode, 0, msg=blocked_activate.stderr)
            blocked_activate_payload = json.loads(blocked_activate.stdout)
            self.assertEqual(blocked_activate_payload["stage"], "activate_blocked")

            trust = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_guardrails.py",
                    "trust",
                    "--repo-root",
                    ".",
                    "--trust-store",
                    str(trust_store),
                    "--decision",
                    "trusted",
                    "--reason",
                    "reviewed repo-local skills",
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(trust.returncode, 0, msg=trust.stderr)
            trust_payload = json.loads(trust.stdout)
            self.assertTrue(trust_payload["trust_status"]["repo_trusted"])

            discover_allowed = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_guardrails.py",
                    "discover",
                    "--repo-root",
                    ".",
                    "--trust-store",
                    str(trust_store),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(discover_allowed.returncode, 0, msg=discover_allowed.stderr)
            discover_allowed_payload = json.loads(discover_allowed.stdout)
            self.assertGreaterEqual(discover_allowed_payload["count"], 17)
            self.assertEqual(discover_allowed_payload["blocked_count"], 0)

            activate = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_guardrails.py",
                    "activate",
                    "--repo-root",
                    ".",
                    "--skill-name",
                    "aoa-change-protocol",
                    "--session-file",
                    str(session_file),
                    "--explicit-handle",
                    "$aoa-change-protocol",
                    "--trust-store",
                    str(trust_store),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(activate.returncode, 0, msg=activate.stderr)
            activate_payload = json.loads(activate.stdout)
            self.assertEqual(activate_payload["stage"], "activate")
            self.assertTrue(activate_payload["trust_status"]["repo_trusted"])
            self.assertEqual(activate_payload["skill"]["source_scope"], "repo")
            self.assertIn("instruction_sha256", activate_payload["activation"])
            active_record = activate_payload["session"]["active_skills"][0]
            self.assertIn("instruction_sha256", active_record)
            self.assertIn("dedupe_key", active_record)
            self.assertGreaterEqual(len(active_record["resolved_allowlist_paths"]), 1)

            allowlist = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_guardrails.py",
                    "allowlist",
                    "--repo-root",
                    ".",
                    "--session-file",
                    str(session_file),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(allowlist.returncode, 0, msg=allowlist.stderr)
            allowlist_payload = json.loads(allowlist.stdout)
            self.assertEqual(allowlist_payload["stage"], "allowlist")
            self.assertEqual(allowlist_payload["read_access"], "read-only")
            self.assertTrue(any(path.endswith(".agents/skills/aoa-change-protocol") for path in allowlist_payload["paths"]))

            compact = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_guardrails.py",
                    "compact",
                    "--repo-root",
                    ".",
                    "--session-file",
                    str(session_file),
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(compact.returncode, 0, msg=compact.stderr)
            compact_payload = json.loads(compact.stdout)
            packet = compact_payload["active_skill_packets"][0]
            self.assertIn("instruction_sha256", packet)
            self.assertIn("dedupe_key", packet)
            self.assertTrue(packet["resolved_allowlist_paths"])

            rehydrate = run_command(
                [
                    sys.executable,
                    "scripts/skill_runtime_guardrails.py",
                    "rehydrate",
                    "--repo-root",
                    ".",
                    "--session-file",
                    str(session_file),
                    "--include-activation-call",
                    "--format",
                    "json",
                ]
            )
            self.assertEqual(rehydrate.returncode, 0, msg=rehydrate.stderr)
            rehydrate_payload = json.loads(rehydrate.stdout)
            self.assertEqual(rehydrate_payload["stage"], "rehydrate")
            self.assertEqual(rehydrate_payload["skill_packets"][0]["name"], "aoa-change-protocol")
            self.assertIn("dedupe_key", rehydrate_payload["skill_packets"][0])
            self.assertEqual(rehydrate_payload["activation_calls"][0]["name"], "guarded_activate_skill")

    def test_repo_root_only_match_does_not_override_git_origin_identity(self):
        module = load_module("skill_runtime_guardrails", REPO_ROOT / "scripts" / "skill_runtime_guardrails.py")
        store = {
            "entries": [
                {
                    "repo_root": "/tmp/worktree",
                    "git_origin_url": "https://example.com/other.git",
                    "decision": "trusted",
                },
                {
                    "git_origin_url": "https://example.com/right.git",
                    "decision": "trusted",
                },
            ]
        }
        identity = {
            "repo_root": "/tmp/worktree",
            "repo_id": "missing",
            "git_origin_url": "https://example.com/right.git",
        }

        match = module.find_matching_trust_entry(store, identity)

        self.assertEqual(match["git_origin_url"], "https://example.com/right.git")


if __name__ == "__main__":
    unittest.main()
