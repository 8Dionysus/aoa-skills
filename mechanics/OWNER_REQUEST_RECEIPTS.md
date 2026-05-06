# AoA Owner Request Receipts

This is the owner-local receipt surface for `Agents-of-Abyss` owner requests
whose `owner_repo` is `aoa-skills`.

The center queue asks for owner-local truth. This file records what
`aoa-skills` accepts or lands. It does not replace canonical skill bundles,
does not create proof authority, and does not let the AoA center claim
execution, approval, runtime, role, memory, route, playbook, or stats truth.

Center-side source surfaces:

- `Agents-of-Abyss/mechanics/OWNER_REQUEST_PROTOCOL.md`
- `Agents-of-Abyss/mechanics/OWNER_REQUEST_QUEUE.md`
- `Agents-of-Abyss/mechanics/owner-request-queue.json`
- `Agents-of-Abyss/mechanics/*/OWNER_REQUESTS.md`

## Status Vocabulary

Owner-local statuses mirror the center protocol:

- `landed`: the requested `aoa-skills` surface exists and is listed as
  evidence here.
- `accepted`: `aoa-skills` accepts the slice and owner boundary, but a later
  mechanics package, skill review, or receipt is still needed before the center
  may call the request landed.

`accepted` is not executable activation. `landed` is still only skill-layer
landing; proof and public quality claims route to `aoa-evals`.

## Snapshot

| Request | Owner-local status | Center queue status | Owner-local evidence | Remaining boundary |
|---|---|---|---|---|
| `ORQ-METHOD-SKILLS-001` | `landed` | may be `landed` | `mechanics/method-growth/` and method-growth schemas/examples | no final skill truth or activation claim from center |
| `ORQ-DISTILLATION-SKILLS-001` | `accepted` | may be `accepted` | session-growth skills and future `distillation` pressure in `mechanics/README.md` | no generic distillation package has landed yet |
| `ORQ-GROWTHCYCLE-SKILLS-001` | `landed` | may be `landed` | session-growth skill family and `mechanics/growth-cycle/` | no final harvest, progression, quest, proof, or owner-acceptance authority |
| `ORQ-CHECKPOINT-SKILLS-001` | `landed` | may be `landed` | `aoa-checkpoint-closeout-bridge` and `mechanics/checkpoint/` | checkpoint notes stay below reviewed closeout |
| `ORQ-EXPERIENCE-SKILLS-001` | `accepted` | may be `accepted` | Experience skill docs remain routed as future package pressure | no Experience mechanics package or executable approval authority has landed |
| `ORQ-RPG-SKILLS-001` | `landed` | may be `landed` | `mechanics/rpg/` reader surfaces and ability/loadout companions | no skill ontology, feat canon, runtime inventory, or progression proof |
| `ORQ-AUDIT-SKILLS-001` | `accepted` | may be `accepted` | existing audit-adjacent skills and future `audit` pressure in `mechanics/README.md` | no general audit mechanics package has landed yet |

## ORQ-METHOD-SKILLS-001

Owner-local status: `landed`

What landed:

- `mechanics/method-growth/README.md`
- `mechanics/method-growth/docs/CANDIDATE_LINEAGE_CONTRACT.md`
- `mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md`
- `mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md`
- `mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md`
- `mechanics/method-growth/parts/candidate-lineage/README.md`
- `mechanics/method-growth/parts/owner-status-landing/README.md`
- `mechanics/method-growth/parts/governed-followthrough/README.md`
- `mechanics/method-growth/parts/adoption-boundary/README.md`
- `mechanics/method-growth/parts/adoption-evidence-receipts/README.md`
- `mechanics/method-growth/parts/retention-regression-retirement/README.md`
- `mechanics/method-growth/parts/pattern-adoption-handoff/README.md`

The landing gives `aoa-skills` an owner-local candidate identity, owner-status,
followthrough, and adoption route for skill-shaped work. It does not make the
AoA center the source of final skill truth, and it does not promote any
candidate into a canonical `skills/*/SKILL.md` bundle by itself.

Validation evidence:

- `tests/test_mechanics_topology.py`
- `tests/test_session_checkpoint_note.py`
- `tests/test_session_growth_kernel_maturity.py`
- `python scripts/validate_nested_agents.py`

## ORQ-DISTILLATION-SKILLS-001

Owner-local status: `accepted`

What is accepted:

- `aoa-skills` accepts the need for bounded workflows that turn reviewed
  artifacts or packets into reusable outputs without forcing promotion.
- The closest landed evidence is the session-growth family, especially
  `skills/aoa-session-donor-harvest/SKILL.md`, plus route-fork, diagnosis,
  repair, progression, automation, and quest-harvest companions.
- `mechanics/README.md` keeps `distillation` as future package pressure until a
  dedicated active route or narrower superseding request lands.

Not landed yet:

- no `mechanics/distillation/` owner-local package exists in `aoa-skills`
- no general distillation skill bundle has been accepted as canonical workflow

Center posture: the AoA queue may advance from `requested` to `accepted`, but
must not mark this request `landed` until a dedicated owner-local landing or a
reviewed supersession exists.

## ORQ-GROWTHCYCLE-SKILLS-001

Owner-local status: `landed`

What landed:

