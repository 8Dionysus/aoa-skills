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

## Boundary notes

This is a session-self-repair case, not a session-self-diagnose case.

## Verification hooks

- cite the reviewed diagnosis packet
- name rollback and health-check posture
- keep repair authority bounded and owner-routed
