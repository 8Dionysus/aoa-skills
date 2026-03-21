# Evaluation Snapshot
## Prompt
Clarify which documentation file is authoritative rather than refactoring a code dependency seam.
## Expected selection
do_not_use
## Why
The main problem is clarifying repository docs or source-of-truth ownership; use `aoa-source-of-truth-check` first.
## Expected object
A deflection toward source-of-truth clarification instead of a port or adapter refactor.
## Boundary notes
Do not use this skill when the real issue is document authority rather than infrastructure coupling.
## Verification hooks
The response should point to the docs-authority skill and avoid proposing a dependency seam.

