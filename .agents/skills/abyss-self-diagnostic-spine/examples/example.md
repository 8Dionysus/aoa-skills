# Example

## Scenario

You need one bounded runtime diagnosis artifact inside an `abyss-*` repository
because doctor, machine-fit, render-truth, and autonomy signals exist, but they
are scattered and the next honest move might be retest, governed repair, quest
follow-up, or manual regrounding.

## Why this skill fits

The base diagnosis workflow is correct, but the remaining work is a thin local
adaptation for one `abyss-*` repo. The overlay keeps the diagnosis runtime-owned,
repo-relative, citation-friendly, and explicit about owner-aware handoff.

## Expected inputs

- the diagnostic target selectors
- repo-relative runtime evidence refs
- any reviewed session or harvest refs that should be cited
- any last-good comparison ref
- the local truth goal

## Expected outputs

- one bounded runtime-owned `diagnostic_session_v1`
- one explicit `exit_class`
- named drift classes and unknowns
- any honest handoff note toward reviewed diagnosis, repair, progression, or quest surfaces

## Boundary notes

- If the route is asking for silent or immediate repair, use `aoa-session-self-repair` only after reviewed diagnosis exists.
- If the base `aoa-session-self-diagnose` workflow is already sufficient, do not force the overlay.
- Keep the local adaptation thin and avoid widening into project doctrine.

## Verification notes

- Confirm the target path was resolved before judgment.
- Confirm the artifact stayed runtime-owned and citation-friendly.
- Confirm one exit class was chosen.
- Confirm no quest, repair, or progression authority was auto-mutated.
