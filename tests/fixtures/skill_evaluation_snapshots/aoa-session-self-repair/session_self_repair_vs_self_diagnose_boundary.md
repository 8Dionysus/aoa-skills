# Evaluation Snapshot

## Prompt

Compare repair planning with diagnosis when a reviewed diagnosis packet already exists and the next honest move is a bounded repair packet.

## Expected selection

use

## Why

The diagnosis prerequisite is already satisfied, so the next useful object is
repair planning with rollback, health checks, and owner targets instead of
another diagnosis pass.

## Expected object

A repair packet with rollback, health check, and owner targets from an existing diagnosis.
The repair packet should include execution posture rather than implying that
planning, execution, and verification are the same state.

## Boundary notes

This is a session-self-repair case, not a session-self-diagnose case.

## Verification hooks

- cite the reviewed diagnosis packet
- name rollback and health-check posture
- distinguish prepared repair from executed or verified repair
- keep repair authority bounded and owner-routed
