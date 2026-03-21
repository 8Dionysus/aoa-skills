# Evaluation Snapshot

## Prompt
Apply a bounded configuration change with explicit validation and rollback thinking on an operational surface.

## Expected selection
use

## Why
The task changes a runtime-facing surface and needs safer execution discipline than an ordinary code edit.

## Expected object
A bounded change plan or recommendation that names the operational surface, the validation path, and rollback or recovery notes.

## Boundary notes
This should stay focused on the operational change itself, not authority classification or generic code cleanup.

## Verification hooks
- names the operational surface
- keeps the change small and reviewable
- includes explicit validation
- includes rollback or recovery thinking
