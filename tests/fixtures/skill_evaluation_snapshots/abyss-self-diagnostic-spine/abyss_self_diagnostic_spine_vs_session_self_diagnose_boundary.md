# Evaluation Snapshot

## Prompt

In an abyss repository, choose between a local runtime diagnosis overlay and the
base reviewed-session diagnosis skill because the repo needs one runtime-owned
diagnostic session artifact with repo-relative evidence refs.

## Expected selection

use

## Why

This is an abyss-local runtime diagnosis normalization case, not a plain base
reviewed-session diagnosis case.

## Expected object

This is an abyss-self-diagnostic-spine case, not an
aoa-session-self-diagnose case.

A bounded runtime-owned diagnostic session artifact with repo-relative evidence
refs and one explicit exit class.

## Boundary notes

Use the base skill when no `abyss-*` local adaptation is needed. Use this
overlay when the runtime-owned artifact and repo-relative evidence surface are
the missing local seam.

## Verification hooks

The response should prefer the bounded overlay, keep the artifact runtime-owned,
and avoid absorbing the broader session-diagnosis canon.
