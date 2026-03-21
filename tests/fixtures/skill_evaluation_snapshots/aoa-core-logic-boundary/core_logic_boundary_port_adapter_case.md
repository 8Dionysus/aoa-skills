# Evaluation Snapshot
## Prompt
The core-versus-edge split is already clear; the real task is introducing a port around a concrete dependency.
## Expected selection
do_not_use
## Why
The boundary is already clear and the main task is introducing a port or adapter around a concrete dependency; use `aoa-port-adapter-refactor`.
## Expected object
A deflection toward the port/adapter refactor skill rather than a new boundary analysis.
## Boundary notes
Do not force this skill when the architecture split has already been decided.
## Verification hooks
The response should name the more specific skill and avoid re-litigating core-versus-edge placement.

