import json
import pathlib
import subprocess
import sys
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class Wave6RuntimeGuardrailsBuilderTests(unittest.TestCase):
    def test_guardrail_builder_has_no_drift(self):
        completed = subprocess.run(
            [sys.executable, "scripts/build_runtime_guardrails.py", "--repo-root", ".", "--check"],
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

    def test_generated_guardrail_artifacts_exist(self):
        trust_gate = json.loads((REPO_ROOT / "generated" / "repo_trust_gate_manifest.json").read_text())
        allowlist = json.loads((REPO_ROOT / "generated" / "permission_allowlist_manifest.json").read_text())
        context_guard = json.loads((REPO_ROOT / "generated" / "skill_context_guard_manifest.json").read_text())
        tool_schemas = json.loads((REPO_ROOT / "generated" / "runtime_guardrail_tool_schemas.json").read_text())

        self.assertEqual(trust_gate["profile"], "codex-facing-wave-6-runtime-guardrails")
        self.assertGreaterEqual(len(trust_gate["skills"]), 17)
        self.assertGreaterEqual(len(allowlist["skills"]), 17)
        self.assertGreaterEqual(len(context_guard["skills"]), 17)
        tool_names = {tool["name"] for tool in tool_schemas["tools"]}
        self.assertIn("repo_trust_gate", tool_names)
        self.assertIn("guarded_activate_skill", tool_names)
        self.assertIn("rehydrate_skill_context", tool_names)


if __name__ == "__main__":
    unittest.main()
