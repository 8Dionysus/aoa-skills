# Growth-Cycle Provenance

This bridge keeps the current active route tied to the source surfaces that
landed it. Use it for auditing, not as the main entry route.

## Moved Active Docs

The first growth-cycle package landing moved these active docs out of flat
`docs/` and into package-local active docs:

| Former path | Current path | Active route |
|---|---|---|
| `docs/ADAPTIVE_SKILL_ORCHESTRATION.md` | `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md` | [Adaptive Orchestration](parts/adaptive-orchestration/README.md) |
| `docs/SESSION_GROWTH_KERNEL_MATURITY.md` | `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md` | [Session Kernel Maturity](parts/session-kernel-maturity/README.md) |

These docs were not archived as raw legacy because they remain active contract
surfaces. The move changes their route, not their authority level.

## Evidence And Example Companions

Current evidence companions remain in:

- `mechanics/growth-cycle/session-harvests/`
- `mechanics/growth-cycle/examples/session-growth-artifacts/`
- `templates/SKILL_APPLICABILITY_MAP.template.md`
- `mechanics/growth-cycle/templates/SESSION_CANDIDATE_HARVEST.template.md`
- `config/project_core_skill_kernel.json`
- `scripts/receipts/publish_core_skill_receipts.py`

This package may route to those surfaces, but it does not turn evidence notes
or examples into promotion truth.

Example families use semantic suffixes. `reviewed-donor-harvest`,
`derived-visibility-handoff`, and `kernel-maturity` are active evidence-family
names, not pass numbers or maturity scores.

Session-harvest notes and their candidate-harvest template moved from the flat
docs/templates lanes into Growth-cycle because the harvest-note boundary is a
Growth-cycle part:

| Former path | Current path | Active route |
|---|---|---|
| `docs/session-harvests/` | `mechanics/growth-cycle/session-harvests/` | [Harvest Note Boundary](parts/harvest-note-boundary/README.md) |
| `templates/SESSION_CANDIDATE_HARVEST.template.md` | `mechanics/growth-cycle/templates/SESSION_CANDIDATE_HARVEST.template.md` | [Harvest Note Boundary](parts/harvest-note-boundary/README.md) |

## Preserved Reformation Rhythm Source

The mechanics reformation notebook is preserved as package-local raw lineage:

| Former path | Preserved raw path | Active route |
|---|---|---|
| `legacy/MECHANICS_REFORMATION_RHYTHM.md` | `mechanics/growth-cycle/legacy/reformation-rhythm/raw/MECHANICS_REFORMATION_RHYTHM.md` | [Harvest Note Boundary](parts/harvest-note-boundary/README.md) and [Adaptive Orchestration](parts/adaptive-orchestration/README.md) |

The distilled public learning lives in
`mechanics/growth-cycle/session-harvests/2026-05-18.mechanics-reformation-root-legacy-distillation.md`.
The raw notebook is not a current route card.

## Recurrence Companion

The recurrence component
`mechanics/recurrence/manifests/component.skills.bundle-and-activation-beacons.json`
observes adaptive orchestration and harvest pressure. Its decision-surface refs
must follow the package-local active path.

## Neighbor Routes

- `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md` owns lower-authority
  checkpoint capture before reviewed harvest.
- `mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md` owns reviewed
  `candidate_ref` after donor harvest.
- `QUESTBOOK.md` and `mechanics/questbook/docs/QUESTBOOK_SKILL_INTEGRATION.md` own durable
  obligations and quest-harvest posture.

## Stop-Line

The growth-cycle package orders and routes reviewed lifecycle stages. It does
not execute skills, prove claims, write memory, accept owner truth, refresh
stats, or promote quests by itself.
