# Mechanics Method-Growth Lineage

Date: 2026-05-06

Status: accepted

## Context

The mechanics reformation started with Agon because it was the smallest complete
candidate bridge. The next tempting package was `distillation`, but direct
reading showed that the candidate lineage family speaks the Growth Refinery
route:

```text
cluster_ref -> candidate_ref -> seed_ref -> object_ref
```

Those files are not raw-to-active distillation docs. They define reviewed
candidate identity, first owner-status landing, and one bounded followthrough
decision after `candidate_ref` exists.

## Decision

Create `mechanics/method-growth/` as the second local mechanics package and
land only the candidate-lineage slice:

- `docs/CANDIDATE_LINEAGE_CONTRACT.md` -> `mechanics/method-growth/docs/CANDIDATE_LINEAGE_CONTRACT.md`
- `docs/CANDIDATE_REF_REFINERY.md` -> `mechanics/method-growth/docs/CANDIDATE_REF_REFINERY.md`
- `docs/OWNER_STATUS_SURFACES.md` -> `mechanics/method-growth/docs/OWNER_STATUS_SURFACES.md`
- `docs/GOVERNED_FOLLOWTHROUGH.md` -> `mechanics/method-growth/docs/GOVERNED_FOLLOWTHROUGH.md`

Add a package card, direction, parts, provenance, landing log, roadmap, active
docs map, and active parts for candidate lineage, owner-status landing, and
governed followthrough.

Do not move session-growth maturity, checkpoint, questbook, adoption,
release-support, or audit surfaces in this slice.

## Consequences

- The docs root no longer owns candidate-ref and owner-status movement.
- `mechanics/method-growth/` becomes the local route for reviewed candidate
  identity without becoming a skill bundle tree.
- `distillation` stays available for session-harvest, donor intake, and
  source-to-active extraction instead of absorbing Growth Refinery identity.
- Later adoption lifecycle work has a package route to inspect, but it is not
  automatically landed here.
- Canonical donor-harvest skill meaning remains under `skills/`.

## Verification

Verify with:

```bash
python -m pytest -q tests/test_session_checkpoint_note.py tests/test_session_growth_kernel_maturity.py tests/test_roadmap_parity.py tests/test_current_direction_routes.py tests/test_mechanics_topology.py
python scripts/validate_nested_agents.py
python -m unittest discover -s tests
```
