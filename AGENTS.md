# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-skills`.

## Purpose

`aoa-skills` is the bounded execution canon of AoA.
It stores public, reusable, Codex-facing skill bundles that package reusable
practice into reviewable workflows an agent can execute.

A skill is normally a multi-technique or multi-action package.
A single-technique skill is allowed only as an explicit reviewed exception.

This repository owns workflow meaning, not agent destiny.
Bounded execution is the start discipline here, not the final horizon of the
ecosystem.

## Owns

This repository is the source of truth for:

- skill bundle wording and workflow structure
- trigger boundaries
- invocation posture
- skill-level inputs and outputs
- reviewability and anti-pattern language at the skill layer
- technique dependency declaration at the skill layer
- generated skill catalogs, capsules, walkthroughs, evaluation matrices, portable export surfaces, and bounded bridge manifests derived from canonical skills
- skill-layer ability-card, loadout-reader, and quest-dispatch surfaces when they are explicitly derived from canonical skills

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering techniques in `aoa-techniques`
- proof doctrine or verdict logic in `aoa-evals`
- routing and dispatch logic in `aoa-routing`
- role contracts, progression doctrine, or self-agent checkpoint posture in `aoa-agents`
- scenario composition or questline / campaign / raid posture in `aoa-playbooks`
- memory objects or recall surfaces in `aoa-memo`
- derived substrate semantics in `aoa-kag`
- derived observability or movement summaries in `aoa-stats`
- private project-specific operations or unsanitized internal instructions

## Core rules

Only contribute skills that are:

- bounded
- reviewable
- public-safe
- useful to Codex
- traceable to reusable practice

A skill is not the origin of practice.
A skill is not a playbook.
A skill is not an agent profile.

If the meaning belongs upstream, route to the upstream repo instead of
duplicating it here.

## Growth posture

`aoa-skills` is where reusable practice becomes bounded execution.

This layer may support adaptive orchestration, checkpoint capture, quest
carry-forward, and reader surfaces such as ability cards or loadouts.
Those adjuncts must stay subordinate to canonical `SKILL.md` meaning.
They are not runtime inventory, not live quest sovereignty, and not a hidden
control plane.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. `ROADMAP.md`
3. `docs/ARCHITECTURE.md`
4. `docs/BRIDGE_SPEC.md`
5. `docs/LAYER_POSITION.md`
6. `docs/RUNTIME_PATH.md`
7. the target `skills/*/SKILL.md`
8. any generated surfaces directly affected by the task

Then branch by task:

- adaptive orchestration, closeout, or checkpoint capture:
  `docs/ADAPTIVE_SKILL_ORCHESTRATION.md` and
  `docs/CHECKPOINT_NOTE_PATH.md`
- ability-card or loadout reader surfaces:
  `docs/SKILL_ABILITY_MODEL.md` and
  `docs/ABILITY_LOADOUT_POSTURE.md`
- quest carry-forward or quest dispatch:
  `QUESTBOOK.md` and
  `docs/QUESTBOOK_SKILL_INTEGRATION.md`
- portable export, component refresh, adapter, or runtime seams:
  `docs/CODEX_PORTABLE_LAYER.md`,
  `docs/COMPONENT_REFRESH_LAW.md`,
  `docs/LOCAL_ADAPTER_CONTRACT.md`,
  `docs/RUNTIME_TOOL_CONTRACTS.md`, and
  `docs/OPENAI_SKILL_EXTENSIONS.md`, and
  `docs/CODEX_SKILL_MCP_WIRING.md`
- deterministic resources, tiny-router bridge, or support bundles:
  `docs/DETERMINISTIC_RESOURCE_BUNDLES.md`,
  `docs/BRIDGE_FROM_AOA_SUPPORT_DIRS.md`, and
  `docs/TWO_STAGE_SKILL_SELECTION.md`

If the task touches technique dependencies, inspect the upstream technique
bundles before editing.

If a deeper directory defines its own `AGENTS.md`, follow the nearest one.

## Primary objects

The most important objects in this repository are:

- canonical skill bundles under `skills/*/SKILL.md`
- dependency and policy inputs under `skills/*/techniques.yaml` and `config/`
- deterministic support resources under `skills/*/{scripts,references,assets}`
- generated catalogs, capsules, walkthroughs, evaluation matrices, ability-card surfaces, quest surfaces, export surfaces, and bridge manifests under `generated/` and `.agents/skills/`
- architecture, runtime, portable-layer, orchestration, and reader-surface docs under `docs/`

