# Evaluation Snapshot

## Prompt

In an abyss repository, choose between runtime diagnosis normalization and
self-repair because the evidence still needs to be gathered into one honest
diagnostic artifact before any repair packet can be justified.

## Expected selection

use

## Why

The repo still needs a diagnosis artifact before repair authority becomes
honest, so this remains a runtime diagnosis normalization case.

## Expected object

This is an abyss-self-diagnostic-spine case, not an aoa-session-self-repair
case.

A bounded runtime-owned diagnostic session artifact with repo-relative evidence
refs and one explicit exit class.

## Boundary notes

Use `aoa-session-self-repair` only after reviewed diagnosis exists. This overlay
keeps the route read-only and owner-aware until that point.

## Verification hooks

The response should require diagnosis before repair, keep repair authority out
of the main recommendation, and preserve one bounded exit class.
