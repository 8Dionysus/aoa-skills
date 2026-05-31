# Validator Topology

This map keeps `aoa-skills` validators usable by future agents. A validator is
healthy when an agent can answer: what surface does it protect, what input does
it read, what output proves success, where is it called, and where should a
failure route next?

Use the compact route shape: role -> input -> output -> owner -> lane -> check
-> failure route.

The machine inventory lives in
[`validator_inventory.json`](validator_inventory.json). Update that inventory
when adding, deleting, renaming, splitting, folding, or changing the lane of a
validation-like entrypoint.

## Operating Shape

Use this route before editing validator code:

1. Identify the owner surface.
2. Check whether the input is source, generated, export/runtime, live workspace,
   or advisory evidence.
3. Keep root `scripts/validate_*.py` and `scripts/lint_*.py` files as CLI
   adapters when the execution body is non-trivial.
4. Put bulky deterministic execution in `scripts/validators/*`.
5. Put route-law or contract data in JSON manifests, not Python lists.
6. Wire blocking checks through `scripts/validation_lanes.py`.
7. Keep live workspace and broad evidence reports advisory unless a lane
   explicitly names their failure mode.

## Lanes

| Lane | Role | Typical command |
|---|---|---|
| `source-fast` | Fast source gate for authored skill contracts and route law. | `python scripts/ci_gate.py --mode source-fast` |
| `generated` | Read-model freshness and parity for generated companions. | `python scripts/ci_gate.py --mode generated --group all` |
| `export` | Portable export, runtime, support-resource, tiny-router, and adapter transport checks. | `python scripts/ci_gate.py --mode export` |
| `release` | Frozen release gate plus packaging smoke. | `python scripts/ci_gate.py --mode release` |
| `nightly` | Moving-main growth sentinel plus release identity readout. | `python scripts/ci_gate.py --mode nightly` |
| `advisory` | Reports and audits that guide review but do not fail ordinary CI by default. | Run the named report directly. |
| `manual` | Workspace, sibling, or operator-context check used when that surface is in scope. | Run the named command directly. |

## Surface Families

| Family | Protects | Owner module or surface | Failure route |
|---|---|---|---|
| Source/topology | `skills/**/SKILL.md`, `techniques.yaml`, skill status, route cards, questbook source shape. | `scripts/validate_skills.py`, `scripts/validate_nested_agents.py`, `scripts/validators/questbook_surface.py` | Fix authored source, route card, or manifest; rerun `source-fast`. |
| AGENTS/route-law | Required nested `AGENTS.md` snippets and agent-facing contract shape. | `scripts/validators/nested_agents_contract.json` | Update the local card or contract manifest; do not add a one-off Python validator. |
| Activation/trigger | Explicit/manual posture, collision cases, description signals, trigger cases, tiny-router surfaces. | `scripts/validators/trigger_eval_surface.py`, `scripts/validators/tiny_router_surface.py` | Fix source skill description/policy, rebuild generated cases, then lint. |
| Skill-native eval | Snapshot-backed local evidence and generated evaluation matrix. | `scripts/skill_evaluation_contract.py`, `scripts/skill_evaluation_surface.py` | Repair fixture/snapshot/source bundle mismatch; keep broad proof outside required gates. |
| Generated/read-model | Catalogs, public/governance/evaluation matrices, decision indexes, skill graph, release manifest. | `scripts/build_catalog.py`, `scripts/generate_decision_indexes.py` | Move source input or builder, regenerate, and require drift-free output. |
| Portable export/runtime | `.agents/skills/*`, runtime seam, guardrails, Agent Skills export surface. | `scripts/validators/agent_skills_export_surface.py`, `scripts/skill_runtime_seam.py`, `scripts/skill_runtime_guardrails.py` | Fix source/config/builder and rerun export lane. |
| Support/tiny-router | Support resources, deterministic resource manifests, pack profiles, tiny-router capsules. | `scripts/validators/support_resource_surface.py`, `scripts/validators/pack_profile_surface.py`, `scripts/validators/tiny_router_surface.py` | Fix canonical support files or generated mirrors; rerun export/generated lane. |
| Risk/guardrail | Explicit-only posture, permission/trust/context guardrail manifests. | `scripts/build_runtime_guardrails.py`, `scripts/skill_runtime_guardrails.py` | Fix policy config or source bundle risk posture; rerun runtime generated checks. |
| Release/CI | Lane command order, generated drift paths, packaging smoke, growth-vs-release split. | `scripts/validation_lanes.py`, `scripts/ci_gate.py`, `scripts/release_check.py` | Fix lane definitions and tests before changing GitHub workflow YAML. |
| Advisory audit/report | Promotion pressure, workspace adoption, quality audit, technique drift, reality trials. | Report scripts and audit docs. | Treat as review evidence unless a command is explicitly invoked with a failing flag. |

## Current Debt Closures

- The old semantic AGENTS snippet check was folded into
  `scripts/validators/nested_agents_contract.json`; no separate
  `validate_semantic_agents.py` entrypoint remains.
- Tiny-router, support-resource, trigger-eval, description-trigger,
  pack-profile, and support-resource lint execution now lives in owner modules
  under `scripts/validators/`; root files are CLI adapters.
- `scripts/validation_lanes.py` remains the source of CI command sequencing.
  GitHub workflow YAML should call lanes, not invent hidden validation meaning.

## Boundary

Keep this repository focused on skill-native deterministic contracts. If a
check needs live workspace state, sibling state, broad proof scoring, or model
benchmarking, keep it advisory or route it through an explicit bridge instead
of making it a default required gate.
