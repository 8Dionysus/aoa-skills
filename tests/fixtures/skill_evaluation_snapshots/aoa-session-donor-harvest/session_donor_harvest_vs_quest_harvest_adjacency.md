# Evaluation Snapshot

## Prompt

Compare donor harvest with final quest triage when the reviewed artifact still contains several reusable units that need owner-layer routing first.

## Expected selection

use

## Why

The reviewed artifact still carries multiple reusable units, so the work is
donor extraction and owner-layer placement before any final quest-promotion
verdict.

## Expected object

A HARVEST_PACKET that routes multiple reusable donor units before final quest triage.

## Boundary notes

This is a session-donor-harvest case, not a quest-harvest case.

## Verification hooks

- split candidates into bounded reusable units
- choose one owner layer for each kept unit
- keep quest promotion as a later handoff only when it is the remaining question
