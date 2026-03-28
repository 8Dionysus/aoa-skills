# Evaluation Snapshot

## Prompt

Compare a first-pass context map with a narrower core-versus-glue split and choose the clearer fit when the context is already named but stable rules and orchestration are still mixed together.

## Expected selection

use

## Why

The broader context is already understood, so the real task is deciding what belongs in reusable core logic versus surrounding orchestration or wiring.

## Expected object

A narrower decision about what belongs in reusable core logic versus orchestration or wiring after the context is already understood.

## Boundary notes

This is a core-logic-boundary case, not a bounded-context-map case.

## Verification hooks

- name the already-understood context
- name the stable rules
- name the orchestration or wiring detail that should stay outside the core
