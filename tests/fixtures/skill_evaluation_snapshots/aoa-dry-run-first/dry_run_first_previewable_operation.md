# Evaluation Snapshot

## Prompt
Preview a configuration migration before applying it to a live service.

## Expected selection
use

## Why
The action can be inspected before real execution, so the skill should favor a dry run or preview path.

## Expected object
A preview-first recommendation that explains how to inspect the change before it touches the live surface.

## Boundary notes
This is about how to preview an operational change, not whether the change is allowed at all.

## Verification hooks
- mentions that the action can be simulated or inspected first
- identifies the live surface risk
- keeps the recommendation preview-focused
- does not claim the change should execute immediately
