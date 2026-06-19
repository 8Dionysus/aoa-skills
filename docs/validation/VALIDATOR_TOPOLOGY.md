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

Full blocking lane command sequences live in
[`../../config/validation_lanes.json`](../../config/validation_lanes.json).
Nearest `AGENTS.md` cards may name focused owner checks and lane ids; they
should not become a second copy of full lane sequences. The balancing rule lives
in [`COMMAND_AUTHORITY.md`](COMMAND_AUTHORITY.md).

## Operating Shape

Use this route before editing validator code:

1. Identify the owner surface.
2. Check whether the input is source, generated, export/runtime, live workspace,
   or advisory evidence.
3. Put validation CLI entrypoints under `scripts/validation/`; do not add root
   `scripts/validate_*.py` or `scripts/lint_*.py` wrappers.
4. Put bulky deterministic execution in `scripts/validation/validators/*`.
5. Put route-law or contract data in JSON manifests, not Python lists.
6. Store blocking lane sequences in `config/validation_lanes.json`.
7. Wire active callers through `scripts/lanes/validation_lanes.py` and
   `scripts/lanes/ci_gate.py`; keep root `scripts/validation_lanes.py` as
   compatibility ingress only.
8. Keep live workspace and broad evidence reports advisory unless a lane
   explicitly names their failure mode.

## Lanes

| Lane | Role | Typical command |
|---|---|---|
| `source-fast` | Fast source gate for authored skill contracts and route law. | `python scripts/lanes/ci_gate.py --mode source-fast` |
| `generated` | Read-model freshness and parity for generated companions. | `python scripts/lanes/ci_gate.py --mode generated --group all` |
| `export` | Portable export, runtime, support-resource, tiny-router, and adapter transport checks. | `python scripts/lanes/ci_gate.py --mode export` |
| `release` | Frozen release gate plus packaging smoke. | `python scripts/lanes/ci_gate.py --mode release` |
| `nightly` | Moving-main growth sentinel plus release identity readout. | `python scripts/lanes/ci_gate.py --mode nightly` |
| `advisory` | Reports and audits that guide review but do not fail ordinary CI by default. | Run the named report directly. |
| `manual` | Workspace, sibling, or operator-context check used when that surface is in scope. | Run the named command directly. |

## Surface Families

| Family | Protects | Owner module or surface | Failure route |
|---|---|---|---|
| Source/topology | `skills/**/SKILL.md`, `techniques.yaml`, skill status, route cards, questbook source shape. | `scripts/validation/validate_skills.py`, `scripts/validation/validate_nested_agents.py`, `scripts/validation/validators/questbook_surface.py` | Fix authored source, route card, or manifest; rerun `source-fast`. |
| AGENTS/route-law | Required nested `AGENTS.md` snippets and agent-facing contract shape. | `scripts/validation/validators/nested_agents_contract.json` | Update the local card or contract manifest; do not add a one-off Python validator. |
| Activation/trigger | Explicit/manual posture, collision cases, description signals, trigger cases, tiny-router surfaces. | `scripts/validation/validators/trigger_eval_surface.py`, `scripts/validation/validators/tiny_router_surface.py` | Fix source skill description/policy, rebuild generated cases, then lint. |
| Skill-native eval | Snapshot-backed local evidence and generated evaluation matrix. | `scripts/skill_model/skill_evaluation_contract.py`, `scripts/skill_model/skill_evaluation_surface.py` | Repair fixture/snapshot/source bundle mismatch; keep broad proof outside required gates. |
| Generated/read-model | Catalogs, public/governance/evaluation matrices, decision indexes, skill graph, release manifest. | `scripts/builders/build_catalog.py`, `scripts/decisions/generate_decision_indexes.py` | Move source input or builder, regenerate, and require drift-free output. |
| OS Abyss artifact bundle | `generated/release_manifest.json` as a release-contract subject for the root OS Abyss artifact verifier. | `scripts/validation/validate_abyss_machine_artifact_bundle.py`, `mechanics/release-support/manifests/release_manifest.bundle.json` | Fix the generated release manifest, bundle manifest, runner-provided `abyss-machine` verifier, or `abyss-machine` artifact policy class; rerun the release lane. |
| Portable export/runtime | `.agents/skills/*`, runtime seam, guardrails, Agent Skills export surface. | `scripts/validation/validators/agent_skills_export_surface.py`, `scripts/validation/validators/agent_skills_project_surface.py`, `scripts/runtime/skill_runtime_seam.py`, `scripts/runtime/skill_runtime_guardrails.py` | Fix source/config/builder and rerun export lane. |
| Support/tiny-router | Support resources, deterministic resource manifests, pack profiles, tiny-router capsules. | `scripts/validation/validators/support_resource_surface.py`, `scripts/validation/validators/pack_profile_surface.py`, `scripts/validation/validators/tiny_router_surface.py` | Fix canonical support files or generated mirrors; rerun export/generated lane. |
| Risk/guardrail | Explicit-only posture, permission/trust/context guardrail manifests. | `scripts/runtime/build_runtime_guardrails.py`, `scripts/runtime/skill_runtime_guardrails.py` | Fix policy config or source bundle risk posture; rerun runtime generated checks. |
| Release/CI | Lane command order, generated drift paths, packaging smoke, growth-vs-release split. | `config/validation_lanes.json`, `scripts/lanes/validation_lanes.py`, `scripts/lanes/ci_gate.py`, `scripts/lanes/release_check.py`; root wrappers remain compatibility ingress. | Fix lane manifest definitions and tests before changing GitHub workflow YAML. |
| Advisory audit/report | Promotion pressure, workspace adoption, quality audit, technique drift, reality trials. | Report scripts and audit docs. | Treat as review evidence unless a command is explicitly invoked with a failing flag. |

## Current Debt Closures

- The old semantic AGENTS snippet check was folded into
  `scripts/validation/validators/nested_agents_contract.json`; no separate
  `validate_semantic_agents.py` entrypoint remains.
- Tiny-router, support-resource, trigger-eval, description-trigger,
  pack-profile, and support-resource lint execution now lives in owner modules
  under `scripts/validation/validators/`; validation CLI adapters live under
  `scripts/validation/`, with no root validation wrapper layer.
- `config/validation_lanes.json` is the source of CI command sequencing;
  `scripts/lanes/validation_lanes.py` is the loader/API, and root
  `scripts/validation_lanes.py` is compatibility ingress with safe manifest
  inspection.
- Blocking lane sequences and active route cards now execute organ
  implementation paths such as `scripts/validation/validate_skills.py`,
  `scripts/builders/build_catalog.py`, and
  `scripts/runtime/build_runtime_seam.py`; root validation, builder, report,
  refresh, receipt, and adapter wrappers have been retired.

## Boundary

Keep this repository focused on skill-native deterministic contracts. If a
check needs live workspace state, sibling state, broad proof scoring, or model
benchmarking, keep it advisory or route it through an explicit bridge instead
of making it a default required gate.
