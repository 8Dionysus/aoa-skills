# Roadmap

## v0 bootstrap

Goal: create a coherent public skeleton.

Includes:
- docs surface
- bridge spec
- templates
- skill index
- first starter skills as scaffolds

## v0.1 first core skills

Target starter skills:
- `aoa-change-protocol`
- `aoa-tdd-slice`
- `aoa-contract-test`
- `aoa-bounded-context-map`
- `aoa-property-invariants`

Target outcomes:
- each skill has a bounded `SKILL.md`
- each skill records technique references
- at least one example or checklist exists per starter skill

## v0.2 project overlays

Add first project-shaped overlays:
- `atm10-*`
- `abyss-*`

Examples:
- `atm10-perception-tests`
- `atm10-safe-action-policy`
- `abyss-port-exposure-guard`
- `abyss-safe-compose-change`
- `abyss-backup-dryrun`

## v0.3 generation helpers

Add optional tooling to:
- validate skill bundle shape
- compose `SKILL.md` from selected technique sections
- detect drift when a referenced technique changes
- check naming and policy conventions

## v0.4 evaluation harness

Add:
- prompt fixtures
- trigger-boundary tests
- expected output snapshots for selected skills
- review checklists for risk skills

## Long-term direction

- reusable public core
- thin project overlays
- clear separation between canonical techniques and executable skills
- stable skill refresh path when techniques evolve
