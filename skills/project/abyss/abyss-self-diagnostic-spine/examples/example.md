# Example

## Scenario

You need one bounded runtime diagnosis artifact inside an `abyss-*` repository
because doctor, machine-fit, render-truth, and autonomy signals exist, but they
are scattered and the next honest move might be retest, governed repair, quest
follow-up, owner handoff, insufficient-evidence collection, or manual regrounding.

## Why this skill fits

The base diagnosis workflow is correct, but the remaining work is a thin local
adaptation for one `abyss-*` repo. The overlay keeps the diagnosis runtime-owned,
repo-relative, citation-friendly, and explicit about owner-aware handoff.

## Expected inputs

- the diagnostic target selectors
- repo-relative runtime evidence refs grouped by axis
- evidence freshness, command refs, and generated receipt refs
- any reviewed session or harvest refs that should be cited
- any last-good comparison ref
- the local truth goal
- the stop line before repair, quest, progression, or source-of-truth mutation

## Expected outputs

- one bounded runtime-owned `diagnostic_session_v1`
- one explicit `exit_class`, such as `retest`, `governed_repair`, `manual_regrounding`, `owner_handoff`, or `insufficient_evidence`
- named drift classes, per-axis verdicts, freshness notes, confidence notes, and unknowns
- any honest handoff note toward reviewed diagnosis, repair, progression, or quest surfaces

## Boundary notes

- If the route is asking for silent or immediate repair, use `aoa-session-self-repair` only after reviewed diagnosis exists.
- If the real problem is conflicting diagnostic docs or runbooks, use `aoa-source-of-truth-check` instead.
- If the route only needs a generic health command, do not force a diagnostic session artifact.
- If the base `aoa-session-self-diagnose` workflow is already sufficient, do not force the overlay.
- Keep the local adaptation thin and avoid widening into project doctrine.

## Verification notes

- Confirm the target path was resolved before judgment.
- Confirm the artifact stayed runtime-owned and citation-friendly.
- Confirm evidence axes, freshness, confidence, and unknowns were preserved.
- Confirm one exit class was chosen and it stayed smaller than repair authority.
- Confirm the scaffold was entered by explicit handle or deliberate manual route decision.
- Confirm no quest, repair, or progression authority was auto-mutated.