- `skills/aoa-session-donor-harvest/SKILL.md`
- `skills/aoa-session-progression-lift/SKILL.md`
- `skills/aoa-session-route-forks/SKILL.md`
- `skills/aoa-automation-opportunity-scan/SKILL.md`
- `skills/aoa-session-self-diagnose/SKILL.md`
- `skills/aoa-session-self-repair/SKILL.md`
- `skills/aoa-quest-harvest/SKILL.md`
- `mechanics/growth-cycle/README.md`
- `mechanics/growth-cycle/docs/ADAPTIVE_SKILL_ORCHESTRATION.md`
- `mechanics/growth-cycle/docs/SESSION_GROWTH_KERNEL_MATURITY.md`
- `mechanics/growth-cycle/parts/adaptive-orchestration/README.md`
- `mechanics/growth-cycle/parts/session-kernel-maturity/README.md`
- `mechanics/growth-cycle/parts/harvest-note-boundary/README.md`

The landing covers the requested executable cycle-stage skills and the local
route that decides when those skills apply. It does not turn skill execution
into owner acceptance, proof, memory, stats, runtime activation, or final
harvest authority.

Validation evidence:

- `tests/test_mechanics_topology.py`
- `tests/test_session_growth_kernel_maturity.py`
- `python scripts/validate_skills.py --fail-on-review-truth-sync`

## ORQ-CHECKPOINT-SKILLS-001

Owner-local status: `landed`

What landed:

- `skills/aoa-checkpoint-closeout-bridge/SKILL.md`
- `mechanics/checkpoint/README.md`
- `mechanics/checkpoint/docs/CHECKPOINT_NOTE_PATH.md`
- `mechanics/checkpoint/parts/checkpoint-note-lane/README.md`
- `mechanics/checkpoint/parts/closeout-bridge-boundary/README.md`
- `schemas/session_checkpoint_note.schema.json`
- `examples/session_checkpoint_note.example.json`

The landing covers checkpoint-note protocol and the explicit bridge into
reviewed closeout. Checkpoint notes remain provisional; final donor harvest,
progression lift, quest harvest, memory, proof, and stats still require their
own reviewed routes.

Validation evidence:

- `tests/test_session_checkpoint_note.py`
- `tests/test_mechanics_topology.py`
- `python scripts/validate_skills.py --fail-on-review-truth-sync`

## ORQ-EXPERIENCE-SKILLS-001

Owner-local status: `accepted`

What is accepted:

- `aoa-skills` accepts the owner-local need for bounded Experience receipt,
  adoption, release, office, and service-operation skill surfaces.
- Existing Experience-shaped docs remain owner-local evidence and future
  package pressure:
  - `mechanics/experience/docs/GOVERNANCE_SKILL_ADOPTION.md`
  - `mechanics/experience/docs/RECEIPT_GENERATION_SKILLS.md`
  - `mechanics/experience/docs/OFFICE_TASK_BOUNDARY_SKILLS.md`
  - `mechanics/experience/docs/SERVICE_HANDOFF_SKILLS.md`
  - `mechanics/experience/docs/ROLLBACK_DRILL_SKILL.md`
  - `mechanics/experience/docs/INSTALLATION_SKILL_SURFACES.md`

Not landed yet:

- no `mechanics/experience/` owner-local package exists in `aoa-skills`
- the existing docs do not grant release approval, runtime authority, assistant
  self-authority, or direct Tree-of-Sophia write authority

Center posture: the AoA queue may advance from `requested` to `accepted`, but
must not mark this request `landed` until the Experience skill surface is
distilled into an active package, canonical skill bundle, or explicit
superseding receipt.

## ORQ-RPG-SKILLS-001

Owner-local status: `landed`

What landed:

- `mechanics/rpg/README.md`
- `mechanics/rpg/parts/ability-reader-boundary/README.md`
- `mechanics/rpg/parts/loadout-posture/README.md`
- `generated/skill_ability_cards.min.example.json`
- `schemas/skill_ability_catalog.schema.json`

The landing decides the `aoa-skills` side of RPG reflection: ability cards and
loadout hints are reader surfaces over existing skill bundles. They do not
rewrite `SKILL.md`, create a skill ontology, define technique feats, prove
progression, create runtime inventory, or accept role/playbook truth.

Validation evidence:

- `tests/test_mechanics_topology.py`
- `tests/test_generated_surface_schemas.py`

## ORQ-AUDIT-SKILLS-001

Owner-local status: `accepted`

What is accepted:

- `aoa-skills` accepts the owner-local need for bounded executable audit
  workflows with triggers, procedures, risks, and verification boundaries.
- Existing audit-adjacent evidence includes
  `skills/aoa-invariant-coverage-audit/SKILL.md`, evaluation-path docs,
  public-surface docs, maturity docs, promotion docs, trigger-eval docs, and
  governance backlog readouts.
- `mechanics/README.md` keeps `audit` as future package pressure.

Not landed yet:

- no `mechanics/audit/` owner-local package exists in `aoa-skills`
- existing audit-adjacent skills do not cover the whole center audit mechanic

Center posture: the AoA queue may advance from `requested` to `accepted`, but
must not mark this request `landed` until an audit package, canonical workflow,
or explicit superseding receipt lands.

## Center Return Rule

When the AoA center consumes this receipt:

- update only the matching `aoa-skills` requests
- keep proof routes separate from landing refs
- do not treat `accepted` as `landed`
- do not treat `landed` as proof, public quality, runtime activation, or owner
  acceptance for any sibling repository
- leave Agon `requested_not_landed` skill-binding candidates under
  `generated/agon_skill_binding_candidates.min.json` until normal skill review
  promotes or rejects them
