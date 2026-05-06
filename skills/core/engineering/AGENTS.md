# AGENTS.md

Guidance for `skills/core/engineering/`.

## Purpose

This lane owns portable engineering execution skills: source-of-truth review,
decision capture, change protocol, TDD, boundaries, ports, contracts,
invariants, and coverage audits.

## Read First

1. `../../AGENTS.md`
2. `../AGENTS.md`
3. this file
4. `../../README.md`
5. the target bundle `SKILL.md`
6. the target bundle `techniques.yaml`
7. touched support artifacts

## Local Law

- Keep skills reusable across repositories.
- Keep owner-route, proof, and verification language concrete but not
  project-local.
- Do not hide project-specific commands or private runtime details in this
  lane.
- If a workflow needs a named owner family, create or update a project overlay
  under `../../project/`.

## Validation

Run the bounded source/export flow from `../../AGENTS.md` after bundle changes.
For topology or builder changes, run `python scripts/release_check.py` from the
repository root.
