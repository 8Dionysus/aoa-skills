# abyss-demo Project Overlay

## Overlay target

- downstream repository family: `abyss-demo`
- overlay family: `abyss-*`

## Base skill surface

- base canon: `aoa-skills`
- example base skills: `aoa-safe-infra-change`, `aoa-sanitized-share`
- this overlay does not change the base skill boundary; it only narrows local execution details

## Local authority and approvals

- operational approvals remain explicit and downstream
- the overlay cannot replace local human authority for risky actions

## Local paths and commands

- keep all paths repository-relative to the downstream repo
- example docs surface: `README.md`, `docs/ARCHITECTURE.md`, `docs/PROMOTION_PATH.md`
- example commands: `python scripts/validate_skills.py`, `python scripts/build_catalog.py --check`

## Local verification

- confirm the overlay stays thin, public-safe, and reviewable
- confirm any local command or path can be inspected before use

## Non-goals and boundaries

- do not turn this overlay into hidden operational doctrine
- do not add private infrastructure details
- keep richer downstream adaptation as a future stub rather than live scope expansion
