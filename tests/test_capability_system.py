from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest


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


def test_titan_runtime_transition_provenance_uses_canonical_routing_owner() -> None:
    families = capability_system.validate_sources(REPO_ROOT)
    node = capability_system.node_map(families)["guard.titan.runtime-transition"]
    source_refs = node["provenance"]["source_refs"]

    assert {
        (
            source["repo"],
            source["path"],
            source["ref"],
            source["role"],
            source["authority"],
        )
        for source in source_refs
    } == {
        (
            "aoa-agents",
            "mechanics/titan/parts/summon-boundary/docs/summon-boundary.md",
            "66f8bf22d03518b1e2367fd4f51dab80650f6d37",
            "role-intent-boundary",
            "external-authority",
        ),
        (
            "aoa-sdk",
            (
                "mechanics/boundary-bridge/parts/consumed-surface-posture-gate/"
                "docs/routing-consumer-contract.md"
            ),
            "7fba39d38cf5902c41dfbb7ae91f405b849880b7",
            "canonical-routing-consumer-contract",
            "external-authority",
        ),
    }


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


def test_shared_task_dag_structure_rejects_reversed_execution_stages() -> None:
    graph = capability_system.load_graph(REPO_ROOT)
    payload = capability_system.build_task_dag(
        graph,
        query="select then apply one evaluation",
        selected_capabilities=["mode.eval.select", "mode.eval.apply"],
        external_inputs=[
            {"type": "evaluation-selection-need", "ref": "manual://need"}
        ],
    )
    reversed_stages = copy.deepcopy(payload)
    reversed_stages["execution_stages"] = list(
        reversed(reversed_stages["execution_stages"])
    )
    schema = capability_system.load_json(
        REPO_ROOT / capability_system.DAG_SCHEMA_PATH
    )

    issues = capability_system.task_dag_structural_issues(
        reversed_stages,
        schema,
    )

    assert (
        "execution stage order violates edge "
        "mode.eval.select -> mode.eval.apply: source must precede target"
    ) in issues


def _write_owner_port(
    root: Path,
    projection: dict[str, object],
) -> Path:
    (root / "capabilities").mkdir(parents=True)
    (root / "skills").mkdir()
    (root / "capabilities" / "AGENTS.md").write_text(
        "# Owner\n",
        encoding="utf-8",
    )
    (root / "capabilities" / "admission.md").write_text(
        "# Admission\n",
        encoding="utf-8",
    )
    (root / "skills" / "port.manifest.json").write_text(
        "{}\n",
        encoding="utf-8",
    )
    manifest = {
        "schema_version": "aoa_capability_home_port_v1",
        "contract_ref": "aoa-skills:schemas/capability-home-port.schema.json",
        "owner_repo": "owner-example",
        "owner_ref": "capabilities/AGENTS.md",
        "admission_ref": "capabilities/admission.md",
        "source": {
            "family_root": "capabilities/families",
            "root_id": "owner-example",
        },
        "federation": {
            "parent_owner": "aoa-skills",
            "parent_node": "sessions",
            "relation": "specializes",
        },
        "skill_home_ref": "skills/port.manifest.json",
        "projection": {
            "authority": False,
            **projection,
            "generated_by": (
                "aoa-skills:scripts/build_capability_home_projection.py"
            ),
        },
    }
    path = root / "capabilities" / "port.manifest.json"
    path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def test_owner_projection_outputs_reject_authored_paths_and_collisions(
    tmp_path: Path,
) -> None:
    unsafe_root = tmp_path / "unsafe"
    _write_owner_port(
        unsafe_root,
        {
            "graph_json": "generated/capability-graph.json",
            "graph_markdown": "capabilities/families/owner-example.yaml",
            "router_markdown": "skills/owner-router/SKILL.md",
        },
    )

    with pytest.raises(
        capability_home_port.CapabilityHomePortError,
        match="projection",
    ):
        capability_home_port.load_port(REPO_ROOT, unsafe_root)

    collision_root = tmp_path / "collision"
    _write_owner_port(
        collision_root,
        {
            "graph_json": "generated/capability-graph.json",
            "graph_markdown": "generated/capability-router.md",
            "router_markdown": "generated/capability-router.md",
        },
    )

    with pytest.raises(
        capability_home_port.CapabilityHomePortError,
        match="projection outputs must be distinct read models",
    ):
        capability_home_port.load_port(REPO_ROOT, collision_root)


