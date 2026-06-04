# Script Topology

`scripts/` is the command-plane source home for the bounded skill execution
canon. It must be tree-shaped: root script paths are compatibility ingress
only, while implementation belongs to named organ directories.

This map is not command authority. Blocking lane sequences live in
[`../../config/validation_lanes.json`](../../config/validation_lanes.json), and
`scripts/lanes/validation_lanes.py` is the loader.

The machine-readable organ map lives in
[`script_inventory.json`](script_inventory.json).

## Root Command Ingress

Root `scripts/*.py` files keep historical command paths working. Except for
`_ingress.py`, they must be thin wrappers that call `_ingress.expose(...)` and
point to one implementation module under an organ directory.

Root wrappers are for command/front-door paths, not for library convenience.
Contract, source-model, surface, bridge, and helper modules should be imported
from their organ package.

Generated local-adapter manifests are export-derived surfaces. They are built
through `scripts/build_agent_skills.py`; a standalone
`scripts/build_local_adapter_manifest.py` ingress is intentionally not retained
because it duplicates the export builder output without owning a separate lane.
Project kernel, outer-ring, risk-ring, and foundation-profile export documents
are generated through the `scripts/export/project_surface.py` phase.
The Agent Skills export builder `main()` should stay a route over load, portable
skill export, generated text assembly, and write phases.
Per-skill portable markdown, OpenAI YAML, resource inventory, context,
handoff, trust, and runtime contract assembly lives in
`scripts/export/portable_skill_export.py`.

`scripts/validators/__init__.py` is a compatibility package for older
`validators.*` imports. Validator implementation and contract JSON live under
`scripts/validation/validators/`.

## Organ Directories

| Organ | Owns |
| --- | --- |
| `activation/` | activation shims and invocation policy |
| `adapters/` | adapter-specific manifests, config snippets, and examples |
| `audit/` | read-only audits and reality-trial reports |
| `bridges/` | sibling bridge helper logic |
| `builders/` | generated/read-model builders |
| `bundles/` | staged bundles, pack install/import/verify, and bundle surfaces |
| `decisions/` | decision index parsing and generation |
| `export/` | portable Agent Skills export and release-manifest contracts |
| `lanes/` | CI/release lane execution and command-manifest loading |
| `receipts/` | receipt publishing helpers |
| `refresh/` | source refresh flows from manifests or technique bridges |
| `reports/` | skill boundary, evaluation, promotion, and technique drift reports |
| `runtime/` | runtime seam, guardrails, activation payloads, and inspection |
| `skill_model/` | source model, contracts, governance, status, lineage, and review surfaces |
| `validation/` | validation and lint entrypoints plus owner validator modules |

## Movement Rule

New script implementation must enter the narrowest organ directory first. Add a
root ingress only when a historical command path, CI lane, generated payload, or
downstream integration needs that stable path.

Do not put new implementation or library wrappers in root `scripts/`.
