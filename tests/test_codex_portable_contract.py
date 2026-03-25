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

    def test_validation_scripts_pass(self):
        commands = [
            [sys.executable, "scripts/validate_agent_skills.py", "--repo-root", "."],
            [sys.executable, "scripts/lint_trigger_evals.py", "--repo-root", "."],
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
