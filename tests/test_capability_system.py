from __future__ import annotations

import copy
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from skill_model import capability_home_port, capability_system


def test_manual_migration_contract_remains_exact_and_live() -> None:
    families = capability_system.validate_sources(REPO_ROOT)
    migration = capability_system.load_migration_contract(REPO_ROOT)

    assert len(families) == 10
    assert migration["baseline"]["skill_count"] == 57
    assert len(migration["entries"]) == 57
    assert capability_system.migration_issues(migration, families) == []


def test_migration_rejects_duplicate_and_missing_target() -> None:
    families = capability_system.validate_sources(REPO_ROOT)
    migration = capability_system.load_migration_contract(REPO_ROOT)

    duplicate = copy.deepcopy(migration)
    duplicate["entries"].append(copy.deepcopy(duplicate["entries"][0]))
    assert any(
        "duplicate legacy_name" in issue
        for issue in capability_system.migration_issues(duplicate, families)
    )

    missing = copy.deepcopy(migration)
    missing["entries"][0]["target_id"] = "mode.missing"
    assert any(
        "target_id 'mode.missing' does not exist" in issue
        for issue in capability_system.migration_issues(missing, families)
    )


def test_deep_discovery_keeps_positive_and_negative_manual_cases_apart() -> None:
    graph = capability_system.load_graph(REPO_ROOT)

    positive = capability_system.discover(
        graph,
        "найди почему мы приняли архитектурное решение",
    )
    negative = capability_system.discover(
        graph,
        "создай общий план тестирования для неопределенного поведения",
    )

    assert positive[0]["id"] == "mode.decision.find"
    assert negative == []


def test_unscoped_recovery_prefers_reusable_family_over_project_adapter() -> None:
    graph = capability_system.load_graph(REPO_ROOT)

    generic = capability_system.discover(
        graph,
        "diagnose stale session evidence and propose safe MCP route recovery",
    )
    titan = capability_system.discover(
        graph,
        "inspect Titan approval queue with exact thread and turn identity",
    )

    assert generic[0]["id"] == "sessions.recovery"
    assert titan[0]["id"] == "projects.titan.session.control"


def test_task_local_dag_connects_abi_and_blocks_conflicting_modes() -> None:
    graph = capability_system.load_graph(REPO_ROOT)
    ready = capability_system.build_task_dag(
        graph,
        query="select then apply one evaluation",
        selected_capabilities=["mode.eval.select", "mode.eval.apply"],
        external_inputs=[
            {"type": "evaluation-selection-need", "ref": "manual://need"}
        ],
    )
    blocked = capability_system.build_task_dag(
        graph,
        query="record and correct the same decision",
        selected_capabilities=["mode.decision.record", "mode.decision.correct"],
        external_inputs=[
            {"type": "accepted-decision", "ref": "manual://accepted"},
            {
                "type": "decision-correction-target",
                "ref": "manual://correction",
            },
        ],
    )

    assert ready["status"] == "ready"
    assert ready["edges"] == [
        {
            "artifact_type": "evaluation-selection",
            "kind": "data",
            "source": "mode.eval.select",
            "target": "mode.eval.apply",
        },
        {
            "kind": "handoff",
            "source": "mode.eval.select",
            "target": "mode.eval.apply",
        },
    ]
    assert ready["execution_stages"] == [
        ["mode.eval.select"],
        ["mode.eval.apply"],
    ]
    assert {
        checkpoint["node"] for checkpoint in ready["checkpoints"]
    } == {"mode.eval.select", "mode.eval.apply"}
    assert ready["terminal"] == {
        "lifetime": "task-local",
        "success_condition": "all selected nodes reached verified terminal conditions",
    }
    assert capability_system.validate_task_dag(REPO_ROOT, ready) == []
    assert blocked["status"] == "blocked"
    assert any("conflict:" in blocker for blocker in blocked["blockers"])
    assert capability_system.validate_task_dag(REPO_ROOT, blocked) == []


