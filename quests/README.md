# Quest District

This directory holds tracked `aoa-skills` obligations that should survive the
current diff.

It is not a private scratchpad and not a second roadmap. Direction is routed
through `mechanics/ROADMAP.md` and package roadmaps. The human quest surface is
root `QUESTBOOK.md`.

Quest sources live in lane-first lifecycle directories. Top-level
`AOA-SK-Q-*` aliases are intentionally absent; route directly to
`quests/<lane>/<state>/AOA-SK-Q-*`.

## Lanes

| Lane | Use |
|---|---|
| `agon/` | Agon requested-skill and candidate follow-through notes. |
| `audit/` | proof, evaluation, and public-surface alignment obligations. |
| `boundary-bridge/` | overlay, downstream, and cross-repo bridge obligations. |
| `checkpoint/` | checkpoint carry and closeout bridge follow-through. |
| `questbook/` | Questbook mechanic obligations and landed questbook setup. |
| `release-support/` | export, local adapter, runtime seam, and release support obligations. |
| `rpg/` | ability-card and loadout reflection obligations. |

## Lifecycle States

Each lane may contain `captured/`, `triaged/`, `ready/`, `active/`,
`blocked/`, `reanchor/`, `done/`, or `dropped/`.

## File Families

| Family | Meaning | Guardrail |
|---|---|---|
| `<lane>/<state>/AOA-SK-Q-*.yaml` | Rich `work_quest_v1` obligations. | YAML `state` must match the path state. |
| `agon/<state>/AOS-Q-AGON-*.md` | Agon requested-skill notes. | Must not grant live Agon authority. |
| `generated/quest_*.json` | Root-published read models built from source quests. | Rebuild with `scripts/builders/build_catalog.py`; do not edit by hand. |

## Owner Route

Use [AGENTS](AGENTS.md) before editing. Check root `QUESTBOOK.md`, choose lane
first, then lifecycle state, keep owner split explicit, and refresh quest read
models through the owning route.