def test_owner_projection_outputs_allow_package_local_generated_router(
    tmp_path: Path,
) -> None:
    _write_owner_port(
        tmp_path,
        {
            "graph_json": "generated/capability-graph.json",
            "graph_markdown": "generated/capability-graph.md",
            "router_markdown": (
                "skills/owner-router/references/capability-router.md"
            ),
        },
    )

    port = capability_home_port.load_port(REPO_ROOT, tmp_path)

    assert port.router_markdown == Path(
        "skills/owner-router/references/capability-router.md"
    )


def test_owner_builder_rechecks_projection_paths_before_source_loading(
    tmp_path: Path,
) -> None:
    port = capability_home_port.CapabilityHomePort(
        contract_root=REPO_ROOT,
        owner_root=tmp_path,
        manifest_path=tmp_path / "capabilities" / "port.manifest.json",
        manifest={
            "projection": {
                "graph_json": "generated/capability-graph.json",
                "graph_markdown": "generated/capability-graph.md",
                "router_markdown": "skills/owner-router/SKILL.md",
            }
        },
    )

    with pytest.raises(
        capability_home_port.CapabilityHomePortError,
        match="projection.router_markdown",
    ):
        capability_home_port.build_outputs(port)


def test_owner_task_dag_preserves_and_validates_configured_graph_path() -> None:
    graph = capability_system.load_graph(REPO_ROOT)
    graph_path = "derived/owner-capability-graph.json"
    payload = capability_system.build_task_dag(
        graph,
        query="select then apply one evaluation",
        selected_capabilities=["mode.eval.select", "mode.eval.apply"],
        external_inputs=[
            {"type": "evaluation-selection-need", "ref": "manual://need"}
        ],
        source_graph_path=graph_path,
    )
    port = capability_home_port.CapabilityHomePort(
        contract_root=REPO_ROOT,
        owner_root=REPO_ROOT,
        manifest_path=REPO_ROOT / "capabilities" / "port.manifest.json",
        manifest={"projection": {"graph_json": graph_path}},
    )

    assert payload["source_graph"]["path"] == graph_path
    assert capability_home_port.validate_task_dag(port, graph, payload) == []

    wrong_path = copy.deepcopy(payload)
    wrong_path["source_graph"]["path"] = "generated/capability_graph.json"
    assert "task-local DAG source path does not match owner graph" in (
        capability_home_port.validate_task_dag(port, graph, wrong_path)
    )


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


def test_owner_router_heading_uses_owner_identity() -> None:
    port = capability_home_port.CapabilityHomePort(
        contract_root=REPO_ROOT,
        owner_root=REPO_ROOT,
        manifest_path=REPO_ROOT / "capabilities" / "port.manifest.json",
        manifest={
            "owner_repo": "owner-example",
            "source": {"root_id": "owner-example-root"},
            "federation": {
                "relation": "specializes",
                "parent_owner": "aoa-skills",
                "parent_node": "sessions",
            },
        },
    )
    graph = {
        "source": {"content_hash": "a" * 64},
        "nodes": [],
    }

    rendered = capability_home_port.render_router_markdown(port, graph)

    assert rendered.startswith("# owner-example capability router\n")
    assert "Session-memory capability router" not in rendered


def test_owner_contract_modes_may_live_below_navigation_categories() -> None:
    nodes = {
        "skill.owner": {
            "id": "skill.owner",
            "kind": "skill",
            "primary_parent": "owner-tree",
            "binding": {"ref": "skills/owner/SKILL.md"},
        },
        "owner.category": {
            "id": "owner.category",
            "kind": "capability",
            "primary_parent": "skill.owner",
        },
        "mode.owner.execute": {
            "id": "mode.owner.execute",
            "kind": "mode",
            "primary_parent": "owner.category",
            "binding": {
                "operation": "execute",
                "ref": "skills/owner/references/execute.md",
            },
        },
        "skill.nested": {
            "id": "skill.nested",
            "kind": "skill",
            "primary_parent": "nested.category",
            "binding": {"ref": "skills/nested/SKILL.md"},
        },
        "nested.category": {
            "id": "nested.category",
            "kind": "capability",
            "primary_parent": "owner.category",
        },
        "mode.nested.execute": {
            "id": "mode.nested.execute",
            "kind": "mode",
            "primary_parent": "nested.category",
            "binding": {
                "operation": "execute",
                "ref": "skills/nested/references/execute.md",
            },
        },
    }

    owner_modes = capability_system._contract_mode_nodes(
        nodes,
        skill_id="skill.owner",
        skill_node=nodes["skill.owner"],
        contract_modes={"execute": {}},
    )
    nested_modes = capability_system._contract_mode_nodes(
        nodes,
        skill_id="skill.nested",
        skill_node=nodes["skill.nested"],
        contract_modes={"execute": {}},
    )

    assert set(owner_modes) == {"execute"}
    assert set(nested_modes) == {"execute"}
    assert owner_modes["execute"]["id"] == "mode.owner.execute"
    assert nested_modes["execute"]["id"] == "mode.nested.execute"