def test_task_local_dag_closure_includes_forward_verifier() -> None:
    def executable_node(
        node_id: str,
        *,
        inputs: list[dict[str, object]],
        outputs: list[dict[str, object]],
    ) -> dict[str, object]:
        return {
            "id": node_id,
            "kind": "skill",
            "contract_level": "executable",
            "binding": {
                "availability": "available",
                "ref": f"skills/{node_id}",
            },
            "owner": {
                "repo": "owner",
                "ref": "AGENTS.md",
            },
            "abi": {
                "inputs": inputs,
                "outputs": outputs,
            },
            "execution": {
                "effects": ["none"],
                "verification": [f"verify {node_id}"],
                "termination": [f"stop after {node_id}"],
            },
        }

    graph = {
        "source": {"content_hash": "sha256:test"},
        "nodes": [
            executable_node(
                "skill.work",
                inputs=[],
                outputs=[{"name": "result", "type": "work-result"}],
            ),
            executable_node(
                "skill.verifier",
                inputs=[
                    {
                        "name": "result",
                        "type": "work-result",
                        "required": True,
                    }
                ],
                outputs=[],
            ),
        ],
        "relations": [
            {
                "kind": "verifies",
                "source": "skill.verifier",
                "target": "skill.work",
            }
        ],
    }

    plan = capability_system.build_task_dag(
        graph,
        query="run work and its declared verifier",
        selected_capabilities=["skill.work"],
    )

    assert plan["status"] == "ready"
    assert [node["id"] for node in plan["nodes"]] == [
        "skill.verifier",
        "skill.work",
    ]
    assert plan["execution_stages"] == [
        ["skill.work"],
        ["skill.verifier"],
    ]
    assert {
        checkpoint["node"]: checkpoint.get("verifier")
        for checkpoint in plan["checkpoints"]
    } == {
        "skill.verifier": None,
        "skill.work": "skill.verifier",
    }
    assert {
        (edge["kind"], edge["source"], edge["target"])
        for edge in plan["edges"]
    } == {
        ("data", "skill.work", "skill.verifier"),
        ("verification", "skill.work", "skill.verifier"),
    }


def test_owner_port_dependency_cycle_includes_guard_relations() -> None:
    acyclic = [
        {
            "kind": "guarded-by",
            "source": "skill.work",
            "target": "guard.approval",
        }
    ]
    cyclic = [
        *acyclic,
        {
            "kind": "guarded-by",
            "source": "guard.approval",
            "target": "skill.work",
        },
    ]

    assert (
        capability_home_port._dependency_cycle(
            {"skill.work", "guard.approval"},
            acyclic,
        )
        is None
    )
    assert capability_home_port._dependency_cycle(
        {"skill.work", "guard.approval"},
        cyclic,
    ) == ["guard.approval", "skill.work"]

    verifies_cycle = [
        {
            "kind": "verifies",
            "source": "skill.verifier",
            "target": "skill.work",
        },
        {
            "kind": "verifies",
            "source": "skill.work",
            "target": "skill.verifier",
        },
    ]
    assert capability_home_port._dependency_cycle(
        {"skill.work", "skill.verifier"},
        verifies_cycle,
    ) == ["skill.verifier", "skill.work"]


def test_shared_task_dag_structure_rejects_dangling_edge_endpoints() -> None:
    graph = capability_system.load_graph(REPO_ROOT)
    payload = capability_system.build_task_dag(
        graph,
        query="select then apply one evaluation",
        selected_capabilities=["mode.eval.select", "mode.eval.apply"],
        external_inputs=[
            {"type": "evaluation-selection-need", "ref": "manual://need"}
        ],
    )
    dangling = copy.deepcopy(payload)
    dangling["edges"][0]["source"] = "mode.missing-source"
    dangling["edges"][0]["target"] = "mode.missing-target"
    schema = capability_system.load_json(
        REPO_ROOT / capability_system.DAG_SCHEMA_PATH
    )

    issues = capability_system.task_dag_structural_issues(dangling, schema)

    assert "edge source does not exist: mode.missing-source" in issues
    assert "edge target does not exist: mode.missing-target" in issues


