# Root Legacy Retirement

Date: 2026-05-18

Status: accepted

## Context

The repository root had a `legacy/` directory with two large temporary
artifacts:

- `MECHANICS_REFORMATION_RHYTHM.md`
- `2026-05-17__skill-intelligence-layer-strategy.md`

Both were useful during long-running work, but their root placement made them
look like an alternate entry route. The mechanics rhythm also contained
active-sounding instructions, stale path hypotheses, and temporary pacing rules
that should not compete with `AGENTS.md`, `DESIGN.md`,
`mechanics/README.md`, package cards, or accepted decisions.

`docs/` already has a home for durable decision rationale. Growth-cycle owns
bounded session harvests, and mechanics packages have package-local provenance
and legacy lanes for raw mechanic lineage.

## Decision

Retire root `legacy/` as a tracked active district.

Move raw evidence to the package-local owner that matches its function:

- mechanics re-entry and iteration rhythm:
  `mechanics/growth-cycle/legacy/reformation-rhythm/raw/`
- skill registry, search, router adjacency, and future retrieval boundary:
  `mechanics/boundary-bridge/legacy/skill-intelligence/raw/`

Distill useful durable meaning into:

- `mechanics/growth-cycle/session-harvests/2026-05-18.mechanics-reformation-root-legacy-distillation.md`
- `mechanics/growth-cycle/session-harvests/2026-05-17.skill-intelligence-strategy-distillation.md`

Keep accepted structural rationale in existing or new decision records instead
of asking future agents to read raw notebooks first.

## Consequences

- Root entry no longer has a broad `legacy/` door.
- Raw artifacts remain available for provenance without becoming operational
  law.
- Future temporary notebooks should either stay local and untracked, or land as
  bounded session harvests, package-local legacy evidence, or decision records
  once the work has a durable role.
- If future work needs a root-level archive again, it must justify why neither
  `mechanics/growth-cycle/session-harvests/`, `docs/decisions/`, nor the corresponding
  package-local `mechanics/<slug>/legacy/` is the correct owner.

## Verification

Verify with:

```bash
python scripts/validate_nested_agents.py
git diff --check
```