def test_owner_graph_hash_includes_skill_package_mode_bits(tmp_path: Path) -> None:
    package_root = tmp_path / "skills" / "example"
    package_root.mkdir(parents=True)
    skill_path = package_root / "SKILL.md"
    skill_path.write_text("# Example\n", encoding="utf-8")
    skill_path.chmod(0o644)
    port = capability_home_port.CapabilityHomePort(
        contract_root=REPO_ROOT,
        owner_root=tmp_path,
        manifest_path=tmp_path / "capabilities" / "port.manifest.json",
        manifest={
            "projection": {
                "graph_json": "generated/capability_graph.json",
                "graph_markdown": "generated/CAPABILITY_GRAPH.md",
                "router_markdown": "generated/CAPABILITY_ROUTER.md",
            }
        },
    )

    _, baseline_fingerprint, baseline_issues = (
        capability_home_port._package_snapshot(port, package_root)
    )
    skill_path.chmod(0o755)
    _, executable_fingerprint, executable_issues = (
        capability_home_port._package_snapshot(port, package_root)
    )
    assert baseline_issues == executable_issues == []
    assert baseline_fingerprint != executable_fingerprint

    payload = {
        "source": {
            "root": "capabilities/families",
            "family_files": [],
            "referenced_files": [
                {
                    "path": "skills/example/SKILL.md",
                    "sha256": capability_home_port._sha256(skill_path.read_bytes()),
                }
            ],
            "content_hash": "",
        },
        "nodes": [
            {
                "id": "skill.example",
                "package": {"fingerprint": baseline_fingerprint},
            }
        ],
    }
    baseline_hash = capability_home_port._graph_source_content_hash(payload)
    payload["nodes"][0]["package"]["fingerprint"] = executable_fingerprint

    assert (
        baseline_hash
        != capability_home_port._graph_source_content_hash(payload)
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


def test_negative_phrase_penalty_uses_only_negative_specific_tokens() -> None:
    graph = {
        "nodes": [],
        "retrieval_documents": [
            {
                "id": "skill.session-router",
                "kind": "skill",
                "visibility": "advertised",
                "title": "Session memory router",
                "description": "Route session memory archive queries.",
                "search_text": "session memory archive route query",
                "positive_text": "session memory archive route query",
                "negative_text": (
                    "A narrower session memory owner is already known and "
                    "no query is required."
                ),
                "negative_phrases": [
                    "A narrower session memory owner is already known and "
                    "no query is required."
                ],
                "routing_tokens": [
                    "archive",
                    "memory",
                    "query",
                    "route",
                    "session",
                ],
                "positive_tokens": [
                    "archive",
                    "memory",
                    "query",
                    "route",
                    "session",
                ],
                "negative_tokens": [
                    "already",
                    "known",
                    "memory",
                    "narrower",
                    "no",
                    "owner",
                    "required",
                    "session",
                ],
                "contract_tokens": [
                    "archive",
                    "memory",
                    "query",
                    "route",
                    "session",
                ],
                "package_tokens": [],
                "tokens": [
                    "archive",
                    "memory",
                    "query",
                    "route",
                    "session",
                ],
            }
        ],
    }

    positive = capability_system.discover(
        graph,
        "session memory archive route query with no mutation",
        retrieval_depth="compact",
    )
    negative = capability_system.discover(
        graph,
        "session memory archive route query narrower owner known",
        retrieval_depth="compact",
    )

    assert positive[0]["negative_matched_tokens"] == []
    assert negative[0]["negative_matched_tokens"] == [
        "known",
        "narrower",
        "owner",
    ]


def test_negative_phrase_preserves_explicit_scope_over_positive_terms() -> None:
    graph = {
        "nodes": [],
        "retrieval_documents": [
            {
                "id": "workflow.titan.summon",
                "kind": "workflow",
                "visibility": "internal",
                "title": "Explicit Titan summon",
                "description": "Summon Titans for bounded delegated tasks.",
                "search_text": "explicit titan summon bounded delegation tasks",
                "positive_text": (
                    "explicit titan summon bounded delegation requested tasks"
                ),
                "negative_text": (
                    "delegation was not requested tasks are not bounded"
                ),
                "negative_phrases": [
                    "delegation was not requested",
                    "tasks are not bounded",
                ],
                "routing_tokens": ["explicit", "summon", "titan"],
                "positive_tokens": [
                    "bounded",
                    "delegation",
                    "explicit",
                    "requested",
                    "summon",
                    "tasks",
                    "titan",
                ],
                "negative_tokens": [
                    "bounded",
                    "delegation",
                    "not",
                    "requested",
                    "tasks",
                    "was",
                ],
                "contract_tokens": [
                    "bounded",
                    "delegation",
                    "explicit",
                    "requested",
                    "summon",
                    "tasks",
                    "titan",
                ],
                "package_tokens": [],
                "tokens": [
                    "bounded",
                    "delegation",
                    "explicit",
                    "requested",
                    "summon",
                    "tasks",
                    "titan",
                ],
            }
        ],
    }

    positive = capability_system.discover(
        graph,
        "explicit titan summon with bounded tasks and requested delegation",
        retrieval_depth="compact",
    )
    unbounded = capability_system.discover(
        graph,
        "explicit titan summon tasks are not bounded",
        retrieval_depth="compact",
    )
    unrequested = capability_system.discover(
        graph,
        "explicit titan summon but delegation was not requested",
        retrieval_depth="compact",
    )
    no_delegation = capability_system.discover(
        graph,
        "explicit titan summon no delegation requested",
        retrieval_depth="compact",
    )
    without_delegation = capability_system.discover(
        graph,
        "explicit titan summon without requested delegation",
        retrieval_depth="compact",
    )
    no_bounded_tasks = capability_system.discover(
        graph,
        "explicit titan summon with no bounded tasks",
        retrieval_depth="compact",
    )

    assert positive[0]["negative_matched_tokens"] == []
    assert unbounded[0]["negative_matched_tokens"] == [
        "bounded",
        "not",
        "tasks",
    ]
    assert unrequested[0]["negative_matched_tokens"] == [
        "delegation",
        "not",
        "requested",
        "was",
    ]
    assert no_delegation[0]["negative_matched_tokens"] == [
        "no",
        "requested",
    ]
    assert without_delegation[0]["negative_matched_tokens"] == [
        "requested",
        "without",
    ]
    assert no_bounded_tasks[0]["negative_matched_tokens"] == [
        "bounded",
        "no",
    ]


def test_negative_phrase_preserves_exact_clause_with_shared_vocabulary() -> None:
    graph = capability_system.load_graph(REPO_ROOT)

    positive = capability_system.discover(
        graph,
        "create a concrete memo candidate",
        retrieval_depth="compact",
        limit=30,
    )
    absent_queries = [
        "no existing concrete memo candidate",
        "no suitable existing concrete memo candidate",
        "not a suitable existing concrete memo candidate",
    ]
    absent_results = [
        capability_system.discover(
            graph,
            query,
            retrieval_depth="compact",
            limit=30,
        )
        for query in absent_queries
    ]
    existing = capability_system.discover(
        graph,
        "existing concrete memo candidate",
        retrieval_depth="compact",
        limit=30,
    )

    for results in (positive, *absent_results):
        memo = next(
            row for row in results if row["id"] == "sessions.memo-writeback"
        )
        assert memo["negative_matched_tokens"] == []

    memo = next(
        row for row in existing if row["id"] == "sessions.memo-writeback"
    )
    assert memo["negative_matched_tokens"] == [
        "candidate",
        "concrete",
        "existing",
        "memo",
    ]


def test_negative_phrase_preserves_short_exact_shared_clause() -> None:
    graph = capability_system.load_graph(REPO_ROOT)

    runtime_activation = capability_system.discover(
        graph,
        "titan console runtime activation",
        retrieval_depth="compact",
        limit=200,
    )
    role_truth = capability_system.discover(
        graph,
        "titan console role truth",
        retrieval_depth="compact",
        limit=200,
    )
    explicit_absence = capability_system.discover(
        graph,
        "titan console with no runtime activation",
        retrieval_depth="compact",
        limit=200,
    )
    positive = capability_system.discover(
        graph,
        "titan console inspect visible helper state",
        retrieval_depth="compact",
        limit=200,
    )

    for node_id in ("projects.titan.session.control", "tool.titan.console"):
        row = next(
            item for item in runtime_activation if item["id"] == node_id
        )
        assert row["negative_matched_tokens"] == [
            "activation",
            "runtime",
        ]
        row = next(
            item for item in explicit_absence if item["id"] == node_id
        )
        assert row["negative_matched_tokens"] == []
        row = next(item for item in positive if item["id"] == node_id)
        assert row["negative_matched_tokens"] == []

    parent = next(
        item
        for item in role_truth
        if item["id"] == "projects.titan.session.control"
    )
    assert parent["negative_matched_tokens"] == ["role", "truth"]
