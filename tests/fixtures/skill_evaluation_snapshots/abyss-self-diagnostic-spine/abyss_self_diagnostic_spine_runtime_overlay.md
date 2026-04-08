# Evaluation Snapshot

## Prompt

Diagnose one abyss runtime path by normalizing doctor, machine-fit,
render-truth, and autonomy evidence into one local diagnostic artifact before
any repair claim is made.

## Expected selection

use

## Why

The base `aoa-session-self-diagnose` workflow is already correct, but the local
repo needs a runtime-owned diagnostic session artifact with repo-relative
evidence refs and one explicit exit class.

## Expected object

A bounded runtime-owned diagnostic session artifact with repo-relative evidence
refs and one explicit exit class.

## Boundary notes

Use this overlay when one `abyss-*` repo needs runtime diagnosis normalization
before repair. Keep the artifact citation-friendly and do not turn it into free
self-repair.

## Verification hooks

The response should resolve a concrete target, name drift classes, preserve
unknowns where needed, and keep any next move smaller than repair authority.
