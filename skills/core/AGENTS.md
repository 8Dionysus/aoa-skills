# AGENTS.md

Guidance for `skills/core/`.

## Purpose

`core/` holds portable AoA skill workflows that are not owned by one project
family. It splits reusable engineering execution from reviewed session-growth
movement so agents do not treat all core skills as one flat lane.

## Read First

1. `../AGENTS.md`
2. this file
3. the nearest child `AGENTS.md`
4. `../README.md`
5. the target bundle `SKILL.md` and `techniques.yaml`

## Local Law

- Keep core wording portable and public-safe.
- Route project-specific paths, commands, approvals, and runtime assumptions to
  `../project/`.
- Route approval, destructive potential, sanitized sharing, and local runtime
  bring-up to `../risk/` unless the current bundle is only referencing those
  guards.
- Do not add per-bundle `AGENTS.md` by default; bundle contracts belong in
  `SKILL.md`, `techniques.yaml`, and support artifacts.

## Validation

After source changes under this subtree, rebuild generated surfaces and run the
validation path named by `../AGENTS.md`.
