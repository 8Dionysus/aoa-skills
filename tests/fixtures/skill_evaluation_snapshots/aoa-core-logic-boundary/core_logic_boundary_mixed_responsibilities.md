# Evaluation Snapshot
## Prompt
Clarify whether reusable rules belong in the core or at the edges because a module mixes domain logic with wiring detail.
## Expected selection
use
## Why
A module mixes stable rules with wiring or execution detail, and you need to decide whether something belongs in the core or at the edges.
## Expected object
A boundary judgment that separates reusable core logic from adapter or wiring responsibilities.
## Boundary notes
Use this skill when the architecture split itself is unclear. If the main task is a port or adapter seam, use a different skill.
## Verification hooks
The response should explain the split between core rules and outer concerns in concrete terms.