## Hard NO

Do not:

- invent source practice here that belongs in `aoa-techniques`
- write eval doctrine here
- store role-contract meaning here
- store memory meaning here
- collapse scenario-level playbooks into the skill layer
- let ability cards or loadouts become canonical skill truth
- let quest surfaces become live quest state, campaign authority, or a hidden runtime ledger
- move full Codex-facing interface or named MCP dependency metadata into source `skills/*/agents/openai.yaml`; keep that file policy-only and route generated-export metadata through `config/openai_skill_extensions.json`
- commit secrets, tokens, internal-only URLs, or sensitive infrastructure detail
- hide destructive workflows behind vague trigger boundaries
- silently widen scope beyond the stated task

Do not hand-edit `.agents/skills/*` unless the task is explicitly about export
debugging.
Canonical authoring remains in `skills/*`, `config/`, and the documented
generated manifests.

## Contribution doctrine

Use this flow: `PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- which skill or skill-surface family is changing
- whether trigger boundaries, invocation posture, contracts, or technique dependencies are changing
- whether adaptive orchestration, ability-card, loadout, or quest surfaces are changing
- whether portable export or downstream bridge surfaces will change
- what boundary risk exists

### DIFF

Keep the change focused and reviewable.
Preserve portability, public hygiene, and bounded execution.
Do not mix unrelated cleanup into skill meaning unless it is necessary for
repository integrity.

### VERIFY

Run the smallest applicable validation set from `README.md`.

Minimum validation for canonical skill changes:

```bash
python scripts/build_catalog.py
python scripts/validate_skills.py
python scripts/build_catalog.py --check
```

Use the broader current-state or release-prep path when the change touches
evaluation matrices, portable export, drift checks, policy posture, support
resources, or bridge inputs:

```bash
python scripts/report_skill_evaluation.py --fail-on-canonical-gaps
python scripts/report_technique_drift.py --techniques-repo ../aoa-techniques --fail-on-drift
python scripts/build_openai_yaml_examples.py --map examples/skill_mcp_wiring.map.json --output-dir examples --check
python scripts/validate_agent_skills.py --repo-root .
python scripts/validate_support_resources.py --repo-root . --check-portable
python scripts/validate_tiny_router_inputs.py --repo-root .
python -m pytest -q tests
python scripts/release_check.py
```

Confirm that:

- the skill remains bounded and reviewable
- canonical `SKILL.md` meaning still governs the derived surfaces
- trigger boundaries and invocation posture remain explicit
- ability-card, loadout, and quest surfaces stay adjunct-only
- technique dependencies and generated matrices remain aligned
- no neighboring layer meaning was silently pulled into this repo

### REPORT

Summarize:

- what changed
- whether meaning changed or only docs, metadata, or generated surfaces changed
- whether trigger boundaries, invocation posture, or technique dependencies changed
- whether named MCP dependency wiring or workspace-alignment scaffolds changed
- whether orchestration, ability-card, loadout, quest, portable export, or downstream bridge surfaces changed
- what validation you actually ran
- any remaining follow-up work

## Validation

Do not claim checks you did not run.

## Audit contract

For repository audits and GitHub review, read `AUDIT.md` after the core docs.

## Review guidelines

For GitHub review in this repository, treat the following as P0:

- committed secrets, private instructions, or internal-only URLs in skill or overlay surfaces
- a risk-heavy skill changing from `explicit-only` to a weaker invocation posture without explicit approval and matching docs/evidence updates
- overlay or skill wording that silently routes a bounded public workflow toward destructive or live operational behavior

Treat the following as P1:

- a skill widens beyond a bounded workflow
- runtime wording duplicates or rewrites technique truth instead of packaging it
- single-technique composition appears without exception review or without updating the composition audit surface
- `SKILL.md`, `techniques.yaml`, and derived catalogs or matrices drift apart
- status or invocation changes appear without matching review or evidence surfaces
- ability-card, loadout, or quest adjuncts begin acting like downstream integrations, playbooks, or live state
- claiming validation that was not actually run

Ignore trivial wording nits unless the task explicitly asks for copyediting.

For runtime-path debugging, prefer the documented local paths such as:

```bash
python scripts/inspect_skill.py --skill <skill-name>
python scripts/skill_runtime_guardrails.py discover --repo-root . ...
```

Those paths are for inspection and activation testing, not for replacing the
canonical authoring surface.
