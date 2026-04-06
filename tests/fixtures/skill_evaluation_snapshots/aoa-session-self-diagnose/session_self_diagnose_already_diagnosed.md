# Evaluation Snapshot

## Prompt

The issue is already fully diagnosed, the repair path is known, and the team now needs a bounded repair packet rather than another diagnosis pass.

## Expected selection

do_not_use

## Why

Diagnosis is no longer the bottleneck. Reopening it would only duplicate work
that should now move into a bounded repair packet.

## Expected object

A deflection toward repair work instead of reopening diagnosis.

## Boundary notes

Do not use this skill when the issue is already diagnosed and the honest next
move is repair. Diagnosis should stay read-only and should not become a ritual
repetition step.

## Verification hooks

The response should say that diagnosis already exists and should redirect
toward `aoa-session-self-repair` or another bounded repair surface.
