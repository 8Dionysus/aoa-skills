# Evaluation Snapshot

## Prompt
Compare preview-first planning with bounded infrastructure change planning and choose the clearer fit when the main task is still to inspect a risky change before execution.

## Expected selection
use

## Why
The task still turns on previewing or simulating the risky action before choosing a real execution plan.

## Expected object
A preview-first recommendation that explains how to inspect the change before it touches the live surface.

## Boundary notes
This is a dry-run-first case, not a safe-infra-change case.

## Verification hooks
- name the preview or inspect-only path first
- explain what the preview does not prove
- avoid switching into execution planning before the preview seam is interpreted
