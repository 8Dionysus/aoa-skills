# Quest District

This directory holds tracked `aoa-skills` obligations that should survive the
current diff.

It is not a private scratchpad and not a second roadmap. Program direction
belongs in `mechanics/ROADMAP.md`. The human quest surface is
`mechanics/questbook/QUESTBOOK.md`.

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
| `generated/quest_*.json` | Root-published read models built from source quests. | Rebuild with `scripts/build_catalog.py`; do not edit by hand. |

## Before Editing

1. Check `mechanics/questbook/QUESTBOOK.md`.
2. Choose lane first, then lifecycle state.
3. Keep owner split explicit.
4. Regenerate and validate quest read models.
