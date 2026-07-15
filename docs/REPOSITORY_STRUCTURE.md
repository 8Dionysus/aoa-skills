# Repository Structure

| Path | Authority |
| --- | --- |
| `capabilities/` | authored semantic tree, graph contracts, migration map |
| `skills/` | seven callable bundle sources |
| `config/` | export, policy, pack, and lane inputs |
| `schemas/` | shared machine shape |
| `scripts/` | builders, validators, planner, handoff, lane entrypoints |
| `tests/` | durable invariants derived from manual observations |
| `generated/` | deterministic read models |
| `.agents/skills/` | generated portable flat export |
| `kag/` | derived source-linked KAG provider packet and indexes |
| `mechanics/release-support/` | portable release and installation contract |
| `mechanics/questbook/`, `quests/`, `QUESTBOOK.md` | durable obligation source and read model |
| `mechanics/agon/` | requested external workflow candidates, not skill truth |
| `docs/decisions/` | durable repository rationale |
| `evals/` | forming owner-local eval port; no proof authority |

Task-local DAGs, raw trials, temporary fixtures, clean-home installations, and
session ledgers stay outside the repository. Historical retired topology stays
in Git history or explicitly named `legacy/` areas, never in active routing.
