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

- `docs/session-harvests/`
- `examples/session_growth_artifacts/`
- `templates/SKILL_APPLICABILITY_MAP.template.md`
- `templates/SESSION_CANDIDATE_HARVEST.template.md`
- `config/project_core_skill_kernel.json`
- `scripts/publish_core_skill_receipts.py`

This package may route to those surfaces, but it does not turn evidence notes
or examples into promotion truth.

## Recurrence Companion

The recurrence component
`manifests/recurrence/component.skills.bundle-and-activation-beacons.json`
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
