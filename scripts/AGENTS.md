# AGENTS.md

## Applies to

This card applies to `scripts/`.

## Role

`scripts/` owns deterministic builders, validators, audits, release helpers, and repo-relative automation for the skill canon.

## Read before editing

Read root `AGENTS.md`, `DESIGN.md`, `DESIGN.AGENTS.md` when route-law is
touched, and the tests for the script being changed. For CI or release command
ordering, read `config/validation_lanes.json` before editing
`scripts/validation_lanes.py`, `scripts/ci_gate.py`, or
`scripts/release_check.py`. Start from callers before changing shared helpers.

## Boundaries

Scripts must stay deterministic, repo-relative, public-safe, and explicit about source versus generated authority. Keep builder output stable, avoid network assumptions unless already part of the contract, and keep bounded language in reports.
Keep validator contract data out of Python when it is route-law data rather than
execution logic; prefer manifest-backed contracts under `scripts/validators/`
such as `nested_agents_contract.json`, `agent_skills_export_contract.json`, and
`questbook_contract.json`.
Keep bulky validator execution with its owner surface under `scripts/validators/`
when the checks protect generated/read-model, questbook, or Agent Skills
export/runtime surfaces; keep root `scripts/validate_*.py` entrypoints as CLI
and orchestration adapters.

## Validation

Full lane command sequences live in `config/validation_lanes.json`; this local card may name only focused owner checks, lane ids, or the nearest route for the changed surface.

Run the script directly. For CI lane behavior, use `python scripts/ci_gate.py
--mode source-fast`, `python scripts/ci_gate.py --mode generated --group all`,
`python scripts/ci_gate.py --mode export`, or `python scripts/ci_gate.py --mode
release` as appropriate. For common builders and validators, use `python
scripts/build_catalog.py`, `python scripts/validate_skills.py`, `python
scripts/validate_agents_design.py`, related tests, and `python
scripts/release_check.py` for release-facing changes.

## Closeout

Report changed surfaces, checks run, checks skipped, remaining risk, and the next owner route. If a nearby source document carried agent-facing working law into this card, name that transfer.
