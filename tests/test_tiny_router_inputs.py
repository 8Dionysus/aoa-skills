from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: pathlib.Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class TinyRouterInputsTest(unittest.TestCase):
    def test_build_and_validate_live_repo(self) -> None:
        commands = [
            [sys.executable, "scripts/build_tiny_router_inputs.py", "--repo-root", ".", "--check"],
            [sys.executable, "scripts/validate_tiny_router_inputs.py", "--repo-root", "."],
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

    def test_manifest_and_capsules_cover_all_skills(self) -> None:
        catalog = load_json(REPO_ROOT / "generated" / "skill_catalog.min.json")
        signals = load_json(REPO_ROOT / "generated" / "tiny_router_skill_signals.json")
        capsules = load_json(REPO_ROOT / "generated" / "tiny_router_capsules.min.json")
        manifest = load_json(REPO_ROOT / "generated" / "tiny_router_overlay_manifest.json")
        actual_names = {entry["name"] for entry in catalog["skills"]}
        self.assertEqual({entry["name"] for entry in signals["skills"]}, actual_names)
        self.assertEqual({entry["name"] for entry in capsules["skills"]}, actual_names)
        self.assertEqual({entry["name"] for entry in manifest["skills"]}, actual_names)
        self.assertEqual(manifest["skill_count"], len(actual_names))

    def test_explicit_only_skills_stay_manual_and_project_skills_stay_overlays(self) -> None:
        catalog = load_json(REPO_ROOT / "generated" / "skill_catalog.min.json")
        overlay_readiness = load_json(REPO_ROOT / "generated" / "overlay_readiness.json")
        signals = load_json(REPO_ROOT / "generated" / "tiny_router_skill_signals.json")
        eval_cases = load_jsonl(REPO_ROOT / "generated" / "tiny_router_eval_cases.jsonl")
        catalog_by_name = {entry["name"]: entry for entry in catalog["skills"]}

        for entry in signals["skills"]:
            source = catalog_by_name[entry["name"]]
            self.assertEqual(entry["manual_invocation_required"], source["invocation_mode"] == "explicit-only")
            self.assertEqual(entry["project_overlay"], source["scope"] == "project")

        overlay_cases = [case for case in eval_cases if case.get("repo_family_hint")]
        self.assertTrue(overlay_cases)
        live_families = {
            entry["family"]: entry["project_skill_names"]
            for entry in overlay_readiness["families"]
        }
        self.assertEqual(set(live_families), {case["repo_family_hint"] for case in overlay_cases})
        for family, skill_names in live_families.items():
            family_cases = [
                case for case in overlay_cases if case.get("repo_family_hint") == family
            ]
            self.assertTrue(family_cases, msg=f"missing tiny-router cases for family '{family}'")
            for skill_name in skill_names:
                self.assertTrue(
                    any(
                        skill_name in case.get("expected_shortlist_includes", [])
                        for case in family_cases
                    ),
                    msg=f"missing family-hinted shortlist coverage for '{skill_name}'",
                )

    def test_defer_cases_use_expected_skill_band(self) -> None:
        signals = load_json(REPO_ROOT / "generated" / "tiny_router_skill_signals.json")
        eval_cases = load_jsonl(REPO_ROOT / "generated" / "tiny_router_eval_cases.jsonl")
        band_by_skill = {entry["name"]: entry["band"] for entry in signals["skills"]}

        defer_cases = [
            case for case in eval_cases if str(case.get("case_id", "")).startswith("tiny-defer-")
        ]
        self.assertTrue(defer_cases)
        for case in defer_cases:
            includes = case.get("expected_shortlist_includes", [])
            if includes:
                expected_skill = includes[0]
                self.assertEqual(case["expected_band"], band_by_skill[expected_skill])

    def test_defer_cases_only_require_shortlist_hits_within_same_band_and_overlay_targets_carry_family_hints(self) -> None:
        signals = load_json(REPO_ROOT / "generated" / "tiny_router_skill_signals.json")
        eval_cases = load_jsonl(REPO_ROOT / "generated" / "tiny_router_eval_cases.jsonl")
        signal_by_name = {entry["name"]: entry for entry in signals["skills"]}

        defer_cases = [
            case for case in eval_cases if str(case.get("case_id", "")).startswith("tiny-defer-")
        ]
        self.assertTrue(defer_cases)
        for case in defer_cases:
            source_skill = case["case_id"][len("tiny-defer-") :]
            source_band = signal_by_name[source_skill]["band"]
            includes = case.get("expected_shortlist_includes", [])
            if case["expected_band"] == source_band:
                self.assertTrue(
                    includes,
                    msg=f"same-band defer case should require a shortlist include: {case['case_id']}",
                )
            else:
                self.assertEqual(
                    includes,
                    [],
                    msg=f"cross-band defer case should not require a shortlist include: {case['case_id']}",
                )
            for skill_name in includes:
                if signal_by_name[skill_name]["project_overlay"]:
                    self.assertTrue(
                        case.get("repo_family_hint"),
                        msg=f"overlay defer target must carry repo_family_hint: {case['case_id']}",
                    )

    def test_validator_rejects_cross_band_overlay_defer_case_without_repo_family_hint(self) -> None:
        required_files = [
            "config/tiny_router_skill_bands.json",
            "generated/skill_catalog.min.json",
            "generated/skill_description_signals.json",
            "generated/description_trigger_eval_cases.jsonl",
            "generated/tiny_router_skill_signals.json",
            "generated/tiny_router_candidate_bands.json",
            "generated/tiny_router_capsules.min.json",
            "generated/tiny_router_eval_cases.jsonl",
            "generated/tiny_router_overlay_manifest.json",
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = pathlib.Path(tmpdir)
            for relative_path in required_files:
                source_path = REPO_ROOT / relative_path
                target_path = repo_root / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, target_path)

            eval_cases_path = repo_root / "generated" / "tiny_router_eval_cases.jsonl"
            eval_cases = load_jsonl(eval_cases_path)
            target_case = next(
                case
                for case in eval_cases
                if case["case_id"] == "tiny-defer-aoa-source-of-truth-check"
            )
            target_case["expected_band"] = "change-validation"
            target_case["expected_shortlist_includes"] = []
            target_case["repo_family_hint"] = None
            eval_cases_path.write_text(
                "\n".join(json.dumps(case) for case in eval_cases) + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [sys.executable, "scripts/validate_tiny_router_inputs.py", "--repo-root", str(repo_root)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 2, msg=completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertIn(
            "tiny-defer-aoa-source-of-truth-check: cross-band overlay defer targets must set repo_family_hint",
            payload["errors"],
        )


if __name__ == "__main__":
    unittest.main()
