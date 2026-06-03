from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from skill_model import skill_intelligence_surface
from tests.support.source_catalog import source_skill_count


class SkillIntelligenceSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = (
            skill_intelligence_surface.build_skill_intelligence_registry_payload(
                REPO_ROOT
            )
        )
        cls.skills = {entry["name"]: entry for entry in cls.payload["skills"]}

    def test_registry_covers_every_source_skill(self) -> None:
        self.assertEqual(len(self.payload["skills"]), source_skill_count(REPO_ROOT))
        self.assertEqual(
            self.payload["profile"],
            "skill-intelligence-registry-v1",
        )

    def test_source_policy_resource_and_graph_refs_are_present(self) -> None:
        skill = self.skills["aoa-source-of-truth-check"]
        self.assertTrue(skill["source"]["skill_path"].endswith("SKILL.md"))
        self.assertTrue(skill["source"]["techniques_path"].endswith("techniques.yaml"))
        self.assertRegex(skill["source"]["content_hash"], r"^[0-9a-f]{64}$")
        self.assertIn(
            skill["policy"]["implicit_activation_policy"],
            {"invoke", "suggest", "manual"},
        )
        self.assertIn("bundle_support_artifacts", skill["resources"])
        self.assertIn("node_id", skill["graph_refs"])
        self.assertGreater(skill["graph_refs"]["outgoing_edge_count"], 0)

    def test_search_documents_point_back_to_source_sections(self) -> None:
        skill = self.skills["aoa-change-protocol"]
        section_roles = {doc["section_role"] for doc in skill["search_documents"]}
        self.assertIn("trigger_boundary", section_roles)
        self.assertIn("verification", section_roles)
        for doc in skill["search_documents"]:
            self.assertEqual(doc["skill_name"], "aoa-change-protocol")
            self.assertTrue(doc["source_path"].endswith("SKILL.md"))
            self.assertRegex(doc["text_sha256"], r"^[0-9a-f]{64}$")

    def test_manual_policy_never_classifies_as_invoke(self) -> None:
        manual_skills = [
            entry
            for entry in self.payload["skills"]
            if entry["policy"]["implicit_activation_policy"] == "manual"
        ]
        self.assertTrue(manual_skills)
        for skill in manual_skills:
            self.assertEqual(
                skill_intelligence_surface.activation_class(skill),
                "manual",
            )
            self.assertTrue(skill["policy"]["requires_manual_invocation"])

    def test_sqlite_search_returns_policy_aware_candidates(self) -> None:
        results = skill_intelligence_surface.sqlite_search(
            self.payload,
            "source truth docs conflict canonical guidance",
            limit=5,
        )
        names = [result["name"] for result in results]
        self.assertIn("aoa-source-of-truth-check", names)
        for result in results:
            self.assertIn(
                result["candidate_class"],
                {"invoke", "suggest", "manual"},
            )

    def test_explain_candidate_includes_boundaries_and_load_refs(self) -> None:
        explanation = skill_intelligence_surface.explain_candidate(
            self.payload,
            "aoa-source-of-truth-check",
            intent="docs conflict over authoritative source",
        )
        self.assertEqual(explanation["candidate"], "aoa-source-of-truth-check")
        self.assertIn("policy", explanation)
        self.assertIn("negative_or_boundary_evidence", explanation)
        self.assertTrue(explanation["next_load_refs"][0].endswith("SKILL.md"))

    def test_generated_files_are_deterministic(self) -> None:
        generated_texts = skill_intelligence_surface.build_skill_intelligence_texts(
            REPO_ROOT
        )
        for rel_path, expected_text in generated_texts.items():
            with self.subTest(path=rel_path.as_posix()):
                self.assertEqual(
                    (REPO_ROOT / rel_path).read_text(encoding="utf-8"),
                    expected_text,
                )

    def test_min_payload_omits_full_search_text(self) -> None:
        min_payload = skill_intelligence_surface.build_min_payload(self.payload)
        first_doc = min_payload["skills"][0]["search_document_refs"][0]
        self.assertNotIn("text", first_doc)
        json.dumps(min_payload)

    def test_fallback_trust_uses_policy_matrix_when_generated_trust_is_absent(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            skill_dir = (
                repo_root / "skills" / "core" / "engineering" / "aoa-test-policy"
            )
            skill_dir.mkdir(parents=True)
            (repo_root / "config").mkdir()
            (skill_dir / "SKILL.md").write_text(
                """---
name: aoa-test-policy
scope: core
status: canonical
summary: Tests policy fallback.
invocation_mode: explicit-preferred
---

# aoa-test-policy

## Intent

Check policy matrix fallback.

## Trigger boundary

Use when generated trust is absent.

## Inputs

- policy matrix

## Outputs

- source-derived policy

## Procedure

1. read the policy matrix.

## Contracts

- generated trust absence must not erase policy.

## Risks and anti-patterns

- treating explicit-preferred as hidden invocation without policy.

## Verification

- inspect the emitted policy.
""",
                encoding="utf-8",
            )
            (skill_dir / "techniques.yaml").write_text(
                "techniques: []\n", encoding="utf-8"
            )
            (repo_root / "config" / "skill_policy_matrix.json").write_text(
                json.dumps(
                    {
                        "skills": {
                            "aoa-test-policy": {
                                "trust_posture": "portable-core",
                                "mutation_surface": "repo",
                                "implicit_activation_policy": "invoke",
                                "requires_confirmation_seam": False,
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            payload = (
                skill_intelligence_surface.build_skill_intelligence_registry_payload(
                    repo_root
                )
            )

        skill = payload["skills"][0]
        self.assertEqual(skill["policy"]["implicit_activation_policy"], "invoke")
        self.assertEqual(skill["policy"]["trust_posture"], "portable-core")
        self.assertEqual(skill["policy"]["mutation_surface"], "repo")
        self.assertFalse(skill["policy"]["candidate_only"])
        self.assertTrue(skill["runtime"]["allow_implicit_invocation"])

    def test_fallback_trust_keeps_explicit_preferred_candidate_only_without_policy(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            skill_dir = (
                repo_root / "skills" / "core" / "engineering" / "aoa-test-suggest"
            )
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                """---
name: aoa-test-suggest
scope: core
status: canonical
summary: Tests policy-free fallback.
invocation_mode: explicit-preferred
---

# aoa-test-suggest

## Intent

Surface as a candidate without hidden invocation.

## Trigger boundary

Use when no policy matrix is available.

## Inputs

- source metadata

## Outputs

- candidate-only policy

## Procedure

1. classify explicit-preferred cautiously.

## Contracts

- no hidden invocation comes from invocation mode alone.

## Risks and anti-patterns

- collapsing suggest and invoke.

## Verification

- inspect the emitted policy.
""",
                encoding="utf-8",
            )
            (skill_dir / "techniques.yaml").write_text(
                "techniques: []\n", encoding="utf-8"
            )

            payload = (
                skill_intelligence_surface.build_skill_intelligence_registry_payload(
                    repo_root
                )
            )

        skill = payload["skills"][0]
        self.assertEqual(skill["policy"]["implicit_activation_policy"], "suggest")
        self.assertTrue(skill["policy"]["candidate_only"])
        self.assertFalse(skill["runtime"]["allow_implicit_invocation"])

    def test_fallback_search_rows_rank_by_score_before_text(self) -> None:
        rows = skill_intelligence_surface.fallback_search_rows(
            [
                {
                    "doc_id": "low",
                    "skill_name": "aoa-low",
                    "section_role": "intent",
                    "source_path": "skills/aoa-low/SKILL.md",
                    "text": "a alpha",
                },
                {
                    "doc_id": "high",
                    "skill_name": "aoa-high",
                    "section_role": "intent",
                    "source_path": "skills/aoa-high/SKILL.md",
                    "text": "z alpha beta",
                },
            ],
            "alpha beta",
        )
        self.assertEqual(rows[0][0], "high")

    def test_sqlite_search_applies_filters_before_match_truncation(self) -> None:
        skills = []
        for index in range(130):
            name = f"aoa-noise-{index:03d}"
            skills.append(
                {
                    "name": name,
                    "scope": "core",
                    "status": "canonical",
                    "policy": {
                        "implicit_activation_policy": "invoke",
                        "mutation_surface": "repo",
                    },
                    "search_documents": [
                        {
                            "doc_id": f"{name}:intent",
                            "skill_name": name,
                            "section_role": "intent",
                            "source_path": f"skills/{name}/SKILL.md",
                            "text": "needle",
                        }
                    ],
                }
            )
        skills.append(
            {
                "name": "aoa-target-suggest",
                "scope": "core",
                "status": "canonical",
                "policy": {
                    "implicit_activation_policy": "suggest",
                    "mutation_surface": "repo",
                },
                "search_documents": [
                    {
                        "doc_id": "aoa-target-suggest:intent",
                        "skill_name": "aoa-target-suggest",
                        "section_role": "intent",
                        "source_path": "skills/aoa-target-suggest/SKILL.md",
                        "text": "needle",
                    }
                ],
            }
        )

        results = skill_intelligence_surface.sqlite_search(
            {"skills": skills},
            "needle",
            invocation_policy="suggest",
            limit=5,
        )
        self.assertEqual([result["name"] for result in results], ["aoa-target-suggest"])

    def test_fallback_search_rows_match_hyphenated_query_to_spaced_text(self) -> None:
        rows = skill_intelligence_surface.fallback_search_rows(
            [
                {
                    "doc_id": "source-truth",
                    "skill_name": "aoa-source-of-truth-check",
                    "section_role": "intent",
                    "source_path": "skills/aoa-source-of-truth-check/SKILL.md",
                    "text": "source truth boundary",
                }
            ],
            "source-truth",
        )
        self.assertEqual(rows[0][0], "source-truth")

    def test_document_match_score_treats_stronger_bm25_as_stronger_signal(self) -> None:
        skill = {"name": "aoa-target", "scope": "core"}
        weak = skill_intelligence_surface.document_match_score(
            skill,
            "needle",
            "intent",
            ["needle"],
            fts_score=-1.0,
        )
        strong = skill_intelligence_surface.document_match_score(
            skill,
            "needle",
            "intent",
            ["needle"],
            fts_score=-5.0,
        )
        self.assertGreater(strong, weak)

    def test_sqlite_search_applies_filters_in_fallback_branch(self) -> None:
        payload = {
            "skills": [
                {
                    "name": "aoa-noise",
                    "scope": "core",
                    "status": "canonical",
                    "policy": {
                        "implicit_activation_policy": "invoke",
                        "mutation_surface": "repo",
                    },
                    "search_documents": [
                        {
                            "doc_id": "aoa-noise:intent",
                            "skill_name": "aoa-noise",
                            "section_role": "intent",
                            "source_path": "skills/aoa-noise/SKILL.md",
                            "text": "needle",
                        }
                    ],
                },
                {
                    "name": "aoa-target-suggest",
                    "scope": "core",
                    "status": "canonical",
                    "policy": {
                        "implicit_activation_policy": "suggest",
                        "mutation_surface": "repo",
                    },
                    "search_documents": [
                        {
                            "doc_id": "aoa-target-suggest:intent",
                            "skill_name": "aoa-target-suggest",
                            "section_role": "intent",
                            "source_path": "skills/aoa-target-suggest/SKILL.md",
                            "text": "needle",
                        }
                    ],
                },
            ]
        }
        with mock.patch.object(
            skill_intelligence_surface.sqlite3,
            "connect",
            side_effect=sqlite3.Error("fts unavailable"),
        ):
            results = skill_intelligence_surface.sqlite_search(
                payload,
                "needle",
                invocation_policy="suggest",
                limit=5,
            )
        self.assertEqual([result["name"] for result in results], ["aoa-target-suggest"])

    def test_explain_candidate_gathers_evidence_from_requested_candidate(self) -> None:
        skills = []
        for index in range(25):
            name = f"aoa-noise-{index:03d}"
            skills.append(
                {
                    "name": name,
                    "scope": "core",
                    "status": "canonical",
                    "policy": {"implicit_activation_policy": "invoke"},
                    "source": {"skill_path": f"skills/{name}/SKILL.md"},
                    "boundaries": {},
                    "tiny_router": {},
                    "search_documents": [
                        {
                            "doc_id": f"{name}:intent",
                            "skill_name": name,
                            "section_role": "intent",
                            "source_path": f"skills/{name}/SKILL.md",
                            "text": "needle",
                        }
                    ],
                }
            )
        skills.append(
            {
                "name": "aoa-target",
                "scope": "core",
                "status": "canonical",
                "policy": {"implicit_activation_policy": "invoke"},
                "source": {
                    "skill_path": "skills/aoa-target/SKILL.md",
                    "techniques_path": "skills/aoa-target/techniques.yaml",
                },
                "boundaries": {},
                "tiny_router": {},
                "search_documents": [
                    {
                        "doc_id": "aoa-target:intent",
                        "skill_name": "aoa-target",
                        "section_role": "intent",
                        "source_path": "skills/aoa-target/SKILL.md",
                        "text": "needle",
                    }
                ],
            }
        )

        explanation = skill_intelligence_surface.explain_candidate(
            {"skills": skills},
            "aoa-target",
            intent="needle",
        )
        self.assertEqual(
            explanation["positive_evidence"][0]["doc_id"],
            "aoa-target:intent",
        )


if __name__ == "__main__":
    unittest.main()
