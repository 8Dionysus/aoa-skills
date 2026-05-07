# Evaluation Snapshot

## Prompt

Compare automation-readiness classification with ordinary branch cards when a repeated manual route is visible and the honest question is whether it can become automation.

## Expected selection

use

## Why

The main signal is repeated manual work with an automation-readiness question,
so the output should classify readiness and risk rather than merely list next
route options.

## Expected object

An automation opportunity packet that classifies readiness without granting automation authority.

## Boundary notes

This is an automation-opportunity-scan case, not a session-route-forks case.

## Verification hooks

- name the repeated manual route
- classify readiness and risk without scheduling automation
- route any seed-ready outcome to the correct owner layer
