# Test Topology

This map keeps the `aoa-skills` test surface readable as an agentic-OS
contract harness. Tests should answer: what surface is protected, which owner
source is authoritative, which lane runs the check, whether the result blocks
ordinary work, and where a failure routes next.

The machine inventory is
[`test_inventory.json`](test_inventory.json). Update it when adding, deleting,
renaming, splitting, folding, or changing the lane of a test file.

## Baseline

The pre-split green baseline was captured on 2026-05-31 from a clean
`main...origin/main` worktree. The observed default tests lane returned
`520 passed` and `1653 subtests passed` in `64.91s`. The first
split-preservation focused check returned `138 passed` across the
`validate_skills` and `build_catalog` owner slices.

## Operating Shape

Use the compact route shape: family -> protects -> owner source -> lane ->
focused target -> failure route.

Test files are not command authority. Blocking lane sequences live in
[`../../config/validation_lanes.json`](../../config/validation_lanes.json).
`tests/AGENTS.md` names the local route and focused iteration command behavior.
`pytest.ini` owns test classification markers.

## Families

| Family | Protects | Owner Source | Lane | Failure Route |
|---|---|---|---|---|
| `source/skill-contract` | `skills/**/SKILL.md`, frontmatter, technique manifests, source bundle rules. | `scripts/validation/validate_skills.py` | `source` | Fix authored skill source or source validator before changing generated output. |
| `source/questbook` | Questbook source shape and quest dispatch contracts. | `scripts/validation/validators/questbook_surface.py` | `source` | Fix questbook source, schema, or generated quest companion. |
| `source/review-status` | reviewed/evaluated/canonical status, review evidence, overlay governance. | `docs/reviews/`, `scripts/validation/validate_skills.py` | `source` | Fix review evidence, status, or governance lane truth. |
| `skill-native-eval` | local fixture/snapshot evidence and deterministic evaluation matrix. | `tests/fixtures/skill_evaluation_cases.yaml`, `scripts/skill_model/skill_evaluation_contract.py` | `source` / `router` | Repair fixture, snapshot, or source bundle mismatch; do not widen into broad model evals. |
| `generated/*` | catalogs, public/read-models, governance, graph, overlay/profile, evaluation matrix. | `scripts/builders/build_catalog.py` and generated-surface owners | `generated` | Move source or builder, regenerate, then require drift-free output. |
| `router/*` | trigger, description-trigger, tiny-router, golden route, and trace posture contracts. | trigger/tiny-router builders and validators | `router` | Fix source trigger boundary or generated router companions. |
| `export/*` | portable export, runtime seam, guardrails, support resources, packaging. | release-support builders and validators | `export` | Fix source/config/builder and rerun export or release lane. |
| `AGENTS/route-law` | nested route-law shape and command-authority balance. | `AGENTS.md`, `DESIGN.AGENTS.md`, validator topology | `source` | Fix nearest route card or contract manifest. |
| `release/ci-lane` | CI/release command order and lane composition. | `config/validation_lanes.json`, `scripts/ci_gate.py`, `scripts/release_check.py` | `release` | Fix lane manifest before changing workflow YAML. |
| `advisory/*` | quality, promotion pressure, workspace adoption, technique drift. | audit/report scripts | `advisory` | Treat as review evidence unless an explicit failing flag is invoked. |
| `external/*` / `live` | sibling fixtures or external tools such as `aoa-sdk` and `skills-ref`. | bridge scripts and referenced sibling artifacts | `advisory` / `live` | Keep soft unless the lane explicitly declares the dependency. |
| `live-harness/dispatch` | source locks, cohort expansion, safe adapters, host gates, private/public separation, and distinct route/source-declared downstream procedure-outcome projection without model calls. | `evals/runners/run_live_skill_dispatch.py` and its plan/schemas | `source` | Repair the deterministic harness contract before spending any live turn. |
| `mechanics/*` | mechanic-local schema, examples, generated companions, and Agon candidate surfaces. | nearest mechanic package | `source` / `release` | Fix the mechanic-local owner surface first. |

## Lane Rules

- `source` and `generated` tests must stay deterministic and repo-local.
- `export` tests may run packaging/runtime CLIs, but should not duplicate the
  full release sequence inside a unit test.
- `router` tests may use fixture/golden route contracts, but must remain
  deterministic and local to `aoa-skills`.
- `advisory`, `external`, and `live` checks must be visibly marked and should
  not silently become default proof for semantic/model quality.
- Broad semantic/model evals belong in the eval organ unless the case protects
  a skill-native trigger, description, router, or export contract.