def test_owner_contract_metadata_fingerprints_full_shared_closure() -> None:
    port = capability_home_port.CapabilityHomePort(
        contract_root=REPO_ROOT,
        owner_root=REPO_ROOT,
        manifest_path=REPO_ROOT / "capabilities" / "legacy-skill-migration.yaml",
        manifest={},
    )

    metadata = capability_home_port._contract_source_metadata(port)
    rows = metadata["contract"]["contract_files"]

    assert [row["path"] for row in rows] == [
        path.as_posix() for path in capability_home_port.CONTRACT_SOURCE_PATHS
    ]
    for row in rows:
        assert row["sha256"] == capability_home_port._sha256(
            (REPO_ROOT / row["path"]).read_bytes()
        )


def test_two_stage_retrieval_keeps_package_text_behind_owner_admission() -> None:
    graph = {
        "nodes": [],
        "retrieval_documents": [
            {
                "id": "skill.owner-router",
                "kind": "skill",
                "visibility": "advertised",
                "title": "Archive owner router",
                "description": "Route archive inspection requests.",
                "search_text": "archive inspection",
                "positive_text": "archive inspection",
                "negative_text": "",
                "negative_phrases": [],
                "routing_tokens": ["archive", "inspect"],
                "positive_tokens": ["archive", "inspect"],
                "negative_tokens": [],
                "contract_tokens": ["archive", "inspect"],
                "package_tokens": [],
                "tokens": ["archive", "inspect"],
            },
            {
                "id": "skill.generic-reader",
                "kind": "skill",
                "visibility": "deferred",
                "title": "Generic archive reader",
                "description": "Inspect archived evidence.",
                "search_text": "archive inspect evidence",
                "positive_text": "archive inspect evidence",
                "negative_text": "",
                "negative_phrases": [],
                "routing_tokens": ["archive", "inspect"],
                "positive_tokens": ["archive", "evidence", "inspect"],
                "negative_tokens": [],
                "contract_tokens": ["archive", "evidence", "inspect"],
                "package_tokens": [],
                "tokens": ["archive", "evidence", "inspect"],
            },
            {
                "id": "skill.z-correlated-reader",
                "kind": "skill",
                "visibility": "deferred",
                "title": "Correlated archive reader",
                "description": "Inspect archived evidence.",
                "search_text": (
                    "archive inspect evidence correlation checkpoint verifier"
                ),
                "positive_text": "archive inspect evidence",
                "negative_text": "",
                "negative_phrases": [],
                "routing_tokens": ["archive", "inspect"],
                "positive_tokens": ["archive", "evidence", "inspect"],
                "negative_tokens": [],
                "contract_tokens": ["archive", "evidence", "inspect"],
                "package_tokens": ["checkpoint", "correlation", "verifier"],
                "tokens": [
                    "archive",
                    "checkpoint",
                    "correlation",
                    "evidence",
                    "inspect",
                    "verifier",
                ],
            },
        ],
    }
    query = "inspect archive evidence correlation checkpoint verifier"

    compact = capability_system.discover(
        graph,
        query,
        retrieval_depth="compact",
    )
    routed = capability_system.discover_two_stage(graph, query)

    assert compact[0]["id"] == "skill.generic-reader"
    assert [
        item["id"]
        for item in routed["candidate_selection"]["candidates"]
    ] == ["skill.owner-router"]
    assert routed["deep_rerank"]["candidates"][0]["id"] == (
        "skill.z-correlated-reader"
    )
    assert routed["owner_admitted"] is True

    no_owner_match = capability_system.discover_two_stage(
        graph,
        "unrelated payroll invoice",
    )
    assert no_owner_match["owner_admitted"] is False
    assert no_owner_match["deep_rerank"]["candidates"] == []
