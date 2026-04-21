from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]


class AgonEpistemicSkillCandidateTests(unittest.TestCase):
    def test_generated_registry_shape(self) -> None:
        reg = json.loads(
            (ROOT / "generated/agon_epistemic_skill_candidates.min.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(reg["wave"], "XV")
        self.assertIn(reg["runtime_posture"], ("candidate_only", "pre_protocol_candidate_only"))
        self.assertEqual(reg["count"], 9)
        self.assertEqual(len(reg["skills"]), 9)
        for item in reg["skills"]:
            self.assertIs(item["live_protocol"], False)
            self.assertIn("auto_doctrine_rewrite", item.get("forbidden_effects", []))

    def test_builder_check_and_validator(self) -> None:
        self.assertEqual(
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/build_agon_epistemic_skill_candidates.py"),
                    "--check",
                ],
                cwd=ROOT,
            ).returncode,
            0,
        )
        self.assertEqual(
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/validate_agon_epistemic_skill_candidates.py"),
                ],
                cwd=ROOT,
            ).returncode,
            0,
        )

    def test_registry_schema_validates_without_ref_workaround(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/agon-epistemic-skill-candidate-registry.schema.json").read_text(
                encoding="utf-8"
            )
        )
        registry = json.loads(
            (ROOT / "generated/agon_epistemic_skill_candidates.min.json").read_text(
                encoding="utf-8"
            )
        )

        jsonschema.Draft202012Validator(schema).validate(registry)


if __name__ == "__main__":
    unittest.main()
